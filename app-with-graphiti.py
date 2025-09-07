import streamlit as st
import os
from graphiti_core import Graphiti
from openai import OpenAI

# Initialize OpenAI client for chat responses
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Graphiti with Neo4j (hardcoded for demo; use st.secrets in production)
@st.cache_resource
def get_graphiti():
    return Graphiti(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"  # Change this to your actual password
    )

graphiti = get_graphiti()

# Streamlit UI
st.title("Knowledge Graph Demo with Graphiti & Neo4j")

# Sidebar for ingestion
st.sidebar.header("Ingest Document into KG")
doc_text = st.sidebar.text_area("Enter document text:", height=200)
uploaded_file = st.sidebar.file_uploader("Or upload TXT file", type="txt")

if st.sidebar.button("Ingest into KG"):
    if uploaded_file:
        doc_text = uploaded_file.read().decode("utf-8")
    if doc_text:
        try:
            graphiti.add_episode(doc_text)
            st.sidebar.success("Document ingested! Entities and relations extracted via LLM.")
        except Exception as e:
            st.sidebar.error(f"Ingestion error: {str(e)}")
    else:
        st.sidebar.error("Provide text or upload a file.")

# Button to clear graph (for demo resets)
if st.sidebar.button("Clear Graph"):
    graphiti.clear_graph()
    st.sidebar.success("Graph cleared.")

# Chat section
st.header("Chat with KG-Augmented LLM")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_query = st.chat_input("Ask a question:")
if user_query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Retrieve from KG
    try:
        edges = graphiti.search_edges(query=user_query, top_k=5)
        context = "\n".join([f"{edge['name']}: {edge['episode_facts']}" for edge in edges])  # Serialize edges; adjust based on actual response format if needed
        if not context:
            context = "No relevant knowledge found in graph."
    except Exception as e:
        context = f"KG retrieval error: {str(e)}"

    # Augment prompt and generate response
    prompt = f"Based on this knowledge graph context: {context}\n\nUser question: {user_query}"
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4o"
            messages=[
                {"role": "system", "content": "You are a helpful assistant using a knowledge graph for accurate responses."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        ai_response = response.choices[0].message.content
    except Exception as e:
        ai_response = f"OpenAI error: {str(e)}"

    # Add AI message to history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)

# Note for class
st.info("This demo uses Graphiti to handle LLM-based extraction and Neo4j storage. Review the code to see how ingestion is simplified to one call.")
import streamlit as st
import os
import asyncio
from graphiti_core import Graphiti
from openai import OpenAI
from neo4j import GraphDatabase
from pyvis.network import Network

# Initialize OpenAI client for chat responses
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Graphiti with Neo4j (hardcoded for demo; use st.secrets in production)
@st.cache_resource
def get_graphiti():
    graphiti = Graphiti(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"  # Change this to your actual password
    )
    return graphiti

graphiti = get_graphiti()

# Debug: Show available methods on Graphiti object
st.write("Graphiti methods:", [method for method in dir(graphiti) if not method.startswith('_')])

# Initialize Neo4j driver for visualization
@st.cache_resource
def get_neo4j_driver():
    return GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))  # Match credentials

driver = get_neo4j_driver()

# Function to fetch graph data for visualization
def fetch_graph_data(limit=100):
    try:
        import concurrent.futures
        
        def run_async_query():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Create a fresh Graphiti instance in this thread
                g = Graphiti(
                    uri="bolt://localhost:7687",
                    user="neo4j",
                    password="password"
                )
                # Initialize indices and constraints
                loop.run_until_complete(g.build_indices_and_constraints())
                
                # Use the same query as your working app
                cypher = """
                    MATCH (n)-[r]->(m)
                    RETURN n.uuid AS source, n.name AS sname,
                           m.uuid AS target, m.name AS tname,
                           type(r) AS rel
                    LIMIT $limit
                """
                return loop.run_until_complete(g.driver.execute_query(cypher, limit=limit))
            finally:
                loop.close()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_async_query)
            return future.result(timeout=30)
    except Exception as e:
        st.error(f"Error fetching graph data: {str(e)}")
        return []

# Function to visualize graph with pyvis
def visualize_graph():
    data = fetch_graph_data()
    if not data:
        st.info("No data in graph to visualize.")
        return
    
    # Handle EagerResult from Neo4j driver
    if hasattr(data, 'records'):
        records = data.records
    else:
        records = data
    
    if not records:
        st.info("No records found in graph data.")
        return
    
    net = Network(height="700px", width="100%", bgcolor="#ffffff", directed=True)
    added_nodes = set()
    
    # Process the records
    for record in records:
        # Extract data from Neo4j Record object
        source_id = record.get("source", "unknown")
        source_name = record.get("sname", "Unknown")[:25] if record.get("sname") else "Unknown"
        target_id = record.get("target", "unknown")
        target_name = record.get("tname", "Unknown")[:25] if record.get("tname") else "Unknown"
        relation = record.get("rel", "related")
        
        # Add nodes if not already added
        if source_id not in added_nodes:
            net.add_node(source_id, label=source_name, title=source_name)
            added_nodes.add(source_id)
        if target_id not in added_nodes:
            net.add_node(target_id, label=target_name, title=target_name)
            added_nodes.add(target_id)
        
        # Add edge
        net.add_edge(source_id, target_id, title=relation)
    
    # Configure and display the network
    net.repulsion()
    net_html = net.generate_html(notebook=False)
    st.components.v1.html(net_html, height=720, scrolling=True)

# Streamlit UI
st.title("Knowledge Graph Demo with Graphiti & Neo4j")

# Sidebar for ingestion
st.sidebar.header("Ingest Document into KG")
doc_text = st.sidebar.text_area("Enter document text:", height=200)
uploaded_file = st.sidebar.file_uploader("Or upload TXT file", type="txt")

if st.sidebar.button("Ingest into KG"):
    if uploaded_file:
        doc_text = uploaded_file.read().decode("utf-8")
        source_description = uploaded_file.name
        episode_name = uploaded_file.name.replace('.txt', '')
    else:
        source_description = "Manual text input"
        episode_name = "Manual Episode"
    
    if doc_text:
        try:
            # Use the correct async approach from your working app
            import concurrent.futures
            from datetime import datetime, timezone
            from graphiti_core.nodes import EpisodeType
            
            def run_async_ingest(text_content, description, name):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    # Create a fresh Graphiti instance in this thread
                    g = Graphiti(
                        uri="bolt://localhost:7687",
                        user="neo4j",
                        password="password"
                    )
                    # Initialize indices and constraints
                    loop.run_until_complete(g.build_indices_and_constraints())
                    # Ingest text
                    return loop.run_until_complete(g.add_episode(
                        name=name,
                        episode_body=text_content,
                        source=EpisodeType.text,
                        source_description=description,
                        reference_time=datetime.now(timezone.utc),
                    ))
                finally:
                    loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async_ingest, doc_text, source_description, episode_name)
                future.result(timeout=60)
            
            st.sidebar.success("Document ingested! Entities and relations extracted via LLM.")
        except Exception as e:
            st.sidebar.error(f"Ingestion error: {str(e)}")
    else:
        st.sidebar.error("Provide text or upload a file.")

# Button to clear graph (for demo resets)
if st.sidebar.button("Clear Graph"):
    try:
        with driver.session() as session:
            # Clear all nodes and relationships
            session.run("MATCH (n) DETACH DELETE n")
            st.sidebar.success("Graph cleared successfully!")
    except Exception as e:
        st.sidebar.error(f"Clear graph error: {str(e)}")

# Button to check existing indexes
if st.sidebar.button("Check Existing Indexes"):
    try:
        with driver.session() as session:
            # Show existing indexes
            result = session.run("SHOW INDEXES")
            indexes = list(result)
            st.sidebar.write("Existing indexes:")
            for idx in indexes:
                st.sidebar.write(f"- {idx}")
    except Exception as e:
        st.sidebar.error(f"Index check error: {str(e)}")

# Button to create database schema (if needed)
if st.sidebar.button("Create Database Schema"):
    try:
        with driver.session() as session:
            # Create basic indexes that Graphiti might need
            session.run("CREATE INDEX entity_name_index IF NOT EXISTS FOR (n:Entity) ON (n.name)")
            session.run("CREATE INDEX episodic_name_index IF NOT EXISTS FOR (n:Episodic) ON (n.name)")
            
            # Try different variations of the fulltext index
            try:
                session.run("CREATE FULLTEXT INDEX node_name_and_summary IF NOT EXISTS FOR (n:Entity) ON EACH [n.name, n.summary]")
                st.sidebar.success("Fulltext index created with name and summary!")
            except Exception as e1:
                st.sidebar.write(f"Fulltext with summary failed: {e1}")
                try:
                    session.run("CREATE FULLTEXT INDEX node_name_and_summary IF NOT EXISTS FOR (n:Entity) ON EACH [n.name]")
                    st.sidebar.success("Fulltext index created with name only!")
                except Exception as e2:
                    st.sidebar.write(f"Fulltext with name only failed: {e2}")
                    # Try without the specific name
                    try:
                        session.run("CREATE FULLTEXT INDEX entity_fulltext IF NOT EXISTS FOR (n:Entity) ON EACH [n.name]")
                        st.sidebar.success("Fulltext index created with generic name!")
                    except Exception as e3:
                        st.sidebar.error(f"All fulltext index attempts failed: {e3}")
            
            st.sidebar.success("Database schema creation attempted!")
    except Exception as e:
        st.sidebar.error(f"Schema creation error: {str(e)}")

# Graph Visualization Section
st.header("Graph Visualization")
if st.button("Visualize Current Graph"):
    visualize_graph()

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
        import concurrent.futures
        
        def run_async_search():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Create a fresh Graphiti instance in this thread
                g = Graphiti(
                    uri="bolt://localhost:7687",
                    user="neo4j",
                    password="password"
                )
                # Initialize indices and constraints
                loop.run_until_complete(g.build_indices_and_constraints())
                # Perform search
                return loop.run_until_complete(g.search(user_query))
            finally:
                loop.close()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_async_search)
            results = future.result(timeout=30)
        
        context = "\n".join(f"- {r.fact}" for r in results)
        if not context:
            context = "No relevant knowledge found in graph."
    except Exception as e:
        context = f"KG retrieval error: {str(e)}"
        st.write(f"Debug - search error: {e}")

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
st.info("This demo uses Graphiti to handle LLM-based extraction and Neo4j storage. Review the code to see how ingestion is simplified to one call. Visualization uses pyvis for interactive graph rendering.")
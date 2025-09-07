import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Ensure OPENAI_API_KEY is set

# Initialize graph in session state to persist across reruns
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()  # Or nx.DiGraph() for directed edges

G = st.session_state.graph

# Function to save graph to JSON
def save_graph_to_json(filename="kg.json"):
    data = nx.node_link_data(G, edges="links")
    with open(filename, 'w') as f:
        json.dump(data, f)
    st.success(f"Graph saved to {filename}")

# Function to load graph from JSON string
def load_graph_from_json(json_data, merge=True):
    try:
        data = json.loads(json_data)
        new_graph = nx.node_link_graph(data, edges="links")
        if merge:
            # Add edges from the loaded graph to the current graph
            for edge in new_graph.edges(data=True):
                st.session_state.graph.add_edge(edge[0], edge[1], **edge[2])
            st.success(f"Graph merged successfully! Added {new_graph.number_of_edges()} relationships.")
        else:
            # Replace the current graph
            st.session_state.graph = new_graph
            st.success("Graph replaced successfully!")
        # Force a rerun to update the visualization
        st.rerun()
    except Exception as e:
        st.error(f"Failed to load graph: {str(e)}")

# Streamlit UI
st.title("Hello World Knowledge Graph App")

# Sidebar for adding nodes/edges
st.sidebar.header("Build the KG")
node1 = st.sidebar.text_input("Entity 1 (Node)")
relation = st.sidebar.text_input("Relationship (Edge Label)")
node2 = st.sidebar.text_input("Entity 2 (Node)")

if st.sidebar.button("Add Relationship", key="add_relationship"):
    if node1 and relation and node2:
        st.session_state.graph.add_edge(node1, node2, label=relation)
        st.sidebar.success(f"Added: {node1} --[{relation}]--> {node2}")
        # Force a rerun to update the visualization
        st.rerun()
    else:
        st.sidebar.error("Fill all fields.")

# File uploader for loading JSON
st.sidebar.header("Load/Save Graph")
uploaded_json = st.sidebar.file_uploader("Upload JSON file", type=["json"], key="json_uploader", accept_multiple_files=True)
if uploaded_json:
    st.sidebar.write(f"Selected files: {len(uploaded_json)}")
    for i, file in enumerate(uploaded_json):
        st.sidebar.write(f"{i+1}. {file.name}")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Merge All Files", key="merge_files"):
            for file in uploaded_json:
                json_data = file.read().decode("utf-8")
                load_graph_from_json(json_data, merge=True)
    with col2:
        if st.button("Replace Graph", key="replace_graph"):
            # Use the last uploaded file to replace the graph
            if uploaded_json:
                json_data = uploaded_json[-1].read().decode("utf-8")
                load_graph_from_json(json_data, merge=False)

if st.sidebar.button("Save to JSON", key="save_to_json"):
    save_graph_to_json()

# Visualize the graph
st.header("Graph Visualization")
if G.number_of_nodes() > 0:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)
else:
    st.info("Add some relationships or load a JSON file to see the graph.")

# Query section with OpenAI integration
st.header("Query the KG")

# Initialize session state for query results
if 'query_results' not in st.session_state:
    st.session_state.query_results = None

def process_query(query_entity):
    if query_entity and query_entity in G:
        # Get all edges connected to the query entity
        context_parts = []
        
        # Check all edges to find relationships involving the query entity
        for edge in G.edges(data=True):
            source, target, data = edge
            label = data.get('label', '')
            
            # If query_entity is the source, relationship goes from source to target
            if source == query_entity:
                context_parts.append(f"{source} {label} {target}")
            # If query_entity is the target, relationship goes from source to target
            elif target == query_entity:
                context_parts.append(f"{source} {label} {target}")
        
        context_text = " ".join(context_parts)
        
        # Feed to OpenAI API for generation
        prompt = f"Based on this knowledge: {context_text}. Answer: What is related to {query_entity}?"
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Or "gpt-4o" if preferred
                messages=[
                    {"role": "system", "content": "You are a helpful assistant using a knowledge graph."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return {
                'context': context_text,
                'response': response.choices[0].message.content,
                'entity': query_entity
            }
        except Exception as e:
            return {'error': f"OpenAI API error: {str(e)}"}
    elif query_entity and query_entity not in G:
        return {'error': "Entity not found in graph."}
    return None

# Create a form for the query to handle Enter key properly
with st.form("query_form", clear_on_submit=False):
    query_entity = st.text_input("Enter an entity to query (e.g., 'Tom Hanks')", key="query_input")
    submitted = st.form_submit_button("Query and Generate Response")
    
    if submitted and query_entity:
        st.session_state.query_results = process_query(query_entity)

# Display query results
if st.session_state.query_results:
    results = st.session_state.query_results
    if 'error' in results:
        st.error(results['error'])
    else:
        st.write("**Retrieved Context:**", results['context'])
        st.write("**LLM Response:**", results['response'])

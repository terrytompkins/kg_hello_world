import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
from openai import OpenAI

# Initialize graph and OpenAI client
G = nx.Graph()  # Or nx.DiGraph() for directed edges
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Ensure OPENAI_API_KEY is set

# Function to save graph to JSON
def save_graph_to_json(filename="kg.json"):
    data = nx.node_link_data(G)
    with open(filename, 'w') as f:
        json.dump(data, f)
    st.success(f"Graph saved to {filename}")

# Function to load graph from JSON
def load_graph_from_json(filename="kg.json"):
    global G
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        G = nx.node_link_graph(data)
        st.success(f"Graph loaded from {filename}")
    except FileNotFoundError:
        st.warning("No saved graph found.")

# Streamlit UI
st.title("Hello World Knowledge Graph App")

# Sidebar for adding nodes/edges
st.sidebar.header("Build the KG")
node1 = st.sidebar.text_input("Entity 1 (Node)")
relation = st.sidebar.text_input("Relationship (Edge Label)")
node2 = st.sidebar.text_input("Entity 2 (Node)")

if st.sidebar.button("Add Relationship"):
    if node1 and relation and node2:
        G.add_edge(node1, node2, label=relation)
        st.sidebar.success(f"Added: {node1} --[{relation}]--> {node2}")
    else:
        st.sidebar.error("Fill all fields.")

# Option to load/save
if st.sidebar.button("Load from JSON"):
    load_graph_from_json()
if st.sidebar.button("Save to JSON"):
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
    st.info("Add some relationships to see the graph.")

# Query section with OpenAI integration
st.header("Query the KG")
query_entity = st.text_input("Enter an entity to query (e.g., 'Tom Hanks')")
if st.button("Query and Generate Response"):
    if query_entity in G:
        # Simple traversal: Get neighbors and relations
        neighbors = list(G.neighbors(query_entity))
        relations = [G.edges[query_entity, n]['label'] for n in neighbors]
        context = [f"{query_entity} {rel} {nei}" for rel, nei in zip(relations, neighbors)]
        context_text = " ".join(context)
        
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
            st.write("Retrieved Context:", context_text)
            st.write("LLM Response:", response.choices[0].message.content)
        except Exception as e:
            st.error(f"OpenAI API error: {str(e)}")
    else:
        st.error("Entity not found in graph.")

# Sample data button for quick start
if st.button("Add Sample Movie KG"):
    G.add_edge("Tom Hanks", "Forrest Gump", label="starred_in")
    G.add_edge("Forrest Gump", "Robert Zemeckis", label="directed_by")
    G.add_edge("Tom Hanks", "Meg Ryan", label="co_starred_with")
    st.success("Sample data added!")

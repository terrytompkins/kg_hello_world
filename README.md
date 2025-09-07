# Hello World Knowledge Graph Apps

Two Streamlit-based web applications demonstrating different approaches to building, managing, and querying knowledge graphs with OpenAI integration.

## Applications Overview

### 1. NetworkX Version (`app-with-networkx.py`)
A lightweight, in-memory knowledge graph application using NetworkX for graph operations and Matplotlib for visualization.

**Features:**
- **Interactive Graph Building**: Manually add entities and relationships through a web interface
- **Graph Visualization**: Visual representation using NetworkX and Matplotlib
- **JSON Persistence**: Save and load knowledge graphs as JSON files
- **AI-Powered Queries**: Query your knowledge graph using OpenAI's GPT models
- **Sample Data**: Quick start with pre-built movie knowledge graph

### 2. Graphiti Version (`app-with-graphiti.py`)
A sophisticated knowledge graph application using Graphiti for LLM-based entity extraction and Neo4j for persistent storage.

**Features:**
- **Document Ingestion**: Upload text documents or paste text for automatic entity/relationship extraction
- **LLM-Powered Extraction**: Graphiti automatically extracts entities and relationships using OpenAI
- **Neo4j Storage**: Persistent graph storage in Neo4j database
- **Chat Interface**: Conversational interface for querying the knowledge graph
- **Context-Aware Responses**: AI responses augmented with relevant graph context

## Prerequisites

### For NetworkX Version:
- Python 3.7 or higher
- OpenAI API key

### For Graphiti Version:
- Python 3.7 or higher
- OpenAI API key
- Neo4j database (running on localhost:7687)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd kg_hello_world
```

2. Install dependencies for your chosen version:

**For NetworkX version:**
```bash
pip install -r requirements-networkx.txt
```

**For Graphiti version:**
```bash
pip install -r requirements-graphiti.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

4. (Graphiti version only) Set up Neo4j:
   - Install and start Neo4j database
   - Default connection: `bolt://localhost:7687`
   - Default credentials: `neo4j/password` (change in the app code)

## Usage

### NetworkX Version

1. Start the application:
```bash
streamlit run app-with-networkx.py
```

2. Build your knowledge graph:
   - Use the sidebar to manually add entities and relationships
   - Click "Add Relationship" to add connections
   - Use "Add Sample Movie KG" for quick start with example data

3. Visualize and query:
   - View your graph visualization in the main area
   - Query entities using the query section
   - Save/load your graph as JSON files

### Graphiti Version

1. Start the application:
```bash
streamlit run app-with-graphiti.py
```

2. Ingest documents:
   - Paste text or upload TXT files in the sidebar
   - Click "Ingest into KG" to automatically extract entities and relationships
   - Use "Clear Graph" to reset the database

3. Chat with your knowledge graph:
   - Use the chat interface to ask questions
   - The system retrieves relevant context from the graph
   - Get AI-powered responses augmented with graph knowledge

## Project Structure

```
kg_hello_world/
├── app-with-networkx.py      # NetworkX-based knowledge graph app
├── app-with-graphiti.py      # Graphiti-based knowledge graph app
├── requirements-networkx.txt # Dependencies for NetworkX version
├── requirements-graphiti.txt # Dependencies for Graphiti version
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── kg.json                  # Saved NetworkX graph (created when you save)
```

## Dependencies

### NetworkX Version:
- **streamlit**: Web application framework
- **networkx**: Graph data structure and algorithms
- **matplotlib**: Graph visualization
- **openai**: OpenAI API client for AI-powered queries

### Graphiti Version:
- **streamlit**: Web application framework
- **graphiti-core**: Knowledge graph framework with LLM integration
- **neo4j**: Neo4j Python driver for database connectivity
- **openai**: OpenAI API client for AI-powered queries

## Configuration

Both applications use the following environment variable:
- `OPENAI_API_KEY`: Your OpenAI API key for AI-powered graph queries

The Graphiti version also requires Neo4j database configuration (hardcoded in the demo).

## Example Usage

### NetworkX Version:
1. Start with sample data by clicking "Add Sample Movie KG"
2. Query "Tom Hanks" to see AI-generated insights about his relationships
3. Manually add your own entities and relationships
4. Save your work to continue building later

### Graphiti Version:
1. Ingest a document about movies, companies, or any topic
2. Ask questions like "What movies did Tom Hanks star in?"
3. The system automatically extracts and stores relationships
4. Get context-aware responses based on your ingested knowledge

## Comparison

| Feature | NetworkX Version | Graphiti Version |
|---------|------------------|------------------|
| **Setup Complexity** | Simple | Requires Neo4j |
| **Data Input** | Manual entry | Document ingestion |
| **Entity Extraction** | Manual | LLM-powered |
| **Storage** | JSON files | Neo4j database |
| **Scalability** | Limited | High |
| **Visualization** | Built-in | Not included |
| **Query Interface** | Simple form | Chat interface |

## Troubleshooting

### Common Issues:
- **OpenAI API errors**: Ensure your API key is set correctly and you have sufficient credits
- **Neo4j connection errors** (Graphiti version): Verify Neo4j is running and credentials are correct
- **Import errors**: Verify all dependencies are installed with the appropriate requirements file
- **Graph not displaying** (NetworkX version): Make sure you have added at least one relationship

## License

This project is open source and available under the MIT License.

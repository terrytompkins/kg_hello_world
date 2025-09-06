# Hello World Knowledge Graph App

A Streamlit-based web application for building, visualizing, and querying knowledge graphs with OpenAI integration.

## Features

- **Interactive Graph Building**: Add entities and relationships through a simple web interface
- **Graph Visualization**: Visual representation of your knowledge graph using NetworkX and Matplotlib
- **Persistent Storage**: Save and load knowledge graphs as JSON files
- **AI-Powered Queries**: Query your knowledge graph using OpenAI's GPT models
- **Sample Data**: Quick start with pre-built movie knowledge graph

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd kg_hello_world
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

3. Build your knowledge graph:
   - Use the sidebar to add entities and relationships
   - Click "Add Relationship" to add connections to your graph
   - Use "Add Sample Movie KG" for a quick start with example data

4. Visualize your graph:
   - The main area displays your knowledge graph visualization
   - Nodes represent entities, edges represent relationships

5. Query your knowledge graph:
   - Enter an entity name in the query section
   - Click "Query and Generate Response" to get AI-powered insights

6. Save and load your work:
   - Use "Save to JSON" to persist your knowledge graph
   - Use "Load from JSON" to restore a previously saved graph

## Project Structure

```
kg_hello_world/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore rules
└── kg.json           # Saved knowledge graph (created when you save)
```

## Dependencies

- **streamlit**: Web application framework
- **networkx**: Graph data structure and algorithms
- **matplotlib**: Graph visualization
- **openai**: OpenAI API client for AI-powered queries

## Configuration

The application uses the following environment variable:
- `OPENAI_API_KEY`: Your OpenAI API key for AI-powered graph queries

## Example Usage

1. Start with sample data by clicking "Add Sample Movie KG"
2. Query "Tom Hanks" to see AI-generated insights about his relationships
3. Add your own entities and relationships to build a custom knowledge graph
4. Save your work to continue building later

## Troubleshooting

- **OpenAI API errors**: Ensure your API key is set correctly and you have sufficient credits
- **Graph not displaying**: Make sure you have added at least one relationship
- **Import errors**: Verify all dependencies are installed with `pip install -r requirements.txt`

## License

This project is open source and available under the MIT License.

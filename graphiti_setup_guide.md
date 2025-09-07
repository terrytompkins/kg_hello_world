# Setup Guide for Graphiti Knowledge Graph App

This guide outlines the steps to run the Graphiti-based knowledge graph app (`kg_graphiti_app.py`) with a local Neo4j database for your class demo. The app uses Graphiti for entity/relation extraction, Neo4j for storage, and Streamlit for the UI, with OpenAI for LLM augmentation.

## 1. Install Python Dependencies
Install the required Python packages:
```bash
pip install graphiti-core streamlit openai
```
- `graphiti-core`: Handles knowledge graph ingestion and querying.
- `streamlit`: Powers the web UI.
- `openai`: Used for chat responses and Graphiti’s internal LLM calls.

Verify installation:
```bash
pip show graphiti-core streamlit openai
```

## 2. Set Up OpenAI API Key
Graphiti and the app require an OpenAI API key for entity extraction and chat responses.
1. Obtain an API key from [OpenAI](https://platform.openai.com/account/api-keys).
2. Set it as an environment variable:
   - **Linux/Mac**:
     ```bash
     export OPENAI_API_KEY="your-api-key"
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     set OPENAI_API_KEY=your-api-key
     ```
   - Alternatively, add to a `.env` file and load with `python-dotenv` (not implemented in the app for simplicity).
3. Verify the key is set:
   ```bash
   echo $OPENAI_API_KEY
   ```
   If empty, re-run the export command.

## 3. Run a Local Neo4j Instance via Docker
The app uses Neo4j Community Edition as the graph database backend. Docker is the easiest way to run it locally.
1. Ensure Docker is installed:
   ```bash
   docker --version
   ```
   If not, install from [Docker’s website](https://docs.docker.com/get-docker/).
2. Pull and run the Neo4j container:
   ```bash
   docker run --publish=7474:7474 --publish=7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
   ```
   - `--publish=7474:7474`: Exposes Neo4j’s browser interface.
   - `--publish=7687:7687`: Exposes the Bolt protocol for the app’s connection.
   - `-e NEO4J_AUTH=neo4j/password`: Sets default credentials (username: `neo4j`, password: `password`).
3. Verify Neo4j is running:
   - Open http://localhost:7474 in a browser.
   - Log in with username `neo4j` and password `password`.
   - You should see the Neo4j Browser interface.
4. Keep the terminal running the Docker container open. To stop later:
   ```bash
   docker stop $(docker ps -q --filter ancestor=neo4j)
   ```

## 4. Save and Review the App Code
Ensure you have the app code saved as `kg_graphiti_app.py` (from artifact ID `37e1f7cd-f48c-4a8c-ab1f-f88415efc85e`). Key details:
- **Neo4j Connection**: The app uses `bolt://localhost:7687`, `user="neo4j"`, `password="password"`. If you change the Neo4j password in the Docker command, update these in the `Graphiti` initialization.
- **OpenAI**: Uses `gpt-3.5-turbo` by default; switch to `gpt-4o` if desired (edit `model` in the `openai_client.chat.completions.create` call).
- **Ingestion**: Supports text input or TXT file uploads (e.g., the provided SOAP notes).

## 5. Save SOAP Note Files
For the demo, use the provided pet SOAP notes (artifacts `38deca1f-7321-4fc5-9c6c-e18818dfb18e`, `a5576679-e46e-4020-95f5-d97c4c716baf`, `305cf632-1008-4812-b8ae-76c0b688b1bb`). Save them as text files:
- `soap_note_1.txt`
- `soap_note_2.txt`
- `soap_note_3.txt`
Copy the content from each artifact into a `.txt` file on your system.

## 6. Start the Streamlit App
Run the app:
```bash
streamlit run kg_graphiti_app.py
```
- Streamlit will open a browser window (e.g., http://localhost:8501).
- If it doesn’t, navigate to the URL shown in the terminal.

## 7. Demo the App
1. **Ingest Data**:
   - In the sidebar, paste a SOAP note into the text area or upload a `.txt` file (e.g., `soap_note_1.txt`).
   - Click "Ingest into KG". Graphiti uses OpenAI to extract entities/relations (e.g., "Max has_condition arthritis") and stores them in Neo4j.
   - Repeat for other SOAP notes to build a cumulative graph.
2. **Query**:
   - Enter a question in the chat input (e.g., "What medications has Max received?").
   - The app retrieves relevant edges from the graph, augments the OpenAI prompt, and displays the response.
3. **Clear Graph**:
   - Click "Clear Graph" to reset the Neo4j database for a fresh demo.
4. **Teaching Tips**:
   - Show the code’s simplicity: `add_episode` for ingestion, `search_edges` for retrieval.
   - Ingest SOAP notes sequentially to demonstrate knowledge aggregation.
   - Query examples: "What conditions has Max had?" or "Who owns Max?" to highlight relational retrieval.

## Troubleshooting
- **Neo4j Connection Error**:
  - Ensure the Docker container is running and ports 7474/7687 are not blocked.
  - Verify credentials in `kg_graphiti_app.py` match the Docker setup (`neo4j/password`).
  - Check Neo4j Browser at http://localhost:7474.
- **OpenAI Error**:
  - Confirm `OPENAI_API_KEY` is set correctly (`echo $OPENAI_API_KEY`).
  - Check your API quota at OpenAI’s dashboard.
- **Streamlit Issues**:
  - Upgrade Streamlit: `pip install --upgrade streamlit`.
  - Ensure Python 3.8+ and all dependencies are installed.
- **Ingestion Failure**:
  - Verify the input text is not empty.
  - Check OpenAI API key and network connectivity.

## Notes
- **Neo4j Persistence**: The Docker container persists data unless you remove it (`docker rm`). To reset, stop the container, remove it (`docker rm $(docker ps -a -q --filter ancestor=neo4j)`), and restart.
- **Graphiti**: Automatically handles entity/relation extraction, making it ideal for a simple demo. Review the code with students to show how `add_episode` simplifies ingestion compared to manual extraction.
- **SOAP Notes**: The provided notes (e.g., Max’s arthritis, gastroenteritis) create a rich graph for queries like treatment history or owner relationships.
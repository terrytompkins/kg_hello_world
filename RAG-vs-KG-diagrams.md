RAG vs. Knowledge Graph Diagrams for LLM Memory
Below are two Mermaid.js flowcharts illustrating how Retrieval-Augmented Generation (RAG) and Knowledge Graphs (KGs) serve as external memory for LLMs in generative AI applications.
RAG Pipeline
This diagram shows the process of RAG, where unstructured documents are chunked, embedded, and retrieved via similarity search to augment an LLM's response.
graph TD
    A[Documents] -->|Chunking| B[Text Chunks]
    B -->|Embedding e.g. Sentence Transformers| C[Vector Embeddings]
    C -->|Store| D[Vector Database e.g. Pinecone, FAISS]
    E[User Query] -->|Embedding| F[Query Vector]
    F -->|Similarity Search e.g. Cosine| D
    D -->|Retrieve Top-K| G[Relevant Chunks]
    G -->|Augment Prompt| H[LLM e.g. GPT-3.5]
    H --> I[Generated Response]

    classDef data fill:#d0eafd,stroke:#3399cc,stroke-width:2px;
    classDef query fill:#f3efd6,stroke:#ddbc0d,stroke-width:2px;
    classDef gen fill:#e8f5e9,stroke:#43a047,stroke-width:2px;

    class A,B,C,D data;
    class E,F query;
    class G,H,I gen;

Knowledge Graph Pipeline
This diagram illustrates the KG process, where structured entities and relations are extracted, stored in a graph, traversed based on a query, and used to augment an LLM's response.
flowchart TD
    A[Data Sources] -->|Entity/Relation Extraction| B[Triples]
    B -->|Construct| C[Knowledge Graph]
    C -->|Store| D[Graph Storage]
    E[User Query] -->|Parse Entities| F[Query Entities]
    F -->|Traversal/Query| D
    D -->|Retrieve Subgraph| G[Relevant Entities/Relations]
    G -->|Serialize to Text| H[Augmented Prompt]
    H -->|Feed to| I[LLM]
    I --> J[Generated Response]

    %% Assign styles for nodes
    style A fill:#4CB7F6,stroke:#02577A,stroke-width:2px,color:#fff
    style B fill:#56D798,stroke:#187541,stroke-width:2px,color:#fff
    style C fill:#FFE275,stroke:#A69A29,stroke-width:2px
    style D fill:#E7B6F7,stroke:#7C2287,stroke-width:2px
    style E fill:#60C1F6,stroke:#076A8F,stroke-width:2px,color:#fff
    style F fill:#5EBD8C,stroke:#1E7544,stroke-width:2px,color:#fff
    style G fill:#FFD86C,stroke:#A68022,stroke-width:2px
    style H fill:#F6B47B,stroke:#A65C25,stroke-width:2px
    style I fill:#9AC2FF,stroke:#29468A,stroke-width:2px
    style J fill:#FF8D8D,stroke:#A62626,stroke-width:2px,color:#fff


Key Contrasts

RAG: Relies on unstructured text, uses vector embeddings for semantic similarity, excels at broad topical retrieval.
KG: Uses structured relations (nodes/edges), leverages graph traversal for precise relational queries, ideal for multi-hop reasoning.
Both augment LLMs by providing external context, reducing hallucinations, and enabling domain-specific or updated knowledge.

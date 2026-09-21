═══════════════════════════════════════
TOPIC: 15 | Quadrant Vector Database | Free AI Engineer Course | 8 Weeks
LECTURER: Pratyush
SOURCE: [https://youtu.be/7bxSYeNSWmQ](https://youtu.be/7bxSYeNSWmQ?utm_source=gemini)
═══════════════════════════════════════

## 1. Introduction and Context

### 1.1 Transitioning to Vector Databases

* Previous RAG implementations stored knowledge directly inside Python code using standard Python dictionaries.
* Storing knowledge inside Python code works for tiny datasets but breaks down when scaling.
* This lecture integrates Qdrant into the RAG system as a dedicated vector database.

---

## 2. Why Vector Database?

### 2.1 Limitations of In-Code Vector Storage

* As the knowledge base grows from 7 lines to 700 lines or 7 million lines, Python in-code storage encounters major bottlenecks:
* **Time / Linear Search Problem:**
* Computing cosine similarity line-by-line across all stored vectors is a linear search.
* 7 lines take milliseconds/nanoseconds.
* 10,000 lines (10,000 vectors) take ~1 second per search.
* 1,000,000 lines (1 million vectors) take ~30 seconds per search.
* A 30-second delay per search query leads to unacceptable user experience.


* **Persistence Problem:**
* Vectors held in local Python memory are completely lost if the program closes or electricity/power cuts off.
* Regenerating 1 million vector embeddings on restart can take 1 hour or more every time.
* Qdrant keeps vectors persistently stored independent of local machine power or restarts.


* **Memory Problem:**
* Storing 7 lines takes ~7 KB/MB of space, but 1 million vector lines require ~7 GB of RAM.
* A standard laptop with 8 GB RAM cannot accommodate 7 GB of vector memory in local execution.


* **Concurrent Access:**
* Handling concurrent multi-user requests directly in local Python code depends heavily on software configurations and is inefficient.





Example from video:
A user chatting with a ChatGPT-like system where every query takes 30 seconds to search through 1 million vectors becomes frustrated.

---

## 3. Vector Database Softwares & Selection of Qdrant

### 3.1 Overview of Vector Databases

* Various vector databases exist in the industry, including:
* Weaviate
* Chroma DB
* FAISS
* Pinecone
* PGVector
* Qdrant



### 3.2 Reasons for Choosing Qdrant

* **Free Tier Availability:** Qdrant offers a free cloud option up to 1 GB, allowing hands-on learning without payment (unlike Pinecone which requires payment).
* **Ease of Use:** Simple to write, configure, and integrate (unlike Weaviate which has a steep learning curve).

---

## 4. Qdrant Concepts vs SQL Databases

### 4.1 Structural Mapping

* **Table vs Collection:**
* SQL databases store relational data in **Tables** with rows and columns (e.g., ID, Name, Address).
* Vector databases like Qdrant store data in **Collections** containing array vectors (e.g., 384-dimensional embeddings).


* **Row vs Point:**
* Individual data records in SQL tables are called Rows.
* Individual records in Qdrant Collections are called **Points**.



### 4.2 Anatomy of a Qdrant Point

A Point in Qdrant consists of three core elements:

1. **ID:** Unique identifier (e.g., `1001`).
2. **Vector:** The actual numerical embedding array (e.g., a 384-length array like `[1, 0, 1, -2, -3, -1]`).
3. **Payload:** The actual raw text/data string from which the vector embedding was generated (e.g., `"Pratyush is a Good Teacher"`).

Example from video:
An SQL Table storing columns ID, Name, Address (`1001, Pratyush, Bengaluru`) versus a Qdrant Collection storing Points with ID, Vector, and Payload.

---

## 5. End-to-End RAG Workflow with Qdrant

### 5.1 Storage Phase

* Knowledge base text file (`knowledge.txt`) is read line-by-line into a Python document list.
* SentenceTransformer model converts each text line into a 384-length vector array.
* Each line is structured as a Qdrant Point (ID, Vector, Payload text line) and uploaded (`upsert`) to the Qdrant Cloud collection.

### 5.2 Retrieval Phase and Purpose of Payload

* User query is converted into a query vector array using the same embedding model.
* Query vector is sent to Qdrant, which runs Cosine Similarity across points to find top-k matching vectors (using internal algorithms like HNSW rather than naive linear search).
* **Why Payload is mandatory:** LLMs are text-based machines and cannot interpret raw numerical arrays. Qdrant returns both the matching Vector AND its Payload (the original text line).
* The retrieved text lines (Payload) are passed as context alongside the user query to the LLM.
* The LLM processes the text context and returns the final textual response.

Example from video:
For the user question `"How many vacation days do I get?"`, Qdrant returns top match with score `0.480` and payload `"Employees receive 24 days of paid leave per year"`.

---

## 6. Qdrant Setup & Code Implementation

### 6.1 Prerequisites and Environment Configuration

* Qdrant Cloud Cluster setup yields two credentials stored in `.env`:
* `QDRANT_URL` (Cluster Endpoint)
* `QDRANT_API_KEY`


* Dependencies installed via `uv add`:
* `qdrant-client`
* `sentence-transformers`
* `python-dotenv`
* `groq`



### 6.2 Step-by-Step Code Walkthrough

* Connect Qdrant Client using URL and API Key.
* Create a collection named `knowledge` with vector size `384` and `Distance.COSINE`.
* Load text lines from `knowledge.txt`, generate vector embeddings, wrap into `PointStruct` objects, and `upsert` to Qdrant.
* Search Qdrant using `client.query_points()` with `with_payload=True`.
* Pass retrieved payload text into Groq LLM API to output the answer.

Code (if any):

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Set up API Keys and URL
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Qdrant Client
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print("Connected to Qdrant Cloud")

# Collection Configuration
COLLECTION_NAME = "knowledge"
EMBEDDING_SIZE = 384

# Delete collection if it already exists
client.delete_collection(collection_name=COLLECTION_NAME)

# Create collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE)
)

# Load Knowledge Base
with open("knowledge.txt", "r") as f:
    documents = [line.strip() for line in f if line.strip()]

# Generate Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(documents)

# Create Qdrant Points
points = []
for i, embedding in enumerate(embeddings):
    points.append(
        PointStruct(
            id=i + 1,
            vector=embedding.tolist(),
            payload={"text": documents[i]}
        )
    )

# Upload / Upsert Points to Qdrant
client.upsert(collection_name=COLLECTION_NAME, points=points)

# Search Function
def search(query, top_k=3):
    query_vector = model.encode(query).tolist()
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )
    return results

# Ask LLM Function
def ask_llm(question, context):
    groq_client = Groq(api_key=GROQ_API_KEY)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Complete RAG Pipeline Execution
query = "How many vacation days do I get?"
search_results = search(query, top_k=3)

# Extract context from Qdrant response payload
context_lines = [point.payload["text"] for point in search_results.points]
context = "\n".join(context_lines)

# Generate answer
final_answer = ask_llm(query, context)
print("Final Answer:", final_answer)

```

---

═══════════════════════════════════════
QUICK REVISION SUMMARY
═══════════════════════════════════════

* RAG system previously used Python in-code dictionary storage which fails as dataset size grows.
* In-code storage causes 3 major problems: Time (Linear Search latency), Persistence (Loss of vectors on restart/power loss), and Memory (Excessive RAM consumption).
* Qdrant solves these 3 issues by storing vectors persistently, offloading memory, and utilizing fast search algorithms.
* Vector DB options include Qdrant, Weaviate, Chroma DB, FAISS, Pinecone, and PGVector.
* Qdrant was chosen due to its 1 GB free tier and low learning curve.
* SQL Tables map to Qdrant Collections; SQL Rows map to Qdrant Points.
* A Qdrant Point contains 3 parts: ID, Vector array, and Payload (original text).
* Payload is essential because LLMs are text-based and require original text rather than vector arrays to answer questions.
* Qdrant `upsert` handles uploading and inserting points into a collection.
* Qdrant `query_points` executes vector search using Cosine Similarity and returns matching vectors along with their payload text.
* The retrieved payload text is supplied as context to Groq LLM to answer the user's question.

═══════════════════════════════════════
DEFINITIONS (from video only)
═══════════════════════════════════════

* **Qdrant:** A vector database software used to persistently store and quickly search vector embeddings.
* **Collection:** The vector database equivalent of a table in SQL databases, used to store vector embeddings and points.
* **Point:** A single data entry inside a Qdrant Collection, composed of an ID, a Vector array, and a Payload.
* **Payload:** The original raw text/data string stored alongside a vector in a Qdrant Point, representing the text from which the embedding was computed.
* **Upsert:** An operation that combines Upload and Insert (inserts a point if it does not exist, or updates/leaves it if it already exists based on point ID).
* **Linear Search:** Sequential iteration across every vector in a dataset to calculate Cosine Similarity, which becomes extremely slow at scale.

═══════════════════════════════════════
EXAMPLES USED IN VIDEO
═══════════════════════════════════════

* **Knowledge Base Scaling & Latency:** 7 lines (ms/ns execution) vs 10,000 lines (~1 second execution) vs 1,000,000 lines (~30 seconds execution per query).
* **Power Cut Loss:** Power failure on a local computer losing 1 million generated vectors, requiring 1 hour of recalculation on restart.
* **RAM Constraint:** Storing 1 million vector lines consuming ~7 GB RAM on an 8 GB RAM laptop.
* **SQL vs Qdrant Mapping:** SQL table with ID, Name, Address (`1001, Pratyush, Bengaluru` and `102, Soham, Delhi`) compared to a Qdrant Collection with Points.
* **Point Structure:** Point ID `1001`, Vector `[1, 0, 1, -2, -3, -1]`, and Payload `"Pratyush is a Good Teacher"`.
* **Query Execution:** User question `"How many vacation days do I get?"` returning top score `0.480` for payload `"Employees receive 24 days of paid leave per year"`, producing final LLM output `"You receive 24 days of paid leave per year."`

═══════════════════════════════════════
CODE WRITTEN IN VIDEO (if any)
═══════════════════════════════════════

* **Python Integration Script with Qdrant and Groq:**
* Demonstrates initialization of `QdrantClient` using cluster URL and API Key.
* Creation of collection `knowledge` with vector size `384` and `Distance.COSINE`.
* Reading `knowledge.txt`, generating 384-dimensional embeddings via `SentenceTransformer('all-MiniLM-L6-v2')`.
* Constructing `PointStruct(id, vector, payload)` objects and pushing via `client.upsert()`.
* Executing query vector search via `client.query_points()` with `with_payload=True`.
* Passing payload context to Groq LLM API (`llama3-8b-8192`) to answer user question.
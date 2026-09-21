═══════════════════════════════════════
TOPIC: Multi-Tenant RAG with Qdrant | Free AI Engineer Course | 8 Weeks
LECTURER: Pratyush
SOURCE: [https://youtu.be/ZCNayichcKE](https://youtu.be/ZCNayichcKE?utm_source=gemini)
═══════════════════════════════════════

## 1. Introduction & Minor Project Idea (YouTube Reviser)

### 1.1 The YouTube Reviser Concept

* Students revising Data Structures and Algorithms (DSA) after watching 100+ videos struggle to recall which specific video or timestamp covered a particular problem or concept (e.g., Sliding Window, Binary Search).
* Searching manually by scrolling through multiple videos wastes time and effort.
* Solution: Automate revision using YouTube video transcriptions.
* YouTube transcript tools convert video audio into text (e.g., a 40-minute video becomes ~3 pages of text).
* Transcripts across all 100 videos are converted into embeddings and stored in a Qdrant vector database as a RAG knowledge base.
* Metadata (video link, exact timestamp) is stored inside the Qdrant point's payload.
* When a user asks about a concept, Qdrant retrieves the relevant transcript chunk along with the video link and exact timestamp (e.g., Video #12 at `30:07`), enabling instant revision.

Example from video:
A student revising a Sliding Window question queries the LLM. Instead of opening 6 different Binary Search / Sliding Window videos, Qdrant searches the transcript vectors and returns: *"Discussed in Video 12 at timestamp 30 minutes 7 seconds"* along with the YouTube URL.

Code (if any):
N/A

---

## 2. Revision of Qdrant Fundamentals

### 2.1 Baseline Qdrant RAG Workflow

* **Knowledge Base:** Plain text file (`knowledge.txt`) containing knowledge lines.
* **Collection:** Storage container in Qdrant holding points (equivalent to a table in SQL).
* **Point Structure:** Composed of three core items:
* `ID`: Unique identifier.
* `Vector`: Array embedding (e.g., 384 size from `all-MiniLM-L6-v2`).
* `Payload`: Raw underlying data/text used to construct the vector.


* **Upsert:** Upload + Insert operation (inserts if new, ignores/updates if existing).
* **Search:** Query vector compared against stored vectors to return top matching context for LLM generation.

Example from video:
A 6-line `knowledge.txt` loaded into Python, converted into 384-dimensional arrays, upserted to Qdrant, and retrieved for Groq LLM prompting.

Code (if any):
N/A

---

## 3. Hierarchical Navigable Small World (HNSW) Algorithm

### 3.1 Intuition and Purpose of HNSW

* **Full Form:** Hierarchical Navigable Small World.
* **Problem with Linear Search:**
* In a database of 100 million vectors (size 384), calculating Cosine Similarity against every vector individually takes 20+ minutes per query.
* Linear search fails completely at production scale.


* **HNSW Concept:**
* Instead of brute-force scanning, HNSW treats vectors as a connected multi-layer graph network.
* It makes large "hops" across vector regions to move directly closer to the query destination before performing local searches.


* **Qdrant Integration:** Qdrant automatically uses HNSW internally for top-k vector retrieval, removing the need for manual mathematical implementation.

Example from video:
*Goal:* Reaching "Kalyan Jewellers" in Connaught Place, Delhi while starting from home in BTM (Bangalore).

* **Linear Search Approach:** Walk out of home into local BTM street, ask shop #1 *"Are you Kalyan Jewellers?"*, ask shop #2, ask every shop/bathroom in Bangalore, then ask every shop in every city between Bangalore and Delhi. Eventually works, but takes forever and is extremely inefficient.
* **HNSW Approach:** Ignore local BTM shops completely. Take high-level hops:
1. Ask for local Bangalore Airport.
2. Fly directly from Bangalore Airport to Delhi Airport (skips millions of irrelevant shops in one hop).
3. At Delhi Airport, ask for Connaught Place.
4. Arrive at Connaught Place (as close as possible to target region).
5. Perform local search among the ~10 shops in Connaught Place to instantly find Kalyan Jewellers.



Code (if any):
N/A

---

## 4. Qdrant Filtering (Payload Filtering)

### 4.1 JSON Structure and Real Production Data

* Production RAG knowledge bases use structured JSON format rather than flat string lines.
* JSON entries contain multiple metadata fields: `text`, `category` (e.g., `leave`, `workplace`, `reimbursement`, `career`), `is_active` (boolean `True`/`False`), and `company` (e.g., `Google`, `Akamai`, `Microsoft`).

### 4.2 Payload Indexing

* Before filtering on a payload field (e.g., `category`), a **Payload Index** must be created in Qdrant.
* Indexing allows Qdrant to pre-memorize which point IDs correspond to which field values (e.g., `reimbursement` corresponds to Point IDs `4` and `5`).

### 4.3 Filter Operators (`must`, `must_not`, `should`)

* **`must` (AND Operator):** All specified field conditions must be `True` for a point to be included in vector search.
* **`must_not` (NOT Operator):** Excludes points matching the condition (e.g., exclude `category = "reimbursement"`).
* **`should` (OR Operator):** Points matching at least one condition are included.

Example from video:
An HR policy database containing entries for 24 days leave (`is_active: True`), 12 days leave (`is_active: False`), and 8 hours workday (`category: "workplace"`). A user asking about leave reimbursement triggers a filter for `category = "reimbursement"` and `is_active = True`, narrowing 10 million vectors down to 10 before running HNSW similarity.

Code (if any):
N/A

---

## 5. Code Implementation of Qdrant Filtering

### 5.1 Step-by-Step Code Walkthrough

* Load `knowledge.json` containing `text`, `category`, and `is_active` fields.
* Create Payload Index using `client.create_payload_index()`.
* Extract `text` from JSON documents and encode into 384-dimensional embeddings.
* Upsert `PointStruct` objects with full JSON object stored in `payload`.
* Define filter using `Filter(must=[FieldCondition(key="category", match=MatchValue(value="reimbursement"))])`.
* Execute query search using `client.query_points()` with `query_filter`.
* Note on LLM Model: Groq decommissioned `llama-versatile`, so code updates to supported models (e.g., `openai/gpt-oss-120b`).

Code (if any):

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, Filter, FieldCondition, 
    MatchValue, PayloadSchemaType
)
from sentence_transformers import SentenceTransformer
from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Setup Environment Keys
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Qdrant Client
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print("Connected to Qdrant Cloud")

COLLECTION_NAME = "knowledge_with_filter"
EMBEDDING_SIZE = 384

# Delete existing collection if present
client.delete_collection(collection_name=COLLECTION_NAME)

# Create collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE)
)

# Create Payload Index on 'category' field
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)

# Load JSON Knowledge Base
with open("knowledge.json", "r") as f:
    documents = json.load(f)

# Extract text field for embedding generation
texts = [doc["text"] for doc in documents]

# Generate Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)

# Prepare Qdrant Points
points = []
for i, embedding in enumerate(embeddings):
    points.append(
        PointStruct(
            id=i + 1,
            vector=embedding.tolist(),
            payload=documents[i] # Store full JSON dict as payload
        )
    )

# Upsert Points
client.upsert(collection_name=COLLECTION_NAME, points=points)

# Search Function with Query Filter
def search_with_filter(query, query_filter=None, top_k=3):
    query_vector = model.encode(query).tolist()
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=top_k,
        with_payload=True
    )
    return results

# Define Reimbursement Filter
reimbursement_filter = Filter(
    must=[
        FieldCondition(
            key="category",
            match=MatchValue(value="reimbursement")
        )
    ]
)

# Query Execution
query = "How do I claim money back?"
results = search_with_filter(query, query_filter=reimbursement_filter, top_k=3)

# Extract Context from Payload
context_lines = [point.payload["text"] for point in results.points]
context = "\n".join(context_lines)

# Ask LLM Function (Updated Groq Model)
def ask_llm(question, context):
    groq_client = Groq(api_key=GROQ_API_KEY)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

final_answer = ask_llm(query, context)
print("Final Answer:", final_answer)

```

Lecturer's explanation:

* **Index Creation:** Creating a payload index (`create_payload_index`) is mandatory before filtering; otherwise Qdrant does not pre-map point IDs to metadata keys.
* **Payload Assignment:** Storing the whole document dictionary directly in `payload=documents[i]` allows filtering on any indexed JSON field (`category`, `is_active`, etc.).
* **Query Filter Passing:** Passing `query_filter` inside `client.query_points()` restricts similarity evaluation exclusively to points satisfying the filter criteria.
* **Model Update:** Updated Groq model parameter to `openai/gpt-oss-120b` because `llama-versatile` was decommissioned by Groq.

---

════════════════════════════════════════════════
⚡ QUICK REVISION SUMMARY
════════════════════════════════════════════════

1. Minor Project Idea involves building a YouTube Reviser RAG system for DSA videos using transcripts, timestamps, and Qdrant.
2. Qdrant stores data as Points inside Collections, where each Point holds an ID, Vector array, and Payload dictionary.
3. Linear search across 100 million vectors takes 20+ minutes per query due to brute-force Cosine Similarity checks.
4. HNSW (Hierarchical Navigable Small World) solves linear search slowness by creating multi-layered vector graphs for fast region hops.
5. Real production RAG knowledge bases store structured JSON data containing text alongside metadata fields like category and status.
6. Payload filtering narrows down search space so Qdrant only evaluates vectors matching specific metadata constraints.
7. Filtering on HNSW across 10 relevant vectors is significantly faster than running vector search over 10 million vectors.
8. Payload Indexing (`create_payload_index`) must be executed prior to filtering so Qdrant pre-remembers point ID mappings.
9. `must` acts as a logical AND operator where all field conditions in the filter must evaluate to True.
10. `must_not` acts as a logical NOT operator to exclude specific vector metadata values.
11. `should` acts as a logical OR operator where at least one field condition in the filter must evaluate to True.
12. Groq decommissioned `llama-versatile`, requiring model configuration updates to supported options like `openai/gpt-oss-120b`.

════════════════════════════════════════════════
❓ QUESTIONS RAISED BY LECTURER (if any)
════════════════════════════════════════════════

Q: Why use payload filters instead of searching all vectors in the collection?
A: Searching across all vectors wastes compute and time; filtering restricts search to relevant categories/fields first, drastically reducing vector count before running vector similarity.

Q: What happens if you attempt to filter without creating a payload index first?
A: Qdrant requires payload indexing on specific fields to maintain lookup mappings; without an index, payload filtering cannot be performed efficiently.

════════════════════════════════════════════════
⚠️ IMPORTANT POINTS LECTURER EMPHASISED
════════════════════════════════════════════════

* **Always Create Payload Index First:** You must call `client.create_payload_index()` for every field you plan to use in filters before running queries.
* **Do Not Memorize Code Syntax:** Syntax varies and can be looked up; focus purely on understanding concepts like HNSW intuition and filtering logic.
* **HNSW is Automatic:** You do not write HNSW graph algorithms manually; Qdrant handles HNSW internally when executing vector searches.
* **Update Groq Model Name:** `llama-versatile` has been decommissioned by Groq; replace it with supported model strings in code.

════════════════════════════════════════════════
🔗 CONNECTIONS LECTURER MADE
════════════════════════════════════════════════

* Connected HNSW region hops to traveling from BTM (Bangalore) to Connaught Place (Delhi) via direct airport flights instead of asking every local shop.
* Connected Qdrant filter types (`must`, `must_not`, `should`) to computer science Bitwise / Logic operators (`AND`, `NOT`, `OR`).
* Connected payload filtering to multi-section website FAQ systems (e.g., clicking on specific sections like "Leave" or "Salary" on company/college portals).

═══════════════════════════════════════
DEFINITIONS (from video only)
═══════════════════════════════════════

* **HNSW (Hierarchical Navigable Small World):** A vector graph indexing algorithm that enables fast approximate nearest-neighbor search by performing hierarchical hops across vector regions.
* **Payload Indexing:** Pre-computing and storing mappings between metadata field values and point IDs in Qdrant to enable fast filtering.
* **`must` Filter:** A Qdrant filter constraint requiring all contained conditions to be met (logical AND).
* **`must_not` Filter:** A Qdrant filter constraint excluding points that match the specified condition (logical NOT).
* **`should` Filter:** A Qdrant filter constraint requiring at least one of the contained conditions to be met (logical OR).

═══════════════════════════════════════
EXAMPLES USED IN VIDEO
═══════════════════════════════════════

* **YouTube Reviser Project:** 100 DSA videos converted into text transcripts and loaded into Qdrant, returning exact video link and timestamp (`30:07`) when asked about Sliding Window concepts.
* **Kalyan Jewellers Analogy:** Finding a specific shop in Connaught Place (Delhi) starting from BTM (Bangalore). Linear search asks every shop along the way; HNSW hops directly via Bangalore Airport -> Delhi Airport -> Connaught Place -> local search.
* **HR Policy JSON Metadata:** Filtering policy documents using fields `category` (`leave`, `workplace`, `reimbursement`, `career`), `is_active` (`True`/`False`), and `company` (`Google`, `Akamai`, `Microsoft`).

═══════════════════════════════════════
CODE WRITTEN IN VIDEO (if any)
═══════════════════════════════════════

* **Python Qdrant Filtering Script:** Demonstrates initializing `QdrantClient`, creating collection `knowledge_with_filter`, setting up payload index on `category`, loading `knowledge.json`, upserting points with full dictionary payload, defining `Filter` with `FieldCondition`, executing filtered vector search via `client.query_points(query_filter=...)`, and generating an answer using Groq LLM API.
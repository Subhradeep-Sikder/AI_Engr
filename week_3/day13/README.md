# Study Notes: Building an End-to-End RAG System

**Course Module:** Week 3, Episode 14 (8-Week Free AI Engineer Course)

**Channel:** Padho with Pratyush

**Topic:** Build Your First End-to-End RAG System

---

---

## 1. Evolution of the RAG Architecture

The development of the retrieval mechanism evolves across three main stages:

* **Day 1 — Basic Keyword Retrieval:** Relied on exact string/keyword matching. If a query contained a typo or synonymous term (e.g., searching for *"vacation"* when the policy explicitly says *"paid leave"*), retrieval failed completely.
* **Day 2 — Vector Embeddings:** Focused on converting raw text strings into high-dimensional vector arrays. Texts with similar semantic meanings map close to each other in vector space, yielding high similarity scores even without keyword overlap.
* **Day 3 — End-to-End RAG Integration:** Integrates sentence transformer embeddings into the retrieval phase ($R$). The system retrieves context based on semantic relevance scores and injects it into the LLM prompt ($A$) to generate grounded responses ($G$).

---

## 2. Environment Setup & Dependencies

### Directory Structure & Virtual Environment

1. Create a dedicated folder for the project: `Week_3/Day_13` *(avoid spaces in directory names)*.
2. Initialize and activate a Python virtual environment (`venv`).

### Required Dependencies

```bash
pip install groq python-dotenv sentence-transformers numpy

```

| Package | Purpose |
| --- | --- |
| **`groq`** | Client library for fast LLM inference via Groq API. |
| **`python-dotenv`** | Manages environment variables (API keys) securely. |
| **`sentence-transformers`** | Pre-trained mini-LLM used to compute text vector embeddings. |
| **`numpy`** | Performs mathematical vector array operations. |

---

## 3. End-to-End Implementation Steps

### Step 1: Model & Client Initialization

Create a script named `full_rag.py` and set up the models:

* Load API credentials via `load_dotenv()`.
* Instantiate `SentenceTransformer` for vector encoding.
* Instantiate the Groq API client (`groq_model`).

### Step 2: Knowledge Base Creation

Define the knowledge base documents as a list of strings representing company policies:

```python
documents = [
    "Employees receive 24 days of paid leave per year.",
    "Work from home allowance is $3000 per month.",
    # ... additional policy documents
]

```

### Step 3: Compute Document & Query Embeddings

* Generate vector embeddings for all documents in the knowledge base:
```python
document_embeddings = model.encode(documents)

```


* Convert the incoming user query into a vector representation:
```python
q_embedding = model.encode(query)

```



> **Why Embeddings Outperform Keyword Search:**
> Searching for *"How much vacation do I get?"* fails under exact keyword search because the word *"vacation"* isn't present in the document. By encoding both the query and documents into vectors, Cosine Similarity calculates that *"vacation"* matches the semantic meaning of *"paid leave"*.

### Step 4: Semantic Retrieval Function

Define a `retrieve()` function to compare vector distances and extract the best context:

1. Iterate over document embeddings using `enumerate()` to capture both index and vector content.
2. Calculate the similarity score: `score = cosine_similarity(q_embedding, doc_embedding)`.
3. Append `(score, document_text, index)` to a results list.
4. Sort the results list in descending order (`reverse=True`).
5. Return the top match (`scores[0]`) containing the highest score and its matching document text.

### Step 5: LLM Context Injection & Response Generation

Pass the retrieved top-matching text snippet alongside the original user query to the Groq LLM model (`ask_llm`):

* The LLM reads the injected context snippet and returns an accurate, grounded answer: *"You receive 24 days of paid leave per year."*

---

## 4. Core RAG System Architecture

```
[ User Query ] ──► [ Model Encode ] ──► [ Query Embedding ]
                                              │
                                   Cosine Similarity Search
                                              │
                                              ▼
[ Knowledge Base ] ──► [ Doc Embeddings ] ──► [ Top Matching Context ]
                                              │
                                              ▼
[ Injected Prompt: Context + Query ] ──► [ Groq LLM ] ──► [ Final Answer ]

```

* **R (Retrieval):** Extracting the most semantically relevant text snippet from the knowledge base using vector similarity.
* **A (Augmentation):** Prepending the retrieved context to the prompt sent to the LLM.
* **G (Generation):** The LLM synthesizing a coherent, natural-language answer based strictly on the provided context.

---

## 5. Memory Limitations & The Need for Vector Databases

Checking the memory footprint of vector arrays in Python using `sys.getsizeof()` highlights why storing vectors in standard RAM does not scale:

| Knowledge Base Size | Estimated Memory Usage | Practical Feasibility |
| --- | --- | --- |
| **6 Document Lines** | ~7.8 KB (7,808 bytes) | Negligible (Works in RAM) |
| **600,000 Lines** | ~70 MB | Fits in memory |
| **6,000,000 Lines** | ~700 MB | High memory consumption |
| **60,000,000 Lines** | ~7 GB RAM | Exceeds standard machine RAM capacity |

### Critical Bottlenecks

1. **Memory Capacity Constraints:** Enterprise knowledge bases containing millions of lines exceed available system RAM when kept purely as Python lists/arrays.
2. **Computational Latency ($O(N)$ Linear Search):** Running brute-force cosine similarity checks across millions of vectors for every single query causes massive search delays and unacceptably high response latency.

### Solution: Vector Databases (e.g., Qdrant)

Vector Databases solve both bottlenecks by efficiently indexing and storing high-dimensional vectors on disk, enabling sub-second similarity search across millions of documents without overloading system RAM.

---

## 6. Key Takeaways & Best Practices

* **Threshold Filtering:** Implement a similarity score cutoff. If the top similarity score falls below a set threshold (e.g., a negative score for off-topic queries), return `None` as context so the LLM explicitly states the answer is unavailable rather than hallucinating.
* **Scaling Path:** Transitioning from in-memory array operations to a dedicated Vector DB like **Qdrant** is essential for production-grade RAG pipelines.
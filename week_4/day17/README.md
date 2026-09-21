═══════════════════════════════════════

TOPIC: RAG Evaluation | The Most Imp AI Interview Question

LECTURER: Pratyush

SOURCE: [https://youtu.be/KhHr4Y6v2TE](https://youtu.be/KhHr4Y6v2TE?utm_source=gemini)
═══════════════════════════════════════

## 1. Introduction to RAG Evaluation & Interview Perspective

### 1.1 Why RAG Evaluation Matters

* In AI engineering interviews, interviewers rarely ask candidates to write basic RAG boilerplate code. Instead, they probe deeply into internal system mechanics and evaluation.
* RAG Evaluation answers the foundational question: "Is my RAG system working correctly or not?"
* Simply looking at an answer and visually checking if it looks fine is insufficient because RAG systems have multiple internal failure layers.

### 1.2 LeetCode and Failed Student Analogies

* **LeetCode DSA Analogy:** In LeetCode, code correctness is evaluated automatically against hidden test cases (Passed, Wrong Answer, Time Limit Exceeded). RAG evaluation serves as the test suite for a RAG pipeline.
* **Student Exam Analogy:**
* When a student fails an exam, people assume the student lacks intelligence.
* However, the failure could be caused by three distinct issues:
1. The student did not study or lacked intelligence (LLM error).
2. The teacher provided incorrect or incomplete revision notes (Context Retrieval error).
3. The syllabus/textbook itself was wrong or for a completely different subject (Knowledge Base error).


* An incorrect final answer in RAG cannot automatically be blamed on the LLM; the exact layer of failure must be isolated.



Example from video:
A student studying for a Social Studies exam is given incorrect notes by a teacher. Even if the student studies perfectly, they will fail the exam due to bad input notes, not due to personal stupidity.

Lecturer's explanation:

* **Root Cause Isolation:** Stressed that buying a more expensive LLM model will not fix a broken RAG pipeline if the underlying failure lies in context retrieval or source knowledge quality.

---

## 2. The Three Points of Failure in a RAG Pipeline

### 2.1 Pipeline Flow & Failure Modes

* **RAG Architecture Flow:** Source Knowledge Base -> Vector Embeddings -> Vector DB (Qdrant) -> Query Embedding -> Cosine Similarity Matching -> Context Retrieval -> LLM -> Final Answer.
* **Failure Mode 1: Knowledge Base Failure (Syllabus Error)**
* The source data itself contains incorrect or outdated facts (e.g., source file says 15 days leave when company policy is actually 12 days).


* **Failure Mode 2: Context Retrieval Failure (Notes Error)**
* Vector search returns irrelevant context chunks (e.g., query asks about leave policy, but vector DB retrieves salary information).


* **Failure Mode 3: LLM Generation Failure (Student Error)**
* Correct context is retrieved and passed, but the LLM misinterprets the text or hallucinates an incorrect answer.



Example from video:
Asking a RAG system "How many days of leave does Akamai provide?" where the system retrieves a context chunk stating "Monthly salary is ₹50,000". The failure occurs at the context retrieval layer, not the LLM layer.

---

## 3. The Golden Dataset & Evaluation Setup

### 3.1 What is a Golden Dataset?

* A Golden Dataset is the set of ground-truth test cases used to evaluate a RAG system (equivalent to LeetCode test cases).
* Constructed by a human expert (or an LLM auditor) reading the knowledge base.

### 3.2 Components of a Golden Dataset Entry

1. **Question:** A test query expected from end users (e.g., `"How many vacation days do I get?"`).
2. **Ground Truth:** The absolute factual answer based on the knowledge base (e.g., `"Employees in India receive 24 days of paid leave per year"`).
3. **Expected Information:** Key factual details that must appear in the output to maintain answer relevancy and prevent irrelevant topic dumps.

Example from video:
For a 5-line knowledge base, a 1-question Golden Dataset may suffice. For a complex corporate policy database, a Golden Dataset may contain 30 to 200+ test questions to cover edge cases.

---

## 4. Context Retrieval Evaluation Metrics

### 4.1 Context Precision

* **Definition:** The ratio of relevant retrieved context chunks to the total number of context chunks retrieved from the vector database.
* **Formula:**

$$\text{Context Precision} = \frac{\text{Number of Relevant Retrieved Chunks}}{\text{Total Number of Chunks Retrieved}}$$


* **Significance:** Measures retrieval accuracy and signal-to-noise ratio.
* **How to Fix Low Precision:**
1. Reduce `top_k` (e.g., retrieve top 3 results instead of top 10).
2. Increase the similarity score threshold (e.g., only pass vectors with cosine similarity $> 0.4$ or $0.5$).



Example from video:
Qdrant retrieves 3 lines for a leave query:

1. "12 days of paid leave" (Relevant)
2. "3 additional days of sick leave" (Relevant)
3. "₹50,000 monthly salary" (Irrelevant)
Total retrieved = 3, Relevant = 2. Context Precision = $2 / 3 = 66.6\%$.

### 4.2 Context Recall

* **Definition:** The ratio of relevant retrieved context chunks to the total number of relevant context chunks existing in the source knowledge base.
* **Formula:**

$$\text{Context Recall} = \frac{\text{Number of Relevant Retrieved Chunks}}{\text{Total Actual Relevant Chunks in Knowledge Base}}$$


* **Significance:** Measures retrieval completeness (whether the vector DB forgot or missed key information).
* **How to Fix Low Recall:**
1. Increase `top_k` (e.g., retrieve top 5 results instead of top 1).
2. Lower the similarity score threshold (e.g., lower threshold from 0.9 to 0.4).



Example from video:
Knowledge base contains two relevant facts: (1) "12 days normal leave" and (2) "3 days sick leave" (Total = 15 days). Qdrant retrieves only line (1). Context Precision is $1/1 = 100\%$, but Context Recall is $1/2 = 50\%$. The LLM outputs "12 days total", which is incomplete because Qdrant failed to recall the second line.

Lecturer's explanation:

* **Precision vs Recall Tradeoff:** Demonstrates that precision and recall require opposite tuning actions: fixing low precision requires reducing `top_k`/raising thresholds, whereas fixing low recall requires increasing `top_k`/lowering thresholds.

---

## 5. LLM Generation Evaluation Metrics

### 5.1 Faithfulness

* **Definition:** Evaluates whether the LLM's generated answer is derived *strictly* and *faithfully* from the retrieved context without hallucinating outside information.
* **Unfaithful Output:** The LLM receives context stating "12 days paid leave", but outputs "10 days paid leave" or adds unprovided facts.
* **How to Fix Low Faithfulness:** Update the LLM system prompt with strict negative constraints (e.g., `"Answer strictly using the provided context. Do not hallucinate or use outside knowledge."`).

### 5.2 Answer Correctness

* **Definition:** Evaluates whether the LLM's generated answer matches the absolute `Ground Truth` defined in the Golden Dataset.
* **Distinction Between Faithfulness and Correctness:**
* *Faithful but Incorrect:* The retrieved context falsely says "10 days leave", and the LLM faithfully outputs "10 days leave". The LLM is 100% faithful to the context, but the answer is incorrect relative to Ground Truth (12 days).
* *Unfaithful but Correct:* The retrieved context falsely says "Newton has 4 laws", but the LLM uses its external pre-training memory to output "Newton has 3 laws". The answer is correct in the real world, but unfaithful to the provided context (hallucination).


* **How to Fix Low Correctness:** Audit and correct source knowledge base files, and fix context retrieval issues.

Example from video:
A teacher teaches a student that Newton has 4 laws of motion.

* If the student writes "4 laws" on the exam: Faithful to teacher, but Incorrect relative to real-world ground truth.
* If the student writes "3 laws" on the exam: Unfaithful to teacher's notes, but Correct relative to real-world ground truth.

### 5.3 Answer Relevancy

* **Definition:** Evaluates whether the generated answer directly answers the user's prompt without introducing off-topic definitions or fluff.
* **Irrelevant Output:** User asks `"When does promotion happen?"`. The LLM outputs `"Promotion refers to advancing an employee's rank and salary status..."`. The definition is factually correct, but completely irrelevant to *when* promotion occurs (November).
* **How to Fix Low Relevancy:** Refine the system prompt (e.g., `"Answer to the point. Do not provide definitions or off-topic information unless requested."`).

Lecturer's explanation:

* **LLM-as-a-Judge:** Explained that automated evaluation scripts use an evaluator LLM to judge Precision, Recall, Faithfulness, Relevancy, and Correctness for each query run against the RAG system.

---

## 6. Summary Matrix of RAG Evaluation Metrics & Actions

| Metric | Measured Layer | What it Evaluates | Root Cause if Low | Corrective Action |
| --- | --- | --- | --- | --- |
| **Context Precision** | Retrieval (Vector DB) | Percentage of retrieved chunks that are relevant | Vector DB returning noisy/irrelevant chunks | Reduce `top_k`, raise similarity threshold |
| **Context Recall** | Retrieval (Vector DB) | Percentage of total available relevant facts retrieved | Vector DB missing relevant chunks | Increase `top_k`, lower similarity threshold |
| **Faithfulness** | Generation (LLM) | Grounding of answer strictly in retrieved context | LLM hallucinating outside context | Add system prompt rule: "Do not hallucinate" |
| **Answer Correctness** | End-to-End Pipeline | Alignment of final answer with Ground Truth | Source data errors or context retrieval errors | Fix knowledge base source files & retrieval |
| **Answer Relevancy** | Generation (LLM) | Directness of answer relative to question asked | LLM failing to comprehend prompt intent | Add system prompt rule: "Answer to the point" |

---

## 7. Code Implementation Walkthrough

### 7.1 Automated Evaluation Pipeline Script

* The script loads `knowledge.json`, creates embeddings, upserts to Qdrant, and executes queries from the Golden Dataset.
* Evaluates retrieved context chunks and generated LLM answers against Ground Truth using an evaluator LLM.
* Outputs detailed diagnostic logs per test case.

Code (if any):

```python
import json
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

# Environment Keys
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Clients
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

COLLECTION_NAME = "eval_demo"
EMBEDDING_SIZE = 384

# Golden Dataset Definition
golden_dataset = [
    {
        "id": 1,
        "question": "How many vacation days do I get?",
        "ground_truth": "Employees in India receive 24 days of paid leave per year.",
        "expected_information": "Employees receive 24 days of paid leave per year."
    }
]

# RAG Pipeline Function
def run_rag(question, top_k=3):
    query_vector = embedding_model.encode(question).tolist()
    
    # Retrieve Context Chunks from Qdrant
    search_results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )
    
    retrieved_chunks = [point.payload["text"] for point in search_results.points]
    context_text = "\n".join(retrieved_chunks)
    
    # Generate Answer via LLM
    prompt = f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer strictly based on context:"
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )
    
    generated_answer = response.choices[0].message.content
    return retrieved_chunks, generated_answer, search_results.points

# Evaluation Metric: Precision Calculation (LLM-as-a-Judge)
def evaluate_precision(question, retrieved_chunks):
    relevant_count = 0
    for chunk in retrieved_chunks:
        eval_prompt = f"Question: {question}\nChunk: {chunk}\nIs this chunk relevant to answering the question? Reply with YES or NO."
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": eval_prompt}]
        )
        if "YES" in response.choices[0].message.content.upper():
            relevant_count += 1
            
    precision = relevant_count / len(retrieved_chunks) if retrieved_chunks else 0.0
    return precision

# Run Evaluation Loop
for test_case in golden_dataset:
    chunks, answer, points = run_rag(test_case["question"], top_k=3)
    precision_score = evaluate_precision(test_case["question"], chunks)
    
    print(f"Question: {test_case['question']}")
    print(f"Retrieved Chunks Count: {len(chunks)}")
    print(f"Context Precision: {precision_score * 100:.2f}%")
    print(f"Generated Answer: {answer}\n")

```

Lecturer's explanation:

* **Precision Diagnostic Output:** If `top_k=3` retrieves 1 relevant line (`24 days leave`) with similarity `0.49`, and 2 irrelevant lines (`promotion cycle`, `hybrid work model`) with lower similarity, Precision drops to $33.3\%$. The script flags `Retrieval is returning irrelevant chunks`, directing the developer to raise the score threshold to $0.40$ or reduce `top_k`.

---

════════════════════════════════════════════════

⚡ QUICK REVISION SUMMARY
════════════════════════════════════════════════

1. Interviewers focus heavily on RAG evaluation and root-cause analysis rather than basic code syntax.
2. RAG Evaluation answers whether a RAG system works correctly and identifies which specific component fails when errors occur.
3. RAG evaluation is analogous to LeetCode test cases that evaluate code correctness automatically.
4. RAG failures stem from 3 distinct points: Knowledge Base errors, Context Retrieval errors, or LLM Generation errors.
5. Buying a more expensive LLM will not fix pipeline errors caused by bad source data or poor context retrieval.
6. A Golden Dataset consists of Questions, Ground Truth answers, and Expected Information compiled by experts.
7. Context Precision measures the percentage of retrieved context chunks that are actually relevant to the question.
8. Fixing low Context Precision requires reducing `top_k` or increasing the similarity score threshold.
9. Context Recall measures whether all available relevant facts in the knowledge base were successfully retrieved.
10. Fixing low Context Recall requires increasing `top_k` or lowering the similarity score threshold.
11. Faithfulness measures whether the LLM's answer is grounded strictly in the retrieved context without hallucinating.
12. Low Faithfulness is fixed by updating the system prompt with negative constraints ("Do not hallucinate").
13. Answer Correctness measures whether the final output matches the Golden Dataset Ground Truth.
14. Answer Relevancy measures whether the LLM directly answers the query without outputting off-topic fluff or definitions.
15. RAG Evaluation uses an evaluator LLM (LLM-as-a-Judge) to score pipeline metrics automatically.

════════════════════════════════════════════════

❓ QUESTIONS RAISED BY LECTURER (if any)
════════════════════════════════════════════════

Q: If a RAG system gives a wrong answer, is it always the LLM's fault?
A: No. The error can originate from bad source knowledge, incorrect vector context retrieval, or LLM hallucination.

Q: Can an LLM response be 100% Faithful but still Incorrect?
A: Yes. If the retrieved context contains false information (e.g., "10 days leave"), a faithful LLM will output "10 days leave". The response is 100% faithful to the context, but incorrect relative to real-world Ground Truth (12 days).

Q: Can an LLM response be Unfaithful but Correct?
A: Yes. If context falsely states "Newton has 4 laws", but the LLM ignores context and outputs "Newton has 3 laws", the answer is correct in the real world, but unfaithful to the provided context.

════════════════════════════════════════════════

⚠️ IMPORTANT POINTS LECTURER EMPHASISED
════════════════════════════════════════════════

* **Do Not Just Buy Better LLMs:** Blindly upgrading to a higher-tier LLM model will not solve RAG failure if context retrieval or source data is faulty.
* **Understand Precision vs Recall Actions:** Precision and recall require inverse tuning parameters (Precision needs lower `top_k` / higher threshold; Recall needs higher `top_k` / lower threshold).
* **Master Faithfulness vs Correctness Distinction:** Expect interviewers to ask deeply about the exact difference between Faithfulness and Correctness.
* **No System Achieves 100% Across All Metrics:** Real-world production RAG aims for a stable, satisfactory state with acceptable margins of error rather than theoretical perfection.

════════════════════════════════════════════════

🔗 CONNECTIONS LECTURER MADE
════════════════════════════════════════════════

* Connected RAG evaluation test suites to LeetCode automated DSA test cases.
* Connected RAG failure layers to a student failing an exam due to student intelligence vs teacher notes vs textbook syllabus.
* Connected LLM Faithfulness vs Correctness to a student answering exam questions according to a teacher's flawed notes vs real-world textbook facts (Newton's laws of motion).
* Connected low Precision to retrieving noise in a search engine when requesting top 10 results for a topic with only 2 relevant pages.

═══════════════════════════════════════

DEFINITIONS (from video only)
═══════════════════════════════════════

* **RAG Evaluation:** The process of measuring the accuracy, retrieval quality, and generation correctness of a RAG pipeline.
* **Golden Dataset:** A benchmark dataset containing questions, ground-truth answers, and expected information used to test RAG pipelines.
* **Ground Truth:** The absolute, factually correct answer for a query based on source knowledge files.
* **Context Precision:** The proportion of retrieved context chunks that are relevant to the input query.
* **Context Recall:** The proportion of total available relevant facts in the knowledge base that were successfully retrieved.
* **Faithfulness:** The degree to which an LLM's generated answer is grounded exclusively in the provided context without hallucinating outside facts.
* **Answer Correctness:** The degree to which a generated answer matches the Ground Truth.
* **Answer Relevancy:** The degree to which a generated answer directly addresses the user's specific prompt without adding irrelevant information.

═══════════════════════════════════════

EXAMPLES USED IN VIDEO
═══════════════════════════════════════

* **Student Exam Failure Analogy:** Student failing because of student error (LLM), teacher's bad notes (Context Retrieval), or wrong textbook syllabus (Knowledge Base).
* **Newton's Laws Analogy:** Context states Newton has 4 laws. Writing 4 laws is Faithful but Incorrect; writing 3 laws is Unfaithful to context but Correct in reality.
* **Akamai HR Policy Retrieval:** Querying leave policy returning 12 days paid leave (relevant), 3 days sick leave (relevant), and ₹50,000 salary (irrelevant), resulting in 66% Precision.
* **Promotion Relevancy Example:** Asking "When does promotion happen?" and receiving a dictionary definition of promotion instead of "November".

═══════════════════════════════════════

CODE WRITTEN IN VIDEO (if any)
═══════════════════════════════════════

* **Python RAG Evaluation Script:**
* Demonstrates `QdrantClient` vector retrieval, Groq LLM answer generation (`openai/gpt-oss-120b`), and LLM-as-a-judge evaluation of `Context Precision`, `Context Recall`, `Faithfulness`, `Relevancy`, and `Correctness` against a `golden_dataset`.
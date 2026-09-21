═══════════════════════════════════════
TOPIC: Chunking Strategies for RAG | Free AI Engineer Course | 8 Weeks
LECTURER: Pratyush
SOURCE: [https://youtu.be/bm_0jH5ve8U](https://youtu.be/bm_0jH5ve8U?utm_source=gemini)
═══════════════════════════════════════

## 1. Introduction to Chunking in RAG

### 1.1 What is Chunking?

* Recapping the standard RAG pipeline: A knowledge base document is converted into vector embeddings (arrays). When a query comes in, it is also converted into a query embedding array. Cosine similarity retrieves the top 3 matching embedding arrays, which are sent as context to the LLM to generate an answer.
* Previously, a simple 6-line knowledge base was used where each line had an isolated meaning and was converted directly into an array.
* Real-world knowledge bases are not simple 6-line files; they can be 300-page novels (100,000 words, 20,000 lines, 700 paragraphs) or massive code files.
* You cannot create a single 384-dimensional vector embedding for an entire 300-page book and expect accurate retrieval.
* "Chunk" means a piece, fragment, or section (e.g., a "chunk of land").
* **Chunking in RAG:** The process of breaking down a large knowledge base into smaller pieces or fragments so that an individual vector embedding array can be generated for each fragment.

### 1.2 Chunking as a DSA (Data Structures and Algorithms) Problem

* Chunking cannot be memorized or applied via a single universal rule.
* Chunking is like Data Structures and Algorithms (DSA) — deciding whether to use an Array or a Linked List depends on the problem, experience, and developer intuition gained from solving many real-world problems.

Example from video:
A 300-page novel with 100,000 words, 20,000 lines, and 700 paragraphs, or a large source code repository, passed as a PDF knowledge base.

Code (if any):
N/A

---

Lecturer's explanation:

* **Intuition over Memorization:** Emphasized that selecting a chunking strategy requires assessing the nature of the data rather than memorizing fixed rules.
* **Why Simple Single-Line Embeddings Fail:** Real-world documents contain unstructured, continuous narrative or code that must be segmented logically before embedding.

---

## 2. Chunking Strategy 1: Fixed-Size Chunking

### 2.1 Concept and Mechanics

* Splitting text after a strict, fixed character or word limit (e.g., creating a new chunk every 50 words and converting each 50-word block into an embedding array).

### 2.2 Flaws and Limitations

* **Arbitrary Constraint:** Rigidly enforcing a fixed size (like 50 words) is overly strict and artificial.
* **Destruction of Sentence Meaning:** If a critical sentence spans across the fixed limit boundary, it gets severed mid-sentence.
* **"Too Small" vs. "Too Big" Dilemma:**
* *Too Small (e.g., 10 words):* The chunk lacks sufficient semantic context to carry meaning.
* *Too Big (e.g., 5,000 words):* Contains 10 different concepts or plot twists mixed together. Embedding 5,000 words into a small vector (e.g., size 384) loses fine-grained details and fails during search.



Example from video:

* **Carnival Ride Analogy:** Fixed-size chunking is like a carnival ride with a strict 4-foot height limit. When a 6-foot person shows up, instead of allowing them on, fixed-size chunking metaphorically cuts the person in half at 4 feet, sending the top 4 feet into Ride #1 and the remaining 2 feet into Ride #2.
* **Mystery Novel Plot Twist Example:**
* Sentence: `"The man who did the crime was John"`
* Fixed-size chunking cuts at 50 words right after `"was"`.
* Chunk 1: `"The man who did the crime was"`
* Chunk 2: `"John"`
* When a user asks `"Who did the crime?"`, Chunk 1 matches best via cosine similarity and goes to the LLM. But Chunk 1 lacks `"John"`, so the LLM cannot answer. Chunk 2 (`"John"`) has no semantic similarity to `"Who did the crime?"`, so it is never retrieved. The LLM fails on the most important question because the key information was severed.



Code (if any):
N/A

---

Lecturer's explanation:

* **Meaning Loss:** Showed how cutting text strictly by character/word count severs entity names from their descriptive actions.
* **Vector Embedding Limitations:** Highlighted that attempting to cram 5,000 words into a single embedding vector causes information overload and degraded retrieval accuracy.

---

## 3. Chunking Strategy 2: Separator-Based / Paragraph-Based Chunking

### 3.1 Concept and Mechanics

* Splitting text using natural structural boundaries like paragraphs (e.g., double newline `\n\n`) to preserve paragraph context and prevent mid-sentence cuts.

### 3.2 Flaws and Limitations

* **Unpredictable Paragraph Lengths:** Paragraph lengths vary wildly depending on the author's writing style.
* Reintroduces the "Too Small" and "Too Big" chunk problem when paragraph lengths are inconsistent.

Example from video:

* **Shakespeare Analogy:** Shakespeare writes Paragraph 1 with 20 lines, but writes Paragraph 2 with 2,000 lines.
* Result: Chunk 1 has 20 lines (too small, only mentions "the house has yellow paint"), while Chunk 2 has 2,000 lines (too big, contains half the book's information, making precise retrieval impossible).

Code (if any):
N/A

---

Lecturer's explanation:

* **Author Style Dependency:** Explained that paragraph-based chunking fails because authors do not format text to accommodate RAG vector databases.

---

## 4. Chunking Strategy 3: Recursive Chunking

### 4.1 Concept and Mechanics

* Uses a prioritized list of fallback separators (e.g., double newline `\n\n` for paragraphs, single newline `\n`, periods `.`, punctuation, spaces) combined with a target `chunk_size` constraint.
* **Process:** First attempts to split by the highest-priority separator (paragraph `\n\n`). If a paragraph fits within the target `chunk_size` (e.g., ~500 lines/characters), it forms a chunk. If a paragraph exceeds the limit (e.g., 2,000 lines), it recursively falls back to lower-priority separators (e.g., full stops `.`) to break the large block into acceptable sub-chunks.

### 4.2 Code Chunking

* Code cannot be split by plain character counts or text paragraphs.
* Fixed-size chunking breaks code mid-statement (e.g., splitting `c = a + b` across chunks).
* Recursive chunking for code uses programming-specific separators (e.g., `def`, colons `:`, `if`, `else`, curly braces `{}`) to split large code blocks along logical function/control-flow boundaries.

### 4.3 Overlap Feature

* Overlap carries over a specified number of characters or words from the end of the previous chunk into the beginning of the next chunk (`chunk_overlap`).
* Overlap preserves boundary context so split sentences maintain semantic continuity across consecutive chunks.

Example from video:

* **Code Chunking Example:**
```python
def sum(a, b):
    c = a + b
    if c % 2 == 0:
        return "Even"
    else:
        return "Odd"

```


* Fixed-size (every 2 lines) creates meaningless chunks like `c = a + b` in isolation.
* Recursive chunking uses separators like `def`, `:`, `if`, `else` to break code logically.


* **Overlap Example:**
* Original Text: `"The detective found something. Room were silent and the bloodstained letter that..."`
* Chunk 1 ends with: `"...silent and the"`
* Chunk 2 begins with: `"silent and the bloodstained letter that..."` (20-character overlap prevents loss of context at the split point).



Code (if any):
N/A

---

Lecturer's explanation:

* **Hierarchical Fallback:** Explained how recursive splitting tries large logical blocks first and progressively subdivides only when target size constraints are violated.
* **Role of Overlap:** Highlighted overlap as an essential mechanism to bridge context gaps across adjacent chunks.

---

## 5. Chunking Strategy 4: Semantic Chunking

### 5.1 Concept and Mechanics

* Splitting text based on changes in semantic meaning rather than word counts, static separators, or paragraph structures.
* Detects topic shifts in the text and creates new chunks whenever the underlying meaning or context changes.

Example from video:

* **Apple Corporate Report Document:**
`"We launched iPhone 18 today. It has 200 MP camera. Apple's revenue went up by 18%."`
* Semantic chunking reads meaning and creates 2 chunks:
* **Chunk 1:** `"We launched iPhone 18 today. It has 200 MP camera."` (Category: iPhone technical specifications).
* **Chunk 2:** `"Apple's revenue went up by 18%."` (Category: Apple financial report).





Code (if any):
N/A

---

Lecturer's explanation:

* **Meaning Shift Detection:** Emphasized that semantic chunking groups sentences by topic regardless of whether they appear in the same paragraph.

---

## 6. Code Implementation with LangChain Text Splitters

### 6.1 Setup and Classes

* Library: `langchain-text-splitters` (installed via `uv add langchain-text-splitters`).
* Key Classes:
* `CharacterTextSplitter`: Used for fixed-size and paragraph-based chunking.
* `RecursiveCharacterTextSplitter`: Used for recursive chunking with built-in default separators (`\n\n`, `\n`, space, empty string).



### 6.2 Code Execution

Code (if any):

```python
# Installation via uv
# uv add langchain-text-splitters

from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

sample_text = """The detective found something. Room were silent and the bloodstained letter that revealed everything."""

# 1. Fixed-Size Chunking (cuts strictly at character limit)
fixed_splitter = CharacterTextSplitter(
    separator="",
    chunk_size=100,
    chunk_overlap=0
)
fixed_chunks = fixed_splitter.split_text(sample_text)

# 2. Paragraph-Based Chunking (uses double newline separator)
paragraph_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=0
)
paragraph_chunks = paragraph_splitter.split_text(sample_text)

# 3. Recursive Chunking (with overlap)
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)
recursive_chunks = recursive_splitter.split_text(sample_text)




```

Lecturer's explanation:

* **Fixed-Size Output Defect:** Pointed out that `CharacterTextSplitter` with `separator=""` sever words mid-string (e.g., splitting `"Windows"` into `"Windo"` and `"ws"`).
* **Modern Paragraph Splitter Behavior:** Noted that modern paragraph splitters also accept `chunk_size` limits to cut overly large paragraphs (e.g., >100 characters) to prevent the "Too Big" chunk problem.
* **Recursive Overlap Verification:** Demonstrated how `chunk_overlap=20` duplicates 20 characters across chunk boundaries (e.g., `"silent and the"` appearing at both the end of Chunk 1 and start of Chunk 2).

---

════════════════════════════════════════════════
⚡ QUICK REVISION SUMMARY
════════════════════════════════════════════════

1. Chunking is the process of breaking down large knowledge bases into smaller text fragments to generate individual vector embeddings.
2. Selecting a chunking strategy is like choosing a Data Structure in DSA; it relies on intuition and problem context rather than memorization.
3. Fixed-size chunking splits text strictly at character/word limits without regard for sentence boundaries.
4. Fixed-size chunking destroys sentence meaning by splitting critical context across chunk boundaries.
5. "Too Small" chunks lack context, while "Too Big" chunks cram multiple concepts into one vector, degrading retrieval precision.
6. Paragraph-based chunking splits text at paragraph breaks (`\n\n`) to preserve local context.
7. Paragraph-based chunking fails when paragraph lengths are unpredictable (e.g., Shakespeare writing a 20-line paragraph followed by a 2,000-line paragraph).
8. Recursive chunking uses a prioritized list of fallback separators (`\n\n`, `\n`, `.`, spaces) alongside a target chunk size constraint.
9. Recursive chunking for code uses language syntax elements (`def`, `:`, `if`, `else`, `{}`) as logical separators.
10. Chunk overlap copies trailing characters/words from a previous chunk into the next chunk to preserve boundary context.
11. Semantic chunking splits text based on shifts in topic meaning rather than word counts or structural punctuation.
12. There is no single "best" chunking strategy; the optimal choice depends strictly on the specific use case and data format.
13. Chunking quality directly determines RAG accuracy and retrieval performance (evaluated via RAG Evaluation / RAG Eval).
14. LangChain provides `CharacterTextSplitter` and `RecursiveCharacterTextSplitter` to implement various chunking strategies in Python.

════════════════════════════════════════════════
❓ QUESTIONS RAISED BY LECTURER (if any)
════════════════════════════════════════════════

Q: What is the single best chunking strategy for RAG?
A: There is no single best chunking strategy. It depends entirely on the specific use case and data format you are handling (just as there is no single "best data structure" in computer science).

Q: Why does fixed-size chunking fail on important queries?
A: Because it severs text strictly at word/character boundaries, separating entity names from their actions across different chunks so the LLM never receives the complete answer context.

Q: Why does standard paragraph chunking fail on long documents?
A: Because paragraph sizes are author-dependent and unpredictable; a document may contain 20-line paragraphs alongside 2,000-line paragraphs, causing the "Too Big" vs. "Too Small" chunk problem.

════════════════════════════════════════════════
⚠️ IMPORTANT POINTS LECTURER EMPHASISED
════════════════════════════════════════════════

* **Chunking is like DSA:** Never memorize chunking rules; select strategies based on data structure and application requirements.
* **Never Claim Recursive is Always Best:** Stating "Recursive chunking is always best" is incorrect; different use cases suit fixed, paragraph, recursive, or semantic approaches.
* **Chunking Determines RAG Accuracy (RAG Eval):** Poor chunking severely degrades RAG pipeline accuracy regardless of vector database or LLM performance.
* **Overlap Prevents Boundary Loss:** Setting `chunk_overlap` carries over context across split boundaries to prevent loss of meaning.

════════════════════════════════════════════════
🔗 CONNECTIONS LECTURER MADE
════════════════════════════════════════════════

* Connected selecting a chunking strategy to choosing a Data Structure in DSA (e.g., Array vs. Linked List).
* Connected rigid fixed-size chunking to a 4-foot height limit on a carnival ride where a 6-foot person is metaphorically cut in half.
* Connected paragraph size inconsistency to Shakespeare writing a 20-line paragraph followed by a 2,000-line paragraph.
* Connected code chunking separators to Python programming syntax elements (`def`, `:`, `if`, `else`, `{}`).

═══════════════════════════════════════
DEFINITIONS (from video only)
═══════════════════════════════════════

* **Chunk:** A piece, fragment, or segmented portion of a knowledge base document.
* **Chunking:** The process of dividing a large knowledge base document into smaller fragments to compute individual vector embeddings.
* **Fixed-Size Chunking:** Splitting text strictly at a fixed character or word count.
* **Paragraph-Based Chunking:** Splitting text using paragraph structural boundaries (such as double newlines `\n\n`).
* **Recursive Chunking:** Splitting text hierarchically using a prioritized list of separators while respecting target chunk size and overlap constraints.
* **Chunk Overlap:** Including a trailing portion of text from the previous chunk at the beginning of the next chunk to maintain boundary context.
* **Semantic Chunking:** Splitting text at points where the underlying topic or semantic meaning changes.
* **RAG Eval (RAG Evaluation):** The metric/process used to measure the accuracy and performance of a RAG pipeline.

═══════════════════════════════════════
EXAMPLES USED IN VIDEO
═══════════════════════════════════════

* **Carnival Ride Analogy:** Fixed-size chunking enforcing a 4-foot height limit on a 6-foot person by metaphorically cutting them in half.
* **Mystery Novel Plot Twist:** `"The man who did the crime was John"` cut after `"was"`, causing retrieval of `"The man who did the crime was"` while leaving `"John"` unretrieved.
* **Shakespeare Paragraphs:** A 20-line paragraph ("too small") next to a 2,000-line paragraph ("too big").
* **Code Function Split:** Python `sum(a, b)` function split mid-expression (`c = a + b`) vs. logical splitting using `def`, `:`, `if`, `else`.
* **Apple Report Semantic Split:** Technical specs (`iPhone 18`, `200 MP camera`) split from financial data (`Apple's revenue went up by 18%`).

═══════════════════════════════════════
CODE WRITTEN IN VIDEO (if any)
═══════════════════════════════════════

* **Python LangChain Text Splitter Script:**
* Demonstrates `CharacterTextSplitter` with `separator=""` for fixed-size chunking (showing mid-word cuts like `"Windo"` / `"ws"`).
* Demonstrates `CharacterTextSplitter` with `separator="\n\n"` for paragraph-based chunking.
* Demonstrates `RecursiveCharacterTextSplitter` with `chunk_size=100` and `chunk_overlap=20` (showing 20-character overlapping strings across adjacent chunks).
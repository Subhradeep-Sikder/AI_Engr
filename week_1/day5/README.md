Here are the comprehensive revision notes based strictly on the lecture provided. These are formatted in Markdown, ready to be copied and pasted into your GitHub repository.

---

# 📝 AI Mini Project: LLM-Based Resume Evaluator

## 🎯 Project Objective

Build an AI agent that takes a Job Description (JD) in plain text and a folder containing resumes (PDF/DOCX formats). The tool extracts structured data from both, compares them using an LLM, and assigns a **compatibility score (0-100%)** along with a **detailed verdict** to help HR quickly filter the top candidates.

---

## 🏗️ Architecture & Step-by-Step Implementation

### Part 1: Parsing the Job Description (JD)

Never work directly with raw text. We need to convert the unstructured JD into a structured JSON object using an LLM and Pydantic schemas.

**1. Define JD Schema (`JobD`)**
Create a schema to define what information we need from the JD:

* `role` (e.g., SDE 1)
* `required_skills` (Mandatory for the job)
* `preferred_skills` (Good-to-have skills)
* `minimum_experience`
* `educational_requirements`
* `responsibilities`

**2. Prompting the LLM**

* **System Prompt:** "You are an Expert HR Assistant. Analyze the JD and extract structured info. Return valid JSON matching the provided schema. Do not return the schema itself. If data is missing (like experience), set it to null. Do not invent information."
* **User Prompt:** "Analyze the following job description: `<JD_TEXT>`."
* **Action:** Convert the LLM's raw JSON response into a Python object using `json.loads()` and load it into your `JobD` schema.

### Part 2: Defining the Resume Schema

Resumes are tricky because they don't follow strict rules. Some have experience, some don't. You need a generalized structure where fields are **optional**.

**1. Define Experience Schema**

* `company_name`
* `role`
* `duration`
* `description`
* `skills_used`

**2. Define Resume Schema**

* `name`
* `email`
* `phone_number`
* `total_experience_years` (LLM calculates this automatically)
* `skills` (List of strings)
* `experiences` (List of `Experience` class)
* `projects` (List of strings)
* `certifications` (List of strings)
* *Note:* Use `None = None` to mark fields as optional so the parser doesn't break if a candidate forgot to include their email or projects.

### Part 3: Reading Resume Files (PDF & DOCX)

Create utility functions to convert physical files into raw text strings.

* **`read_pdf(file_path)`:** Loops through every page of the PDF and extracts text to a single string.
* **`read_docx(file_path)`:** Extracts text from paragraphs. **Crucial detail:** Iterate through document tables (`doc.tables -> row -> cells -> cell.text`). Students often put their education data in tables; ignoring tables means losing vital information!
* **`read_resume(file_path)`:** The router function. Checks `file_path.suffix.lower()`. If it's `.pdf`, it calls `read_pdf`. If it's `.docx`, it calls `read_docx`. If neither, it returns `None` (ignores the file).

### Part 4: Parsing Candidate Resumes

We loop through a directory of candidate resumes and parse them one by one.

**Steps inside the loop:**

1. Grab the `file_path`. Skip images or unreadable files.
2. Call `read_resume(file_path)` to get `resume_text`.
3. Pass the text to a `parse_resume(resume_text)` function.
4. **System Prompt for Resume Parsing:** "You are an Expert Resume Parser. Extract information into the given schema. Understand that 'Work History' or 'Employment' means Experience. Do not invent info. Return empty lists if nothing is found."
5. The result is a clean JSON object for every candidate.

### Part 5: Scoring and Matching

Now we compare the structured JD against the structured Resumes.

**1. Define Match Result Schema**

* `score` (Float, 0 to 100)
* `details` (Dictionary including: Candidate Name, Matching Skills, Missing Skills, Overall Percentage, and a Short Final Verdict explaining *why* they got that score).

**2. LLM Matcher Function (`final_score`)**

* Pass the JSON of the JD and the JSON of the Resume to the LLM.
* **System Prompt:** "You are an HR Recruiter. Compare the candidate's resume with the JD. Assign a score out of 100 and write a short final verdict explaining your reasoning. Keep it short and sweet."
* Save the results to an array `all_results`.

**3. Sorting and Output**

* Sort the array in descending order based on the `score` (`reverse=True`).
* Print out the Top 2 candidates (to call for interviews) and the Bottom 2 candidates.

---

## 💡 Best Practices & System Design Principles Discussed

1. **Avoid Text-to-Text Comparison:** Never compare raw JD text to raw Resume text. Always convert both into structured JSON objects (schemas) before comparing. This improves accuracy and structure.
2. **Handling Rate Limits (`time.sleep`):** When putting the extraction inside a `for` loop, you must introduce a `time.sleep(5)` after LLM calls. Firing off too many requests at once acts like a DoS (Denial of Service) attack on the LLM server. The API will block you (Rate Limiting). Give it a 5-second buffer between candidates.
3. **Prevent Hallucinations:** Always strictly command the LLM in the system prompt: `"Do not invent information"`.
4. **Handling Ambiguity:** Explicitly tell the LLM that candidates might use varying headings. Remind it that "Professional Experience" and "Internship" should be mapped to the `Experience` array.

---

*(Note: These notes accurately map to the structure, logic, and philosophy taught in Episode 06 of the 8 Weeks Free AI Engineer Course).*
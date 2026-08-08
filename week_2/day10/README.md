

---

# Mini Project Challenge: Personal AI Portfolio Chatbot

## 1. Project Overview & Objective

* **The Goal:** Instead of sending a standard PDF resume or a static portfolio website to HR recruiters or managers, you will build and share a custom AI Chatbot that acts as your personal representative.
* **How it Works:** When a recruiter clicks your link, a ChatGPT-style interface opens. This AI knows your entire professional background, projects, skills, and CGPA. The recruiter can converse with the AI to ask questions about your background or upload a Job Description (JD) to see how well you match the role.
* **Why Do This?** It is a highly unique way to stand out. Even if your past projects aren't groundbreaking, the effort and technical skill required to build a personal AI agent will instantly impress recruiters.

## 2. Step-by-Step Requirements

### Step 1: Create the Candidate Profile (The Knowledge Base)

* You must provide the AI with deep knowledge about yourself.
* This can be done by parsing your existing resume (using the resume parsing techniques learned previously), and by providing additional detailed text/PDF/Word files containing your skills, achievements, college journey, and professional experience.
* *Implementation:* You can save this data as a JSON file or inject it directly into the AI's memory.

### Step 2: Choose the LLM

* Use the free tier of the **Groq API** (which has been used throughout the course).
* Because your portfolio will not have thousands of daily users (likely just a few recruiters per week), the free tier is perfectly sufficient.

### Step 3: Write a Strict System Prompt

* Write a highly detailed System Prompt defining the AI's role, constraints, and output format.
* **Crucial Rule:** Instruct the AI to be **100% honest**. It must *never* invent or hallucinate skills. If a recruiter asks if you know IoT and you don't, the AI must truthfully say no.

### Step 4: Build the Backend (Python / FastAPI)

* Convert your standard Python script (e.g., `hello_llm.py`) into a proper backend server using **FastAPI**.
* This backend will handle the logic of receiving questions, passing them to Groq, and streaming the response back.
* *Note:* The instructor allows using ChatGPT/Claude to help write the FastAPI boilerplate code, as it's a standard web development task, not a core AI concept.

### Step 5: Build the Frontend

* Create a simple UI using **JavaScript/HTML/CSS**.
* The UI must mimic ChatGPT: it needs a chat window, an input text box, a "Send" button, and auto-scrolling.

### Step 6: Connect Frontend & Backend (Streaming)

* Use the Fetch API (or similar methods) in JavaScript to connect your frontend to your FastAPI backend.
* Implement **Streaming** (taught in the previous lecture) so the text appears chunk-by-chunk on the screen rather than forcing the user to wait for the entire response.

### Step 7: Implement Conversational Memory

* The chatbot must remember the context of the conversation.
* If a recruiter asks, *"Explain his 3 projects,"* and follows up with *"Which of these was the most complex?"*, the AI needs to remember the projects it just listed.
* *Implementation:* You must continuously append both the "User" prompts and "Assistant" responses to the `messages` array payload sent to the API.

### Step 8: JD Matching Feature

* Allow the recruiter to upload a PDF or Word file containing a Job Description.
* The backend should parse this file and compare it against your stored profile, returning a match percentage (e.g., "80% Match") and explaining which skills match and which are missing (reusing the logic from the earlier Resume Parser project).

### Step 9: Deployment

* **Backend Deployment:** Deploy your FastAPI backend for free using **Render** or **Railway**.
* **Frontend Deployment:** Deploy your frontend interface for free using **Vercel** (`vercel.app`).
* Ensure all code is pushed to a GitHub repository.

## 3. Instructor's Expectations

* You are expected to build at least 70% of this (the Python logic, resume parsing, memory, and prompts) using the knowledge from Weeks 1 and 2.
* If you struggle with the web development aspects (FastAPI, Vercel, connecting frontend to backend), that is okay. Try your best using ChatGPT, and the instructor will provide a full walkthrough in the next video.
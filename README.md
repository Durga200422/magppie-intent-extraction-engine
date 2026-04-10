# ✨ Magppie Intelligent Kitchen Design Assistant
**ML/LLM Engineer Technical Assessment | April 2026** 
> **🚀 Live Demo:** [Access the Intelligent Intent Extraction Engine here](https://magppie-intent-extraction-engine-txcv88z6hojhiuekpqesmh.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-orange?style=for-the-badge)
![LangSmith](https://img.shields.io/badge/Observability-LangSmith-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)

## 📖 Executive Summary
This system is a production-ready **Intent Extraction Pipeline** that converts unstructured customer dialogue—captured via text or voice—into structured JSON data for Magppie's design engine.

Beyond simple extraction, this implementation solves for real-world showroom complexities: **Hinglish code-switching**, **budget-unit normalization** (Lakh/Cr), and **security-first prompt engineering**. It is built with a "Builder Mindset"—a system that doesn't just fail when confused, but utilizes a **Human-in-the-Loop (HITL)** refinement loop to capture ground-truth data and improve over time.

---

## 🧬 System Architecture & Data Flow
The pipeline is architected to prioritize **Reliability** and **Data Integrity**:

1.  **Security Layer (Regex Firewall):** Regex-based pre-filtering to block prompt injection (e.g., "ignore all instructions") before hitting API endpoints.
2.  **Intent Engine (Dual-Provider):**
    * **Primary:** Gemini 2.5 Flash (Optimized for JSON schema adherence).
    * **Fallback:** Llama-3.3-70B via Groq LPU (Ensures high availability during outages).
3.  **Semantic Guardrails:** Detects out-of-scope requests or logical contradictions (e.g., requesting an "Island counter" for a "tiny 20 sq. ft." space).
4.  **Hinglish/Range Normalization:** A post-extraction processor that standardizes Indian currency (Lakh/Cr) and resolves budget ranges (e.g., "5-6 Lakh" → `600000`).
5.  **Validation:** Strict data contract enforcement via **Pydantic**.
6.  **Observability:** Integrated with **LangSmith** for full-trace logging and interaction history for a data-improvement flywheel.

---

## 🚀 Key "Elite" Features

### 1. Dual-Engine Resilience
To ensure 99.9% uptime in a high-stakes showroom environment, the system includes automatic fallback logic. If the primary Gemini engine hits rate limits or latency spikes, the system auto-routes to the Groq/Llama-3.3 endpoint.

### 2. V2 Strict Business Logic
Built-in support for **"Luxury Consultation"** flags (for budgets >50L) and **"Micro-budget"** alerts (for budgets <1L) to assist showroom floor management.

### 3. Pre-LLM Security Layer
Rather than relying solely on LLM guardrails, we implement a hardened regex firewall that detects common jailbreak patterns before they reach the model, saving tokens and protecting system integrity.

### 4. HITL Refinement Flywheel
When extraction confidence falls below 85%, the UI triggers a **"Refinement"** module. This allows the consultant to clarify details (e.g., "Make it L-shape instead"), which are then merged with the original input. This creates a loop where user corrections serve as high-fidelity labels for future model fine-tuning.

### 5. Hinglish & Budget Intelligence
Customers naturally code-switch. Our pipeline maps Hinglish semantics (e.g., *"Bana do kuch achha"* → `style: "elegant"`) and converts complex Indian budget strings (Lakhs/Cr/Ranges) into standardized integers.

---

## 📂 Project Directory Structure
```plaintext
MAGPPIE_INTENT_ENGINE/
├── src/
│   ├── extractor.py    # Dual-provider routing & LLM logic
│   ├── prompts.py      # Versioned System Instructions (V1 & V2_Strict)
│   ├── schema.py       # Pydantic data models for JSON enforcement
│   ├── utils.py        # Security firewall & currency normalization
│   └── __init__.py     # Package initialization
├── app.py              # Streamlit Premium UI & HITL Refinement Logic
├── main.py             # CLI Assessment script for Test Case validation
├── requirements.txt    # Production dependencies
└── README.md           # Engineering Brief
```
---
## 🛠️ Setup & Execution

### Prerequisites
- Python 3.11+
- API Keys for Google Gemini, Groq, and LangSmith.
### Installation
1. Clone the repository:
```Bash

git clone https://github.com/Durga200422/magppie-intent-extraction-engine.git
cd magppie-intent-engine

```
2. Setup Virtual Environment:

```Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

3. Install Dependencies:

```Bash

pip install -r requirements.txt

```
4. Configure Environment Variables:
Create a .env file in the root directory:

```Code snippet

GOOGLE_API_KEY = your_gemini_key
GROQ_API_KEY = your_groq_key
# LangSmith (Optional but recommended)
LANGCHAIN_TRACING_V2 = true
LANGCHAIN_API_KEY = your_langsmith_key

```

### Running the Project
- **To run the UI:** streamlit run app.py

- **To run the CLI Assessment (4 Test Cases):** python main.py

---

## 🎯 Edge Case Handling

- **Case 3 (Ranges):** Input *"around 5 to 6 lakh"* is processed to extract the maximum (**600,000**) to ensure design feasibility.
- **Case 4 (Hinglish):** Input *"Bana do kuch achha"* is semantically mapped to a high-quality style tier rather than failing as a translation error.
- **Logical Contradictions:** If a user provides physically impossible requirements, the **confidence score** is penalized, and a specific note is added to the ambiguities section of the output.

---

## 🧠 Task 02: System Thinking

### 1. Data Collection & Improvement
We collect raw input, provider metadata, and extraction confidence. To create a **data flywheel**, we link these to **Showroom Outcomes** (design approval) and **User Refinement clicks**. 

- **Gold Mines:** Low-confidence extractions that lead to approvals are prioritized for prompt iteration. 
- **Hallucination Patterns:** High-confidence extractions that require human correction are flagged. 
- **Tooling:** We use **LangSmith** to cluster these failures and automatically generate new test cases.

### 2. Detecting Degradation
We monitor for **Confidence Distribution Shifts** (average confidence dropping week-over-week) and **Ambiguity Rate Spikes**. Additionally, we track **Semantic Drift**; if similar customer intents start producing structurally different JSON outputs, it signals a model update or prompt regression that requires an immediate rollback.

---

## 📝 Assumptions

- **Context Year:** The system is built under the assumption of **2026** availability for **Gemini 2.5 Flash**.
- **Voice Simulation:** For evaluation stability, the "Voice" input uses a functional simulation to demonstrate the UI/UX path from audio transcription to structured intent.
- **Currency:** All budget values are standardized to **INR**.

---

## 👤 Candidate Information

- **Candidate:** Narapureddy Durga Prasad Reddy
- **University:** Manav Rachna University
- **Status:** Graduate (CSE-AIML)
- **Linkedin:** [linkedin.com/in/narapureddy-d](https://www.linkedin.com/in/narapureddy-d-2a5402252/)

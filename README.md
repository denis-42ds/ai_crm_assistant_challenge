# AI CRM Assistant Service

This project is a demo application for CRM assistants powered by large language models (LLMs). It automates routine tasks such as lead classification, key data extraction, note editing, and deal risk assessment.

The project provides two user interfaces: a web application and a Telegram bot.

## Tech Stack

- **Frontend:** Plain HTML/CSS/JavaScript
- **Backend:** FastAPI
- **Telegram Bot:** Python Telegram Bot
- **Orchestration:** Docker Compose
- **Web Server:** Nginx

---

### 1. Problem

Sales managers spend a significant amount of time on routine tasks such as **classifying incoming leads**, **manually filling out client cards**, **maintaining detailed notes**, and **monitoring risks**. This leads to delays in handling the most promising clients and reduces the overall effectiveness of working with the customer base.

---

### 2. Solution

Our AI assistant automates these processes, allowing managers to focus on direct sales.

#### **Assistant 1: Lead Prioritization**
Analyzes the text of an incoming request and instantly assigns it a tag of **"Hot"**, **"Warm"**, or **"Cold"**, enabling immediate prioritization.

#### **Assistant 2: Automatic Client Card Fill-In**
Extracts key information from text (notes, emails) — such as name, company name, and email address — and returns it in a structured format for automatic field population.

#### **Assistant 3: Note Editing**
Corrects grammatical errors, improves structure, and highlights key points in a manager's notes, making the information in the CRM cleaner and more useful for the entire team.

#### **Assistant 4: Risk Radar**
Analyzes the text of correspondence or deal notes and identifies potential risks (e.g., "client is not responding", "requested a pause"), helping the manager react in a timely manner.

---

### 3. Metrics and Measurable Impact

The effectiveness of the solution is measured through:

- **Reduction in time spent on routine operations:** Automating classification, data entry, and note editing saves up to **90%** of the time a manager previously spent on these tasks.
- **Increased processing speed for "hot" leads:** Instant prioritization allows immediate outreach to the most promising clients, directly impacting **conversion growth** and shortening the deal cycle.

---

### 4. Project Structure

```
.
├── docker-compose.yml              # Docker Compose configuration for running all services
├── nginx.conf                      # Nginx configuration for routing
├── index.html                      # Frontend interface
├── .dockerignore                   # Files ignored during Docker image build
├── .env                            # Environment variables
├── .gitignore                      # Files ignored by Git
├── Dockerfile                      # Instructions for building the Docker image
├── README.md                       # This file
├── AI_Assistant_in_CRM.md          # AI assistant description
├── requirements.txt                # Python dependencies
└── /src                            # Application source code
    ├── app.py                      # Main FastAPI application file
    ├── telegram_bot.py             # Telegram bot code
    ├── /tests                      # Unit tests
    ├   ├── test_assistants.py      # Testing assistant logic
    ├   └── test_app.py             # Testing API endpoints
    └── /assistants                 # Assistant logic
        ├── __init__.py             # Package initialization
        ├── classifier.py           # Classifier assistant logic
        ├── extractor.py            # Extractor assistant logic
        ├── editor.py               # Editor assistant logic
        └── risk_assessor.py        # Stalled deal risk radar logic
```

---

### 5. Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/denis-42ds/ai_crm_assistant_challenge.git
    cd ai_crm_assistant_challenge
    ```

2. **Configure API keys:**
    Create a `.env` file in the project root directory and insert your API keys:
    ```text
    API_KEY=your_llm_api_key
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    ```
    *Note:* To obtain a `TELEGRAM_BOT_TOKEN`, use `@BotFather` in Telegram.

3. **Start Docker Compose (for the web application):**
    This command will build the images and start all web services (FastAPI, Nginx) in the background.
    ```bash
    docker-compose up --build -d
    ```

4. **Stop the services:**
    ```bash
    docker-compose down
    ```

---

### 6. API Usage

- **Web interface:** available at `http://localhost/`
- **API documentation (Swagger UI):** available at `http://localhost:8000/docs`
- **Telegram bot:** find your bot in Telegram and start interacting.

---

#### **Endpoint 1: `/classify`**

**Request example:**
```json
{ "text": "Good afternoon, we are interested in website development. We already have a specification and are ready to discuss the details and budget." }
```

**Response example:**
```json
{
  "classification": "Hot"
}
```

---

#### **Endpoint 2: `/extract-info`**

**Request example:**
```json
{ "text": "Good afternoon, my name is Ivan Petrov, I am from the company 'TechnoSphere'. Our email is info@technosfera.ru." }
```

**Response example:**
```json
{
  "name": "Ivan Petrov",
  "company": "TechnoSphere",
  "email": "info@technosfera.ru"
}
```

---

#### **Endpoint 3: `/edit-note`**

**Request example:**
```json
{ "text": "Clientcalled asked toprice said willcall tomorrow. think good lead" }
```

**Response example:**
```json
{
  "edited_note": "The client called today but I was unavailable. They asked for a price quote and said they would call back tomorrow.\n\nKey points:\n- Client called today.\n- Requesting a price quote.\n- Will call back tomorrow.\n\nAssessment: Good lead, requires an immediate response."
}
```

---

#### **Endpoint 4: `/risk-assessment`**

**Request example:**
```json
{ "text": "The client has been unreachable for a week. Last week they asked to 'take a pause' in communication. The deal seems stalled." }
```

**Response example:**
```json
{
  "is_at_risk": true,
  "reason": "The client has been unreachable for a week and asked to take a pause."
}
```

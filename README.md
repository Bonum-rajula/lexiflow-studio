# LexiFlow Studio

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-deployed-url.streamlit.app)

## Intelligent Interface for Multi-Agent RAG Systems

LexiFlow Studio is the official frontend client for LexiFlow AI, a production-ready multi-agent Retrieval-Augmented Generation (RAG) platform powered by LangGraph, OpenAI, and ChromaDB.

Built with Streamlit, LexiFlow Studio provides a clean, interactive, and transparent user experience for document ingestion, semantic search, and AI-powered question answering. Users can upload technical documents, ask natural language questions, and observe how specialized AI agents collaborate to generate accurate, context-aware responses.

Whether you're analyzing technical manuals, research papers, compliance documentation, or knowledge bases, LexiFlow Studio offers a streamlined interface for interacting with the LexiFlow AI ecosystem.

---

## Overview

LexiFlow Studio serves as the presentation layer of the LexiFlow platform.

It connects to the LexiFlow AI backend through REST APIs and provides:

* Document upload and ingestion workflows
* Natural language querying
* Multi-agent reasoning visibility
* Retrieval transparency
* Response evaluation insights
* Interactive user feedback

---

## Key Features

### Document Upload

Upload PDF documents directly through the interface for ingestion into the LexiFlow knowledge base.

### Natural Language Question Answering

Ask questions in plain language and receive context-aware answers generated through the LexiFlow multi-agent workflow.

### Multi-Agent Transparency

Gain visibility into how the system produces answers:

* Retrieved document chunks
* Critic agent evaluations
* Final synthesized responses
* Retry attempts and validation feedback

### Interactive User Experience

Modern interface components provide:

* Loading indicators
* Status notifications
* Progress feedback
* Error handling
* Session persistence

### Branded Experience

Custom LexiFlow design system featuring:

* Consistent visual identity
* Professional layouts
* Accessible interface patterns
* Responsive user interactions

### Backend Agnostic Configuration

Connect to:

* Local LexiFlow instances
* Docker deployments
* Cloud-hosted environments
* Development and staging systems

without modifying application code.

---

## Architecture

LexiFlow Studio follows a lightweight layered architecture.

```text
┌───────────────────────────────────────────────────────────────┐
│                    LexiFlow Studio                           │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  User Interface Layer                                         │
│  ├── Sidebar                                                   │
│  ├── Upload Components                                         │
│  ├── Chat Interface                                            │
│  └── Results Dashboard                                         │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Application Layer                                             │
│  ├── Session State                                             │
│  ├── Configuration                                              │
│  ├── Theme Management                                           │
│  └── Response Rendering                                         │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Service Layer                                                 │
│  ├── API Client                                                │
│  ├── Request Handling                                          │
│  ├── Retry Policies                                            │
│  └── Error Management                                          │
│                                                               │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                │ HTTP / REST
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                       LexiFlow AI                            │
├───────────────────────────────────────────────────────────────┤
│ FastAPI Gateway                                               │
│ LangGraph Orchestrator                                        │
│ Retriever Agent                                               │
│ Critic Agent                                                  │
│ Synthesizer Agent                                             │
│ ChromaDB Vector Store                                         │
│ OpenAI Models                                                 │
└───────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer                 | Technology                |
| --------------------- | ------------------------- |
| Frontend Framework    | Streamlit                 |
| HTTP Client           | Requests / HTTPX          |
| State Management      | Streamlit Session State   |
| Configuration         | Python Dotenv             |
| Backend Communication | REST API                  |
| Styling               | Custom CSS                |
| Deployment            | Streamlit Community Cloud |
| Backend Integration   | LexiFlow AI               |

---

## Getting Started

### Prerequisites

Before running the application, ensure you have:

* Python 3.11 or later
* Access to a running LexiFlow AI backend instance

The backend may be:

* Running locally
* Running inside Docker
* Hosted on a cloud platform

---

## Clone the Repository

```bash
git clone https://github.com/yourusername/lexiflow-studio.git
cd lexiflow-studio
```

---

## Create a Virtual Environment

Using Conda:

```bash
conda create -n lexiflow-studio python=3.11 -y
conda activate lexiflow-studio
```

Using venv:

```bash
python -m venv .venv
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Update the backend URL:

```env
API_BASE_URL=http://localhost:8000
```

Example cloud deployment:

```env
API_BASE_URL=https://api.lexiflow.ai
```

---

## Run the Application

```bash
streamlit run src/app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## Usage

### Step 1 — Upload a Document

1. Open the application.
2. Navigate to the upload section.
3. Select a PDF document.
4. Submit for ingestion.

The backend will:

* Parse the document
* Create chunks
* Generate embeddings
* Store vectors in ChromaDB

---

### Step 2 — Ask Questions

After ingestion:

1. Enter a question in the chat interface.
2. Submit the query.
3. Review the generated answer.

---

### Step 3 — Explore Agent Insights

LexiFlow Studio exposes internal workflow information, including:

* Retrieved context chunks
* Critic evaluations
* Confidence indicators
* Retry attempts
* Final synthesized response

This transparency helps users understand how answers are generated.

---

## Deployment

### Streamlit Community Cloud

Deploying LexiFlow Studio is straightforward.

#### 1. Push the Repository to GitHub

```bash
git push origin main
```

#### 2. Log In to Streamlit Cloud

Visit:

https://streamlit.io/cloud

#### 3. Create a New Application

Configure:

| Setting        | Value                  |
| -------------- | ---------------------- |
| Repository     | Your GitHub repository |
| Branch         | Main                   |
| Main File Path | src/app.py             |

#### 4. Configure Secrets

Add:

```toml
API_BASE_URL="https://your-backend-url.com"
```

#### 5. Deploy

Streamlit will automatically build and host the application.

---

## Environment Variables

| Variable     | Description                         | Example               |
| ------------ | ----------------------------------- | --------------------- |
| API_BASE_URL | Base URL of the LexiFlow AI backend | http://localhost:8000 |

---

## Project Structure

```text
lexiflow-studio/
├── .streamlit/
│   └── config.toml
│
├── docs/
│   └── demo.gif
│
├── src/
│   ├── app.py
│   │
│   ├── components/
│   │   ├── upload.py
│   │   ├── chat.py
│   │   └── results.py
│   │
│   ├── services/
│   │   └── api_client.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── session_state.py
│   │   └── styles.py
│   │
│   └── assets/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Future Enhancements

Planned roadmap items include:

* Conversation history
* Multi-document collections
* Authentication and user accounts
* Streaming responses
* Citation highlighting
* Agent execution timeline visualization
* Document management dashboard
* Dark mode support
* Mobile-responsive layouts

---

## Contributing

Contributions are welcome.

### Development Workflow

Create a feature branch:

```bash
git checkout -b feature/my-feature
```

Make your changes, add tests where appropriate, and submit a pull request.

Please ensure:

* Code follows project conventions
* Documentation is updated
* Changes are tested before submission

---

## License

This project is licensed under the MIT License.

See the LICENSE file for additional details.

---

## Acknowledgments

LexiFlow Studio is built on top of several excellent open-source technologies:

* Streamlit
* Python
* FastAPI
* LangGraph
* ChromaDB
* OpenAI

Special thanks to the open-source community for enabling modern AI application development.

---

## Related Projects

### LexiFlow AI

The backend multi-agent RAG platform powering LexiFlow Studio.

Repository:

https://github.com/yourusername/lexiflow-ai

---

## Author

**Bonum Rajula**

Email: [bonumrajula01@gmail.com](mailto:bonumrajula01@gmail.com)

GitHub: https://github.com/bonumrajul

---

LexiFlow Studio provides a transparent, user-friendly gateway into the power of autonomous multi-agent Retrieval-Augmented Generation systems.

# MLOps Deployment of a Task-Automation Agent

## Project Overview

This project implements a web application that accepts a research topic, searches for relevant information on the web, summarizes the results, and returns exactly three concise bullet points.

## Technology Stack

- **Python 3.x** - Core programming language
- **Streamlit** - Web interface
- **LangChain** - LLM integration framework
- **DuckDuckGo Search** - Web search integration
- **OpenAI API** - Summarization model (gpt-4o-mini)
- **Git & GitHub** - Version control
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Hugging Face Spaces / Render** - Deployment

## Project Structure

```
.
├── app.py              # Streamlit web interface
├── agent.py            # Core search-and-summarize agent
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker container definition
├── .dockerignore       # Files to exclude from Docker build
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
├── tests/
│   └── test_agent.py   # Unit tests
├── .github/
│   └── workflows/
│       └── ci.yml      # CI/CD pipeline
└── .env.example        # Environment variables template
```

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Ex_10
```

2. Create a virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example file
Copy-Item .env.example .env

# Edit .env and add your OpenAI API key
notepad .env
```

## Usage

### Running the Agent Directly

```bash
# Set your API key (if not using .env)
$env:OPENAI_API_KEY="your-api-key-here"

# Run the agent
python agent.py
```

### Running the Web Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

### Running Tests

```bash
pytest tests/ -v
```

### Running with Docker

```bash
# Build the image
docker build -t mlops-agent:latest .

# Run the container
docker run -p 8501:8501 -e OPENAI_API_KEY=$env:OPENAI_API_KEY mlops-agent:latest
```

## Agent API

### `search_web(topic: str, num_results: int = 5) -> List[Dict]`

Searches the web for a topic using DuckDuckGo.

**Args:**
- `topic`: The search query topic.
- `num_results`: Maximum number of results to retrieve (default: 5).

**Returns:**
List of dictionaries with keys: 'title', 'snippet', 'url', 'source'.

### `summarize_results(results: List[Dict], topic: str) -> List[str]`

Summarizes search results using OpenAI LLM.

**Args:**
- `results`: List of search result dictionaries.
- `topic`: The original search topic.

**Returns:**
List of exactly 3 bullet point strings.

### `run_agent(topic: str) -> Dict`

Orchestrates the search-and-summarize pipeline.

**Args:**
- `topic`: The research topic to investigate.

**Returns:**
Dictionary with keys: success, topic, bullets, sources, error.

## Error Handling

The agent handles the following error cases gracefully:

- Empty topics
- Search failures
- API errors (OpenAI rate limits, authentication)
- Missing API keys
- Network issues

All errors are logged without exposing sensitive data.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| OPENAI_API_KEY | Your OpenAI API key | Yes |

## Deployment

### Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Set the environment variable in Space settings
3. Push the code to the Space repository

### Render

1. Create a new Web Service on Render
2. Set the environment variable in the service settings
3. Connect to your GitHub repository
4. Deploy

## CI/CD

The project uses GitHub Actions for continuous integration. The workflow:

1. Runs on pull requests and pushes to main
2. Installs dependencies
3. Runs tests
4. Builds and pushes Docker image

## License

MIT License
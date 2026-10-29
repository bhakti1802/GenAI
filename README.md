# MLOps Task-Automation Agent

**Live Demo:** https://genai-gwki.onrender.com

**GitHub Repository:** https://github.com/bhakti1802/GenAI

An AI-powered research assistant that searches the web, summarizes information using a Groq LLM, and returns three concise bullet points with source links.

## Features
- Web search using DuckDuckGo
- AI-powered summarization using Groq and LangChain
- Exactly three concise summary points
- Source links for research verification
- Automated testing using pytest
- Continuous Integration using GitHub Actions
- Docker support

## Tech Stack
- Python
- Streamlit
- Groq API
- LangChain
- DuckDuckGo Search
- Pytest
- GitHub Actions
- Docker

## Run Locally

1. Clone the repository:

   `git clone https://github.com/bhakti1802/GenAI.git`

2. Open the project directory:

   `cd GenAI`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file and add your Groq API key:

   `GROQ_API_KEY=your_groq_api_key_here`

5. Start the application:

   `streamlit run app.py`

## Testing

Run the automated tests using:

`pytest -v`

## Deployment

The application is deployed on Render.

**Live Application:** https://genai-gwki.onrender.com

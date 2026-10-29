"""
Core search-and-summarize agent for the MLOps Task-Automation Agent.

This module implements web search using DuckDuckGo and summarization
using Groq's LLM (Llama 3) via LangChain.
"""

import os
import logging
import re
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Groq API imports for LangChain
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# DuckDuckGo search import
from ddgs import DDGS

# Module-level logger
logger = logging.getLogger('agent')


def search_web(topic: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for a topic using DuckDuckGo and return structured results.
    
    Args:
        topic: The search query topic.
        num_results: Maximum number of results to retrieve (default: 5).
        
    Returns:
        List of dictionaries with keys: 'title', 'snippet', 'url', 'source'.
    """
    # Validate topic: if empty/whitespace, raise ValueError
    if not topic or not topic.strip():
        raise ValueError("Topic must be a non-empty string.")
    
    try:
        with DDGS() as ddgs:
            # Use list() to materialize results and avoid iterator issues
            raw_results = list(ddgs.text(topic, max_results=num_results))
        
        # Handle empty results
        if not raw_results:
            logger.warning(f"No search results found for topic")
            return []
        
        # Parse results
        parsed_results = []
        for r in raw_results:
            parsed_results.append({
                'title': r.get('title', ''),
                'snippet': r.get('body', ''),
                'url': r.get('href', ''),
                'source': r.get('href', '')
            })
        
        return parsed_results
        
    except Exception as e:
        logger.error(f"SearchWeb error: {type(e).__name__}: {str(e)}")
        return []


def summarize_results(results: List[Dict[str, str]], topic: str) -> List[str]:
    """
    Summarize search results using Groq LLM (Llama 3) via LangChain and return exactly 3 bullet points.
    
    Args:
        results: List of search result dictionaries.
        topic: The original search topic.
        
    Returns:
        List of exactly 3 bullet point strings.
        
    Raises:
        EnvironmentError: If GROQ_API_KEY is not set.
        RuntimeError: If rate limit reached or summarization fails.
    """
    # If results is empty, return a single-item list with informative message
    if not results:
        return ["No search results were found for the given topic."]
    
    # Read GROQ_API_KEY from environment
    api_key = os.environ.get('GROQ_API_KEY', '').strip()
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY environment variable is not set.")
    
    # Build context string from results (limit to 5 to control token usage)
    context_parts = []
    for r in results[:5]:
        if r.get('title') or r.get('snippet'):
            context_parts.append(f"- {r.get('title', '')}: {r.get('snippet', '')}")
    
    context = "\n".join(context_parts)
    
    # Initialize Groq LLM - LangChain reads GROQ_API_KEY from environment automatically
    # Groq model names (2026): openai/gpt-oss-120b, qwen/qwen3
    # Using openai/gpt-oss-120b for best quality (available on free tier)
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3, api_key=api_key)
    
    # Create messages
    system_msg = SystemMessage(
        content="You are a research assistant. Summarize the provided search results about the given topic. Return EXACTLY three concise bullet points. Each bullet point must start with '- '. Base your summary ONLY on the provided information. Do not invent facts or present unsupported claims."
    )
    
    human_msg = HumanMessage(
        content=f"Topic: {topic}\n\nSearch results:\n{context}"
    )
    
    try:
        # Invoke LLM
        response = llm.invoke([system_msg, human_msg])
        
        # Parse response content
        bullets = []
        if response and response.content:
            lines = response.content.split('\n')
            for line in lines:
                line = line.strip()
                # Keep lines starting with '- ' or '* '
                if line.startswith('- ') or line.startswith('* '):
                    # Normalize to '- ' prefix
                    if line.startswith('* '):
                        line = '- ' + line[2:]
                    bullets.append(line)
        
        # Pad with default message if fewer than 3 bullet points
        while len(bullets) < 3:
            bullets.append("- Information on this aspect was not available in the search results.")
        
        # Keep only first 3 if more than 3
        if len(bullets) > 3:
            bullets = bullets[:3]
        
        return bullets
        
    except Exception as e:
        logger.error(f"SummarizeResults error: {type(e).__name__}: {str(e)}")
        raise RuntimeError(f"Summarization failed: {type(e).__name__}") from e


def run_agent(topic: str) -> Dict[str, Any]:
    """
    Orchestrate the search-and-summarize pipeline for a given topic.
    
    Args:
        topic: The research topic to investigate.
        
    Returns:
        Dictionary with keys: success, topic, bullets, sources, error.
    """
    # Strip the topic string
    topic = topic.strip() if topic else ""
    
    # Check for empty topic
    if not topic:
        return {
            'success': False,
            'topic': topic,
            'bullets': [],
            'sources': [],
            'error': 'Topic must not be empty.'
        }
    
    # Search the web
    results = search_web(topic)
    
    # Collect unique source URLs
    sources = []
    seen_urls = set()
    for r in results:
        url = r.get('url', '').strip()
        if url and url not in seen_urls:
            sources.append(url)
            seen_urls.add(url)
    
    # Summarize results
    try:
        bullets = summarize_results(results, topic)
        return {
            'success': True,
            'topic': topic,
            'bullets': bullets,
            'sources': sources,
            'error': None
        }
    except EnvironmentError as e:
        return {
            'success': False,
            'topic': topic,
            'bullets': [],
            'sources': [],
            'error': str(e)
        }
    except RuntimeError as e:
        return {
            'success': False,
            'topic': topic,
            'bullets': [],
            'sources': [],
            'error': str(e)
        }
    except Exception as e:
        logger.error(f"RunAgent error: {type(e).__name__}: {str(e)}")
        return {
            'success': False,
            'topic': topic,
            'bullets': [],
            'sources': [],
            'error': f"Unexpected error: {type(e).__name__}"
        }


if __name__ == '__main__':
    # Quick smoke test
    if 'GROQ_API_KEY' not in os.environ:
        print("GROQ_API_KEY not found in environment. Please set it before running.")
        exit(1)
    
    result = run_agent('machine learning in healthcare')
    
    if result['success']:
        print("Search and summarization successful!")
        for i, bullet in enumerate(result['bullets'], 1):
            print(f"{i}. {bullet}")
    else:
        print(f"Error: {result['error']}")

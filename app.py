"""
Streamlit web application for the MLOps Task-Automation Agent.

This module provides a web interface for the agent that searches the web
and summarizes research topics.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from agent import run_agent

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="MLOps Task-Automation Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🤖 MLOps Task-Automation Agent")
st.markdown("Search the web and get concise summaries in exactly 3 bullet points.")

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.info(
        "This agent searches the web for your research topic and returns "
        "exactly three concise bullet points summarizing the findings."
    )
    
    st.divider()
    
    st.header("Instructions")
    st.markdown(
        "1. Enter a research topic in the text box below\n"
        "2. Click **Search** to initiate the search\n"
        "3. View the results in the output area"
    )
    
    st.divider()
    
    # API Key status indicator (Groq)
    if os.environ.get('GROQ_API_KEY'):
        st.success("✅ Groq API key configured")
    else:
        st.warning("⚠️ Groq API key not set. Set GROQ_API_KEY environment variable.")

# Main content area
st.divider()

# Topic input
topic = st.text_input(
    "Enter a research topic:",
    placeholder="e.g., Machine learning applications in healthcare",
    help="Enter a specific research topic you'd like to investigate"
)

# Search button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

# Results display
if search_button:
    if not topic or not topic.strip():
        st.error("Please enter a valid research topic.")
        st.stop()
    
    # Progress indicator
    with st.status("Searching the web...", expanded=True) as status:
        st.write("🔍 Querying DuckDuckGo...")
        
        try:
            # Run the agent
            result = run_agent(topic)
            
            if result['success']:
                status.update(label="✅ Search complete!", state="complete")
                
                # Display bullet points
                st.subheader("Summary")
                for i, bullet in enumerate(result['bullets'], 1):
                    st.markdown(f"**{i}.** {bullet}")
                
                # Display sources if available
                if result['sources']:
                    st.divider()
                    st.subheader("Sources")
                    for i, source in enumerate(result['sources'], 1):
                        st.markdown(f"[Source {i}]({source})")
                
                # Add a copy button for bullet points
                with st.expander("📋 Copy all bullet points"):
                    all_bullets = "\n".join(result['bullets'])
                    st.code(all_bullets, language="markdown")
            else:
                status.update(label="❌ Error occurred", state="error")
                st.error(f"**Error:** {result['error']}")
                st.info("Please check your Groq API key and try again.")
                
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"**Unexpected error:** {str(e)}")
            st.info("Please try again later.")

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by Groq Llama 3 & DuckDuckGo Search"
    "</div>",
    unsafe_allow_html=True
)

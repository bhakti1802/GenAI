"""
Tests for the Streamlit web application.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



class TestAppImports:
    """Tests for app.py imports and structure."""
    
    def test_app_imports_streamlit(self):
        """Test that streamlit is imported in app.py."""
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.py'), 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'import streamlit' in content
    
    def test_app_imports_agent(self):
        """Test that agent is imported in app.py."""
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.py'), 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'from agent import run_agent' in content
    
    def test_app_has_run_agent_call(self):
        """Test that app.py calls run_agent function."""
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.py'), 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'run_agent' in content


class TestAgentFunctionality:
    """Tests for agent.py function structure."""
    
    def test_agent_has_search_web_function(self):
        """Test that agent.py has search_web function."""
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'agent.py'), 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'def search_web(' in content
    
    def test_agent_has_summarize_results_function(self):
        """Test that agent.py has summarize_results function."""
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'agent.py'), 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'def summarize_results(' in content
    
    def test_agent_has_run_agent_function(self):
        """Test that agent.py has run_agent function."""
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'agent.py'), 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'def run_agent(' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

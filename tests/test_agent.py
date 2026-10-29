"""
Tests for the search-and-summarize agent.
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import search_web, summarize_results, run_agent


class TestSearchWeb:
    """Tests for the search_web function."""
    
    def test_search_web_valid_topic(self):
        """Test search with a valid topic."""
        results = search_web("artificial intelligence")
        assert isinstance(results, list)
        # Note: This may return empty results depending on network conditions
    
    def test_search_web_empty_topic(self):
        """Test search with empty topic raises ValueError."""
        with pytest.raises(ValueError, match="Topic must be a non-empty string"):
            search_web("")
    
    def test_search_web_whitespace_topic(self):
        """Test search with whitespace-only topic raises ValueError."""
        with pytest.raises(ValueError, match="Topic must be a non-empty string"):
            search_web("   ")
    
    def test_search_web_num_results(self):
        """Test search with custom num_results."""
        results = search_web("test", num_results=3)
        assert isinstance(results, list)


class TestSummarizeResults:
    """Tests for the summarize_results function."""
    
    def test_summarize_results_empty(self):
        """Test summarization with empty results."""
        bullets = summarize_results([], "test topic")
        assert isinstance(bullets, list)
        assert len(bullets) == 1
        assert "No search results" in bullets[0]
    
    @patch('agent.ChatGroq')
    def test_summarize_results_with_results(self, mock_chat):
        """Test summarization with mock results."""
        # Setup mock
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="- Point 1\n- Point 2\n- Point 3")
        mock_chat.return_value = mock_llm
        
        results = [
            {'title': 'Result 1', 'snippet': 'Content 1', 'url': 'http://example.com'},
            {'title': 'Result 2', 'snippet': 'Content 2', 'url': 'http://example2.com'}
        ]
        
        with patch.dict(os.environ, {'GROQ_API_KEY': 'fake-key'}):
            bullets = summarize_results(results, "test topic")
        
        assert isinstance(bullets, list)
        assert len(bullets) == 3
    
    def test_summarize_results_no_api_key(self):
        """Test that missing API key raises EnvironmentError."""
        results = [{'title': 'Test', 'snippet': 'Content', 'url': 'http://test.com'}]
        
        with patch.dict(os.environ, {'GROQ_API_KEY': ''}, clear=True):
            with pytest.raises(EnvironmentError, match="GROQ_API_KEY environment variable is not set"):
                summarize_results(results, "test topic")


class TestRunAgent:
    """Tests for the run_agent function."""
    
    def test_run_agent_empty_topic(self):
        """Test agent with empty topic."""
        result = run_agent("")
        assert result['success'] is False
        assert 'error' in result
        assert result['bullets'] == []
    
    def test_run_agent_whitespace_topic(self):
        """Test agent with whitespace-only topic."""
        result = run_agent("   ")
        assert result['success'] is False
    
    @patch('agent.search_web')
    @patch('agent.summarize_results')
    def test_run_agent_success(self, mock_summarize, mock_search):
        """Test successful agent run."""
        mock_search.return_value = [
            {'title': 'Result 1', 'snippet': 'Content 1', 'url': 'http://test1.com'},
            {'title': 'Result 2', 'snippet': 'Content 2', 'url': 'http://test2.com'}
        ]
        mock_summarize.return_value = ["- Bullet 1", "- Bullet 2", "- Bullet 3"]
        
        with patch.dict(os.environ, {'GROQ_API_KEY': 'fake-key'}):
            result = run_agent("test topic")
        
        assert result['success'] is True
        assert len(result['bullets']) == 3
        assert len(result['sources']) == 2
        assert result['error'] is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

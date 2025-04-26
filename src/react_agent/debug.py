"""Debugging utilities for LangGraph deployment"""

import os
import sys
import logging
import importlib
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("debug")

def check_environment_variables() -> Dict[str, bool]:
    """Check if required environment variables are set.
    Returns a dictionary with variable names and boolean indicating if they exist.
    Does NOT log the actual values for security.
    """
    required_vars = [
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "TAVILY_API_KEY",
        # Add any other environment variables your deployment might need
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_TRACING_V2",
        "LANGCHAIN_ENDPOINT",
        "LANGCHAIN_PROJECT",
    ]
    
    results = {}
    for var in required_vars:
        exists = var in os.environ and bool(os.environ[var])
        results[var] = exists
        logger.info(f"Environment variable {var}: {'EXISTS' if exists else 'MISSING'}")
    
    return results

def check_imports() -> bool:
    """Check if all required packages can be imported."""
    required_packages = [
        "langchain",
        "langchain_core",
        "langgraph",
        "langchain_anthropic",
        "langchain_openai",
        "langchain_tavily",
    ]
    
    all_successful = True
    for package in required_packages:
        try:
            importlib.import_module(package)
            logger.info(f"Import check: {package} ✓")
        except ImportError as e:
            logger.error(f"Import check: {package} ✗ - {str(e)}")
            all_successful = False
    
    return all_successful

def check_file_exists(filepath: str) -> bool:
    """Check if a file exists and log the result."""
    exists = os.path.isfile(filepath)
    logger.info(f"File check {filepath}: {'EXISTS' if exists else 'MISSING'}")
    return exists

def log_diagnostic_info() -> None:
    """Log diagnostic information about the deployment environment"""
    logger.info("=== DEPLOYMENT DIAGNOSTICS ===")
    
    # Check Python version
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python executable: {sys.executable}")
    
    # Check environment variables
    check_environment_variables()
    
    # Check imports
    check_imports()
    
    # Log current working directory and contents
    cwd = os.getcwd()
    logger.info(f"Current working directory: {cwd}")
    
    try:
        files = os.listdir(cwd)
        logger.info(f"Directory contents: {', '.join(files[:10])}")
        if len(files) > 10:
            logger.info(f"...and {len(files) - 10} more files")
    except Exception as e:
        logger.error(f"Error listing directory: {str(e)}")
    
    # Check for .env file
    check_file_exists(os.path.join(cwd, '.env'))
    
    # Log environment variables starting with LANGGRAPH or LG
    lg_vars = [k for k in os.environ.keys() if k.startswith(("LANGGRAPH", "LG", "LANGCHAIN"))]
    logger.info(f"LangGraph/LangChain-related environment variables: {lg_vars}")
    
    logger.info("=== END DIAGNOSTICS ===") 
"""Command line tool for diagnosing environment issues"""

import argparse
from react_agent.debug import log_diagnostic_info

def main():
    parser = argparse.ArgumentParser(description="LangGraph deployment diagnostics")
    parser.add_argument(
        "--check-env", action="store_true", 
        help="Check environment variables required for deployment"
    )
    
    args = parser.parse_args()
    
    if args.check_env:
        log_diagnostic_info()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
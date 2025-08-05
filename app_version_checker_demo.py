#!/usr/bin/env python3
"""
Application Version Checker - Demo Version
Demonstrates the CLI interface without requiring external dependencies
"""

import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Check for outdated applications on the system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Check all package managers
  %(prog)s --format json      # Output in JSON format
  %(prog)s --verbose          # Show detailed logging
  %(prog)s --managers apt pip # Check only specific managers
        """
    )
    
    parser.add_argument(
        '--format', 
        choices=['table', 'json', 'csv'],
        default='table',
        help='Output format (default: table)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--managers', '-m',
        nargs='+',
        choices=['apt', 'yum', 'dnf', 'pacman', 'snap', 'flatpak', 'pip', 'npm', 'manual'],
        help='Specific package managers to check'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=300,
        help='Timeout for the entire scan in seconds (default: 300)'
    )
    
    args = parser.parse_args()
    
    print("This is a demo version showing the CLI interface.")
    print("To use the full application, install dependencies and run app_version_checker.py")
    print()
    print("Your selected options:")
    print(f"  Format: {args.format}")
    print(f"  Verbose: {args.verbose}")
    print(f"  Managers: {args.managers or 'all'}")
    print(f"  Timeout: {args.timeout}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script for the Application Version Checker
This version works without external dependencies for demonstration purposes.
"""

import subprocess
import json
import re
import sys

def run_command(command):
    """Run a shell command and return success status and output"""
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        return result.returncode == 0, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, ""

def test_system_info():
    """Test basic system information gathering"""
    print("=== System Information Test ===")
    
    # Test OS information
    success, output = run_command(['uname', '-a'])
    if success:
        print(f"System: {output}")
    
    # Test Python version
    success, output = run_command(['python3', '--version'])
    if success:
        print(f"Python: {output}")
    
    # Test available package managers
    package_managers = {
        'apt': ['apt', '--version'],
        'yum': ['yum', '--version'],
        'dnf': ['dnf', '--version'],
        'pacman': ['pacman', '--version'],
        'snap': ['snap', '--version'],
        'pip': ['pip', '--version'],
        'npm': ['npm', '--version']
    }
    
    print("\n=== Available Package Managers ===")
    for manager, command in package_managers.items():
        success, output = run_command(command)
        status = "✓ Available" if success else "✗ Not available"
        print(f"{manager:10}: {status}")
        if success and len(output) < 100:
            print(f"           Version: {output.split()[0] if output else 'Unknown'}")

def test_package_detection():
    """Test package detection capabilities"""
    print("\n=== Package Detection Test ===")
    
    # Test dpkg (Debian/Ubuntu systems)
    success, output = run_command(['dpkg-query', '-W', '-f=${Package}\t${Version}\n'])
    if success:
        lines = output.split('\n')[:5]  # Show first 5 packages
        print("Sample installed packages (dpkg):")
        for line in lines:
            if '\t' in line:
                package, version = line.split('\t', 1)
                print(f"  {package}: {version}")
    
    # Test pip packages
    success, output = run_command(['pip', 'list'])
    if success:
        lines = output.split('\n')[2:7]  # Skip header, show first 5
        print("\nSample Python packages (pip):")
        for line in lines:
            if line.strip():
                print(f"  {line}")

def test_version_extraction():
    """Test version extraction from common applications"""
    print("\n=== Version Extraction Test ===")
    
    applications = {
        'git': ['git', '--version'],
        'curl': ['curl', '--version'],
        'python3': ['python3', '--version'],
        'bash': ['bash', '--version'],
        'grep': ['grep', '--version']
    }
    
    for app, command in applications.items():
        success, output = run_command(command)
        if success:
            # Extract version number
            version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', output)
            version = version_match.group(1) if version_match else "Unknown"
            print(f"{app:10}: {version}")
        else:
            print(f"{app:10}: Not installed")

def test_update_checking():
    """Test update checking simulation"""
    print("\n=== Update Checking Simulation ===")
    
    # Simulate checking for apt updates (without actually updating)
    success, output = run_command(['apt', 'list', '--upgradable'])
    if success:
        lines = output.split('\n')[1:6]  # Skip header, show first 5
        if lines and any(line.strip() for line in lines):
            print("Sample upgradable packages (apt):")
            for line in lines:
                if line.strip() and '/' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        package = parts[0].split('/')[0]
                        print(f"  {package}: Update available")
        else:
            print("No apt updates available or apt not accessible")
    else:
        print("Could not check apt updates (may need permissions)")
    
    # Test snap refresh list
    success, output = run_command(['snap', 'refresh', '--list'])
    if success and output:
        print("\nSnap packages with updates:")
        lines = output.split('\n')[1:6]  # Skip header
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    print(f"  {parts[0]}: {parts[1]} → {parts[2]}")
    else:
        print("\nNo snap updates available or snap not accessible")

def test_json_output():
    """Test JSON output formatting"""
    print("\n=== JSON Output Test ===")
    
    sample_data = [
        {
            "name": "example-package",
            "current_version": "1.0.0",
            "latest_version": "1.2.0",
            "package_manager": "apt",
            "update_available": True,
            "repository": None
        },
        {
            "name": "another-package",
            "current_version": "2.1.0",
            "latest_version": "2.3.0",
            "package_manager": "pip",
            "update_available": True,
            "repository": None
        }
    ]
    
    print("Sample JSON output:")
    print(json.dumps(sample_data, indent=2))

def main():
    """Run all tests"""
    print("Application Version Checker - Test Suite")
    print("=" * 50)
    
    try:
        test_system_info()
        test_package_detection()
        test_version_extraction()
        test_update_checking()
        test_json_output()
        
        print("\n" + "=" * 50)
        print("Test completed successfully!")
        print("\nTo run the full application:")
        print("1. Install dependencies: pip install requests packaging")
        print("2. Run: python3 app_version_checker.py")
        print("3. For help: python3 app_version_checker.py --help")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
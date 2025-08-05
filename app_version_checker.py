#!/usr/bin/env python3
"""
Application Version Checker
A tool to identify older versions of applications installed on the system
and check for available updates.

Supports:
- System package managers (apt, yum, dnf, pacman, zypper)
- Snap packages
- Flatpak applications
- Python packages (pip)
- Node.js packages (npm global)
- Manual version checking for popular applications
"""

import subprocess
import json
import re
import sys
import argparse
import requests
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from packaging import version
import time

@dataclass
class Application:
    name: str
    current_version: str
    latest_version: Optional[str] = None
    package_manager: str = ""
    update_available: bool = False
    repository: Optional[str] = None

class VersionChecker:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.applications: List[Application] = []
        
    def log(self, message: str):
        """Log verbose messages"""
        if self.verbose:
            print(f"[DEBUG] {message}")
    
    def run_command(self, command: List[str]) -> Tuple[bool, str]:
        """Run a shell command and return success status and output"""
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False, ""
    
    def check_apt_packages(self) -> List[Application]:
        """Check APT packages for updates"""
        apps = []
        self.log("Checking APT packages...")
        
        # Get list of installed packages
        success, output = self.run_command(['dpkg-query', '-W', '-f=${Package}\t${Version}\n'])
        if not success:
            return apps
        
        installed_packages = {}
        for line in output.split('\n'):
            if '\t' in line:
                package, version = line.split('\t', 1)
                installed_packages[package] = version
        
        # Check for updates
        self.run_command(['sudo', 'apt', 'update'])
        success, output = self.run_command(['apt', 'list', '--upgradable'])
        
        if success:
            for line in output.split('\n')[1:]:  # Skip header
                if '/' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        package = parts[0].split('/')[0]
                        if package in installed_packages:
                            current_version = installed_packages[package]
                            # Extract available version
                            available_match = re.search(r'(\d+[.\d]*[.\d\w-]*)', parts[1])
                            if available_match:
                                latest_version = available_match.group(1)
                                apps.append(Application(
                                    name=package,
                                    current_version=current_version,
                                    latest_version=latest_version,
                                    package_manager="apt",
                                    update_available=True
                                ))
        
        return apps
    
    def check_yum_dnf_packages(self) -> List[Application]:
        """Check YUM/DNF packages for updates"""
        apps = []
        
        # Try dnf first, then yum
        for manager in ['dnf', 'yum']:
            self.log(f"Checking {manager.upper()} packages...")
            success, output = self.run_command([manager, 'check-update'])
            if success or output:  # check-update returns 100 when updates available
                for line in output.split('\n'):
                    if re.match(r'^[a-zA-Z0-9]', line) and '.' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            package = parts[0].split('.')[0]
                            available_version = parts[1]
                            
                            # Get current version
                            success_current, current_output = self.run_command([
                                'rpm', '-q', '--queryformat', '%{VERSION}-%{RELEASE}', package
                            ])
                            if success_current:
                                apps.append(Application(
                                    name=package,
                                    current_version=current_output,
                                    latest_version=available_version,
                                    package_manager=manager,
                                    update_available=True
                                ))
                break  # Use first available package manager
        
        return apps
    
    def check_pacman_packages(self) -> List[Application]:
        """Check Pacman packages for updates"""
        apps = []
        self.log("Checking Pacman packages...")
        
        success, output = self.run_command(['checkupdates'])
        if success:
            for line in output.split('\n'):
                if ' ' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        package = parts[0]
                        current_version = parts[1]
                        latest_version = parts[3]
                        apps.append(Application(
                            name=package,
                            current_version=current_version,
                            latest_version=latest_version,
                            package_manager="pacman",
                            update_available=True
                        ))
        
        return apps
    
    def check_snap_packages(self) -> List[Application]:
        """Check Snap packages for updates"""
        apps = []
        self.log("Checking Snap packages...")
        
        success, output = self.run_command(['snap', 'refresh', '--list'])
        if success:
            for line in output.split('\n')[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        package = parts[0]
                        current_version = parts[1]
                        latest_version = parts[2]
                        apps.append(Application(
                            name=package,
                            current_version=current_version,
                            latest_version=latest_version,
                            package_manager="snap",
                            update_available=True
                        ))
        
        return apps
    
    def check_flatpak_packages(self) -> List[Application]:
        """Check Flatpak packages for updates"""
        apps = []
        self.log("Checking Flatpak packages...")
        
        success, output = self.run_command(['flatpak', 'remote-ls', '--updates'])
        if success:
            for line in output.split('\n'):
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        package = parts[0]
                        current_version = "installed"
                        latest_version = parts[1]
                        apps.append(Application(
                            name=package,
                            current_version=current_version,
                            latest_version=latest_version,
                            package_manager="flatpak",
                            update_available=True
                        ))
        
        return apps
    
    def check_pip_packages(self) -> List[Application]:
        """Check Python pip packages for updates"""
        apps = []
        self.log("Checking pip packages...")
        
        success, output = self.run_command(['pip', 'list', '--outdated', '--format=json'])
        if success:
            try:
                outdated_packages = json.loads(output)
                for package in outdated_packages:
                    apps.append(Application(
                        name=package['name'],
                        current_version=package['version'],
                        latest_version=package['latest_version'],
                        package_manager="pip",
                        update_available=True
                    ))
            except json.JSONDecodeError:
                pass
        
        return apps
    
    def check_npm_packages(self) -> List[Application]:
        """Check Node.js npm global packages for updates"""
        apps = []
        self.log("Checking npm global packages...")
        
        success, output = self.run_command(['npm', 'outdated', '-g', '--json'])
        if success and output:
            try:
                outdated_packages = json.loads(output)
                for package_name, package_info in outdated_packages.items():
                    apps.append(Application(
                        name=package_name,
                        current_version=package_info.get('current', 'unknown'),
                        latest_version=package_info.get('latest', 'unknown'),
                        package_manager="npm",
                        update_available=True
                    ))
            except json.JSONDecodeError:
                pass
        
        return apps
    
    def check_github_releases(self, repo: str, current_version: str) -> Optional[str]:
        """Check GitHub releases for latest version"""
        try:
            url = f"https://api.github.com/repos/{repo}/releases/latest"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('tag_name', '').lstrip('v')
                return latest_version
        except requests.RequestException:
            pass
        return None
    
    def check_popular_applications(self) -> List[Application]:
        """Check popular applications manually"""
        apps = []
        self.log("Checking popular applications...")
        
        # Define applications to check with their GitHub repositories
        popular_apps = {
            'docker': 'docker/cli',
            'git': 'git/git',
            'code': 'microsoft/vscode',
            'firefox': 'mozilla/gecko-dev',
            'chrome': None,  # No public repo
            'node': 'nodejs/node',
            'python': 'python/cpython',
        }
        
        for app_name, repo in popular_apps.items():
            # Try to get current version
            current_version = self.get_application_version(app_name)
            if current_version and repo:
                latest_version = self.check_github_releases(repo, current_version)
                if latest_version:
                    try:
                        if version.parse(current_version) < version.parse(latest_version):
                            apps.append(Application(
                                name=app_name,
                                current_version=current_version,
                                latest_version=latest_version,
                                package_manager="manual",
                                update_available=True,
                                repository=repo
                            ))
                    except version.InvalidVersion:
                        # If version parsing fails, still add it for manual review
                        apps.append(Application(
                            name=app_name,
                            current_version=current_version,
                            latest_version=latest_version,
                            package_manager="manual",
                            update_available=True,
                            repository=repo
                        ))
        
        return apps
    
    def get_application_version(self, app_name: str) -> Optional[str]:
        """Get version of a specific application"""
        version_commands = {
            'docker': ['docker', '--version'],
            'git': ['git', '--version'],
            'code': ['code', '--version'],
            'firefox': ['firefox', '--version'],
            'node': ['node', '--version'],
            'python': ['python3', '--version'],
            'python3': ['python3', '--version'],
            'npm': ['npm', '--version'],
            'pip': ['pip', '--version'],
        }
        
        if app_name in version_commands:
            success, output = self.run_command(version_commands[app_name])
            if success:
                # Extract version number from output
                version_match = re.search(r'(\d+\.\d+(?:\.\d+)?(?:[.-]\w+)?)', output)
                if version_match:
                    return version_match.group(1)
        
        return None
    
    def scan_all_packages(self) -> List[Application]:
        """Scan all package managers for outdated applications"""
        all_apps = []
        
        # Use ThreadPoolExecutor for parallel checking
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = []
            
            # Submit all check functions
            check_functions = [
                self.check_apt_packages,
                self.check_yum_dnf_packages,
                self.check_pacman_packages,
                self.check_snap_packages,
                self.check_flatpak_packages,
                self.check_pip_packages,
                self.check_npm_packages,
                self.check_popular_applications,
            ]
            
            for check_func in check_functions:
                futures.append(executor.submit(check_func))
            
            # Collect results
            for future in as_completed(futures):
                try:
                    apps = future.result()
                    all_apps.extend(apps)
                except Exception as e:
                    self.log(f"Error in check function: {e}")
        
        return all_apps
    
    def format_output(self, apps: List[Application], output_format: str = "table") -> str:
        """Format the output in different formats"""
        if not apps:
            return "No outdated applications found!"
        
        if output_format == "json":
            app_dicts = []
            for app in apps:
                app_dicts.append({
                    'name': app.name,
                    'current_version': app.current_version,
                    'latest_version': app.latest_version,
                    'package_manager': app.package_manager,
                    'update_available': app.update_available,
                    'repository': app.repository
                })
            return json.dumps(app_dicts, indent=2)
        
        elif output_format == "csv":
            lines = ["Name,Current Version,Latest Version,Package Manager,Repository"]
            for app in apps:
                lines.append(f"{app.name},{app.current_version},{app.latest_version},{app.package_manager},{app.repository or ''}")
            return "\n".join(lines)
        
        else:  # table format
            output = []
            output.append("=" * 80)
            output.append("OUTDATED APPLICATIONS FOUND")
            output.append("=" * 80)
            output.append(f"{'Application':<20} {'Current':<15} {'Latest':<15} {'Manager':<10} {'Repository':<20}")
            output.append("-" * 80)
            
            for app in apps:
                repo_str = (app.repository or "")[:20] if app.repository else ""
                output.append(f"{app.name:<20} {app.current_version:<15} {app.latest_version:<15} {app.package_manager:<10} {repo_str:<20}")
            
            output.append("-" * 80)
            output.append(f"Total outdated applications: {len(apps)}")
            return "\n".join(output)

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
    
    checker = VersionChecker(verbose=args.verbose)
    
    print("Scanning for outdated applications...")
    if args.verbose:
        print(f"Timeout set to {args.timeout} seconds")
    
    start_time = time.time()
    
    try:
        if args.managers:
            # Check only specific managers
            apps = []
            manager_functions = {
                'apt': checker.check_apt_packages,
                'yum': checker.check_yum_dnf_packages,
                'dnf': checker.check_yum_dnf_packages,
                'pacman': checker.check_pacman_packages,
                'snap': checker.check_snap_packages,
                'flatpak': checker.check_flatpak_packages,
                'pip': checker.check_pip_packages,
                'npm': checker.check_npm_packages,
                'manual': checker.check_popular_applications,
            }
            
            for manager in args.managers:
                if manager in manager_functions:
                    apps.extend(manager_functions[manager]())
        else:
            # Check all managers
            apps = checker.scan_all_packages()
        
        elapsed_time = time.time() - start_time
        
        if args.verbose:
            print(f"Scan completed in {elapsed_time:.2f} seconds")
        
        # Output results
        output = checker.format_output(apps, args.format)
        print(output)
        
        # Exit with appropriate code
        sys.exit(1 if apps else 0)
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error during scan: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
# Application Version Checker

A comprehensive tool to identify older versions of applications installed on your system and check for available updates across multiple package managers and installation methods.

## Features

- **Multi-Package Manager Support**: Checks APT, YUM/DNF, Pacman, Snap, Flatpak, pip, and npm
- **Popular Application Detection**: Manually checks versions of common applications like Docker, Git, VS Code, Firefox, Node.js, and Python
- **GitHub Integration**: Fetches latest versions from GitHub releases for applications
- **Multiple Output Formats**: Table, JSON, and CSV output formats
- **Parallel Processing**: Fast concurrent checking across all package managers
- **Flexible Filtering**: Check specific package managers or all at once
- **Verbose Logging**: Detailed debug information when needed

## Installation

### From Source

```bash
# Clone or download the files
git clone <repository-url>
cd app-version-checker

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x app_version_checker.py
```

### Using pip

```bash
# Install from local directory
pip install .

# Or install in development mode
pip install -e .
```

## Usage

### Basic Usage

```bash
# Check all package managers
python3 app_version_checker.py

# Or if installed via pip
app-version-checker
```

### Advanced Usage

```bash
# Check specific package managers only
python3 app_version_checker.py --managers apt pip npm

# Output in JSON format
python3 app_version_checker.py --format json

# Output in CSV format (good for spreadsheets)
python3 app_version_checker.py --format csv

# Enable verbose logging
python3 app_version_checker.py --verbose

# Combine options
python3 app_version_checker.py --managers apt snap --format json --verbose
```

### Command Line Options

- `--format {table,json,csv}`: Output format (default: table)
- `--verbose, -v`: Enable verbose logging
- `--managers, -m`: Specific package managers to check
  - Available: `apt`, `yum`, `dnf`, `pacman`, `snap`, `flatpak`, `pip`, `npm`, `manual`
- `--timeout`: Timeout for the entire scan in seconds (default: 300)

## Supported Package Managers

| Package Manager | Description | Example Distributions |
|-----------------|-------------|----------------------|
| APT | Advanced Package Tool | Ubuntu, Debian, Linux Mint |
| YUM/DNF | Yellowdog Updater Modified / Dandified YUM | CentOS, RHEL, Fedora |
| Pacman | Package Manager | Arch Linux, Manjaro |
| Snap | Universal Linux packages | Ubuntu, many others |
| Flatpak | Universal applications | Various distributions |
| pip | Python package manager | All systems with Python |
| npm | Node.js package manager | All systems with Node.js |
| Manual | Direct version checking | Popular applications |

## Popular Applications Checked

The tool can manually check versions for these popular applications:

- Docker
- Git
- Visual Studio Code
- Firefox
- Node.js
- Python

For these applications, it fetches the latest versions from their GitHub repositories and compares them with locally installed versions.

## Output Examples

### Table Format (Default)
```
================================================================================
OUTDATED APPLICATIONS FOUND
================================================================================
Application          Current         Latest          Manager    Repository          
--------------------------------------------------------------------------------
curl                 7.68.0          7.81.0          apt                            
docker               20.10.12        20.10.17        manual     docker/cli          
git                  2.25.1          2.37.1          manual     git/git             
node                 14.17.0         18.7.0          manual     nodejs/node         
numpy                1.19.5          1.23.1          pip                            
--------------------------------------------------------------------------------
Total outdated applications: 5
```

### JSON Format
```json
[
  {
    "name": "curl",
    "current_version": "7.68.0",
    "latest_version": "7.81.0",
    "package_manager": "apt",
    "update_available": true,
    "repository": null
  },
  {
    "name": "docker",
    "current_version": "20.10.12",
    "latest_version": "20.10.17",
    "package_manager": "manual",
    "update_available": true,
    "repository": "docker/cli"
  }
]
```

### CSV Format
```csv
Name,Current Version,Latest Version,Package Manager,Repository
curl,7.68.0,7.81.0,apt,
docker,20.10.12,20.10.17,manual,docker/cli
git,2.25.1,2.37.1,manual,git/git
```

## Exit Codes

- `0`: No outdated applications found
- `1`: Outdated applications found or general error
- `130`: Interrupted by user (Ctrl+C)

## Requirements

- Python 3.6 or higher
- Internet connection (for checking GitHub releases and package repositories)
- Appropriate permissions to run package manager commands

### Python Dependencies

- `requests`: For HTTP requests to GitHub API
- `packaging`: For version comparison

## Permissions

Some operations may require elevated privileges:

- **APT**: `sudo apt update` requires root privileges
- **YUM/DNF**: Package queries might need root access
- **Snap/Flatpak**: Usually work with user privileges

The tool handles missing permissions gracefully and will skip operations that fail due to insufficient privileges.

## Performance

- **Parallel Processing**: All package managers are checked concurrently
- **Timeouts**: Individual commands timeout after 30 seconds
- **Overall Timeout**: Default scan timeout of 5 minutes (configurable)
- **Caching**: Package manager commands may use their own caching

## Troubleshooting

### Common Issues

1. **Permission Denied**: Some package managers require root privileges
   ```bash
   sudo python3 app_version_checker.py
   ```

2. **Command Not Found**: Package manager not installed
   - The tool will skip unavailable package managers

3. **Network Issues**: GitHub API rate limiting or connectivity
   - Use `--verbose` to see detailed error messages
   - Manual checks may fail, but package manager checks will still work

4. **Slow Performance**: Large number of packages
   - Use `--managers` to check only specific package managers
   - Adjust `--timeout` if needed

### Debug Mode

Use `--verbose` to see detailed logging:

```bash
python3 app_version_checker.py --verbose
```

This will show:
- Which package managers are being checked
- Individual command executions
- Network requests and responses
- Timing information

## Contributing

Contributions are welcome! Areas for improvement:

- Additional package manager support
- More popular applications for manual checking
- Better version parsing and comparison
- Performance optimizations
- Additional output formats

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Considerations

- The tool executes system commands to check package managers
- Network requests are made to GitHub API and package repositories
- No sensitive information is transmitted or stored
- All commands are read-only operations (except `apt update`)

## System Compatibility

- **Linux**: Fully supported (primary target)
- **macOS**: Partially supported (Homebrew integration could be added)
- **Windows**: Limited support (mainly pip and npm checking)
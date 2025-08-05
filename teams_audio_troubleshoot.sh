#!/bin/bash

# MS Teams Audio Troubleshooting Script for Linux
# Based on community solutions and Microsoft support forums

set -e

echo "=============================================="
echo "MS Teams Audio Troubleshooting Script"
echo "=============================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check audio system
check_audio_system() {
    print_status "Checking audio system..."
    
    # Check for PulseAudio
    if command_exists pactl; then
        echo "✓ PulseAudio is installed"
        pactl info > /dev/null 2>&1 && echo "✓ PulseAudio server is running" || print_warning "PulseAudio server is not running"
    else
        print_error "PulseAudio is not installed"
        return 1
    fi
    
    # Check for PipeWire
    if command_exists pipewire; then
        echo "✓ PipeWire is installed"
    fi
    
    # Check for ALSA
    if command_exists aplay; then
        echo "✓ ALSA is installed"
    fi
    
    echo ""
}

# Function to list audio devices
list_audio_devices() {
    print_status "Listing audio devices..."
    
    echo "=== Audio Output Devices (Sinks) ==="
    pactl list sinks short 2>/dev/null || print_error "Failed to list sinks"
    echo ""
    
    echo "=== Audio Input Devices (Sources) ==="
    pactl list sources short 2>/dev/null || print_error "Failed to list sources"
    echo ""
}

# Function to restart PulseAudio
restart_pulseaudio() {
    print_status "Restarting PulseAudio..."
    
    # Kill existing PulseAudio processes
    pulseaudio --kill 2>/dev/null || true
    sleep 2
    
    # Start PulseAudio
    pulseaudio --start --daemonize 2>/dev/null || pulseaudio --start
    sleep 2
    
    if pactl info > /dev/null 2>&1; then
        print_success "PulseAudio restarted successfully"
    else
        print_error "Failed to restart PulseAudio"
        return 1
    fi
}

# Function to reset PulseAudio configuration
reset_pulseaudio_config() {
    print_status "Resetting PulseAudio configuration..."
    
    # Backup existing config
    if [ -d ~/.config/pulse ]; then
        mv ~/.config/pulse ~/.config/pulse.backup.$(date +%Y%m%d_%H%M%S)
        print_status "Backed up existing PulseAudio configuration"
    fi
    
    # Remove temporary files
    rm -rf /tmp/pulse-* 2>/dev/null || true
    
    # Restart PulseAudio
    restart_pulseaudio
    
    print_success "PulseAudio configuration reset complete"
}

# Function to check Teams installation
check_teams_installation() {
    print_status "Checking Teams installation..."
    
    # Check for Teams desktop client
    if command_exists teams; then
        echo "✓ Teams desktop client is installed"
        teams --version 2>/dev/null || echo "  (Version info not available)"
    else
        print_warning "Teams desktop client is not installed"
    fi
    
    # Check for snap packages
    if command_exists snap; then
        snap list teams 2>/dev/null && print_warning "Teams snap package found - this may cause issues" || true
        snap list teams-for-linux 2>/dev/null && print_warning "teams-for-linux snap found - this may cause issues" || true
    fi
    
    echo ""
}

# Function to fix common Teams audio issues
fix_teams_audio() {
    print_status "Applying Teams audio fixes..."
    
    # Fix 1: Add user to audio group
    print_status "Adding user to audio group..."
    sudo usermod -a -G audio $USER 2>/dev/null || print_warning "Failed to add user to audio group (may need reboot)"
    
    # Fix 2: Install pavucontrol if not present
    if ! command_exists pavucontrol; then
        print_status "Installing pavucontrol..."
        if command_exists apt; then
            sudo apt update && sudo apt install -y pavucontrol
        elif command_exists dnf; then
            sudo dnf install -y pavucontrol
        elif command_exists pacman; then
            sudo pacman -S pavucontrol
        fi
    fi
    
    # Fix 3: Set inotify limits (Teams needs this for device detection)
    print_status "Setting inotify limits for Teams device detection..."
    echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf > /dev/null
    sudo sysctl -p /etc/sysctl.conf > /dev/null 2>&1 || true
    
    print_success "Common Teams audio fixes applied"
}

# Function to clean Teams cache
clean_teams_cache() {
    print_status "Cleaning Teams cache..."
    
    # Stop Teams if running
    pkill -f teams 2>/dev/null || true
    sleep 2
    
    # Remove Teams cache and config
    if [ -d ~/.config/Microsoft/Microsoft\ Teams ]; then
        rm -rf ~/.config/Microsoft/Microsoft\ Teams
        print_success "Teams configuration and cache cleared"
    else
        print_warning "Teams configuration directory not found"
    fi
}

# Function to test audio
test_audio() {
    print_status "Testing audio playback..."
    
    # Test with a simple beep if speaker-test is available
    if command_exists speaker-test; then
        echo "Playing test sound (2 seconds)..."
        timeout 2s speaker-test -t sine -f 1000 -c 2 2>/dev/null || print_warning "Audio test failed or interrupted"
    elif command_exists paplay; then
        # Generate a test tone with paplay if available
        echo "Testing with PulseAudio..."
        pactl list sinks short | head -1 | awk '{print $2}' | xargs -I {} paplay /dev/zero --device={} --channels=2 --rate=44100 --format=s16le &
        sleep 1
        pkill paplay 2>/dev/null || true
    else
        print_warning "No audio test tools available"
    fi
}

# Function to show Teams-specific tips
show_teams_tips() {
    echo ""
    print_status "Teams-Specific Audio Tips:"
    echo ""
    echo "1. DEVICE SELECTION:"
    echo "   - Set audio devices in Teams Settings > Devices BEFORE joining a call"
    echo "   - Never change devices from within an active call (known to break audio)"
    echo "   - Use pavucontrol to manually route audio if Teams settings fail"
    echo ""
    echo "2. PULSEAUDIO VOLUME CONTROL:"
    echo "   - Install and use pavucontrol: sudo apt install pavucontrol"
    echo "   - During a Teams call, open pavucontrol > Recording tab"
    echo "   - Look for 'Skype' application (Teams uses Skype audio engine)"
    echo "   - Adjust the volume slider slightly to 'wake up' the microphone"
    echo ""
    echo "3. MICROPHONE ISSUES:"
    echo "   - Microphone may stop working after ~1 minute in calls"
    echo "   - Restart Teams completely if microphone fails"
    echo "   - Ensure microphone volume is NOT set to 0% in pavucontrol"
    echo "   - Check that correct input device is selected in pavucontrol Recording tab"
    echo ""
    echo "4. BROWSER vs DESKTOP CLIENT:"
    echo "   - Desktop client: More features but more audio issues"
    echo "   - Browser client: More stable audio but requires allowing third-party cookies"
    echo "   - For Chrome: Enable cookies at chrome://settings/content/cookies"
    echo ""
    echo "5. ALTERNATIVE SOLUTIONS:"
    echo "   - Consider using teams-for-linux (unofficial): https://github.com/IsmaelMartinez/teams-for-linux"
    echo "   - This alternative has more reliable audio handling"
    echo ""
}

# Function to show advanced troubleshooting
show_advanced_troubleshooting() {
    echo ""
    print_status "Advanced Troubleshooting:"
    echo ""
    echo "1. MANUAL PULSEAUDIO RESET:"
    echo "   rm -rf ~/.config/pulse /tmp/pulse-*"
    echo "   pulseaudio --kill"
    echo "   pulseaudio --start"
    echo ""
    echo "2. CHECK TEAMS LOGS:"
    echo "   ~/.config/Microsoft/Microsoft Teams/logs.txt"
    echo ""
    echo "3. TEAMS DEBUG MODE:"
    echo "   Start Teams with: TEAMS_LOGGING=true teams"
    echo ""
    echo "4. ALSA CONFIGURATION:"
    echo "   Check ~/.asoundrc or /etc/asound.conf for conflicts"
    echo ""
    echo "5. HARDWARE DEBUGGING:"
    echo "   arecord -l  # List recording devices"
    echo "   aplay -l    # List playback devices"
    echo "   lsusb       # Check USB audio devices"
    echo ""
}

# Main execution
main() {
    echo "Starting MS Teams audio troubleshooting..."
    echo ""
    
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_error "Do not run this script as root!"
        exit 1
    fi
    
    # Parse command line arguments
    case "${1:-check}" in
        "check")
            check_audio_system
            list_audio_devices
            check_teams_installation
            ;;
        "fix")
            check_audio_system
            fix_teams_audio
            restart_pulseaudio
            clean_teams_cache
            print_success "Audio fixes applied. Please restart Teams and test."
            ;;
        "reset")
            print_warning "This will reset your PulseAudio configuration!"
            read -p "Continue? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                reset_pulseaudio_config
                clean_teams_cache
                print_success "Reset complete. Please restart Teams and reconfigure audio settings."
            else
                echo "Reset cancelled."
            fi
            ;;
        "test")
            test_audio
            ;;
        "tips")
            show_teams_tips
            ;;
        "advanced")
            show_advanced_troubleshooting
            ;;
        "help"|"--help"|"-h")
            echo "Usage: $0 [check|fix|reset|test|tips|advanced|help]"
            echo ""
            echo "Commands:"
            echo "  check     - Check current audio system status (default)"
            echo "  fix       - Apply common Teams audio fixes"
            echo "  reset     - Reset PulseAudio configuration (destructive)"
            echo "  test      - Test audio playback"
            echo "  tips      - Show Teams-specific audio tips"
            echo "  advanced  - Show advanced troubleshooting steps"
            echo "  help      - Show this help message"
            echo ""
            ;;
        *)
            print_error "Unknown command: $1"
            echo "Use '$0 help' for usage information."
            exit 1
            ;;
    esac
    
    if [[ "${1:-check}" != "help" && "${1:-check}" != "tips" && "${1:-check}" != "advanced" ]]; then
        echo ""
        print_status "For Teams-specific tips, run: $0 tips"
        print_status "For advanced troubleshooting, run: $0 advanced"
    fi
}

# Run main function with all arguments
main "$@"
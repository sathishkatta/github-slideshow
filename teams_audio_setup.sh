#!/bin/bash

# Microsoft Teams Audio Fix Setup Script for Linux
# This script implements the most effective solutions for Teams audio issues

set -e

echo "🎧 Microsoft Teams Audio Fix Setup"
echo "=================================="
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root. Please run as regular user."
   exit 1
fi

# Detect system
if command -v lsb_release &> /dev/null; then
    DISTRO=$(lsb_release -si)
    VERSION=$(lsb_release -sr)
else
    DISTRO=$(cat /etc/os-release | grep ^ID= | cut -d'=' -f2)
    VERSION=$(cat /etc/os-release | grep ^VERSION_ID= | cut -d'=' -f2 | tr -d '"')
fi

echo "🖥️  Detected: $DISTRO $VERSION"
echo ""

# Function to install packages
install_packages() {
    echo "📦 Installing audio system packages..."
    
    # Update package list
    sudo apt update
    
    # Install PipeWire (recommended for Ubuntu 22.04+)
    if [[ "$DISTRO" == "Ubuntu" ]] && [[ $(echo "$VERSION >= 22.04" | bc -l) ]]; then
        echo "Installing PipeWire audio system..."
        sudo apt install -y pipewire pipewire-pulse pipewire-audio-client-libraries \
                             wireplumber pavucontrol alsa-utils
        
        # Enable and start PipeWire services
        systemctl --user daemon-reload
        systemctl --user enable pipewire pipewire-pulse
        systemctl --user start pipewire pipewire-pulse
        
        echo "✅ PipeWire installed and started"
    else
        # Fall back to PulseAudio for older systems
        echo "Installing PulseAudio system..."
        sudo apt install -y pulseaudio pulseaudio-utils pavucontrol alsa-utils
        
        systemctl --user restart pulseaudio
        echo "✅ PulseAudio installed and started"
    fi
}

# Function to install Microsoft Edge
install_edge() {
    echo "🌐 Installing Microsoft Edge for Linux..."
    
    # Add Microsoft repository
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null
    
    echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/microsoft.gpg] https://packages.microsoft.com/repos/edge stable main" | sudo tee /etc/apt/sources.list.d/microsoft-edge.list
    
    sudo apt update
    sudo apt install -y microsoft-edge-stable
    
    echo "✅ Microsoft Edge installed"
}

# Function to install Firefox if not present
install_firefox() {
    if ! command -v firefox &> /dev/null; then
        echo "🦊 Installing Firefox..."
        sudo apt install -y firefox
        echo "✅ Firefox installed"
    else
        echo "✅ Firefox already installed"
    fi
}

# Function to test audio
test_audio() {
    echo "🎤 Testing audio system..."
    
    # Check if audio devices are available
    if [[ -f /proc/asound/cards ]]; then
        echo "📊 Available audio devices:"
        cat /proc/asound/cards
    else
        echo "⚠️  No audio devices detected in /proc/asound/cards"
    fi
    
    # Test recording and playback
    echo ""
    echo "🔴 Testing microphone (5 seconds)..."
    echo "Say something now..."
    
    if command -v arecord &> /dev/null; then
        timeout 5s arecord -f cd /tmp/test_audio.wav 2>/dev/null || true
        
        if [[ -f /tmp/test_audio.wav ]]; then
            echo "🔊 Playing back recording..."
            aplay /tmp/test_audio.wav 2>/dev/null || echo "⚠️  Playback failed"
            rm -f /tmp/test_audio.wav
        else
            echo "⚠️  Recording failed"
        fi
    else
        echo "⚠️  arecord not available, skipping audio test"
    fi
}

# Function to show browser recommendations
show_browser_recommendations() {
    echo ""
    echo "🌐 Browser Recommendations for Teams:"
    echo "====================================="
    echo ""
    echo "✅ RECOMMENDED (Working):"
    echo "  1. Firefox - Most reliable for Teams audio"
    echo "  2. Microsoft Edge - Official Microsoft support"
    echo ""
    echo "⚠️  PROBLEMATIC:"
    echo "  - Chromium (vanilla) - Known audio issues"
    echo "  - Some Chrome versions - Inconsistent results"
    echo ""
    echo "🔗 Teams URLs to try:"
    echo "  - Standard: https://teams.microsoft.com"
    echo "  - Alternative: https://teams.microsoft.com/v2/?ring=general"
    echo ""
}

# Function to show next steps
show_next_steps() {
    echo ""
    echo "🚀 Next Steps:"
    echo "=============="
    echo ""
    echo "1. 🔄 Log out and log back in (or restart) to ensure audio services are active"
    echo "2. 🌐 Open Teams in Firefox first: https://teams.microsoft.com"
    echo "3. 🔒 When prompted, allow microphone and camera permissions"
    echo "4. 🎤 Test your microphone in Teams settings"
    echo "5. 📞 Try a test call or meeting"
    echo ""
    echo "🆘 If Firefox doesn't work:"
    echo "   - Try Microsoft Edge"
    echo "   - Check browser permissions (click lock icon in address bar)"
    echo "   - Run: pavucontrol (to adjust audio levels)"
    echo ""
    echo "📋 Troubleshooting:"
    echo "   - View the complete guide: cat $PWD/teams_audio_fix.md"
    echo "   - Test microphone: arecord -f cd -d 5 test.wav && aplay test.wav"
    echo "   - Check audio mixer: pavucontrol"
    echo ""
}

# Main execution
main() {
    echo "This script will:"
    echo "1. Install proper audio system (PipeWire/PulseAudio)"
    echo "2. Install Microsoft Edge"
    echo "3. Install/verify Firefox"
    echo "4. Test your audio setup"
    echo ""
    
    read -p "Continue? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_packages
        echo ""
        install_edge
        echo ""
        install_firefox
        echo ""
        test_audio
        show_browser_recommendations
        show_next_steps
        
        echo "✅ Setup complete!"
        echo ""
        echo "💡 TIP: If you're still having issues, this is a known Microsoft Teams"
        echo "   problem on Linux. Try the Firefox workaround first."
    else
        echo "Setup cancelled."
        show_browser_recommendations
    fi
}

# Run main function
main "$@"
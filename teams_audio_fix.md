# Microsoft Teams Audio Issues on Linux - Troubleshooting Guide

## Problem Overview
Microsoft Teams has known audio issues on Linux systems, particularly affecting microphone functionality during calls. This is a widespread issue reported across multiple Linux distributions including Ubuntu, Fedora, Debian, and others.

## Current Known Issues (as of December 2024)
- **Microphone not working in Teams PWA/web version** - widespread issue affecting Chromium-based browsers
- **Audio drops and reconnections** during calls
- **Teams PWA video button greyed out** on Chromium Linux
- **Microphone volume automatically decreasing** during calls

## Quick Diagnosis

### Check Your Current Setup
```bash
# Check audio system
systemctl --user status pipewire || systemctl --user status pulseaudio

# Check available audio devices
ls /proc/asound/cards 2>/dev/null || echo "No audio cards detected"

# Check installed browsers
which google-chrome firefox microsoft-edge chromium-browser

# Check Teams installation
ls -la /usr/bin/*teams* /snap/bin/*teams* /opt/*teams* 2>/dev/null
```

## Solutions by Priority

### Solution 1: Use Firefox (Immediate Workaround)
**Status: Currently Working**
- Multiple users report Firefox works when Chromium-based browsers fail
- Access Teams at: https://teams.microsoft.com
- Alternative URL: https://teams.microsoft.com/v2/?ring=general

### Solution 2: Install Microsoft Edge for Linux
```bash
# Add Microsoft repository
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/microsoft.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list'

# Install Edge
sudo apt update
sudo apt install microsoft-edge-stable
```

### Solution 3: Install Audio System Components
```bash
# For PipeWire (recommended for newer Ubuntu)
sudo apt install pipewire pipewire-pulse pipewire-audio-client-libraries

# Start PipeWire services
systemctl --user enable pipewire pipewire-pulse
systemctl --user start pipewire pipewire-pulse

# For PulseAudio (if PipeWire not available)
sudo apt install pulseaudio pulseaudio-utils pavucontrol

# Restart audio services
systemctl --user restart pulseaudio
```

### Solution 4: Browser Permission Settings
1. Open Teams in your browser
2. Click the **lock icon** in address bar
3. Ensure **Camera** and **Microphone** are set to "Allow"
4. Refresh the page and test

### Solution 5: Install Teams Desktop App
```bash
# Download Teams for Linux (if available for your distro)
wget https://packages.microsoft.com/repos/ms-teams/pool/main/t/teams/teams_1.4.00.26453_amd64.deb
sudo dpkg -i teams_1.4.00.26453_amd64.deb
sudo apt-get install -f  # Fix dependencies if needed
```

## Advanced Troubleshooting

### Audio Device Configuration
```bash
# Install audio control tools
sudo apt install pavucontrol alsa-utils

# Run audio mixer
pavucontrol

# Test microphone
arecord -f cd -d 5 test.wav && aplay test.wav
```

### Browser-Specific Fixes

#### For Chromium/Chrome:
1. Disable hardware acceleration:
   - Go to `Settings > Advanced > System`
   - Toggle off "Use hardware acceleration when available"
2. Clear browser cache and data
3. Try incognito/private mode

#### For Firefox:
- Usually works without additional configuration
- Check `about:config` for media.navigator settings if needed

### Network/WebRTC Issues
```bash
# Check WebRTC connectivity
# Navigate to about:webrtc in your browser during a Teams call
# Look for ICE connection failures or STUN timeout errors
```

## Environment-Specific Notes

### Ubuntu 25.04 (Your System)
- This is a development version - consider using LTS version (24.04) for better stability
- Audio system may not be fully configured by default
- Install PipeWire for best compatibility

### Common Linux Audio Stack Issues
- **Missing proprietary codecs** in vanilla Chromium
- **WebRTC compatibility** differences between browsers
- **PipeWire vs PulseAudio** configuration conflicts

## Known Working Configurations

| Browser | Linux Distro | Audio System | Status |
|---------|--------------|--------------|--------|
| Firefox | Any | PipeWire/PulseAudio | ✅ Working |
| MS Edge | Ubuntu/Fedora | PipeWire | ✅ Working |
| Chrome | Ubuntu/Fedora | PipeWire | ⚠️ Partial |
| Chromium | Any | Any | ❌ Known Issues |

## Microsoft's Official Response
- This is a **known issue** tracked by Microsoft
- **Tracking ticket**: https://answers.microsoft.com/en-us/msteams/forum/all/web-teams-microphone-issue/6406dab7-4f50-4ec6-b38d-af9aca2ea132
- Some fixes are being rolled out in PWA updates
- **Teams PWA version 1415/24120100207** reportedly fixes some issues

## Immediate Action Plan

1. **Try Firefox first** - most reliable current solution
2. **Install Microsoft Edge** if Firefox isn't suitable
3. **Set up proper audio system** (PipeWire recommended)
4. **Consider Teams desktop app** if web version continues to fail
5. **Report issues** to Microsoft with specific system details

## Testing Your Fix
```bash
# Test microphone
arecord -f cd -d 5 mic_test.wav && aplay mic_test.wav

# Test in browser
# Go to: https://webcammictest.com
```

## Getting Help
- **File feedback** in Teams app (Help > Feedback)
- **Report to Microsoft**: https://feedbackportal.microsoft.com
- **Community forums**: Microsoft Tech Community
- **Include system details**: OS version, browser version, audio system

## Prevention
- Keep browsers updated
- Use LTS Linux distributions for business use
- Monitor Microsoft Teams updates and changelogs
- Have backup communication method (phone dial-in) ready

---

**Last Updated**: January 2025  
**Issue Status**: Ongoing - Microsoft working on fixes
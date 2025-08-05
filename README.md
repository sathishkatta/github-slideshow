# MS Teams Audio Troubleshooting Guide for Linux

## Overview

Microsoft Teams on Linux has well-documented audio issues that affect many users. This guide provides comprehensive solutions based on community reports and Microsoft support forums.

## Quick Fix (Most Common Solution)

**The most effective solution for Teams microphone issues:**

1. **Install PulseAudio Volume Control:**
   ```bash
   sudo apt install pavucontrol
   ```

2. **During a Teams call:**
   - Open `pavucontrol`
   - Go to the **Recording** tab
   - Look for "Skype" application (Teams uses Skype's audio engine)
   - **Slightly adjust the volume slider** - this often "wakes up" the microphone
   - Ensure the correct input device is selected

3. **Set devices BEFORE joining calls:**
   - Configure audio devices in Teams Settings > Devices
   - **Never change devices during an active call** (this breaks audio)

## Common Issues and Solutions

### 1. Microphone Stops Working After ~1 Minute

**Symptoms:**
- Microphone works initially but cuts out after about 1 minute
- Other participants hear background noise until you speak, then silence
- Microphone works fine in other applications

**Solutions:**
- Restart Teams completely when this happens
- Use pavucontrol to manually adjust microphone levels during calls
- Set audio devices before joining calls, not during

### 2. No Audio Devices Detected

**Symptoms:**
- Teams shows "No microphone" or "No speakers"
- Device settings appear frozen or empty

**Solutions:**
1. **Reset PulseAudio configuration:**
   ```bash
   rm -rf ~/.config/pulse /tmp/pulse-*
   pulseaudio --kill
   pulseaudio --start
   ```

2. **Clear Teams cache:**
   ```bash
   rm -rf ~/.config/Microsoft/Microsoft\ Teams
   ```

3. **Add user to audio group:**
   ```bash
   sudo usermod -a -G audio $USER
   # Reboot after this change
   ```

4. **Increase inotify limits** (Teams needs this for device detection):
   ```bash
   echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
   sudo sysctl -p
   ```

### 3. Audio Works in Test But Not in Calls

**Solutions:**
- Use the web version of Teams instead of the desktop client
- Check pavucontrol during actual calls (not just tests)
- Restart Teams before important meetings

## Desktop Client vs Web Client

### Desktop Client (.deb package)
- ✅ Full feature set
- ❌ More audio issues
- ❌ Requires frequent restarts
- ❌ Device switching problems

### Web Client (Browser)
- ✅ More stable audio
- ✅ Better device handling
- ❌ Fewer features
- ❌ Requires allowing third-party cookies

**For Chrome web client:**
1. Go to `chrome://settings/content/cookies`
2. Allow third-party cookies or add Teams domain to allowed list

## Using the Troubleshooting Script

This repository includes an automated troubleshooting script:

```bash
# Check current audio system status
./teams_audio_troubleshoot.sh check

# Apply common fixes
./teams_audio_troubleshoot.sh fix

# Reset PulseAudio configuration (last resort)
./teams_audio_troubleshoot.sh reset

# Show detailed tips
./teams_audio_troubleshoot.sh tips

# Show advanced troubleshooting
./teams_audio_troubleshoot.sh advanced
```

## Alternative Solutions

### 1. Unofficial Teams Client
The community-maintained [teams-for-linux](https://github.com/IsmaelMartinez/teams-for-linux) has more reliable audio:

```bash
# Install via snap
sudo snap install teams-for-linux

# Or download from GitHub releases
```

This client wraps the web interface and has better PulseAudio integration.

### 2. Browser-Only Approach
Use Teams exclusively in your browser:
- More stable audio
- No installation required
- Automatic updates
- Better device switching

## Preventive Measures

1. **Always configure audio devices BEFORE joining calls**
2. **Never change audio devices during active calls**
3. **Keep pavucontrol open during important meetings**
4. **Restart Teams between meetings if audio failed previously**
5. **Use the web client for critical meetings**

## Hardware-Specific Issues

### USB Headsets
- May require specific drivers or configuration
- Test with other applications first
- Check if headset appears in `lsusb` output

### Bluetooth Devices
- Often cause additional issues with Teams
- Consider using wired alternatives for important calls
- Check Bluetooth codec compatibility

### Built-in Microphones
- Usually more reliable than external devices
- May have hardware mute switches to check

## Advanced Troubleshooting

### Check Audio System
```bash
# List audio devices
pactl list sources short
pactl list sinks short

# Check PulseAudio status
pactl info

# Test audio recording
arecord -d 5 test.wav && aplay test.wav
```

### Teams Logs
Check Teams logs for errors:
```bash
tail -f ~/.config/Microsoft/Microsoft\ Teams/logs.txt
```

### Debug Mode
Start Teams with debug logging:
```bash
TEAMS_LOGGING=true teams
```

## Known Issues (Microsoft Acknowledged)

From Microsoft's official documentation:
- Device settings changes during meetings cause audio failure
- Microphone input indicators may not register sound correctly
- Some webcams display video upside-down
- Package managers may not show proper change lists

## When All Else Fails

1. **Use your phone** for audio while keeping video on computer
2. **Switch to alternative platforms** (Zoom, Google Meet, etc.)
3. **Use Teams web client** instead of desktop app
4. **Consider the unofficial teams-for-linux client**

## System Requirements

- Ubuntu 20.04+ (or equivalent)
- PulseAudio or PipeWire
- Modern web browser (for web client)
- Sufficient inotify watchers for device detection

## Getting Help

If issues persist:
1. Test audio with other applications (Zoom, browser calls)
2. Check if issue occurs with web client
3. Run the included troubleshooting script
4. Document specific error messages
5. Consider using alternative Teams clients

## Contributing

This guide is based on community solutions from:
- Microsoft Q&A forums
- GitHub issue trackers
- Linux distribution forums
- User experience reports

Feel free to contribute additional solutions or report new issues.

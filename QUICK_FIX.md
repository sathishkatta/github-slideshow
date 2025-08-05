# MS Teams Audio Quick Fix Guide

## 🚨 IMMEDIATE FIXES (Try These First)

### 1. The PulseAudio Volume Control Fix (90% Success Rate)
```bash
# Install pavucontrol if not already installed
sudo apt install pavucontrol

# During a Teams call:
# 1. Open pavucontrol
# 2. Go to Recording tab
# 3. Find "Skype" application
# 4. Slightly move the volume slider
# 5. Check that correct microphone is selected
```

### 2. Restart Teams Audio System
```bash
# Kill Teams completely
pkill -f teams

# Restart PulseAudio
pulseaudio --kill
pulseaudio --start

# Restart Teams
```

### 3. Clear Teams Cache
```bash
# Close Teams first
pkill -f teams

# Remove Teams configuration
rm -rf ~/.config/Microsoft/Microsoft\ Teams

# Restart Teams
```

## 🔧 DEVICE SETTINGS RULES

### ✅ DO:
- Set audio devices in Teams Settings → Devices **BEFORE** joining calls
- Use pavucontrol to check/adjust devices during calls
- Test microphone with Teams test call before important meetings
- Restart Teams if microphone fails mid-call

### ❌ DON'T:
- **Never change devices from within an active call** (this breaks audio)
- Don't trust Teams device settings during calls
- Don't ignore the microphone test results

## 📞 CALL TROUBLESHOOTING

### If microphone stops working during a call:
1. Open pavucontrol immediately
2. Go to Recording tab
3. Adjust the "Skype" volume slider
4. If still broken: Leave and rejoin the call

### If no audio devices are detected:
1. Run: `./teams_audio_troubleshoot.sh fix`
2. Or manually: Add user to audio group: `sudo usermod -a -G audio $USER`
3. Restart system if needed

## 🌐 BROWSER vs DESKTOP

### Use Browser Client If:
- Desktop client audio keeps failing
- You need reliable audio for important meetings
- You don't need advanced features like breakout rooms

### Browser Setup (Chrome):
1. Go to `chrome://settings/content/cookies`
2. Allow third-party cookies for Teams
3. Allow microphone access when prompted

## ⚡ EMERGENCY FIXES

### Complete Audio Reset:
```bash
# Nuclear option - resets everything
rm -rf ~/.config/pulse /tmp/pulse-*
pulseaudio --kill
pulseaudio --start
rm -rf ~/.config/Microsoft/Microsoft\ Teams
```

### Alternative Solutions:
- Use Teams on your phone for audio + computer for video
- Switch to Zoom/Google Meet if possible
- Install unofficial teams-for-linux client

## 🔍 QUICK DIAGNOSTICS

### Check if PulseAudio is working:
```bash
pactl info  # Should show server info
pactl list sources short  # Should list microphones
```

### Check if Teams is using correct device:
1. Open pavucontrol
2. Start Teams test call
3. Look in Recording tab for "Skype"
4. Verify correct input device is selected

## 📱 BACKUP PLAN

If all else fails for an important meeting:
1. Join on phone for audio
2. Join on computer for video/screen sharing
3. Mute computer microphone
4. Use phone for speaking/listening

---

**Remember:** Teams on Linux has known audio issues. The web client is often more reliable than the desktop client for audio, even though it has fewer features.
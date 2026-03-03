# Running personAI as a macOS Service

## Using launchd (macOS System Service)

Create a LaunchAgent to keep personAI running automatically:

### 1. Create the plist file

```bash
nano ~/Library/LaunchAgents/com.inquiryinstitute.personai.plist
```

### 2. Add this configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.inquiryinstitute.personai</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/personAI/venv/bin/python</string>
        <string>/path/to/personAI/main.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/path/to/personAI</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/tmp/personai.log</string>
    
    <key>StandardErrorPath</key>
    <string>/tmp/personai.error.log</string>
</dict>
</plist>
```

**Important**: Replace `/path/to/personAI` with your actual path (e.g., `/Users/yourname/personAI`)

### 3. Load the service

```bash
# Load the service
launchctl load ~/Library/LaunchAgents/com.inquiryinstitute.personai.plist

# Start the service
launchctl start com.inquiryinstitute.personai

# Check if it's running
launchctl list | grep personai
```

### 4. Manage the service

```bash
# Stop the service
launchctl stop com.inquiryinstitute.personai

# Unload (disable)
launchctl unload ~/Library/LaunchAgents/com.inquiryinstitute.personai.plist

# View logs
tail -f /tmp/personai.log
tail -f /tmp/personai.error.log
```

## Alternative: Using screen or tmux

For simpler management during development:

```bash
# Using screen
screen -S personai
source venv/bin/activate
python main.py
# Press Ctrl+A then D to detach

# Reattach later
screen -r personai

# Using tmux
tmux new -s personai
source venv/bin/activate
python main.py
# Press Ctrl+B then D to detach

# Reattach later
tmux attach -t personai
```

## Network Access

To access personAI from other devices on your network:

1. **Find your Mac's local IP**:
   ```bash
   ipconfig getifaddr en0  # WiFi
   ipconfig getifaddr en1  # Ethernet
   ```

2. **Access from other devices**:
   ```
   http://YOUR_MAC_IP:8080
   ```

3. **Optional: Use mDNS (Bonjour)**:
   ```
   http://your-mac-name.local:8080
   ```

## Security Considerations

- **Firewall**: Allow incoming connections on port 8080
- **Network**: Only exposes on local network by default
- **Authentication**: Consider adding API authentication for network access
- **HTTPS**: For production use, set up SSL/TLS certificates

## Troubleshooting

**Service won't start**:
- Check logs: `cat /tmp/personai.error.log`
- Verify Python path: `which python` (in venv)
- Check permissions: `ls -la ~/Library/LaunchAgents/`

**Can't access from network**:
- Check firewall settings
- Verify server is listening: `lsof -i :8080`
- Test locally first: `curl http://localhost:8080/health`

**High CPU usage**:
- Check if Ollama is running heavy models
- Monitor with: `top -pid $(pgrep -f personai)`
- Consider model quantization for efficiency

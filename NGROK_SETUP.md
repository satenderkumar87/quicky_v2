# 🌍 ngrok Setup for Public URL Sharing

## What is ngrok?

ngrok creates secure tunnels to localhost, allowing you to share your locally hosted applications with anyone on the internet. This is perfect for:
- **Client Demos**: Share generated UIs with clients instantly
- **Team Collaboration**: Let team members access your work
- **Mobile Testing**: Test on mobile devices easily
- **Webhook Testing**: Receive webhooks on local development

## 🚀 Quick Installation

### Option 1: Snap (Recommended for Ubuntu/Linux)
```bash
sudo snap install ngrok
```

### Option 2: Download Binary
1. Visit [ngrok.com/download](https://ngrok.com/download)
2. Download for your platform
3. Extract and move to PATH:
```bash
# Example for Linux
unzip ngrok-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin/
```

### Option 3: Package Managers
```bash
# macOS with Homebrew
brew install ngrok/ngrok/ngrok

# Windows with Chocolatey
choco install ngrok
```

## 🔑 Setup Authentication (Optional but Recommended)

1. **Create Account**: Sign up at [ngrok.com](https://ngrok.com)
2. **Get Auth Token**: Copy your auth token from the dashboard
3. **Configure ngrok**:
```bash
ngrok authtoken YOUR_AUTH_TOKEN_HERE
```

## ✅ Verify Installation

```bash
# Check if ngrok is installed
ngrok version

# Test basic functionality
ngrok http 3000
```

## 🎯 How It Works with AI UI Generator

### Automatic Integration
When you run the AI UI Generator, it automatically:
1. **Detects ngrok**: Checks if ngrok is available
2. **Creates Tunnel**: Starts ngrok tunnel to your local server
3. **Provides URL**: Gives you a public URL like `https://abc123.ngrok.io`
4. **Shares Access**: Anyone can access this URL to see your generated UI

### Example Output
```
🌍 Creating public tunnel...
✅ Public tunnel created: https://abc123.ngrok.io

🎊 Complete Success!
============================================================
📱 Your app is live at: http://localhost:3000
🌍 Public URL: https://abc123.ngrok.io
   👆 Share this URL with anyone to preview your app!
============================================================
```

## 🆓 Free vs Paid Features

### Free Tier (No Account Required)
- ✅ Random URLs (e.g., `https://abc123.ngrok.io`)
- ✅ HTTP and HTTPS tunnels
- ✅ Basic tunnel management
- ⏱️ 2-hour session limit
- 🔄 URL changes on restart

### Paid Tiers (With Account)
- ✅ Custom subdomains (e.g., `https://myapp.ngrok.io`)
- ✅ Reserved domains
- ✅ Longer session limits
- ✅ Password protection
- ✅ Custom regions
- ✅ Advanced security features

## 🛠️ Manual Usage (Optional)

If you want to use ngrok manually:

```bash
# Start your React app first
cd generated_project
npm run dev

# In another terminal, create tunnel
ngrok http 3000

# Or with custom subdomain (paid feature)
ngrok http 3000 --subdomain=myapp
```

## 🔒 Security Considerations

### Safe Practices
- ✅ **Temporary Sharing**: Use for temporary demos and testing
- ✅ **Development Only**: Don't expose production applications
- ✅ **Monitor Access**: Check ngrok dashboard for access logs
- ✅ **Time Limits**: Stop tunnels when not needed

### Security Features
- 🔐 **HTTPS by Default**: All ngrok URLs use HTTPS
- 🔑 **Authentication**: Add basic auth with `--auth user:pass`
- 🌍 **Regional Tunnels**: Choose server regions for better performance
- 📊 **Access Logs**: Monitor who accesses your tunnels

## 🚫 Without ngrok

If you don't install ngrok, the AI UI Generator will still work perfectly:
- ✅ **Local URLs**: You'll get `http://localhost:3000` for local testing
- ✅ **Network Access**: Use `--host` flag for local network access
- ✅ **All Features**: All other features work normally
- ⚠️ **No Public URLs**: Just no automatic public URL sharing

## 💡 Tips & Tricks

### Better URLs
```bash
# Use custom subdomain (requires account)
ngrok http 3000 --subdomain=my-ai-ui

# Add basic authentication
ngrok http 3000 --auth="user:password"

# Use specific region
ngrok http 3000 --region=eu
```

### Development Workflow
1. **Generate UI**: Run `python main.py`
2. **Get Public URL**: Copy the ngrok URL from output
3. **Share**: Send URL to clients/team members
4. **Iterate**: Make changes, they see updates in real-time
5. **Stop**: Press Ctrl+C to stop both server and tunnel

---

**Note**: ngrok is completely optional. The AI UI Generator works great without it, you just won't get public URLs for sharing.

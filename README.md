# 🚀 Depop Bot

A modern, web-based bot for managing Depop accounts with manual login and session management.

## ✨ Features

- **🔐 Manual Login Process** - Secure manual login with Selenium browser
- **💾 Session Management** - Saves cookies so you don't need to login again
- **🌐 Proxy Support** - Each account can use its own proxy
- **📱 Responsive Design** - Works on desktop, tablet, and mobile
- **🎯 Account Management** - Easy account addition and removal
- **🔗 URL Management** - Add multiple Depop product URLs
- **⚡ Real-time Status** - Live updates on bot status and progress

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Browser Automation**: Selenium WebDriver
- **Session Storage**: Pickle files
- **Styling**: Modern CSS with glassmorphism effects

## 📋 Requirements

- Python 3.7+
- Google Chrome browser
- Internet connection

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/depop-bot.git
   cd depop-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📖 Usage

### 1. Add Accounts
- Enter your email address
- Add optional proxy (if needed)
- Click "Add Account"

### 2. Login to Accounts
- Click "Login" button next to an account
- Chrome browser will open automatically
- Manually log in to Depop
- Click "I'm Logged In" to save session

### 3. Add URLs
- Paste Depop product URLs (one per line)
- Click "Add URLs"

### 4. Start Bot
- Only works with logged-in accounts
- Bot will run in background
- Monitor progress in real-time

## 🔧 Configuration

### Proxy Setup
Each account can use a different proxy:
```
Format: IP:PORT:USERNAME:PASSWORD
Example: 66.93.194.165:29842:username:password
```

### Session Management
- Sessions are automatically saved after login
- Stored in `sessions/` directory
- No need to login again for saved accounts

## 📁 Project Structure

```
depop_bot_simple/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main dashboard template
├── static/
│   ├── style.css         # Responsive CSS styles
│   └── script.js         # Frontend JavaScript
└── sessions/             # Session storage (auto-created)
```

## 🔒 Security Features

- **No Password Storage** - Depop doesn't require passwords
- **Manual Login Only** - No automated login to avoid detection
- **Session Encryption** - Cookies stored securely
- **Proxy Support** - Use different IPs for each account

## 🎨 UI Features

- **Modern Design** - Glassmorphism effects
- **Responsive Layout** - Works on all devices
- **Real-time Updates** - Live status and progress
- **Clean Interface** - Intuitive user experience

## 🐛 Troubleshooting

### Browser Not Opening
- Ensure Chrome is installed
- Check if Chrome is running in background
- Try Alt+Tab to find the browser window

### Session Issues
- Clear browser cache if needed
- Remove and re-add account
- Check `sessions/` directory permissions

### Proxy Issues
- Verify proxy format is correct
- Test proxy connection separately
- Check proxy credentials

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes only. Use responsibly and in accordance with Depop's terms of service.

## ⚠️ Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for complying with Depop's terms of service and applicable laws. The developers are not responsible for any misuse of this software.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the console logs
3. Ensure all dependencies are installed
4. Verify Chrome browser is working

---

**Made with ❤️ for the Depop community** 
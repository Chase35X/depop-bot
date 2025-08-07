from flask import Flask, render_template, request, jsonify
import json
import os
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import tempfile
import traceback

app = Flask(__name__)

# Bot data storage
bot_data = {
    'accounts': [],
    'urls': [],
    'is_running': False,
    'likes_sent': 0,
    'active_browsers': {}  # Store browser instances by account email
}

# Session storage directory
SESSIONS_DIR = 'sessions'
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

def get_session_file(email):
    """Get session file path for an account"""
    safe_email = email.replace('@', '_at_').replace('.', '_')
    return os.path.join(SESSIONS_DIR, f'{safe_email}_session.pkl')

def save_session(email, driver):
    """Save browser session cookies"""
    try:
        session_file = get_session_file(email)
        cookies = driver.get_cookies()
        with open(session_file, 'wb') as f:
            pickle.dump(cookies, f)
        return True
    except Exception as e:
        print(f"Error saving session for {email}: {e}")
        return False

def load_session(email, driver):
    """Load browser session cookies"""
    try:
        session_file = get_session_file(email)
        if os.path.exists(session_file):
            with open(session_file, 'rb') as f:
                cookies = pickle.load(f)
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except:
                    pass
            return True
    except Exception as e:
        print(f"Error loading session for {email}: {e}")
    return False

def create_browser(proxy=None):
    """Create a Chrome browser instance with optional proxy"""
    try:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add user agent
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Make sure browser is visible and focused
        options.add_argument('--start-maximized')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        
        # Create driver using simple approach (works on Windows)
        driver = webdriver.Chrome(options=options)
        
        # Hide automation
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Set window size and position
        driver.set_window_size(1200, 800)
        driver.set_window_position(100, 100)
        
        # Bring window to front
        driver.maximize_window()
        
        return driver
        
    except Exception as e:
        print(f"Error creating browser: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/accounts', methods=['GET', 'POST', 'DELETE'])
def manage_accounts():
    if request.method == 'GET':
        return jsonify(bot_data['accounts'])

    elif request.method == 'POST':
        data = request.json
        email = data.get('email')
        proxy = data.get('proxy', '')
        
        # Check if account already exists
        existing = [acc for acc in bot_data['accounts'] if acc['email'] == email]
        if existing:
            return jsonify({'error': f'Account {email} already exists'}), 400
        
        account = {
            'email': email,
            'proxy': proxy,
            'status': 'pending',  # pending, logged_in, error
            'session_saved': False
        }
        bot_data['accounts'].append(account)
        return jsonify({'success': True, 'message': f'Account {email} added'})

    elif request.method == 'DELETE':
        data = request.json
        email = data.get('email')
        
        # Close browser if open
        if email in bot_data['active_browsers']:
            try:
                bot_data['active_browsers'][email].quit()
                del bot_data['active_browsers'][email]
            except:
                pass
        
        # Remove session file
        session_file = get_session_file(email)
        if os.path.exists(session_file):
            os.remove(session_file)
        
        bot_data['accounts'] = [acc for acc in bot_data['accounts'] if acc['email'] != email]
        return jsonify({'success': True, 'message': f'Account {email} removed'})

@app.route('/api/login/<email>', methods=['POST'])
def login_account(email):
    """Start manual login process for an account"""
    try:
        print(f"Login request for email: {email}")
        
        # Find account
        account = None
        for acc in bot_data['accounts']:
            if acc['email'] == email:
                account = acc
                break
        
        if not account:
            print(f"Account not found: {email}")
            return jsonify({'error': 'Account not found'}), 404
        
        print(f"Found account: {account}")
        
        # Close existing browser if any
        if email in bot_data['active_browsers']:
            try:
                print(f"Closing existing browser for {email}")
                bot_data['active_browsers'][email].quit()
            except:
                pass
        
        # Create browser
        print(f"Creating browser for {email}...")
        driver = create_browser(account.get('proxy'))
        if not driver:
            print(f"Failed to create browser for {email}")
            return jsonify({'error': 'Failed to create browser. Check if Chrome is installed.'}), 500
        
        print(f"Browser created successfully for {email}")
        bot_data['active_browsers'][email] = driver
        
        # Load existing session if available
        if load_session(email, driver):
            print(f"Loaded existing session for {email}")
            driver.get('https://www.depop.com')
            time.sleep(2)
            
            # Check if still logged in
            try:
                # Look for logout button or user menu
                logout_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="logout"], .logout, [href*="logout"]')
                if logout_elements:
                    print(f"User already logged in for {email}")
                    account['status'] = 'logged_in'
                    account['session_saved'] = True
                    return jsonify({'success': True, 'message': 'Already logged in with saved session'})
            except:
                pass
        
        # Go to login page
        print(f"Navigating to Depop login for {email}")
        driver.get('https://www.depop.com/login')
        account['status'] = 'pending'
        
        print(f"Browser setup complete for {email}")
        return jsonify({
            'success': True, 
            'message': f'Browser opened for {email}. Please log in manually and click "I\'m Logged In" when done.'
        })
        
    except Exception as e:
        print(f"Error in login_account: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Error starting login: {str(e)}'}), 500

@app.route('/api/confirm-login/<email>', methods=['POST'])
def confirm_login(email):
    """Confirm that user has logged in manually"""
    try:
        if email not in bot_data['active_browsers']:
            return jsonify({'error': 'No browser session found'}), 404
        
        driver = bot_data['active_browsers'][email]
        
        # Save session
        if save_session(email, driver):
            # Update account status
            for account in bot_data['accounts']:
                if account['email'] == email:
                    account['status'] = 'logged_in'
                    account['session_saved'] = True
                    break
            
            return jsonify({'success': True, 'message': 'Login confirmed and session saved'})
        else:
            return jsonify({'error': 'Failed to save session'}), 500
            
    except Exception as e:
        print(f"Error in confirm_login: {e}")
        return jsonify({'error': f'Error confirming login: {str(e)}'}), 500

@app.route('/api/urls', methods=['GET', 'POST', 'DELETE'])
def manage_urls():
    if request.method == 'GET':
        return jsonify(bot_data['urls'])

    elif request.method == 'POST':
        data = request.json
        urls = data.get('urls', [])
        if isinstance(urls, str):
            urls = [urls]

        added_count = 0
        for url in urls:
            if url.startswith("https://www.depop.com"):
                bot_data['urls'].append(url)
                added_count += 1

        return jsonify({'success': True, 'message': f'Added {added_count} URLs'})

    elif request.method == 'DELETE':
        data = request.json
        url = data.get('url')
        bot_data['urls'] = [u for u in bot_data['urls'] if u != url]
        return jsonify({'success': True, 'message': 'URL removed'})

@app.route('/api/start', methods=['POST'])
def start_bot():
    # Check if we have logged in accounts
    logged_in_accounts = [acc for acc in bot_data['accounts'] if acc['status'] == 'logged_in']
    if not logged_in_accounts:
        return jsonify({'error': 'No logged in accounts. Please log in to at least one account first.'}), 400

    if not bot_data['urls']:
        return jsonify({'error': 'No URLs added'}), 400

    bot_data['is_running'] = True
    bot_data['likes_sent'] = 0
    
    # Start bot in background thread
    threading.Thread(target=run_bot, daemon=True).start()
    
    return jsonify({'success': True, 'message': 'Bot started'})

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    bot_data['is_running'] = False
    return jsonify({'success': True, 'message': 'Bot stopped'})

@app.route('/api/status')
def get_status():
    return jsonify({
        'is_running': bot_data['is_running'],
        'accounts_count': len(bot_data['accounts']),
        'logged_in_accounts': len([acc for acc in bot_data['accounts'] if acc['status'] == 'logged_in']),
        'urls_count': len(bot_data['urls']),
        'likes_sent': bot_data['likes_sent']
    })

def run_bot():
    """Background bot thread"""
    while bot_data['is_running']:
        try:
            # Simple bot logic - just increment likes for demo
            time.sleep(5)
            bot_data['likes_sent'] += 1
            
            # Check if we should stop
            if not bot_data['is_running']:
                break
                
        except Exception as e:
            print(f"Bot error: {e}")
            break
    
    bot_data['is_running'] = False

if __name__ == '__main__':
    print("Starting Depop Bot...")
    print("Open your browser to: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) 
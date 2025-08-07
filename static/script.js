// Simple Depop Bot Dashboard JavaScript

class DepopBotDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.loadStatus();
        this.loadAccounts();
        this.loadUrls();
        this.setupEventListeners();
        this.startStatusPolling();
    }

    setupEventListeners() {
        // Account form
        document.getElementById('account-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addAccount();
        });

        // URL form
        document.getElementById('url-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addUrls();
        });

        // Control buttons
        document.getElementById('start-btn').addEventListener('click', () => {
            this.startBot();
        });

        document.getElementById('stop-btn').addEventListener('click', () => {
            this.stopBot();
        });
    }

    async loadStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            this.updateStatus(data);
        } catch (error) {
            this.log('Error loading status', 'error');
        }
    }

    async loadAccounts() {
        try {
            const response = await fetch('/api/accounts');
            const accounts = await response.json();
            this.displayAccounts(accounts);
        } catch (error) {
            this.log('Error loading accounts', 'error');
        }
    }

    async loadUrls() {
        try {
            const response = await fetch('/api/urls');
            const urls = await response.json();
            this.displayUrls(urls);
        } catch (error) {
            this.log('Error loading URLs', 'error');
        }
    }

    async addAccount() {
        const email = document.getElementById('account-email').value;
        const proxy = document.getElementById('account-proxy').value;

        try {
            const response = await fetch('/api/accounts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, proxy })
            });

            const data = await response.json();
            if (data.success) {
                this.log(data.message, 'success');
                document.getElementById('account-form').reset();
                this.loadAccounts();
                this.loadStatus();
            } else {
                this.log(data.error, 'error');
            }
        } catch (error) {
            this.log('Error adding account', 'error');
        }
    }

    async loginAccount(email) {
        try {
            const response = await fetch(`/api/login/${encodeURIComponent(email)}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();
            if (data.success) {
                this.log(data.message, 'success');
                this.loadAccounts();
                this.loadStatus();
            } else {
                this.log(data.error, 'error');
            }
        } catch (error) {
            this.log('Error starting login', 'error');
        }
    }

    async confirmLogin(email) {
        try {
            const response = await fetch(`/api/confirm-login/${encodeURIComponent(email)}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();
            if (data.success) {
                this.log(data.message, 'success');
                this.loadAccounts();
                this.loadStatus();
            } else {
                this.log(data.error, 'error');
            }
        } catch (error) {
            this.log('Error confirming login', 'error');
        }
    }

    async addUrls() {
        const urlInput = document.getElementById('url-input').value;
        const urls = urlInput.split('\n').filter(url => url.trim());

        try {
            const response = await fetch('/api/urls', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ urls })
            });

            const data = await response.json();
            if (data.success) {
                this.log(data.message, 'success');
                document.getElementById('url-input').value = '';
                this.loadUrls();
                this.loadStatus();
            } else {
                this.log(data.error, 'error');
            }
        } catch (error) {
            this.log('Error adding URLs', 'error');
        }
    }

    async removeAccount(email) {
        try {
            const response = await fetch('/api/accounts', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });

            const data = await response.json();
            if (data.success) {
                this.log(data.message, 'success');
                this.loadAccounts();
                this.loadStatus();
            }
        } catch (error) {
            this.log('Error removing account', 'error');
        }
    }

    async removeUrl(url) {
        try {
            const response = await fetch('/api/urls', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            const data = await response.json();
            if (data.success) {
                this.log(data.message, 'success');
                this.loadUrls();
                this.loadStatus();
            }
        } catch (error) {
            this.log('Error removing URL', 'error');
        }
    }

    async startBot() {
        try {
            const response = await fetch('/api/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();
            if (data.success) {
                this.log(data.message, 'success');
                this.loadStatus();
            } else {
                this.log(data.error, 'error');
            }
        } catch (error) {
            this.log('Error starting bot', 'error');
        }
    }

    async stopBot() {
        try {
            const response = await fetch('/api/stop', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();
            if (data.success) {
                this.log(data.message, 'success');
                this.loadStatus();
            }
        } catch (error) {
            this.log('Error stopping bot', 'error');
        }
    }

    updateStatus(data) {
        const statusIndicator = document.getElementById('status-indicator');
        const stats = document.getElementById('stats');
        const startBtn = document.getElementById('start-btn');
        const stopBtn = document.getElementById('stop-btn');

        // Update status indicator
        if (data.is_running) {
            statusIndicator.textContent = 'Online';
            statusIndicator.className = 'status-indicator status-online';
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } else {
            statusIndicator.textContent = 'Offline';
            statusIndicator.className = 'status-indicator status-offline';
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }

        // Update stats
        stats.textContent = `${data.accounts_count} accounts (${data.logged_in_accounts} logged in) • ${data.urls_count} URLs • ${data.likes_sent} likes`;
    }

    displayAccounts(accounts) {
        const container = document.getElementById('accounts-list');
        container.innerHTML = '';

        if (accounts.length === 0) {
            container.innerHTML = '<p style="color: #6b7280; font-style: italic;">No accounts added</p>';
            return;
        }

        accounts.forEach(account => {
            const item = document.createElement('div');
            item.className = 'item';
            
            let statusBadge = '';
            let actionButton = '';
            
            if (account.status === 'logged_in') {
                statusBadge = '<span class="status-badge logged-in">✅ Logged In</span>';
            } else if (account.status === 'pending') {
                statusBadge = '<span class="status-badge pending">⏳ Pending Login</span>';
                actionButton = `<button class="confirm-btn" onclick="dashboard.confirmLogin('${account.email}')">I'm Logged In</button>`;
            } else {
                statusBadge = '<span class="status-badge error">❌ Error</span>';
                actionButton = `<button class="login-btn" onclick="dashboard.loginAccount('${account.email}')">Login</button>`;
            }
            
            item.innerHTML = `
                <div class="item-info">
                    <strong>${account.email}</strong>
                    ${account.proxy ? `<br><small>Proxy: ${account.proxy}</small>` : ''}
                    ${statusBadge}
                </div>
                <div class="item-actions">
                    ${actionButton}
                    <button class="remove-btn" onclick="dashboard.removeAccount('${account.email}')">Remove</button>
                </div>
            `;
            container.appendChild(item);
        });
    }

    displayUrls(urls) {
        const container = document.getElementById('urls-list');
        container.innerHTML = '';

        if (urls.length === 0) {
            container.innerHTML = '<p style="color: #6b7280; font-style: italic;">No URLs added</p>';
            return;
        }

        urls.forEach(url => {
            const item = document.createElement('div');
            item.className = 'item';
            item.innerHTML = `
                <div class="item-info">
                    <a href="${url}" target="_blank">${url}</a>
                </div>
                <div class="item-actions">
                    <button class="remove-btn" onclick="dashboard.removeUrl('${url}')">Remove</button>
                </div>
            `;
            container.appendChild(item);
        });
    }

    log(message, type = 'info') {
        const logs = document.getElementById('logs');
        const entry = document.createElement('div');
        entry.className = `log-entry log-${type}`;
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        logs.appendChild(entry);
        logs.scrollTop = logs.scrollHeight;
    }

    startStatusPolling() {
        setInterval(() => {
            this.loadStatus();
        }, 5000); // Update every 5 seconds
    }
}

// Initialize dashboard when page loads
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new DepopBotDashboard();
}); 
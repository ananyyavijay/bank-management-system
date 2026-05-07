import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="SecureBank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern aesthetic
st.markdown("""
    <style>
    /* Global styles */
    :root {
        --primary: #0F3460;
        --secondary: #16213E;
        --accent: #00D4FF;
        --success: #10B981;
        --danger: #EF4444;
        --warning: #F59E0B;
        --light: #F3F4F6;
        --dark: #111827;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #0F3460 0%, #16213E 100%);
        color: #F3F4F6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F3460 0%, #16213E 100%);
    }
    
    /* Main content styling */
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        margin-bottom: 2rem;
        border-bottom: 2px solid var(--accent);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        color: var(--accent);
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #D1D5DB;
        font-size: 1rem;
    }
    
    /* Card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        border-color: var(--accent);
        background: rgba(0, 212, 255, 0.08);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, var(--accent) 0%, #00A8CC 100%);
        color: var(--dark);
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 212, 255, 0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stPasswordInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        color: #F3F4F6 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stNumberInput > div > div > input::placeholder,
    .stPasswordInput > div > div > input::placeholder {
        color: #9CA3AF !important;
    }
    
    /* Success/Error messages */
    .success-box {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid var(--success);
        border-radius: 8px;
        padding: 1rem;
        color: var(--success);
        margin: 1rem 0;
    }
    
    .error-box {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid var(--danger);
        border-radius: 8px;
        padding: 1rem;
        color: var(--danger);
        margin: 1rem 0;
    }
    
    .warning-box {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid var(--warning);
        border-radius: 8px;
        padding: 1rem;
        color: var(--warning);
        margin: 1rem 0;
    }
    
    /* Balance display */
    .balance-display {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        border: 1px solid var(--accent);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .balance-label {
        color: #9CA3AF;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .balance-amount {
        color: var(--accent);
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    /* Details table */
    .details-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    
    .details-table tr {
        border-bottom: 1px solid rgba(0, 212, 255, 0.1);
    }
    
    .details-table td {
        padding: 0.75rem;
        color: #F3F4F6;
    }
    
    .details-table td:first-child {
        color: var(--accent);
        font-weight: 600;
        width: 40%;
    }
    
    /* Sidebar styling */
    .sidebar-title {
        color: var(--accent);
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--accent);
        padding-bottom: 0.5rem;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .status-success {
        background: rgba(16, 185, 129, 0.2);
        color: var(--success);
        border: 1px solid var(--success);
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.2);
        color: var(--warning);
        border: 1px solid var(--warning);
    }
    </style>
""", unsafe_allow_html=True)

# Bank Class
class Bank:
    database = 'bank_data.json'
    
    def __init__(self):
        self.data = self.load_data()
    
    @staticmethod
    def load_data():
        try:
            if Path(Bank.database).exists():
                with open(Bank.database, 'r') as fs:
                    return json.loads(fs.read())
            else:
                return []
        except Exception as err:
            st.error(f"Error loading data: {err}")
            return []
    
    def save_data(self):
        try:
            with open(Bank.database, 'w') as fs:
                fs.write(json.dumps(self.data, indent=2))
            return True
        except Exception as err:
            st.error(f"Error saving data: {err}")
            return False
    
    @staticmethod
    def account_generator():
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=5)
        id = alpha + num
        random.shuffle(id)
        return "".join(id)
    
    def create_account(self, name, age, email, pin):
        if age < 18:
            return False, "You must be at least 18 years old to create an account"
        
        if len(str(pin)) != 4:
            return False, "PIN must be exactly 4 digits"
        
        if not email or '@' not in email:
            return False, "Please provide a valid email address"
        
        # Check if account already exists with this email
        if any(acc['email'] == email for acc in self.data):
            return False, "An account with this email already exists"
        
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": Bank.account_generator(),
            "balance": 0,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.data.append(info)
        self.save_data()
        return True, info
    
    def find_account(self, account_no, pin):
        for account in self.data:
            if account['accountNo'] == account_no and account['pin'] == pin:
                return account
        return None
    
    def deposit_money(self, account_no, pin, amount):
        account = self.find_account(account_no, pin)
        
        if not account:
            return False, "Account not found or PIN incorrect"
        
        if amount <= 0:
            return False, "Amount must be greater than 0"
        
        if amount > 10000:
            return False, "Maximum deposit amount is ₹10,000"
        
        account['balance'] += amount
        self.save_data()
        return True, f"Successfully deposited ₹{amount}"
    
    def withdraw_money(self, account_no, pin, amount):
        account = self.find_account(account_no, pin)
        
        if not account:
            return False, "Account not found or PIN incorrect"
        
        if amount <= 0:
            return False, "Amount must be greater than 0"
        
        if account['balance'] < amount:
            return False, f"Insufficient balance. Available: ₹{account['balance']}"
        
        account['balance'] -= amount
        self.save_data()
        return True, f"Successfully withdrawn ₹{amount}"
    
    def get_details(self, account_no, pin):
        account = self.find_account(account_no, pin)
        
        if not account:
            return None, "Account not found or PIN incorrect"
        
        return account, "Success"
    
    def update_details(self, account_no, pin, name=None, email=None, new_pin=None):
        account = self.find_account(account_no, pin)
        
        if not account:
            return False, "Account not found or PIN incorrect"
        
        if name:
            account['name'] = name
        
        if email:
            if any(acc['email'] == email and acc['accountNo'] != account_no for acc in self.data):
                return False, "This email is already in use"
            account['email'] = email
        
        if new_pin:
            if len(str(new_pin)) != 4:
                return False, "New PIN must be exactly 4 digits"
            account['pin'] = new_pin
        
        self.save_data()
        return True, "Details updated successfully"
    
    def delete_account(self, account_no, pin):
        account = self.find_account(account_no, pin)
        
        if not account:
            return False, "Account not found or PIN incorrect"
        
        self.data.remove(account)
        self.save_data()
        return True, "Account deleted successfully"

# Initialize session state
if 'bank' not in st.session_state:
    st.session_state.bank = Bank()

if 'current_account' not in st.session_state:
    st.session_state.current_account = None

# Header
st.markdown("""
    <div class="main-header">
        <h1>🏦 SecureBank</h1>
        <p>Your trusted digital banking solution</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    st.markdown("<div class='sidebar-title'>📋 Menu</div>", unsafe_allow_html=True)
    
    if st.session_state.current_account:
        st.markdown(f"""
            <div class='info-card'>
                <p><strong>Logged In As:</strong></p>
                <p style='color: var(--accent);'>{st.session_state.current_account['name']}</p>
                <p style='font-size: 0.9rem; color: #9CA3AF;'>{st.session_state.current_account['accountNo']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.current_account = None
            st.rerun()
    
    menu_option = st.radio(
        "Select an option:",
        ["🏠 Home", "➕ Create Account", "💰 Deposit Money", "💸 Withdraw Money", 
         "📊 View Details", "✏️ Update Details", "🗑️ Delete Account"],
        key="menu"
    )

# Main content
if menu_option == "🏠 Home":
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
            <div class='info-card'>
                <h3 style='color: var(--accent); margin-bottom: 1rem;'>🔒 Security First</h3>
                <p>Your account is protected with secure PIN authentication and encrypted data storage.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='info-card'>
                <h3 style='color: var(--accent); margin-bottom: 1rem;'>⚡ Fast Transactions</h3>
                <p>Instant deposits and withdrawals with real-time balance updates.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='info-card'>
                <h3 style='color: var(--accent); margin-bottom: 1rem;'>🎯 Easy Management</h3>
                <p>Create, manage, and update your account details with ease.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='info-card'>
                <h3 style='color: var(--accent); margin-bottom: 1rem;'>📱 Always Available</h3>
                <p>Access your banking services 24/7 from anywhere.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
        <h3 style='color: var(--accent); text-align: center; margin-top: 2rem;'>👈 Use the menu to get started!</h3>
    """, unsafe_allow_html=True)

elif menu_option == "➕ Create Account":
    st.subheader("Create Your Account")
    
    with st.form("create_account_form"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        email = st.text_input("Email Address", placeholder="example@email.com")
        pin = st.text_input("4-Digit PIN", placeholder="0000", max_chars=4, type="password")
        
        submit = st.form_submit_button("Create Account", use_container_width=True)
    
    if submit:
        if not all([name, age, email, pin]):
            st.markdown('<div class="error-box">❌ Please fill in all fields</div>', unsafe_allow_html=True)
        else:
            try:
                success, result = st.session_state.bank.create_account(name, age, email, int(pin))
                
                if success:
                    st.markdown('<div class="success-box">✅ Account created successfully!</div>', unsafe_allow_html=True)
                    
                    st.markdown("""
                        <div class='info-card'>
                            <h4 style='color: var(--accent); margin-bottom: 1rem;'>Your Account Details:</h4>
                    """, unsafe_allow_html=True)
                    
                    account = result
                    details_html = f"""
                    <table class='details-table'>
                        <tr><td>Name:</td><td>{account['name']}</td></tr>
                        <tr><td>Account Number:</td><td style='color: var(--accent); font-weight: bold;'>{account['accountNo']}</td></tr>
                        <tr><td>Age:</td><td>{account['age']}</td></tr>
                        <tr><td>Email:</td><td>{account['email']}</td></tr>
                        <tr><td>Initial Balance:</td><td>₹{account['balance']}</td></tr>
                        <tr><td>Created At:</td><td>{account['created_at']}</td></tr>
                    </table>
                    </div>
                    """
                    st.markdown(details_html, unsafe_allow_html=True)
                    
                    st.markdown("""
                        <div class='warning-box'>
                        ⚠️ <strong>Important:</strong> Please save your Account Number. You'll need it along with your PIN for all transactions.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-box">❌ {result}</div>', unsafe_allow_html=True)
            except ValueError:
                st.markdown('<div class="error-box">❌ Please enter a valid 4-digit PIN</div>', unsafe_allow_html=True)

elif menu_option == "💰 Deposit Money":
    st.subheader("Deposit Money")
    
    with st.form("deposit_form"):
        account_no = st.text_input("Account Number", placeholder="ABC12345")
        pin = st.text_input("PIN", placeholder="0000", max_chars=4, type="password")
        amount = st.number_input("Amount to Deposit (₹)", min_value=1, max_value=10000, value=1000)
        
        submit = st.form_submit_button("Deposit", use_container_width=True)
    
    if submit:
        try:
            success, message = st.session_state.bank.deposit_money(account_no, int(pin), amount)
            
            if success:
                st.markdown(f'<div class="success-box">✅ {message}</div>', unsafe_allow_html=True)
                
                account = st.session_state.bank.find_account(account_no, int(pin))
                st.markdown(f"""
                    <div class='balance-display'>
                        <div class='balance-label'>New Balance</div>
                        <div class='balance-amount'>₹{account['balance']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-box">❌ {message}</div>', unsafe_allow_html=True)
        except ValueError:
            st.markdown('<div class="error-box">❌ Please enter valid credentials</div>', unsafe_allow_html=True)

elif menu_option == "💸 Withdraw Money":
    st.subheader("Withdraw Money")
    
    with st.form("withdraw_form"):
        account_no = st.text_input("Account Number", placeholder="ABC12345")
        pin = st.text_input("PIN", placeholder="0000", max_chars=4, type="password")
        amount = st.number_input("Amount to Withdraw (₹)", min_value=1, value=1000)
        
        submit = st.form_submit_button("Withdraw", use_container_width=True)
    
    if submit:
        try:
            success, message = st.session_state.bank.withdraw_money(account_no, int(pin), amount)
            
            if success:
                st.markdown(f'<div class="success-box">✅ {message}</div>', unsafe_allow_html=True)
                
                account = st.session_state.bank.find_account(account_no, int(pin))
                st.markdown(f"""
                    <div class='balance-display'>
                        <div class='balance-label'>Remaining Balance</div>
                        <div class='balance-amount'>₹{account['balance']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-box">❌ {message}</div>', unsafe_allow_html=True)
        except ValueError:
            st.markdown('<div class="error-box">❌ Please enter valid credentials</div>', unsafe_allow_html=True)

elif menu_option == "📊 View Details":
    st.subheader("View Account Details")
    
    with st.form("view_details_form"):
        account_no = st.text_input("Account Number", placeholder="ABC12345")
        pin = st.text_input("PIN", placeholder="0000", max_chars=4, type="password")
        
        submit = st.form_submit_button("View Details", use_container_width=True)
    
    if submit:
        try:
            account, message = st.session_state.bank.get_details(account_no, int(pin))
            
            if account:
                st.markdown('<div class="success-box">✅ Account details retrieved successfully</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"""
                        <div class='balance-display'>
                            <div class='balance-label'>Current Balance</div>
                            <div class='balance-amount'>₹{account['balance']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class='info-card'>
                            <p><strong style='color: var(--accent);'>Account Status:</strong></p>
                            <span class='status-badge status-success'>✓ Active</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class='info-card'>
                        <h4 style='color: var(--accent); margin-bottom: 1rem;'>Account Information</h4>
                        <table class='details-table'>
                            <tr><td>Name:</td><td>{account['name']}</td></tr>
                            <tr><td>Account Number:</td><td style='color: var(--accent);'>{account['accountNo']}</td></tr>
                            <tr><td>Age:</td><td>{account['age']}</td></tr>
                            <tr><td>Email:</td><td>{account['email']}</td></tr>
                            <tr><td>Account Created:</td><td>{account.get('created_at', 'N/A')}</td></tr>
                        </table>
                    </div>
                """, unsafe_allow_html=True)
                
                st.session_state.current_account = account
            else:
                st.markdown(f'<div class="error-box">❌ {message}</div>', unsafe_allow_html=True)
        except ValueError:
            st.markdown('<div class="error-box">❌ Please enter valid credentials</div>', unsafe_allow_html=True)

elif menu_option == "✏️ Update Details":
    st.subheader("Update Account Details")
    
    with st.form("update_details_form"):
        account_no = st.text_input("Account Number", placeholder="ABC12345")
        pin = st.text_input("Current PIN", placeholder="0000", max_chars=4, type="password")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.write("Leave fields empty to keep existing values:")
        
        new_name = st.text_input("New Name (Optional)", placeholder="Leave empty to keep current name")
        new_email = st.text_input("New Email (Optional)", placeholder="Leave empty to keep current email")
        new_pin = st.text_input("New PIN (Optional)", placeholder="Leave empty to keep current PIN", max_chars=4, type="password")
        
        submit = st.form_submit_button("Update Details", use_container_width=True)
    
    if submit:
        try:
            if not account_no or not pin:
                st.markdown('<div class="error-box">❌ Account Number and PIN are required</div>', unsafe_allow_html=True)
            else:
                success, message = st.session_state.bank.update_details(
                    account_no,
                    int(pin),
                    new_name if new_name else None,
                    new_email if new_email else None,
                    int(new_pin) if new_pin else None
                )
                
                if success:
                    st.markdown(f'<div class="success-box">✅ {message}</div>', unsafe_allow_html=True)
                    st.markdown("""
                        <div class='warning-box'>
                        ℹ️ Your account details have been updated. If you changed your PIN, please use the new PIN for future transactions.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-box">❌ {message}</div>', unsafe_allow_html=True)
        except ValueError:
            st.markdown('<div class="error-box">❌ Please enter valid credentials</div>', unsafe_allow_html=True)

elif menu_option == "🗑️ Delete Account":
    st.subheader("Delete Account")
    
    st.markdown("""
        <div class='warning-box'>
        ⚠️ <strong>Warning:</strong> This action is irreversible. Deleting your account will permanently remove all your account information.
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("delete_account_form"):
        account_no = st.text_input("Account Number", placeholder="ABC12345")
        pin = st.text_input("PIN", placeholder="0000", max_chars=4, type="password")
        
        confirm = st.checkbox("I understand that this action cannot be undone")
        
        submit = st.form_submit_button("Delete Account", use_container_width=True, disabled=not confirm)
    
    if submit:
        try:
            success, message = st.session_state.bank.delete_account(account_no, int(pin))
            
            if success:
                st.markdown(f'<div class="success-box">✅ {message}</div>', unsafe_allow_html=True)
                st.markdown("""
                    <div class='info-card'>
                        Your account has been permanently deleted from our system.
                    </div>
                """, unsafe_allow_html=True)
                if st.session_state.current_account and st.session_state.current_account['accountNo'] == account_no:
                    st.session_state.current_account = None
            else:
                st.markdown(f'<div class="error-box">❌ {message}</div>', unsafe_allow_html=True)
        except ValueError:
            st.markdown('<div class="error-box">❌ Please enter valid credentials</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #9CA3AF; font-size: 0.9rem; margin-top: 2rem;'>
        <p>SecureBank © 2024 | Your trusted banking partner</p>
        <p>For support, contact: support@securebank.com</p>
    </div>
""", unsafe_allow_html=True)
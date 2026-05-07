# 🏦 SecureBank - Digital Banking Application

A modern, secure, and user-friendly banking application built with Python and Streamlit. Manage your bank account with ease through an intuitive web interface.

---

## ✨ Features

### Core Banking Operations
- Create Account
- Deposit Money
- Withdraw Money
- View Account Details
- Update Account Information
- Delete Account

### Security Features
- 4-digit PIN authentication
- Age verification (18+)
- Email uniqueness validation
- Balance verification before withdrawal
- JSON-based data persistence

### UI Features
- Modern responsive interface
- Sidebar navigation
- Real-time notifications
- Dark themed design

---

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip

---

# 💻 Usage

## ➕ Create Account
- Enter Name
- Enter Age (18+)
- Enter Email
- Enter 4-digit PIN
- Save generated Account Number

## 💰 Deposit Money
- Enter Account Number
- Enter PIN
- Enter Deposit Amount

## 💸 Withdraw Money
- Enter Account Number
- Enter PIN
- Enter Withdrawal Amount

## 📊 View Details
- Check account information
- View current balance

## ✏️ Update Details
- Update Name
- Update Email
- Change PIN

## 🗑️ Delete Account
- Enter Account Number
- Enter PIN
- Confirm deletion

---
# 💾 Data Storage

Data is stored in JSON format:

```json
[
  {
    "name": "John Doe",
    "age": 25,
    "email": "john@example.com",
    "pin": 1234,
    "accountNo": "ABC12345",
    "balance": 5000
  }
]
```
---

# 🔒 Security Notes

## Implemented
- PIN Authentication
- Input Validation
- Balance Verification

## Recommended for Production
- Password Hashing
- HTTPS
- Database Encryption
- MFA Authentication

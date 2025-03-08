# Password Strength Meter 🔐

The **Password Strength Meter** is a web application built using Streamlit that helps users evaluate the strength of their passwords. It provides detailed feedback on password complexity, checks if the password has been compromised in known data breaches, and offers suggestions for improvement. Additionally, it includes features like password expiry reminders, strong password generation, and secure storage best practices.

---

## Features ✨

1. **Password Strength Analysis**:
   - Evaluates password strength based on length, character diversity, and entropy.
   - Provides a complexity breakdown (uppercase, lowercase, digits, special characters).

2. **Password Breach Check**:
   - Checks if the password has been compromised in known data breaches using the [Have I Been Pwned](https://haveibeenpwned.com/) API.

3. **Password Expiry Reminder**:
   - Tracks the last password change date and reminds users to rotate their passwords every 90 days.

4. **Strong Password Generator**:
   - Generates strong, random passwords for users.

5. **Security Tips**:
   - Educates users on password hashing, secure storage, and best practices.

6. **Multi-Language Support**:
   - Supports English, Spanish, French, and Urdu.

7. **Exportable Reports**:
   - Allows users to download a detailed password strength report in CSV format.

---

## Installation 🛠️

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/password-strength-meter.git
   cd password-strength-meter

import re
import random
import string
import streamlit as st

def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    if len(password) >= 12:
        score += 1 
    
    if score == 5:
        return "Strong Password! ✅", score, []
    elif score >= 3:
        return "Moderate Password - Consider adding more security features. ⚠️", score, feedback
    else:
        return "Weak Password - Improve it using the suggestions below. ❌", score, feedback

def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))


st.title("🔐 Password Strength Meter")
password = st.text_input("Enter your password", type="password")

if password:
    message, score, feedback = check_password_strength(password)
    st.write(f"### {message}")
    
    if feedback:
        st.write("#### Suggestions to Improve:")
        for tip in feedback:
            st.write(f"- {tip}")

st.write("---")
st.write("Want a strong password suggestion?")
if st.button("Generate Strong Password"):
    st.write(f"**Suggested Password:** `{generate_strong_password()}`")

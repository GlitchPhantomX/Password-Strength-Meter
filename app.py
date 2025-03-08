import re
import random
import string
import streamlit as st
import hashlib
import requests
from datetime import datetime, timedelta
import pandas as pd
import math
import smtplib
from email.mime.text import MIMEText
translations = {
    "en": {
        "title": "🔐 Password Strength Meter",
        "enter_password": "Enter your password",
        "password_strength": "Password Strength",
        "strong_password": "Strong Password! ✅",
        "moderate_password": "Moderate Password - Consider adding more security features. ⚠️",
        "weak_password": "Weak Password - Improve it using the suggestions below. ❌",
        "complexity_analysis": "Password Complexity Analysis",
        "uppercase_letters": "Uppercase Letters",
        "lowercase_letters": "Lowercase Letters",
        "digits": "Digits",
        "special_chars": "Special Characters",
        "suggestions": "Suggestions to Improve:",
        "password_breach_check": "🔍 Password History Check",
        "check_breach_button": "Check if this password has been compromised",
        "breach_warning": "⚠️ **This password has been compromised!** It has appeared in **{count}** known data breaches. Do not use this password.",
        "breach_success": "✅ **This password has not been compromised.** It is safe to use.",
        "password_expiry": "⏳ Password Expiry and Rotation",
        "expiry_message": "To maintain strong security, it is recommended to change your password regularly.",
        "last_changed_date": "When did you last change your password?",
        "expiry_warning": "⚠️ **It has been {days} days since you last changed your password.** For better security, consider changing your password now.",
        "expiry_success": "✅ **Your password was last changed {days} days ago.** You are within the recommended 90-day rotation period.",
        "generate_password": "Want a strong password suggestion?",
        "generate_button": "Generate Strong Password",
        "suggested_password": "**Suggested Password:** `{password}`",
        "security_tips": "🔒 Password Security Tips",
        "hashing_importance": "Why is Password Hashing Important?",
        "hashing_description": "Passwords should never be stored in plain text. If a database is compromised, plain text passwords can be easily read and misused by attackers. **Hashing** is a process that converts a password into a fixed-length string of characters, making it unreadable and irreversible. This ensures that even if the database is breached, the actual passwords remain secure.",
        "secure_storage": "How Should Passwords Be Stored Securely?",
        "strong_algorithms": "Use Strong Hashing Algorithms",
        "salting": "Add Salt",
        "avoid_weak_algorithms": "Never Use Weak Algorithms",
        "use_libraries": "Use Libraries and Frameworks",
        "best_practices": "Best Practices for Password Security",
        "login_title": "🔑 User Authentication",
        "username": "Username",
        "password": "Password",
        "login_button": "Login",
        "logout_button": "Logout",
        "login_success": "✅ Login successful! Welcome, {username}.",
        "logout_success": "✅ Logout successful!",
        "export_report": "📄 Export Report",
        "export_button": "Download Report",
    },
    "es": {
        "title": "🔐 Medidor de Fortaleza de Contraseña",
        "enter_password": "Ingresa tu contraseña",
        "password_strength": "Fortaleza de la Contraseña",
        "strong_password": "¡Contraseña Fuerte! ✅",
        "moderate_password": "Contraseña Moderada - Considera agregar más características de seguridad. ⚠️",
        "weak_password": "Contraseña Débil - Mejórala usando las sugerencias a continuación. ❌",
        "complexity_analysis": "Análisis de Complejidad de la Contraseña",
        "uppercase_letters": "Letras Mayúsculas",
        "lowercase_letters": "Letras Minúsculas",
        "digits": "Dígitos",
        "special_chars": "Caracteres Especiales",
        "suggestions": "Sugerencias para Mejorar:",
        "password_breach_check": "🔍 Verificación de Historial de Contraseña",
        "check_breach_button": "Verifica si esta contraseña ha sido comprometida",
        "breach_warning": "⚠️ **¡Esta contraseña ha sido comprometida!** Ha aparecido en **{count}** filtraciones de datos conocidas. No uses esta contraseña.",
        "breach_success": "✅ **Esta contraseña no ha sido comprometida.** Es segura para usar.",
        "password_expiry": "⏳ Caducidad y Rotación de Contraseña",
        "expiry_message": "Para mantener una seguridad sólida, se recomienda cambiar tu contraseña regularmente.",
        "last_changed_date": "¿Cuándo cambiaste tu contraseña por última vez?",
        "expiry_warning": "⚠️ **Han pasado {days} días desde que cambiaste tu contraseña.** Para una mejor seguridad, considera cambiarla ahora.",
        "expiry_success": "✅ **Tu contraseña fue cambiada hace {days} días.** Estás dentro del período recomendado de rotación de 90 días.",
        "generate_password": "¿Quieres una sugerencia de contraseña segura?",
        "generate_button": "Generar Contraseña Segura",
        "suggested_password": "**Contraseña Sugerida:** `{password}`",
        "security_tips": "🔒 Consejos de Seguridad para Contraseñas",
        "hashing_importance": "¿Por qué es Importante el Hashing de Contraseñas?",
        "hashing_description": "Las contraseñas nunca deben almacenarse en texto plano. Si una base de datos es comprometida, las contraseñas en texto plano pueden ser leídas y mal utilizadas por atacantes. El **hashing** es un proceso que convierte una contraseña en una cadena de caracteres de longitud fija, haciéndola ilegible e irreversible. Esto asegura que, incluso si la base de datos es vulnerada, las contraseñas reales permanezcan seguras.",
        "secure_storage": "¿Cómo Deben Almacenarse las Contraseñas de Forma Segura?",
        "strong_algorithms": "Usa Algoritmos de Hashing Fuertes",
        "salting": "Agrega Sal",
        "avoid_weak_algorithms": "Nunca Uses Algoritmos Débiles",
        "use_libraries": "Usa Bibliotecas y Frameworks",
        "best_practices": "Mejores Prácticas para la Seguridad de Contraseñas",
        "login_title": "🔑 Autenticación de Usuario",
        "username": "Nombre de usuario",
        "password": "Contraseña",
        "login_button": "Iniciar sesión",
        "logout_button": "Cerrar sesión",
        "login_success": "✅ ¡Inicio de sesión exitoso! Bienvenido, {username}.",
        "logout_success": "✅ ¡Cierre de sesión exitoso!",
        "export_report": "📄 Exportar Informe",
        "export_button": "Descargar Informe",
    },
    "fr": {
        "title": "🔐 Mesureur de Force de Mot de Passe",
        "enter_password": "Entrez votre mot de passe",
        "password_strength": "Force du Mot de Passe",
        "strong_password": "Mot de Passe Fort ! ✅",
        "moderate_password": "Mot de Passe Modéré - Envisagez d'ajouter plus de fonctionnalités de sécurité. ⚠️",
        "weak_password": "Mot de Passe Faible - Améliorez-le en utilisant les suggestions ci-dessous. ❌",
        "complexity_analysis": "Analyse de Complexité du Mot de Passe",
        "uppercase_letters": "Lettres Majuscules",
        "lowercase_letters": "Lettres Minuscules",
        "digits": "Chiffres",
        "special_chars": "Caractères Spéciaux",
        "suggestions": "Suggestions pour Améliorer :",
        "password_breach_check": "🔍 Vérification de l'Historique du Mot de Passe",
        "check_breach_button": "Vérifiez si ce mot de passe a été compromis",
        "breach_warning": "⚠️ **Ce mot de passe a été compromis !** Il est apparu dans **{count}** fuites de données connues. N'utilisez pas ce mot de passe.",
        "breach_success": "✅ **Ce mot de passe n'a pas été compromis.** Il est sûr à utiliser.",
        "password_expiry": "⏳ Expiration et Rotation du Mot de Passe",
        "expiry_message": "Pour maintenir une sécurité forte, il est recommandé de changer votre mot de passe régulièrement.",
        "last_changed_date": "Quand avez-vous changé votre mot de passe pour la dernière fois ?",
        "expiry_warning": "⚠️ **Cela fait {days} jours que vous avez changé votre mot de passe.** Pour une meilleure sécurité, envisagez de le changer maintenant.",
        "expiry_success": "✅ **Votre mot de passe a été changé il y a {days} jours.** Vous êtes dans la période de rotation recommandée de 90 jours.",
        "generate_password": "Vous voulez une suggestion de mot de passe fort ?",
        "generate_button": "Générer un Mot de Passe Fort",
        "suggested_password": "**Mot de Passe Suggeré :** `{password}`",
        "security_tips": "🔒 Conseils de Sécurité pour les Mots de Passe",
        "hashing_importance": "Pourquoi le Hashing des Mots de Passe est-il Important ?",
        "hashing_description": "Les mots de passe ne doivent jamais être stockés en texte clair. Si une base de données est compromise, les mots de passe en texte clair peuvent être facilement lus et mal utilisés par les attaquants. Le **hashing** est un processus qui convertit un mot de passe en une chaîne de caractères de longueur fixe, le rendant illisible et irréversible. Cela garantit que même si la base de données est violée, les mots de passe réels restent sécurisés.",
        "secure_storage": "Comment les Mots de Passe Devraient-ils Être Stockés de Manière Sécurisée ?",
        "strong_algorithms": "Utilisez des Algorithmes de Hashing Forts",
        "salting": "Ajoutez du Sel",
        "avoid_weak_algorithms": "N'Utilisez Jamais des Algorithmes Faibles",
        "use_libraries": "Utilisez des Bibliothèques et des Frameworks",
        "best_practices": "Meilleures Pratiques pour la Sécurité des Mots de Passe",
        "login_title": "🔑 Authentification de l'Utilisateur",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "login_button": "Connexion",
        "logout_button": "Déconnexion",
        "login_success": "✅ Connexion réussie ! Bienvenue, {username}.",
        "logout_success": "✅ Déconnexion réussie !",
        "export_report": "📄 Exporter le Rapport",
        "export_button": "Télécharger le Rapport",
    },
    "ur": {
        "title": "🔐 پاسورڈ طاقت میٹر",
        "enter_password": "اپنا پاسورڈ درج کریں",
        "password_strength": "پاسورڈ کی طاقت",
        "strong_password": "مضبوط پاسورڈ! ✅",
        "moderate_password": "معتدل پاسورڈ - مزید سیکیورٹی خصوصیات شامل کریں۔ ⚠️",
        "weak_password": "کمزور پاسورڈ - نیچے دی گئی تجاویز کا استعمال کرتے ہوئے اسے بہتر بنائیں۔ ❌",
        "complexity_analysis": "پاسورڈ کی پیچیدگی کا تجزیہ",
        "uppercase_letters": "بڑے حروف",
        "lowercase_letters": "چھوٹے حروف",
        "digits": "ہندسے",
        "special_chars": "خصوصی حروف",
        "suggestions": "بہتر بنانے کے لیے تجاویز:",
        "password_breach_check": "🔍 پاسورڈ کی تاریخ کی جانچ",
        "check_breach_button": "جانچیں کہ کیا یہ پاسورڈ سمجھوتہ ہوا ہے",
        "breach_warning": "⚠️ **یہ پاسورڈ سمجھوتہ ہو چکا ہے!** یہ **{count}** معلوم ڈیٹا کی خلاف ورزیوں میں ظاہر ہوا ہے۔ اس پاسورڈ کا استعمال نہ کریں۔",
        "breach_success": "✅ **یہ پاسورڈ سمجھوتہ نہیں ہوا ہے۔** اسے استعمال کرنا محفوظ ہے۔",
        "password_expiry": "⏳ پاسورڈ کی میعاد ختم ہونا اور گردش",
        "expiry_message": "مضبوط سیکیورٹی برقرار رکھنے کے لیے، پاسورڈ کو باقاعدگی سے تبدیل کرنے کی سفارش کی جاتی ہے۔",
        "last_changed_date": "آپ نے آخری بار پاسورڈ کب تبدیل کیا تھا؟",
        "expiry_warning": "⚠️ **آپ نے پاسورڈ تبدیل کیے ہوئے {days} دن ہو چکے ہیں۔** بہتر سیکیورٹی کے لیے، ابھی پاسورڈ تبدیل کرنے پر غور کریں۔",
        "expiry_success": "✅ **آپ کا پاسورڈ {days} دن پہلے تبدیل کیا گیا تھا۔** آپ سفارش کردہ 90 دن کی گردش کی مدت کے اندر ہیں۔",
        "generate_password": "کیا آپ کو ایک مضبوط پاسورڈ کی تجویز چاہیے؟",
        "generate_button": "مضبوط پاسورڈ بنائیں",
        "suggested_password": "**تجویز کردہ پاسورڈ:** `{password}`",
        "security_tips": "🔒 پاسورڈ سیکیورٹی کے نکات",
        "hashing_importance": "پاسورڈ ہیشنگ کیوں اہم ہے؟",
        "hashing_description": "پاسورڈز کو کبھی بھی سادہ متن میں ذخیرہ نہیں کیا جانا چاہیے۔ اگر ڈیٹا بیس سمجھوتہ ہو جاتا ہے، تو حملہ آوروں کے لیے سادہ متن میں پاسورڈز کو پڑھنا اور غلط استعمال کرنا آسان ہو جاتا ہے۔ **ہیشنگ** ایک ایسا عمل ہے جو پاسورڈ کو فکسڈ لمبائی کے حروف کی ایک سٹرنگ میں تبدیل کرتا ہے، جس سے یہ ناقابل پڑھائی اور ناقابل واپسی ہو جاتا ہے۔ یہ یقینی بناتا ہے کہ یہاں تک کہ اگر ڈیٹا بیس سمجھوتہ ہو جائے، تو اصل پاسورڈز محفوظ رہیں۔",
        "secure_storage": "پاسورڈز کو محفوظ طریقے سے کیسے ذخیرہ کیا جائے؟",
        "strong_algorithms": "مضبوط ہیشنگ الگورتھم استعمال کریں",
        "salting": "نمک شامل کریں",
        "avoid_weak_algorithms": "کمزور الگورتھم کبھی نہ استعمال کریں",
        "use_libraries": "لائبریریز اور فریم ورکس استعمال کریں",
        "best_practices": "پاسورڈ سیکیورٹی کے لیے بہترین طریقے",
        "login_title": "🔑 صارف کی تصدیق",
        "username": "صارف نام",
        "password": "پاسورڈ",
        "login_button": "لاگ ان",
        "logout_button": "لاگ آؤٹ",
        "login_success": "✅ لاگ ان کامیاب! خوش آمدید، {username}۔",
        "logout_success": "✅ لاگ آؤٹ کامیاب!",
        "export_report": "📄 رپورٹ برآمد کریں",
        "export_button": "رپورٹ ڈاؤن لوڈ کریں",
    },
     "de": {  
        "title": "🔐 Passwort-Stärke-Messgerät",
        "enter_password": "Geben Sie Ihr Passwort ein",
        "password_strength": "Passwortstärke",
        "strong_password": "Starkes Passwort! ✅",
        "moderate_password": "Mittelmäßiges Passwort - Erwägen Sie, mehr Sicherheitsfunktionen hinzuzufügen. ⚠️",
        "weak_password": "Schwaches Passwort - Verbessern Sie es mit den unten stehenden Vorschlägen. ❌",
        "complexity_analysis": "Analyse der Passwortkomplexität",
        "uppercase_letters": "Großbuchstaben",
        "lowercase_letters": "Kleinbuchstaben",
        "digits": "Ziffern",
        "special_chars": "Sonderzeichen",
        "suggestions": "Verbesserungsvorschläge:",
        "password_breach_check": "🔍 Überprüfung der Passworthistorie",
        "check_breach_button": "Überprüfen Sie, ob dieses Passwort kompromittiert wurde",
        "breach_warning": "⚠️ **Dieses Passwort wurde kompromittiert!** Es ist in **{count}** bekannten Datenlecks aufgetaucht. Verwenden Sie dieses Passwort nicht.",
        "breach_success": "✅ **Dieses Passwort wurde nicht kompromittiert.** Es ist sicher zu verwenden.",
        "password_expiry": "⏳ Passwortablauf und Rotation",
        "expiry_message": "Um eine starke Sicherheit zu gewährleisten, wird empfohlen, Ihr Passwort regelmäßig zu ändern.",
        "last_changed_date": "Wann haben Sie Ihr Passwort zuletzt geändert?",
        "expiry_warning": "⚠️ **Es sind {days} Tage vergangen, seit Sie Ihr Passwort zuletzt geändert haben.** Erwägen Sie, es jetzt zu ändern, um die Sicherheit zu verbessern.",
        "expiry_success": "✅ **Ihr Passwort wurde vor {days} Tagen geändert.** Sie befinden sich innerhalb der empfohlenen 90-tägigen Rotationsperiode.",
        "generate_password": "Möchten Sie ein sicheres Passwort?",
        "generate_button": "Sicheres Passwort generieren",
        "suggested_password": "**Vorgeschlagenes Passwort:** `{password}`",
        "security_tips": "🔒 Tipps zur Passwortsicherheit",
        "hashing_importance": "Warum ist Passwort-Hashing wichtig?",
        "hashing_description": "Passwörter sollten niemals im Klartext gespeichert werden. Wenn eine Datenbank kompromittiert wird, können Klartext-Passwörter leicht gelesen und von Angreifern missbraucht werden. **Hashing** ist ein Prozess, der ein Passwort in eine Zeichenkette fester Länge umwandelt, wodurch es unlesbar und irreversibel wird. Dadurch wird sichergestellt, dass die eigentlichen Passwörter auch bei einem Datenbankverstoß sicher bleiben.",
        "secure_storage": "Wie sollten Passwörter sicher gespeichert werden?",
        "strong_algorithms": "Verwenden Sie starke Hashing-Algorithmen",
        "salting": "Fügen Sie Salt hinzu",
        "avoid_weak_algorithms": "Verwenden Sie niemals schwache Algorithmen",
        "use_libraries": "Verwenden Sie Bibliotheken und Frameworks",
        "best_practices": "Bewährte Praktiken für die Passwortsicherheit",
        "login_title": "🔑 Benutzerauthentifizierung",
        "username": "Benutzername",
        "password": "Passwort",
        "login_button": "Anmelden",
        "logout_button": "Abmelden",
        "login_success": "✅ Anmeldung erfolgreich! Willkommen, {username}.",
        "logout_success": "✅ Abmeldung erfolgreich!",
        "export_report": "📄 Bericht exportieren",
        "export_button": "Bericht herunterladen",
        "export_pdf_button": "Bericht als PDF herunterladen",
        "time_to_crack": "Zeit zum Knacken",
        "recommendations": "Empfehlungen",
    },
}


language = st.sidebar.selectbox("🌐 Select Language", ["English", "Español", "Français", "Urdu"])
lang_code = (
    "en" if language == "English"
    else "es" if language == "Español"
    else "fr" if language == "Français"
    else "ur"
)

def translate(key):
    return translations[lang_code].get(key, key)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "password_history" not in st.session_state:
    st.session_state.password_history = []
if "otp" not in st.session_state:
    st.session_state.otp = None
if "email" not in st.session_state:
    st.session_state.email = None

EMAIL_SENDER = "your_email@example.com"  
EMAIL_PASSWORD = "your_email_password" 
SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587 

def send_email(receiver_email, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = receiver_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def generate_otp():
    return "".join(random.choices(string.digits, k=6))

def two_factor_authentication():
    st.write("### 🔒 Two-Factor Authentication (2FA)")
    email = st.text_input("Enter your email address for OTP verification:")
    if st.button("Send OTP"):
        if email:
            st.session_state.otp = generate_otp()
            st.session_state.email = email
            if send_email(email, "Your OTP for 2FA", f"Your OTP is: {st.session_state.otp}"):
                st.success("OTP sent successfully! Check your email.")
            else:
                st.error("Failed to send OTP. Please try again.")
        else:
            st.error("Please enter a valid email address.")

    if st.session_state.otp:
        otp_input = st.text_input("Enter the OTP you received:")
        if st.button("Verify OTP"):
            if otp_input == st.session_state.otp:
                st.session_state.authenticated = True
                st.success("OTP verified successfully! You are now authenticated.")
            else:
                st.error("Invalid OTP. Please try again.")

def login():
    st.write(f"### {translate('login_title')}")
    username = st.text_input(translate("username"))
    password = st.text_input(translate("password"), type="password")
    if st.button(translate("login_button")):
        if username and password: 
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(translate("login_success").format(username=username))
        else:
            st.error("Please enter both username and password.")

def logout():
    if st.button(translate("logout_button")):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.success(translate("logout_success"))

if not st.session_state.authenticated:
    login()
else:
    logout()
    st.write(f"### Welcome, {st.session_state.username}!")

if st.session_state.authenticated:
    COMMON_PASSWORDS = [
        "password", "123456", "12345678", "1234", "qwerty", "12345", "dragon", "baseball", "football",
        "letmein", "monkey", "abc123", "111111", "mustang", "access", "shadow", "master", "michael",
        "superman", "696969", "123123", "batman", "trustno1", "password123", "admin", "welcome",
        "login", "passw0rd", "1234567", "123456789", "1234567890", "password1", "123qwe", "qwerty123",
    ]

    COMMON_WORDS = [
        "hello", "welcome", "sunshine", "password", "admin", "letmein", "monkey", "football", "iloveyou",
        "starwars", "superman", "batman", "harrypotter", "pokemon", "qwerty", "123456", "12345678",
    ]

    def calculate_entropy(password):
        if not password:
            return 0
        pool_size = 0
        if re.search(r"[a-z]", password):
            pool_size += 26
        if re.search(r"[A-Z]", password):
            pool_size += 26
        if re.search(r"\d", password):
            pool_size += 10
        if re.search(r"[!@#$%^&*]", password):
            pool_size += 8  
        entropy = len(password) * math.log2(pool_size)
        return entropy

    def check_dictionary_words(password):
        for word in COMMON_WORDS:
            if word.lower() in password.lower():
                return True
        return False

    def check_password_strength(password):
        score = 0
        feedback = []
        
        uppercase_count = len(re.findall(r"[A-Z]", password))
        lowercase_count = len(re.findall(r"[a-z]", password))
        digit_count = len(re.findall(r"\d", password))
        special_count = len(re.findall(r"[!@#$%^&*]", password))
        
        min_length = 8
        if len(password) >= min_length:
            score += 1
        else:
            feedback.append(f"Password should be at least {min_length} characters long.")
        
        if uppercase_count > 0 and lowercase_count > 0:
            score += 1
        else:
            feedback.append("Include both uppercase and lowercase letters.")
        
        if digit_count > 0:
            score += 1
        else:
            feedback.append("Add at least one number.")
        
        if special_count > 0:
            score += 1
        else:
            feedback.append("Include at least one special character (!@#$%^&*).")
        
        if password.lower() in COMMON_PASSWORDS:
            score = 0 
            feedback.append("This password is too common and easily guessable. Choose a more unique password.")
        
        if check_dictionary_words(password):
            score = max(score - 1, 0)  
            feedback.append("Avoid using common dictionary words in your password.")
        
        entropy = calculate_entropy(password)
        if entropy >= 60: 
            score += 1
        else:
            feedback.append(f"Password entropy is low ({entropy:.2f}). Consider increasing randomness.")
        
        if len(password) >= 12:
            score += 1 
        
        if score == 6:
            return translate("strong_password"), score, feedback, uppercase_count, lowercase_count, digit_count, special_count, entropy
        elif score >= 3:
            return translate("moderate_password"), score, feedback, uppercase_count, lowercase_count, digit_count, special_count, entropy
        else:
            return translate("weak_password"), score, feedback, uppercase_count, lowercase_count, digit_count, special_count, entropy

    def generate_strong_password():
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(characters) for _ in range(12))

    def check_password_breach(password):
        try:
            sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix, suffix = sha1_password[:5], sha1_password[5:]
            
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=10)  
            if response.status_code == 200:
                for line in response.text.splitlines():
                    if suffix in line:
                        count = int(line.split(":")[1])
                        return True, count
                return False, 0
            else:
                st.error("Failed to check password breach. Please try again later.")
                return False, 0
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while checking password breach: {e}")
            return False, 0

    def generate_report(password, message, score, feedback, uppercase_count, lowercase_count, digit_count, special_count, is_breached, breach_count, days_since_last_change, entropy):
        report_data = {
            "Password": [password],
            "Strength": [message],
            "Score": [score],
            "Uppercase Letters": [uppercase_count],
            "Lowercase Letters": [lowercase_count],
            "Digits": [digit_count],
            "Special Characters": [special_count],
            "Entropy": [f"{entropy:.2f}"],
            "Breached": ["Yes" if is_breached else "No"],
            "Breach Count": [breach_count if is_breached else 0],
            "Days Since Last Change": [days_since_last_change],
            "Suggestions": ["\n".join(feedback)],
        }
        return pd.DataFrame(report_data)

    st.title(translate("title"))
    password_visible = st.checkbox("👁️ Show Password", key="password_visibility")
    password = st.text_input(translate("enter_password"), type="password" if not password_visible else "text", key="password_input")

    if password:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if hashed_password not in [entry["hash"] for entry in st.session_state.password_history]:
            st.session_state.password_history.append({
                "hash": hashed_password,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        message, score, feedback, uppercase_count, lowercase_count, digit_count, special_count, entropy = check_password_strength(password)
        
        st.write(f"### {translate('password_strength')}")
        progress_value = score / 6
        st.progress(progress_value)
        
        st.write(f"#### {message}")
        
        st.write(f"### {translate('complexity_analysis')}")
        st.write(f"- **{translate('uppercase_letters')}:** {uppercase_count}")
        st.write(f"- **{translate('lowercase_letters')}:** {lowercase_count}")
        st.write(f"- **{translate('digits')}:** {digit_count}")
        st.write(f"- **{translate('special_chars')}:** {special_count}")
        st.write(f"- **Entropy:** {entropy:.2f} bits")
        
        if feedback:
            st.write(f"##### {translate('suggestions')}")
            for tip in feedback:
                st.write(f"- {tip}")

        st.write("---")
        st.write(f"### {translate('password_breach_check')}")
        if st.button(translate("check_breach_button"), key="breach_check_button"):
            is_breached, breach_count = check_password_breach(password)
            if is_breached:
                st.error(translate("breach_warning").format(count=breach_count))
            else:
                st.success(translate("breach_success"))
        else:
            is_breached = False
            breach_count = 0

        st.write("---")
        st.write(f"### {translate('password_expiry')}")
        st.write(translate("expiry_message"))

        last_changed_date = st.date_input(translate("last_changed_date"), datetime.now() - timedelta(days=100), key="last_changed_date")

        days_since_last_change = (datetime.now() - datetime.combine(last_changed_date, datetime.min.time())).days

        if days_since_last_change >= 90:
            st.warning(translate("expiry_warning").format(days=days_since_last_change))
            if st.session_state.email:
                send_email(st.session_state.email, "Password Expiry Notification", "Your password is about to expire. Please change it immediately.")
        else:
            st.success(translate("expiry_success").format(days=days_since_last_change))

        st.write("---")
        st.write(translate("generate_password"))
        if st.button(translate("generate_button"), key="generate_password_button"):
            st.write(translate("suggested_password").format(password=generate_strong_password()))

        st.write("---")
        st.write(f"### {translate('security_tips')}")
        st.write(f"#### {translate('hashing_importance')}")
        st.write(translate("hashing_description"))
        st.write(f"#### {translate('secure_storage')}")
        st.write(f"1. **{translate('strong_algorithms')}**")
        st.write(f"2. **{translate('salting')}**")
        st.write(f"3. **{translate('avoid_weak_algorithms')}**")
        st.write(f"4. **{translate('use_libraries')}**")
        st.write(f"#### {translate('best_practices')}")

        st.write("---")
        st.write(f"### 🔒 Password History")
        if st.session_state.password_history:
            st.write("Below is your password history (hashed for security):")
            history_df = pd.DataFrame(st.session_state.password_history)
            st.dataframe(history_df)
        else:
            st.write("No password history available.")

        st.write("---")
        st.write(f"### {translate('export_report')}")
        if st.button(translate("export_button"), key="export_report_button"):
            if 'is_breached' not in locals():
                is_breached = False
                breach_count = 0
            report_df = generate_report(password, message, score, feedback, uppercase_count, lowercase_count, digit_count, special_count, is_breached, breach_count, days_since_last_change, entropy)
            csv = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Report as CSV",
                data=csv,
                file_name='password_strength_report.csv',
                mime='text/csv',
                key="download_report_button"
            )
import os
import base64
import json
import time
import random
from Crypto.Cipher import AES

# --- 🔥 STARTUP LOGO ---
def show_logo():
    os.system('clear')
    print("""
    ███████╗███╗   ██╗██████╗ ██╗███████╗
    ██╔════╝████╗  ██║██╔══██╗██║██╔════╝
    █████╗  ██╔██╗ ██║██████╔╝██║███████╗
    ██╔══╝  ██║╚██╗██║██╔═══╝ ██║╚════██║
    ███████╗██║ ╚████║██║     ██║███████║
    ╚══════╝╚═╝  ╚═══╝╚═╝     ╚══════╝
    """)
    print("🔒 End-to-End Encrypted Chat Loader\n")

# --- इनपुट ऑप्शंस ---
def get_inputs():
    cookie_file = input("🍪 Enter Cookies File Name: ") or "chat_cookie.json"
    encrypted_uid = input("🔐 Enter Encrypted UID: ")
    hater_name = input("😡 Enter Hater Name: ")
    message_file = input("📄 Enter Message File Name: ") or "messages.json"
    speed_sec = float(input("⏳ Enter Speed Seconds (default: 1.5s): ") or 1.5)

    return cookie_file, encrypted_uid, hater_name, message_file, speed_sec

# --- यूनिक कन्वो UID ---
def generate_convo_uid():
    return f"CONVO-{random.randint(1000, 9999)}"

# --- ✅ **FIXED AES-256 KEY (32 BYTES)**
SECRET_KEY = b'This_is_a_fixed_32_byte_key!!'  # ✅ अब 32 बाइट्स, No Error

# --- Padding & Unpadding ---
def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + chr(pad_len) * pad_len

def unpad(data):
    return data[:-ord(data[-1])]

# --- मैसेज एन्क्रिप्ट ---
def encrypt_message(message):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(message).encode())
    return base64.b64encode(encrypted).decode()

# --- मैसेज डिक्रिप्ट ---
def decrypt_message(encrypted_message):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64

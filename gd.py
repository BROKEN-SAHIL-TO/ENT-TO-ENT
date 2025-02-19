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
    decrypted = cipher.decrypt(base64.b64decode(encrypted_message))
    return unpad(decrypted.decode())

# --- Cookies फ़ाइल चेक (Fix Empty JSON File Issue) ---
def load_cookies(cookie_file):
    if not os.path.exists(cookie_file) or os.path.getsize(cookie_file) == 0:
        print(f"⚠️ Warning: {cookie_file} is empty or missing! Using default cookies.")
        return {"session": "default_session"}  # डिफ़ॉल्ट कुकीज़
    
    try:
        with open(cookie_file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Error: {cookie_file} is not a valid JSON file! Resetting...")
        return {"session": "default_session"}  # Reset JSON

# --- Messages फ़ाइल चेक ---
def load_messages(message_file):
    if not os.path.exists(message_file) or os.path.getsize(message_file) == 0:
        print("⚠️ Invalid message file! Using default messages.")
        return ["Hello!", "How are you?", "Goodbye!"]
    with open(message_file, "r") as f:
        return f.read().splitlines()

# --- Chat स्टार्ट ---
def start_chat():
    show_logo()
    cookie_file, encrypted_uid, hater_name, message_file, speed_sec = get_inputs()
    
    convo_uid = generate_convo_uid()
    cookies = load_cookies(cookie_file)
    messages = load_messages(message_file)

    print(f"\n🆔 Conversation UID: {convo_uid}")
    print(f"🔐 Encrypted UID: {encrypted_uid}")
    print(f"😡 Target Hater: {hater_name}")
    print(f"📄 Loading messages from: {message_file}")
    print(f"⏳ Speed: {speed_sec} seconds\n")

    for idx, msg in enumerate(messages, start=1):
        encrypted_msg = encrypt_message(msg)
        print(f"👤 You: {decrypt_message(encrypted_msg)}")
        time.sleep(speed_sec)

# --- स्क्रिप्ट रन ---
if __name__ == "__main__":
    start_chat()

import os
import base64
import json
import time
import random
from Crypto.Cipher import AES

# --- 🔥 STARTUP LOGO ---
def show_logo():
    print("""
    ███████╗███╗   ██╗██████╗ ██╗███████╗
    ██╔════╝████╗  ██║██╔══██╗██║██╔════╝
    █████╗  ██╔██╗ ██║██████╔╝██║███████╗
    ██╔══╝  ██║╚██╗██║██╔═══╝ ██║╚════██║
    ███████╗██║ ╚████║██║     ██║███████║
    ╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝╚══════╝
    """)

# --- कुकीज़ फाइल इनपुट ---
COOKIE_FILE = input("🍪 कुकी फाइल का नाम दर्ज करें (default: chat_cookie.json): ") or "chat_cookie.json"

# --- यूनिक कन्वो UID ---
CONVO_UID = f"CONVO-{random.randint(1000, 9999)}"
print(f"🆔 कन्वो UID: {CONVO_UID}")

# --- स्पीड सेकंड ---
SPEED_SEC = float(input("⏳ स्पीड सेकंड (default: 1.5s): ") or 1.5)

# --- SECRET KEY (AES-256) ---
SECRET_KEY = b'This_is_a_32_byte_secret_key!!'

# --- Padding & Unpadding ---
def pad(data):
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)

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
    decrypted = cipher.decrypt(base64.b64decode(encrypted_message)).decode()
    return unpad(decrypted)

# --- चैट लोड ---
def load_chat():
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r") as file:
            return json.load(file)
    return []

# --- चैट सेव ---
def save_chat(messages):
    with open(COOKIE_FILE, "w") as file:
        json.dump(messages, file)

# --- चैट स्टार्ट ---
def start_chat():
    show_logo()
    print(f"🔒 सुरक्षित ऑफलाइन कन्वर्सेशन ({CONVO_UID})\n")
    
    messages = load_chat()
    
    while True:
        msg = input("👤 आप: ")
        if msg.lower() == "exit":
            break

        encrypted_msg = encrypt_message(msg)
        messages.append(encrypted_msg)
        save_chat(messages)

        print(f"🔐 एन्क्रिप्टेड मैसेज: {encrypted_msg}\n")

        # --- ऑटो रिप्लाई (स्पीड सेटिंग के साथ) ---
        time.sleep(SPEED_SEC)
        reply = "यह एक डिफॉल्ट एन्क्रिप्टेड उत्तर है।"
        encrypted_reply = encrypt_message(reply)
        messages.append(encrypted_reply)
        save_chat(messages)
        print(f"🤖 रिप्लाई: {reply} (🔐 {encrypted_reply})\n")

    print("\n🔓 डिक्रिप्टेड चैट हिस्ट्री:\n")
    for encrypted_msg in messages:
        print(f"💬 {decrypt_message(encrypted_msg)}")

# --- स्क्रिप्ट रन ---
if __name__ == "__main__":
    start_chat()

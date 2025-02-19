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

# --- SECRET KEY (AES-256) ---
SECRET_KEY = b'This_is_a_32_byte_secret_key!!!'  # 32-byte key (FIXED)

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

# --- चैट लोड (Auto-Handle) ---
def load_chat(cookie_file):
    if os.path.exists(cookie_file):
        with open(cookie_file, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):  
                    return data
            except (json.JSONDecodeError, ValueError):
                pass
    return []  # Default Empty List (NO Warning)

# --- चैट सेव ---
def save_chat(messages, cookie_file):
    with open(cookie_file, "w") as file:
        json.dump(messages, file)

# --- मैसेज लोड ---
def load_messages(message_file):
    if os.path.exists(message_file):
        with open(message_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                pass
    return ["Hello", "How are you?", "Goodbye!"]  # Default Messages (NO Warning)

# --- चैट स्टार्ट ---
def start_chat():
    show_logo()
    
    # --- इनपुट्स लें ---
    cookie_file, encrypted_uid, hater_name, message_file, speed_sec = get_inputs()
    
    print(f"\n🆔 Conversation UID: {generate_convo_uid()}")
    print(f"🔐 Encrypted UID: {encrypted_uid}")
    print(f"😡 Target Hater: {hater_name}")
    print(f"📄 Loading messages from: {message_file}")
    print(f"⏳ Speed: {speed_sec} seconds\n")

    messages = load_chat(cookie_file)
    auto_replies = load_messages(message_file)

    while True:
        msg = input("👤 You: ")
        if msg.lower() == "exit":
            break

        encrypted_msg = encrypt_message(msg)
        messages.append(encrypted_msg)
        save_chat(messages, cookie_file)

        print(f"🔐 Encrypted Message: {encrypted_msg}\n")

        # --- ऑटो रिप्लाई ---
        time.sleep(speed_sec)
        reply = random.choice(auto_replies)
        encrypted_reply = encrypt_message(reply)
        messages.append(encrypted_reply)
        save_chat(messages, cookie_file)
        print(f"🤖 Reply: {reply} (🔐 {encrypted_reply})\n")

    print("\n🔓 Decrypted Chat History:\n")
    for encrypted_msg in messages:
        print(f"💬 {decrypt_message(encrypted_msg)}")

# --- स्क्रिप्ट रन ---
if __name__ == "__main__":
    start_chat()

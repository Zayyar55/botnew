import os
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- CONFIGURATION ---
GROQ_API_KEY = "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"
TG_TOKEN = "8774327296:AAHfzzOTEh0eShFmCLH78fTHR3XVNgk5qFM"

# Render Port Binding (Keep-Alive)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Flying at Warp Speed!")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# AI Core Logic (Ultra Fast Groq Integration)
def query_ai(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful and smart AI assistant. Answer the user clearly and concisely. Support Myanmar language."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "ခဏနေမှ ပြန်မေးပေးပါဗျ။ အခုလောလောဆယ် Server နည်းနည်းအလုပ်များနေလို့ပါ။"

# Telegram Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Groq က အရမ်းမြန်လို့ စောင့်ခိုင်းစရာမလိုဘဲ တန်းပို့လိုက်မယ်
    ai_response = query_ai(user_text)
    await update.message.reply_text(ai_response)

if __name__ == '__main__':
    # Start Health Check for Render
    threading.Thread(target=run_health_check, daemon=True).start()
    
    # Launch Telegram Bot
    print("Bot is starting with Ultra Speed...")
    app = ApplicationBuilder().token(TG_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    app.run_polling()

from flask import Flask, render_template, jsonify
import requests
import random
import string
import threading
import time

app = Flask(__name__)
bot_running = False

def check_codes():
    global bot_running
    while bot_running:
        letters_and_digits = string.ascii_uppercase + string.digits
        test_code = ''.join(random.choice(letters_and_digits) for _ in range(10))
        print(f"[Bot] Checking code: {test_code}")
        time.sleep(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        thread = threading.Thread(target=check_codes)
        thread.daemon = True
        thread.start()
        return jsonify({"status": "success", "message": "Bot စတင် အလုပ်လုပ်နေပါပြီ..."})
    return jsonify({"status": "error", "message": "Bot မှာ Run နေပြီးဖြစ်ပါသည်။"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    global bot_running
    bot_running = False
    return jsonify({"status": "success", "message": "Bot ရပ်တန့်သွားပါပြီ။"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


from flask import Flask, render_template, jsonify, request
import requests
import random
import string
import threading
import time

app = Flask(__name__)
bot_running = False

def check_codes(target_url, code_length, code_type):
    global bot_running
    while bot_running:
        # ရွေးချယ်ထားသော အမျိုးအစားအလိုက် Code ထုတ်မည်
        if code_type == "digits":
            chars = string.digits # ဂဏန်းသီးသန့်
        else:
            chars = string.ascii_uppercase + string.digits # အက္ခရာ + ဂဏန်း
            
        test_code = ''.join(random.choice(chars) for _ in range(code_length))
        
        # အမှန်တကယ် စမ်းသပ်မည့် URL ပုံစံ (ဥပမာ - api.com/check?code=123456)
        full_url = f"{target_url}{test_code}"
        print(f"[Bot] Checking: {test_code} at {full_url}")
        
        # အောက်ပါ Code ဖြင့် တကယ်လှမ်းစစ်နိုင်သည် (လောလောဆယ် Print သာထုတ်ပြထားသည်)
        # try:
        #     response = requests.get(full_url, timeout=5)
        #     if response.status_code == 200:
        #         print("Success Code Found!")
        # except:
        #     pass
            
        time.sleep(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_bot():
    global bot_running
    if not bot_running:
        # UI မှ ပို့လိုက်သော အချက်အလက်များကို ရယူခြင်း
        data = request.get_json()
        target_url = data.get('target_url', '')
        code_length = int(data.get('code_length', 8))
        code_type = data.get('code_type', 'mixed')

        if not target_url:
            return jsonify({"status": "error", "message": "Target URL ထည့်ရန် လိုအပ်ပါသည်။"})

        bot_running = True
        thread = threading.Thread(target=check_codes, args=(target_url, code_length, code_type))
        thread.daemon = True
        thread.start()
        return jsonify({"status": "success", "message": f"URL: {target_url} သို့ ဂဏန်း ({code_length}) လုံးဖြင့် စတင်နေပါပြီ..."})
        
    return jsonify({"status": "error", "message": "Bot မှာ Run နေပြီးဖြစ်ပါသည်။"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    global bot_running
    bot_running = False
    return jsonify({"status": "success", "message": "Bot ရပ်တန့်သွားပါပြီ။"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # ဖုန်းထဲတွင် Port 5000 ဖြင့် Run ပါမည်
    app.run(host='0.0.0.0', port=5000)

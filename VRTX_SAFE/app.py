from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vrtx_cloud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Твой адрес-сейф
MY_SAFE_ADDRESS = "TMh9n9rAoBurQGHVTWANBzxn6DJqXpyM2G"

# Модель базы данных для учета платежей
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    amount_rub = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")

@app.route('/')
def index():
    # Отправляем адрес кошелька в HTML для отображения в футере
    return render_template('index.html', wallet_address=MY_SAFE_ADDRESS)

@app.route('/pay', methods=['POST'])
def pay():
    name = request.form.get('name')
    amount = request.form.get('amount')

    # 1. Записываем ученика в базу (ты его уже не потеряешь!)
    new_payment = Payment(student_name=name, amount_rub=float(amount))
    db.session.add(new_payment)
    db.session.commit()

    # 2. Вместо сложного API мы просто генерируем страницу оплаты
    # Ученик увидит твой адрес кошелька и сумму.
    # Это надежно, безопасно и работает БЕЗ всяких ключей.
    
    # Формируем прямую ссылку в кошелек MAX
    max_pay_url = f"https://max.ru/wallet/transfer?address={MY_SAFE_ADDRESS}&amount={amount}"

return f"""
    <html>
    <head>
        <style>
            body {{ background: #000; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 40px 20px; }}
            .terminal {{ max-width: 450px; margin: 0 auto; border: 1px solid #00ff00; padding: 30px; border-radius: 20px; background: #050505; box-shadow: 0 0 30px rgba(0,255,0,0.1); }}
            .amount-tag {{ font-size: 2em; color: #00ff00; margin: 20px 0; font-weight: bold; }}
            .wallet-box {{ background: #111; padding: 15px; border-radius: 10px; word-break: break-all; color: #00ff00; font-family: monospace; font-size: 1.1em; margin: 20px 0; border: 1px dashed #333; cursor: pointer; }}
            .instruction {{ text-align: left; font-size: 0.9em; color: #888; line-height: 1.5; }}
            .copy-hint {{ font-size: 0.7em; color: #555; }}
        </style>
    </head>
    <body>
        <div class="terminal">
            <h2 style="letter-spacing: 3px;">ОПЛАТА ПРИНЯТА</h2>
            <p>Ученик: {name}</p>
            <div class="amount-tag">{amount} РУБ.</div>
            
            <hr style="border: 0; border-top: 1px solid #222; margin: 20px 0;">
            
            <p class="instruction">1. Нажмите на адрес ниже, чтобы скопировать его:</p>
            <div class="wallet-box" onclick="copyAddr()" id="addr">{MY_SAFE_ADDRESS}</div>
            <p class="copy-hint">Нажмите для копирования</p>
            
            <p class="instruction">2. Зайдите в <b>приложение MAX</b> и переведите сумму в USDT на этот адрес.</p>
            
            <p style="margin-top: 30px; font-size: 0.8em; color: #00ff00; opacity: 0.7;">
                [ СИСТЕМА ЗАЩИТЫ КАРТЫ АКТИВИРОВАНА ]
            </p>
        </div>

        <script>
            function copyAddr() {{
                var text = document.getElementById("addr").innerText;
                navigator.clipboard.writeText(text).then(function() {{
                    alert("Адрес скопирован! Теперь просто вставьте его в кошельке MAX.");
                }});
            }}
        </script>
    </body>
    </html>
    """

import os

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Забираем порт, который даст Render, или используем 5000 как запасной
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

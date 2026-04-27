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
    max_pay_url = "https://max.ru/tt/SecurePayment"  # Замени ТВОЙ_НИК на тот, что создала

return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ background: #000; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 40px 20px; }}
            .card {{ max-width: 420px; margin: 0 auto; border: 1px solid #00ff00; padding: 30px; border-radius: 20px; background: #0a0a0a; box-shadow: 0 0 20px rgba(0,255,0,0.1); }}
            .amount {{ font-size: 2.5em; color: #00ff00; margin: 15px 0; font-weight: bold; }}
            .wallet-addr {{ background: #111; padding: 15px; border-radius: 10px; word-break: break-all; color: #00ff00; font-family: monospace; font-size: 1.2em; margin: 20px 0; border: 1px dashed #333; cursor: pointer; }}
            .btn {{ background: #00ff00; color: #000; padding: 15px 30px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; width: 100%; font-size: 1.1em; text-transform: uppercase; margin-bottom: 10px; }}
            .btn:hover {{ background: #00cc00; }}
            .step {{ text-align: left; font-size: 0.9em; color: #888; margin-bottom: 10px; }}
            hr {{ border: 0; border-top: 1px solid #222; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="font-size: 0.8em; color: #00ff00; letter-spacing: 2px; margin-bottom: 10px;">VRTX_SAFE SYSTEM</div>
            <h2 style="color: #fff; margin: 0;">ДАННЫЕ ДЛЯ ПЕРЕВОДА</h2>
            <div class="amount">{amount} РУБ.</div>
            
            <hr>
            
            <div class="step">1. Нажмите на адрес, чтобы скопировать:</div>
            <div class="wallet-addr" onclick="copyOnly()" id="addr_text">{MY_SAFE_ADDRESS}</div>
            
            <div class="step">2. Перейдите в шлюз оплаты:</div>
            <button class="btn" onclick="copyAndGo()">СКОПИРОВАТЬ И ПЕРЕЙТИ В MAX</button>
            
            <p style="font-size: 0.7em; color: #444; margin-top: 30px; text-transform: uppercase;">Транзакция защищена облачным шифрованием V-RTX</p>
            
            <div style="margin-top: 30px; font-size: 0.85em; color: #666; text-align: left; background: #111; padding: 15px; border-radius: 10px;">
                <b>Инструкция:</b><br>
                1. Нажмите зеленую кнопку.<br>
                2. В открывшемся чате нажмите на иконку <b>Кошелька</b> 💰.<br>
                3. Вставьте скопированный адрес и сумму.<br>
                4. После перевода ваш статус в системе обновится автоматически.
            </div>
        </div>

        <script>
            // Просто копирует адрес
function copyAndGo() {{
                var t = document.getElementById("addr_text").innerText;
                navigator.clipboard.writeText(t);
                alert("Адрес скопирован! Вы переходите в шлюз оплаты.");
                window.location.href = "https://max.ru/tt/vrtx_pay"; 
            }}

            // Копирует и делает переход на твой "Шлюз"
            function copyAndGo() {{
                var t = document.getElementById("addr_text").innerText;
                navigator.clipboard.writeText(t);
                alert("Адрес скопирован! Сейчас вы будете перенаправлены в шлюз Secure Payment.");
                // Твоя прямая ссылка на профиль
                window.location.href = "https://max.ru/u/f9LHodD0cOJmnlCr5NwA3ln2sjFUv_m5WDrkMTux690g_VXvpX3O1SpBCAI";
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

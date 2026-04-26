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
        <meta http-equiv="refresh" content="1;url={max_pay_url}">
        <style>
            body {{ background: #000; color: #fff; font-family: sans-serif; text-align: center; padding-top: 150px; }}
            .loader {{ border: 3px solid #222; border-top: 3px solid #00ff00; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        </style>
    </head>
    <body>
        <div class="loader"></div>
        <p>ПЕРЕНАПРАВЛЯЕМ В MAX...</p>
        <p>Для оплаты курса на сумму <b>{amount} руб.</b></p>
        <br>
        <a href="{max_pay_url}" style="color: #00ff00; text-decoration: none; font-size: 0.8em;">Нажмите здесь, если переход не начался</a>
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

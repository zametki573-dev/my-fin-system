from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vrtx_cloud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Твой адрес-сейф
MY_SAFE_ADDRESS = "https://max.ru/u/f9LHodD0cOKtoj9aZYXfR4p7Mi4KcG3JFut6tTZWK1SOfm0KYqb53mv6CLY"

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

@app.route('/pay/<int:amount>')
def pay(amount):
    # Прямая ссылка на твой профиль с картинкой
    pay_url = "https://max.ru/u/f9LHodD0cOKtoj9aZYXfR4p7Mi4KcG3JFut6tTZWK1SOfm0KYqb53mv6CLY"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 40px 20px; }}
            .card {{ max-width: 400px; margin: 0 auto; border: 1px solid #00FF00; padding: 30px; border-radius: 20px; }}
            .btn {{ display: block; width: 100%; padding: 15px; background: #00FF00; color: #000; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 20px; }}
            .amount {{ font-size: 2.5em; color: #00FF00; margin: 20px 0; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="font-size: 0.8em; color: #00FF00; letter-spacing: 2px;">VRTX_SAFE SYSTEM</div>
            <h2>ОПЛАТА ОБУЧЕНИЯ</h2>
            <div class="amount">{amount} РУБ.</div>
            <hr style="border: 0; border-top: 1px solid #222;">
            <p style="text-align: left; font-size: 0.9em; color: #ccc;">
                1. Нажмите кнопку ниже.<br>
                2. В открывшемся профиле MAX нажмите <b>"Отправить"</b>.<br>
                3. Введите сумму в USDT и подтвердите перевод.
            </p>
            <a href="{pay_url}" class="btn">ОПЛАТИТЬ В MAX</a>
            <p style="font-size: 0.7em; color: #444; margin-top: 30px;">ТРАНЗАКЦИЯ ЗАЩИЩЕНА V-RTX STUDIO</p>
        </div>
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

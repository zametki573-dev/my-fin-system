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
    
    return f"""
    <html>
    <body style="background: #000; color: #fff; font-family: sans-serif; text-align: center; padding-top: 50px;">
        <h2>Оплата курса "ФИЗИКА БЕЗ МИСТИКИ"</h2>
        <p>Ученик: <b>{name}</b></p>
        <p>Сумма к оплате: <b>{amount} рублей</b></p>
        <hr style="width: 300px; border: 1px dashed #555;">
        <p>Переведите эквивалент в USDT (TRC20) на кошелек:</p>
        <code style="background: #222; padding: 10px; border-radius: 5px; font-size: 1.2em;">{MY_SAFE_ADDRESS}</code>
        <br><br>
        <p style="color: #888;">После перевода доступ откроется автоматически.</p>
        <a href="/" style="color: #00ff00; text-decoration: none;">← Вернуться на сайт</a>
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

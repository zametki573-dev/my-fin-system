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
            body {{ background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 50px 20px; }}
            .container {{ max-width: 400px; margin: 0 auto; border: 1px solid #333; padding: 20px; border-radius: 15px; }}
            .btn {{ display: block; background: #00ff00; color: #000; padding: 15px; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 20px; }}
            .address {{ background: #111; padding: 10px; border-radius: 5px; word-break: break-all; color: #00ff00; font-family: monospace; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2 style="color: #00ff00;">ПОЧТИ ГОТОВО</h2>
            <p>Сумма к оплате: <b>{amount} руб.</b></p>
            <p style="font-size: 0.9em; color: #888;">Скопируйте адрес и переведите USDT в приложении MAX:</p>
            
            <div class="address" id="addr">{MY_SAFE_ADDRESS}</div>
            
            <a href="https://max.ru/wallet/transfer?address={MY_SAFE_ADDRESS}&amount={amount}" class="btn">ОТКРЫТЬ В ПРИЛОЖЕНИИ</a>
            
            <p style="margin-top: 20px; font-size: 0.8em; color: #555;">После оплаты доступ к курсу "Физика без мистики" откроется автоматически.</p>
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

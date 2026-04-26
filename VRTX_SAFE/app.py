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

    # 1. Записываем в базу (твой "цифровой журнал")
    new_payment = Payment(student_name=name, amount_rub=float(amount))
    db.session.add(new_payment)
    db.session.commit()

    # 2. Твой API-ключ от MAX (возьми его в личном кабинете MAX)
    MAX_API_KEY = "TMh9n9rAoBurQGHVTWANBzxn6DJqXpyM2G"

    # 3. Формируем прямую ссылку на оплату через шлюз MAX
    # Она отправит деньги на твой адрес TMh..., который ты указала выше
    payment_link = f"https://api.max-pay.com/v1/create?api_key={MAX_API_KEY}&amount={amount}&description=Payment_from_{name}&wallet={MY_SAFE_ADDRESS}"

    print(f"DEBUG: Ученик {name} направлен на оплату {amount} руб.")
    
    # 4. Перенаправляем ученика по этой ссылке
    return redirect(payment_link)

import os

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Забираем порт, который даст Render, или используем 5000 как запасной
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

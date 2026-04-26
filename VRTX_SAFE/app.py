from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vrtx_cloud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Твой адрес-сейф
MY_SAFE_ADDRESS = "TGGXbG9qgdZGtK9EumggB7HAXiNXNd7aGf"

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
    
    # Сохраняем попытку оплаты в базу (наш "бухгалтер" записывает всё)
    new_payment = Payment(student_name=name, amount_rub=float(amount))
    db.session.add(new_payment)
    db.session.commit()
    
    print(f"DEBUG: Ученик {name} хочет оплатить {amount} руб.")
    
    # Временно просто перенаправляем обратно, пока не подключили шлюз
    return redirect("https://app.lava.top/products/3496f22d-1e2b-41bf-9b7d-55d53558f826")

import os

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Забираем порт, который даст Render, или используем 5000 как запасной
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

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
def home():
    # Сразу перенаправляем на твой профиль
    return redirect("https://max.ru/u/f9LHodD0cOKtoj9aZYXfR4p7Mi4KcG3JFut6tTZWK1SOfm0KYqb53mv6CLY")

@app.route('/pay/<int:amount>')
def pay(amount):
    # Даже если ввели сумму, всё равно кидаем на профиль
    return redirect("https://max.ru/u/f9LHodD0cOKtoj9aZYXfR4p7Mi4KcG3JFut6tTZWK1SOfm0KYqb53mv6CLY")

if __name__ == "__main__":
    app.run()

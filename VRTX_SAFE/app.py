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

@app.route('/pay/<int:amount>')
def pay(amount):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ background: #000; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 40px 20px; }}
            .card {{ max-width: 400px; margin: 0 auto; border: 1px solid #00FF00; padding: 30px; border-radius: 20px; background: #050505; }}
            .amount {{ font-size: 2.5em; color: #00FF00; margin: 20px 0; font-weight: bold; }}
            .btn {{ display: block; width: 100%; padding: 18px; background: #00FF00; color: #000; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 20px; font-size: 1.1em; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="font-size: 0.8em; color: #00FF00; letter-spacing: 2px; margin-bottom: 10px;">VRTX_SAFE SYSTEM</div>
            <h2 style="margin: 0; font-weight: normal;">ОПЛАТА КУРСА</h2>
            <div class="amount">{amount} РУБ.</div>
            <hr style="border: 0; border-top: 1px solid #222; margin: 20px 0;">
            
            <p style="text-align: left; font-size: 0.9em; color: #888;">
                1. Нажмите кнопку ниже.<br>
                2. В профиле нажмите <b>"Отправить"</b>.<br>
                3. Введите сумму в USDT.
            </p>

            <a href="https://max.ru/u/f9LHodD0cOKtoj9aZYXfR4p7Mi4KcG3JFut6tTZWK1SOfm0KYqb53mv6CLY" class="btn">
                ПЕРЕЙТИ К ОПЛАТЕ
            </a>
            
            <div style="margin-top: 30px; font-size: 0.7em; color: #333;">PROTECTED BY V-RTX STUDIO</div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()

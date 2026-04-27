from flask import Flask, request, redirect
import os

app = Flask(__name__)

@app.route('/pay/<int:amount>')
def pay(amount):
    # Твой дизайн с формой ввода имени
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }}
            .card {{ max-width: 400px; margin: 0 auto; border: 1px solid #00FF00; padding: 30px; border-radius: 20px; background: #050505; }}
            input {{ width: 90%; padding: 15px; margin: 20px 0; border-radius: 10px; border: 1px solid #00FF00; background: #000; color: #fff; text-align: center; }}
            .btn {{ display: block; width: 100%; padding: 18px; background: #00FF00; color: #000; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; text-decoration: none; }}
            .amount {{ font-size: 2em; color: #00FF00; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="font-size: 0.8em; color: #00FF00; opacity: 0.6;">VRTX_SAFE SYSTEM</div>
            <h2>ПОДТВЕРЖДЕНИЕ</h2>
            <div class="amount">{amount} РУБ.</div>
            
            <form action="/confirm" method="POST">
                <input type="hidden" name="amount" value="{amount}">
                <input type="text" name="name" placeholder="ВВЕДИТЕ ВАШЕ ИМЯ" required>
                <button type="submit" class="btn">ПОДТВЕРДИТЬ И ОПЛАТИТЬ</button>
            </form>
            
            <p style="font-size: 0.7em; color: #444; margin-top: 20px;">ДАННЫЕ БУДУТ ПЕРЕДАНЫ КУРАТОРУ</p>
        </div>
    </body>
    </html>
    """

@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form.get('name')
    amount = request.form.get('amount')
    
    # ВОТ ЗДЕСЬ Python "записывает в книжку"
    print(f"ОПЛАТА: {name} на сумму {amount} руб.") 
    # Сюда потом в одну строчку добавим отправку боту, когда оживим его.

    # А теперь просто выкидываем его на твой MAX
    return redirect("https://max.ru/u/f9LHodD0cOKtoj9aZYXfR4p7Mi4KcG3JFut6tTZWK1SOfm0KYqb53mv6CLY")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

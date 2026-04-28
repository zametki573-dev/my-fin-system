from flask import Flask, request, os

app = Flask(__name__)

@app.route('/pay/<int:amount>')
def pay(amount):
    # Твоя страница оплаты VRTX
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }}
            .card {{ max-width: 400px; margin: 0 auto; border: 1px solid #00FF00; padding: 30px; border-radius: 20px; background: #050505; }}
            .btn {{ display: block; width: 100%; padding: 18px; background: #00FF00; color: #000; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; text-decoration: none; margin-top: 10px; }}
            .amount {{ font-size: 2em; color: #00FF00; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="font-size: 0.8em; color: #00FF00; opacity: 0.6;">VRTX_SAFE_SYSTEM</div>
            <h2>ПОДТВЕРЖДЕНИЕ</h2>
            <div class="amount">{amount} РУБ.</div>

            <button class="btn" onclick="copyWallet()" style="background: #222;">
                1. СКОПИРОВАТЬ АДРЕС
            </button>

            <a href="https://60cek.net/obmen-sberbank-na-usdt-ton.html" target="_blank" style="text-decoration: none;">
                <button class="btn">2. ПЕРЕЙТИ К ОПЛАТЕ</button>
            </a>

            <p style="font-size: 0.7em; color: #444; margin-top: 20px;">
                СКОПИРУЙТЕ АДРЕС И ВСТАВЬТЕ ЕГО В ПОЛЕ "КОШЕЛЕК ДЛЯ ПОЛУЧЕНИЯ" НА САЙТЕ ОБМЕННИКА
            </p>
        </div>

        <script>
        function copyWallet() {{
            navigator.clipboard.writeText('UQDwA26gZayasv2rTuQZ5YpfnmyfWSISXavpDUAmfz0S_9kp');
            alert('Адрес скопирован! Теперь вставьте его на сайте обменника.');
        }}
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

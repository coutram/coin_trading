from flask import Flask, jsonify, request
from flask_cors import CORS
from analytics import get_memecoin_data, get_top_performing_wallets
from trader import execute_trade

app = Flask(__name__)
CORS(app)

@app.route('/api/memecoins', methods=['GET'])
def memecoins():
    data = get_memecoin_data()
    return jsonify(data)

@app.route('/api/performing', methods=['GET'])
def performing():
    data = get_top_performing_wallets()
    return jsonify(data)

@app.route('/api/trade', methods=['POST'])
def trade():
    data = request.json
    action = data.get('action')
    coin = data.get('coin')
    result = execute_trade(action, coin)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3100)

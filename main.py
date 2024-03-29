import logging
import db_broker
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/reports', methods=['GET'])
async def reports():
    return jsonify(await db_broker.get_reports_dumb())

@app.route('/api/report/<string:id>', methods=['GET'])
async def report(id):
    res = await db_broker.get_report(id)
    return jsonify(res)

@app.route('/api/report/<string:id>', methods=['DELETE'])
def delete_rep(id):
    res = db_broker.delete_report(id)
    return jsonify(f"report: {res}")

@app.route('/api/report/<string:id>', methods=['PUT'])
def update_rep(id):
    res = db_broker.update_report(id)
    return jsonify(f"report: {res}")

@app.route('/api/report/<string:id>', methods=['POST'])
def create_report(id):
    res = db_broker.insert_report(id)
    return jsonify(f"report: {res}")

def main():
    app.run()

if __name__ == "__main__":
    main()

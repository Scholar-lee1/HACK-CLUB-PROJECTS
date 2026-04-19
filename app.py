from flask import Flask, render_template, request, jsonify
from services.openrouter_service import OpenRouterService # Update this import

app = Flask(__name__)
ai_service = OpenRouterService() # Update this instance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    if not data or 'action' not in data:
        return jsonify({"status": "error"}), 400
        
    outcomes = ai_service.get_simulation(data['action'])
    return jsonify({"status": "success", "outcomes": outcomes})

if __name__ == '__main__':
    app.run(debug=True)
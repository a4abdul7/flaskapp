from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize with default message
message = "Hello World"

@app.route('/', methods=['GET'])
def pull():
    return jsonify({"message": message})

@app.route('/push', methods=['POST'])
def push():
    global message
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in JSON body"}), 400
    message = data["message"]
    return jsonify({"message": f"Message updated to: {message}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

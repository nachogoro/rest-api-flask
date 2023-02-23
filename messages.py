from flask import Flask, request, jsonify

app = Flask(__name__)

# dictionary to store messages
messages = {}

@app.route('/messages', methods=['POST', 'GET'])
def handle_messages():
    if request.method == 'POST':
        # get title and body from request body
        title = request.json['title']
        body = request.json['body']
        # store message in dictionary
        messages[title] = body
        return jsonify({'message': 'Message saved successfully.'})

    elif request.method == 'GET':
        # get title from request parameter
        title = request.args.get('title')
        if title in messages:
            # return message as JSON object
            return jsonify({'title': title, 'body': messages[title]})
        else:
            return jsonify({'message': 'Message not found.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

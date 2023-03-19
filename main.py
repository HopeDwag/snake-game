from os import path

from flask import Flask, render_template, request
import json

app = Flask(__name__)

# leaderboard_path = '/data/leaderboard.json'
leaderboard_path = 'leaderboard.json'

@app.route('/')
def health_check():
    # Perform any necessary checks here to determine if the application is ready
    # to receive traffic. If everything is okay, return a 200 OK response.
    return 'OK', 200

@app.route('/snake')
def snake():
    return render_template('snake.html')


@app.route('/submit', methods=['POST'])
def submit():
    print(request.json)
    username = request.json['username']
    score = int(request.json['score'])
    entry = {'username': username, 'score': score}
    # append the new entry to the JSON file
    with open(leaderboard_path, 'r') as f:
        entries = json.load(f)
    entries.append(entry)
    with open(leaderboard_path, 'w') as f:
        json.dump(entries, f, indent=4)
    return render_template('snake.html', username=username)


@app.route('/leaderboard')
def leaderboard():
    with open(leaderboard_path, 'r') as f:
        entries = json.load(f)
    entries = sorted(entries, key=lambda x: x['score'], reverse=True)
    return render_template('leaderboard.html', entries=entries)


@app.route('/high_score/<username>')
def high_score(username):
    with open(leaderboard_path, 'r') as f:
        leaderboard = json.load(f)
    for user in leaderboard:
        if user['username'] == username:
            print(str(user['score']))
            return str(user['score'])
    return "0"


if __name__ == '__main__':
    # Check if the file already exists
    if not path.exists(leaderboard_path):
        # Create an empty dictionary
        data = []
        # Open a file in write mode
        with open(leaderboard_path, 'w') as file:
            # Write an empty dictionary to the file as JSON
            json.dump(data, file)

    app.run(debug=True, port=8080)

import os
from flask import Flask, render_template, request
import json
from google.cloud import storage

from config import LEADERBOARD_PATH, USE_CLOUD_RUN, USE_CLOUD_STORAGE, KEY_PATH, BUCKET_NAME

app = Flask(__name__)


def read_blob(bucket_name, file_name):
    # Get bucket and file objects
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    try:
        # Read contents of the file
        contents = blob.download_as_string()
        return contents

    except:
        print("file does not exist")
        return None


def local_():
    # Check if the file already exists
    if not os.path.exists(LEADERBOARD_PATH):
        # Create an empty dictionary
        data = []
        # Open a file in write mode
        with open(LEADERBOARD_PATH, 'w') as file:
            # Write an empty dictionary to the file as JSON
            json.dump(data, file)


def cloud_storage_():
    data = read_blob(BUCKET_NAME, LEADERBOARD_PATH)
    # Check if the file already exists
    if data is None:
        # Create an empty dictionary
        data = []
        # Open a file in write mode\
    else:
        data = json.loads(data)

    with open(LEADERBOARD_PATH, 'w') as file:
        # Write an empty dictionary to the file as JSON
        json.dump(data, file)


def env_var(cloudFunc, localFunc):
    if USE_CLOUD_STORAGE:
        if not USE_CLOUD_RUN:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = KEY_PATH

        print("cloud")
        cloudFunc()
    else:
        print("local")
        localFunc()


def write_file(data):
    with open(LEADERBOARD_PATH, 'w') as f:
        json.dump(data, f, indent=4)


def write_file_to_cloud(data, bucket_name):
    storage_client = storage.Client()

    # Get bucket and file objects
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(LEADERBOARD_PATH)

    try:
        # If the file already exists in the bucket, download its contents
        contents = json.loads(blob.download_as_string())

        # Update the contents with new or updated entries
        for entry in data:
            for c in contents:
                if c['username'] == entry['username']:
                    if entry['score'] > c['score']:
                        c['score'] = entry['score']
                    break
            else:
                contents.append(entry)

    except:
        # If the file does not exist in the bucket, set contents to the new entries
        contents = data

    # Upload the updated contents to Cloud Storage
    json_data = json.dumps(contents)
    blob.upload_from_string(json_data, content_type='application/json')


def write_local_then_to_gcs(data):
    write_file(data)
    write_file_to_cloud(data, "snake-game")


@app.before_first_request
def do_something():
    env_var(cloud_storage_, local_)
    print("Flask app started!")


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
    # retrieve username and score from request JSON data
    username = request.json['username']
    score = int(request.json['score'])
    entry = {'username': username, 'score': score}

    # check if the user already exists in the leaderboard
    with open(LEADERBOARD_PATH, 'r') as f:
        entries = json.load(f)
    for e in entries:
        if e['username'] == username:
            # if the new score is higher, update the existing entry
            if score > e['score']:
                e['score'] = score
            # otherwise, don't add the entry to the leaderboard
            break  # exit loop once user has been found and updated

    # add the new entry to the leaderboard if user not already in leaderboard
    else:
        entries.append(entry)

    if USE_CLOUD_STORAGE:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = KEY_PATH

        print("cloud")
        write_local_then_to_gcs(entries)
    else:
        print("local")
        write_file(entries)

    # write updated leaderboard to file
    with open(LEADERBOARD_PATH, 'w') as f:
        json.dump(entries, f, indent=4)

    return render_template('snake.html', username=username)


@app.route('/leaderboard')
def leaderboard():
    with open(LEADERBOARD_PATH, 'r') as f:
        entries = json.load(f)
    entries = sorted(entries, key=lambda x: x['score'], reverse=True)
    return render_template('leaderboard.html', entries=entries)


@app.route('/high_score/<username>')
def high_score(username):
    with open(LEADERBOARD_PATH, 'r') as f:
        leaderboard = json.load(f)
    for user in leaderboard:
        if user['username'] == username:
            return str(user['score'])
    return "0"


if __name__ == '__main__':
    app.run(debug=True, port=8080)

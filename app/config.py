import os

USE_CLOUD_STORAGE = os.getenv('USE_CLOUD_STORAGE') == 'true'
USE_CLOUD_RUN = os.getenv('USE_CLOUD_RUN') == 'true'
LEADERBOARD_PATH = './app/leaderboard.json'
KEY_PATH = './app/key.json'
BUCKET_NAME = 'snake-game'

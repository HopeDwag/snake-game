docker build -t snake .

docker run --hostname snake-game \
  -v snake-volume:/data \
  -p 8080:8080 \
  -e USE_CLOUD_STORAGE=true \
  -e USE_CLOUD_RUN=false \
  -e FLASK_DEBUG=1 \
  snake
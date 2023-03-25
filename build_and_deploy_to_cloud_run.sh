gcloud builds submit --tag gcr.io/snake-381016/snake;
gcloud run deploy --image gcr.io/snake-381016/snake snake-flask-app \
    --service-account=806145391654-compute@developer.gserviceaccount.com \
    --update-env-vars=USE_CLOUD_STORAGE=true,USE_CLOUD_RUN=true\
    --region=europe-west1
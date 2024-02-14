gcloud scheduler jobs create http trigger-backup \
  --schedule="0 20 13 2 *" \
  --uri="https://us-central1-proyect-pma.cloudfunctions.net/backup" \
  --http-method="POST" \
  --oidc-service-account-email="proyect-pma@appspot.gserviceaccount.com" \
  --oidc-token-audience="https://us-central1-proyect-pma.cloudfunctions.net/backup" \
  --time-zone="America/Bogota" \
  --location="us-central1"
# RENDER ENVIRONMENT VARIABLES SETUP

To finalize your deployment, you must add these variables to your Render service environment.

## 1. M-Pesa Payment Variables (Required for Payments)
Get these from [Safaricom Developer Portal](https://developer.safaricom.co.ke/)
- `MPESA_CONSUMER_KEY`: (Your Consumer Key)
- `MPESA_CONSUMER_SECRET`: (Your Consumer Secret)
- `MPESA_SHORTCODE`: `174379` (Sandbox)
- `MPESA_PASSKEY`: (Your Passkey)
- `MPESA_CALLBACK_URL`: `https://homekare-we4j.onrender.com/mpesa-callback/`

## 2. Supabase Storage Variables (Required for Images)
This enables persistent images for Hero section and Worker profiles.
Go to **Supabase Dashboard** -> Project Settings -> **Storage**.

enable S3 protocol if you haven't already.

- `USE_S3`: `True`
- `AWS_ACCESS_KEY_ID`: `dba768fd29566190db968caf0d894a96`
- `AWS_SECRET_ACCESS_KEY`: `68d9fc648e212c831aedf6c58a392fb6c7fcd5f7423c6960057a9f79ad2f1031`
- `AWS_STORAGE_BUCKET_NAME`: `media`
- `AWS_S3_ENDPOINT_URL`: `https://rydcrldzlnqmiknuvjpo.supabase.co/storage/v1/s3`
- `AWS_S3_REGION_NAME`: `eu-central-1`

## 3. Deployment Steps
1. **Push your code changes to GitHub.** (This will update the dashboard CSS and storage settings)
2. **Add the variables above** in Render Dashboard -> Environment.
3. **Manual Deploy** (Clear build cache & deploy) to ensure new requirements (`boto3`, etc) are installed.

---
**Note:** If you don't set `USE_S3` to `True` on Render, it will fall back to local (ephemeral) storage, meaning images will disappear on redeploy.

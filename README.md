
## Google Cloud

```sh
gcloud compute instances create dev-micro \
    --project=ilanes \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=firebase-adminsdk-x5uay@ilanes.iam.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --create-disk=auto-delete=yes,boot=yes,device-name=dev-micro,image=projects/debian-cloud/global/images/debian-12-bookworm-v20240415,mode=rw,size=10,type=projects/ilanes/zones/us-central1-a/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any
```

## Pip Env

```sh
python3 -m venv discord

source discord/bin/activate

pip install -r requirements.txt

set -a

cat <<-EOF > .env
DISCORD_BOT_TOKEN=
FIREBASE_WEB_API_KEY=
REFRESH_TOKEN=
DATATURD_API_URL=
EOF
source .env

python app.py
```

## How to get refresh token

```python
import os
import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# From https://console.firebase.google.com/u/0/project/ilanes/authentication/users
user_id = os.getenv('FIREBASE_USER_UID')

# Generate a custom token
custom_token = auth.create_custom_token()

# Firebase API endpoint for exchanging custom tokens for ID tokens
api_url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken'
params = {
    'key': FIREBASE_WEB_API_KEY,
}
data = {
    'token': custom_token,
    'returnSecureToken': True,
    'refreshToken': True,
}

response = httpx.post(api_url, params=params, json=data)
data = response.json()
print(json.dumps(data, indent=2))
```

#!/bin/bash

AUTH0_DOMAIN=dreamkast.us.auth0.com
CLIENT_ID=<CLIENT ID>
CLIENT_SECRET=<CLIENT_SECRET>
AUDIENCE=https://event.cloudnativedays.jp/
TOKEN=$(curl --url https://${AUTH0_DOMAIN}/oauth/token \
  --header 'content-type: application/json' \
  --data "{\"client_id\":\"${CLIENT_ID}\",\"client_secret\":\"${CLIENT_SECRET}\",\"audience\":\"${AUDIENCE}\",\"grant_type\":\"client_credentials\"}" | jq -r .access_token)
DREAMKAST_DOMAIN='event.cloudnativedays.jp'
SLACKURL=<SLACK WEBHOOK URL>

cat <<EOS > <PATH TO ENV FILE>
AUTH0_DOMAIN=${AUTH0_DOMAIN}
CLIENT_ID=${CLIENT_ID}
CLIENT_SECRET=${CLIENT_SECRET}
AUDIENCE=${AUDIENCE}
TOKEN=${TOKEN}
DREAMKAST_DOMAIN=${DREAMKAST_DOMAIN}
SLACKURL=${SLACKURL}
EOS

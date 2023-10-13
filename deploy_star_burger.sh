#!/bin/bash
set -e
cd /opt/star-burger
source .env
docker-compose down
git pull
docker-compose up --build -d
docker-compose exec backend python manage.py migrate --noinput python manage.py collectstatic --noinput python manage.py load_locations
commit_version=$(git rev-parse --verify HEAD)
curl --request POST \
     --url https://api.rollbar.com/api/1/deploy \
     --header "X-Rollbar-Access-Token: $ROLLBAR_TOKEN" \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
        "environment": "risky-wisshorn",
        "revision": "'${commit_version}'",
        "rollbar_username": "ddsomdim"
}
'
echo $'\nSuccessful deployment'

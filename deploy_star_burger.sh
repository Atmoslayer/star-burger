#!/bin/bash
set -e
cd /opt/star-burger
source .env
git pull
docker-compose down --rmi local
docker-compose up --build -d
docker-compose exec backend python manage.py migrate --noinput
docker-compose exec backend python manage.py collectstatic --noinput
docker-compose exec backend python manage.py load_locations
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

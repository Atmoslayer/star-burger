#!/bin/bash
set -e
cd /opt/star-burger
git pull
source venv/bin/activate
source .env
python manage.py collectstatic  --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py load_locations
deactivate
docker-compose restart
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

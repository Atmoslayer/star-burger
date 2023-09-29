#!/bin/bash
set -e
stty -echo
cd /opt/star-burger
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py load_locations
npm ci -dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
deactivate
systemctl restart star-burger.service
commit_version=$(git rev-parse --verify HEAD)
rollbar_token =`sed -n 's/^X-Rollbar-Access-Token=\(.*\)/\1/p' < .env`
curl --request POST \
     --url https://api.rollbar.com/api/1/deploy \
     --header "${rollbar_token}" \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
        "environment": "risky-wisshorn",
        "revision": "'${commit_version}'",
        "rollbar_username": "ddsomdim"
}
'
stty -echo
echo $'\nSuccessful deployment'

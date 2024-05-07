# music_app
It is a music app BUild usine Python and Vue-js


#start the backend 


terminal 1

wsl
cd trisit_music_backend/
python3.10 -m venv venv
pip install -r requirements.txt
python3.10 app.py



terminal 2(ubuntu20.4) for celery

cd trisit_music_backend/
source venv/bin/activate
celery -A app.celery worker -l info




terminal 3(ubuntu20.4) for celery beat

cd trisit_music_backend/
source venv/bin/activate
celery -A app.celery beat -l info





terminal 4(ubuntu20.4) for redis server

redis-server
terminal 5(ubuntu20.4) for mail hog
~/go/bin/MailHog



#starting Frontend



terminal 5(ubuntu20.4)

cd trisit-music_frontend/
npm install
npm install chart.js@^3.0.0
npm run lint && npm run serve
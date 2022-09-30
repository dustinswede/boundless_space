lessc-each ./core/less/core/ ./core/static/core/css/
python3.8 ./local_manage.py makemigrations
python3.8 ./local_manage.py migrate
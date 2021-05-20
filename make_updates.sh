lessc-each ./galaxy/less/galaxy/ ./galaxy/static/galaxy/css/
python3.8 ./local_manage.py makemigrations
python3.8 ./local_manage.py migrate
#!/bin/bash

PROJ_ROOT="$(pwd)/$(dirname $0)/.."

# clean the app, static and media folders
rm -rf ${PROJ_ROOT}/*/migrations
rm -rf ${PROJ_ROOT}/*/__pycache__
rm -rf ${PROJ_ROOT}/*/*/__pycache__
rm -rf ${PROJ_ROOT}/*/*/*/__pycache__

rm -rf ${PROJ_ROOT}/uploads/*
rm -rf ${PROJ_ROOT}/staticfiles/*

# clean mysql tables
python3 clean_mysql.py --drop_all

# initialize new tables
cd ${PROJ_ROOT}
python3 manage.py makemigrations accounts
python3 manage.py makemigrations blog
python3 manage.py makemigrations home
python3 manage.py migrate

# generate test data
cd ${PROJ_ROOT}/test
python3 generate_data.py -c config.json

# launch webserver
cd ${PROJ_ROOT}
python3 manage.py collectstatic
python3 manage.py runserver 127.0.0.1:8000



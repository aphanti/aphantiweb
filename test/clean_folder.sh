#!/bin/bash

PROJ_ROOT="$(pwd)/$(dirname $0)"

# clean the app, static and media folders
rm -rfv ${PROJ_ROOT}/../*/migrations
rm -rfv ${PROJ_ROOT}/../*/__pycache__
rm -rfv ${PROJ_ROOT}/../*/*/__pycache__
rm -rfv ${PROJ_ROOT}/../*/*/*/__pycache__

rm -rfv ${PROJ_ROOT}/../uploads/*
rm -rfv ${PROJ_ROOT}/../staticfiles/*


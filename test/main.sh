#!/bin/bash

PROJ_ROOT="$(pwd)/$(dirname $0)"

# clean the app, static and media folders
rm -rf ${PROJ_ROOT}/*/migrations
rm -rf ${PROJ_ROOT}/*/__pycache__
rm -rf ${PROJ_ROOT}/*/*/__pycache__
rm -rf ${PROJ_ROOT}/*/*/*/__pycache__


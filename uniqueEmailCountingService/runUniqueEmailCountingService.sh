#!/bin/bash

DIR_PATH=`dirname $0`

source $DIR_PATH/findPython

cd ${DIR_PATH}/app

${PYTHON} ./webservice.py


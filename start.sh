#!/bin/bash

# to check whether the venv has been created
pipenv --venv

# if not, create required environment
if [[ $? -eq 1 ]]; then
    pipenv --python python3 install
fi

# start flask task
pipenv run flask run
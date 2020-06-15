#!/bin/sh
set -e

# Install poetry
pip install poetry

# Do not create a virtual env
poetry config virtualenvs.create false
# Install dependencies
poetry install --no-dev --no-interaction --no-ansi

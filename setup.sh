#!/bin/sh
set -e

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"setu+covid-movement@setu.me\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

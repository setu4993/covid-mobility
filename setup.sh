mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"setu4993@yahoo.co.in\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# IngeniumUAHub-Data
Webserver hosting a streamlit application for easier data analytics

# Development
## Setting up environment variables
1) Copy `.env.example` and rename it `.env`
2) Fill in variables, make sure you don't delete any as they are passed in docker_compose.yml

## Running
Via pycharm:
1) Top right 'configuration'
2) Add configuration
3) Docker compose
4) Select `docker_compose.yml` as source
5) Save and run

Via commandline:
```
docker compose up
```

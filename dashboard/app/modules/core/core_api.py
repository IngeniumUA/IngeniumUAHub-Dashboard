import requests

def fetch_user_table():
    return requests.get("https://dev.ingeniumua.be/api/v1/user")
    
# auth/facebook_auth.py

import requests
from flask import session, redirect
from flask import current_app as app
from module import auth_module

def facebook_login():
    return redirect(f"https://www.facebook.com/v12.0/dialog/oauth?client_id={app.config['FB_APP_ID']}&redirect_uri={app.config['FB_REDIRECT_URL']}&scope=email")

def facebook_callback(code):
    user_response = requests.get(
        f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={app.config['FB_APP_ID']}&redirect_uri={app.config['FB_REDIRECT_URL']}&client_secret={app.config['FB_APP_SECRET']}&code={code}"
    )
    data = user_response.json()
    if "access_token" in data:
        session['access_token'] = data['access_token']
        user_response = requests.get(
            f"https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={data['access_token']}"
        )
        user_data = user_response.json()
        return auth_module.checkSNLogin(user_data,2)
        
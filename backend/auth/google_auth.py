# auth/google_auth.py

from flask import session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from module import auth_module

def init_google_oauth(app):
    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id = app.config['GOOGLE_CLIENT_ID'],
        client_secret = app.config['GOOGLE_CLIENT_SECRET'],
        api_base_url = app.config['API_BASE_URL'],
        access_token_url = app.config['ACCESS_TOKEN_URL'],
        authorize_url = app.config['AUTHORIZE_URL'],
        jwks_uri = app.config['JWKS_URI'],
        client_kwargs = app.config['CLIENT_KWARGS']
    )
    return google

def login(google):
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

def authorize(google):
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    return auth_module.checkSNLogin(user_info,1)


class Config:
    # Google 
    SECRET_KEY = '261204'
    GOOGLE_CLIENT_ID = '92641398292-fmt2ikpf97hdpvui4lfskiofjibefo4k.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
    API_BASE_URL = 'https://www.googleapis.com/oauth2/v1/'
    ACCESS_TOKEN_URL = 'https://oauth2.googleapis.com/token'
    AUTHORIZE_URL = 'https://accounts.google.com/o/oauth2/auth'
    JWKS_URI = 'https://www.googleapis.com/oauth2/v3/certs'
    CLIENT_KWARGS={
        'scope': 'openid email profile'
    }
    # Facebook
    FB_APP_ID= "644004361620553"
    FB_APP_SECRET = "b1fc9257b35ab845d702893e089332b6"
    FB_REDIRECT_URL = "http://localhost:5000/facebook/callback"
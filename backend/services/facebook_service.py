import requests
from settings.facebook_config import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_REDIRECT_URI

def exchange_code_for_token(code: str):
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "client_id": FACEBOOK_APP_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "client_secret": FACEBOOK_APP_SECRET,
        "code": code
    }
    res = requests.get(url, params=params).json()
    return res.get("access_token")

def get_pages(user_access_token: str):
    url = "https://graph.facebook.com/v18.0/me/accounts"
    res = requests.get(url, params={"access_token": user_access_token}).json()
    return res.get("data", [])

def subscribe_page_webhook(page_access_token: str):
    url = f"https://graph.facebook.com/v18.0/me/subscribed_apps"
    requests.post(url, params={"access_token": page_access_token})

def send_message_to_user(recipient_id: str, message: str, page_access_token: str):
    url = f"https://graph.facebook.com/v18.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    requests.post(url, params={"access_token": page_access_token}, json=payload)

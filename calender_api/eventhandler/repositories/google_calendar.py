# Dependencies for Calendar API utility
from typing import final
from django.contrib.auth.models import User
import requests
from eventhandler.models import CustomUser, EventTracker
from eventhandler.helpers.base import get_or_create
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from eventhandler.helpers.constants import GoogleKeys

# from base64 import urlsafe_b64decode
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow


def get_consent_url():
    """
    Function prompts google consent window
    Returns:
        string: consent url
    """
    flow = Flow.from_client_secrets_file(
        "eventhandler/helpers/google_credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/calendar.events.readonly",
            "https://www.googleapis.com/auth/gmail.readonly",
        ],
        redirect_uri=GoogleKeys.CALLBACK_URL,
    )

    # Tell the user to go to the authorization URL.
    auth_url, _ = flow.authorization_url(prompt="consent")
    if not auth_url:
        return False, "URL not Found"
    return True, auth_url


def get_consent_callback(access_code):
    """
    Function to get Access token, refresh token, EmailID from redirect URL
    Parameters:
        access code(string):
    Returns:
        Bool, Response(string)
    """
    flow = Flow.from_client_secrets_file(
        "eventhandler/helpers/google_credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/calendar.events.readonly",
            "https://www.googleapis.com/auth/gmail.readonly",
        ],
        redirect_uri=GoogleKeys.CALLBACK_URL,
    )
    token = flow.fetch_token(code=access_code)

    access_token = token.get("access_token")
    print(access_token)
    refresh_token = token.get("refresh_token")
    api_url = f"{GoogleKeys.USER_INFO_URL}{access_token}"
    user_info_response = requests.get(api_url)
    print(user_info_response)
    if user_info_response.status_code != 200:
        return False, "Google User Info not found"
    user_info_data = user_info_response.json()
    user_email = user_info_data.get("emailAddress")
    response = {
        "email": user_email,
        "access_token": access_code,
        "refresh_token": refresh_token,
    }
    return True, response


def create_or_update_user_token(user_info):
    """
    Function creates or updates user token
    Parameters:
        user_info(string)
    Returns:
        bool, user(string)
    """
    email = user_info.get("email")
    creds = {
        "access_token": user_info.get("access_token"),
        "refresh_token": user_info.get("refresh_token"),
    }
    user = get_or_create(CustomUser, email=email)
    if not user:
        return False, "Somethng went wrong while creating user"
    user.google_token = creds
    user.save()
    return True, user


def generate_credential_object(user_email: str):
    """
    Function gnerates credential object
    Parameters:
        user_email
    Returns:
        bool, Credentials(Dict)
    """
    user = CustomUser.objects.filter(email=user_email)
    if not user:
        return False, "User Not Found"
    user = user.first()
    tokens = user.google_token
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    return True, Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=GoogleKeys.TOKEN_URI,
        client_id=GoogleKeys.GOOGLE_CLIENT_ID,
        client_secret=GoogleKeys.GOOGLE_CLIENT_SECRET,
    )


def get_calendar_events_using_google(user_email: str):
    """
    Function gets all calendar events
    Parameters:
        user_email
    Returns:
        bool, events(list)
    """
    success, cred_object = generate_credential_object(user_email=user_email)
    if not cred_object:
        return False, "Invalid Credentials"
    service = build("calendar", "v3", credentials=cred_object)
    success, events = retrieve_events(service=service)
    if not success:
        return success, events
    return True, events


def retrieve_events(service: str):
    """
    Function retrieves all calendar events
    Parameters:
        service
    Returns:
        bool, events(string)
    """
    final_events = {}
    google_calendar_events = (
        service.events()
        .list(calendarId="primary", singleEvents=True, orderBy="startTime")
        .execute()
    )
    google_calendar_events = google_calendar_events.get("items", [])
    if not google_calendar_events:
        return False, "Events Not found"
    for event in google_calendar_events:
        parsed_event = {
            "user_email": event.get("creator").get("email"),
            "event_name": event.get("summary"),
            "description": event.get("description"),
            "location": event.get("location"),
            "html_link": event.get("htmlLink"),
            "start_date": event.get("start").get("dateTime"),
            "end_date": event.get("end").get("dateTime"),
        }
        final_events.update({parsed_event.get("event_name"): parsed_event})
    return True, final_events


def store_events_for_user(user_email: str, final_events):
    """
    Function stores all calendar events for registered user
    Parameters:
        user_email, final_events
    Returns:
        bool, message
    """
    user = CustomUser.objects.filter(email=user_email)
    if not user:
        return False, "User Not Found"
    user = user.first()
    event_tracker_object = EventTracker(user=user, events=final_events)
    event_tracker_object.save()
    return True, f"Events saved successfully for {user.email}"


def get_user_calendar_events(user_email: str):
    """
    Function gets all calendar events for registered user from DB
    Returns:
        bool, events(string)
    """
    user = CustomUser.objects.filter(email=user_email)
    if not user:
        return False, "User Not Found in DB"
    user = user.first()
    event_tracker_object = EventTracker.objects.filter(user=user)
    if not event_tracker_object:
        return False, "EventTracker Not found"
    events = event_tracker_object[0].events
    if not events:
        return False, "Events Not Found"
    return True, events

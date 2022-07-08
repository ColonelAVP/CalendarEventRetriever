from django.urls import path
from .views import GooglecalendarController

urlpatterns = [
    path(
        "rest/v1/calendar/init/",
        GooglecalendarController.get_consent_screen,
        name="google-consent-screen",
    ),
    path(
        "rest/v1/calendar/redirect/",
        GooglecalendarController.get_consent_callback,
        name="google-consent-callback",
    ),
    path(
        "rest/v1/calendar/store-events/",
        GooglecalendarController.fetch_and_store_event,
        name="user-events-fetch-store",
    ),
    path(
        "rest/v1/calendar/get-user-events/",
        GooglecalendarController.get_user_events,
        name="get-user-events",
    ),
]

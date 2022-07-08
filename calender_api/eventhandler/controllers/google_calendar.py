from rest_framework.decorators import api_view
from eventhandler.repositories.google_calendar import (
    get_consent_url,
    create_or_update_user_token,
    get_consent_callback,
    get_calendar_events_using_google,
    store_events_for_user,
    get_user_calendar_events,
)

from eventhandler.helpers.base import (
    SuccessJSONResponse,
    NotFoundJSONResponse,
    BadRequestJSONResponse,
)


class GooglecalendarController:
    @staticmethod
    @api_view(["GET"])
    def get_consent_screen(request):
        """
        The get_consent_screen() API prompts google login consent window
        """
        success, response = get_consent_url()
        if not success:
            return NotFoundJSONResponse(message=response)
        return SuccessJSONResponse(response, message="Url generated succesfully")

    @staticmethod
    @api_view(["GET"])
    def get_consent_callback(request):
        """
        get_consent_callback() API gets a callback url on mentioned redirect url
        """
        access_code = request.GET.get("code")
        success, response = get_consent_callback(access_code=access_code)
        if not success:
            return NotFoundJSONResponse(message=response)
        token_success, token_response = create_or_update_user_token(user_info=response)
        if not token_success:
            return BadRequestJSONResponse(message=token_response)
        return SuccessJSONResponse(message="User google token stored successfully")

    @staticmethod
    @api_view(["POST"])
    def fetch_and_store_event(request):
        """
        fetch_and_store_event() retrieves and stores the calendar events of the user
        """
        post_data = request.data
        user_email = post_data.get("user_email")
        success, response = get_calendar_events_using_google(user_email=user_email)
        if not success:
            return NotFoundJSONResponse(message=response)
        store_success, store_response = store_events_for_user(
            user_email=user_email, final_events=response
        )
        if not store_success:
            return NotFoundJSONResponse(message=store_response)
        return SuccessJSONResponse(message="User Events store successfully")

    @staticmethod
    @api_view(["GET"])
    def get_user_events(request):
        """
        get_user_events() gets all the events from registered user from DB
        """
        user_email = request.GET.get("user_email")
        if not user_email:
            return NotFoundJSONResponse(message="User Email Not Found")
        success, response = get_user_calendar_events(user_email=user_email)
        if not success:
            return BadRequestJSONResponse(message=response)
        return SuccessJSONResponse(response)

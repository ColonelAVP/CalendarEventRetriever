# Calendar Event Retriever
## Task
- Implement google calendarintegration using django rest api. You need to use the OAuth2 mechanism to
get users calendar access. Below are detail of API endpoint and corresponding views which you need to implement
- /rest/v1/calendar/init/ -> GoogleCalendarInitView()
- /rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()

## Concepts Used:
* API Development
* Backend Development
* Data handling

## Tools and Tecnologies Used
* Python/Django
* VSCode
* Django REST Framework
* Postman
* Google Cloud Platform

## API Info
* `rest/v1/calendar/init/` --> Prompts Google Consent Screen
* `rest/v1/calendar/redirect` --> Handles redirect request sent by google with code for token
* `rest/v1/calendar/store-events/` --> Retrieves and stores the calendar events of the user
* `rest/v1/calendar/get-user-events/` --> Gets user events from database

## References
* [Django docs](https://www.djangoproject.com/start/)
* [Django REST Framework docs](https://www.django-rest-framework.org/)
* [Postman API Platform docs](https://learning.postman.com/docs/getting-started/introduction/)
* [Outh 2.0](https://oauth.net/2/)

## Screenshots
* Get-Consent-Screen
![alt_tag](https://raw.githubusercontent.com/ColonelAVP/CalendarEventRetriever/master/Outputs/consent_window.png)
* Stored-Events
![alt_tag](https://raw.githubusercontent.com/ColonelAVP/CalendarEventRetriever/master/Outputs/events_store_in_DB.png)

# Convin.ai Pre-Internship Task

## Task
- Implement google calendarintegration using django rest api. You need to use the OAuth2 mechanism to
get users calendar access. Below are detail of API endpoint and corresponding views which you need to implement
- /rest/v1/calendar/init/ -> GoogleCalendarInitView()
- /rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()

Concepts Used:
* API Development
* Backend Development
* Data handling

Tools and Tecnologies Used
* Python/Django
* VSCode
* Django REST Framework
* Postman
* Google Cloud Platform

API Info
* `rest/v1/calendar/init/` --> Prompts Google Consent Screen
* `rest/v1/calendar/redirect` --> Handles redirect request sent by google with code for token
* `rest/v1/calendar/store-events/` --> Retrieves and stores the calendar events of the user
* `rest/v1/calendar/get-user-events/` --> Gets user events from database

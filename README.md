### Installation
This application requires Python 3.6.4.
1. Clone this repo.
2. Create virtual environment.
3. Activate virtualenv.
```$ source venv/bin/activate```
4. Install all dependencies from requirements.txt.
```$ pip install -r requirements.txt```
5. Fill in API-keys EMAIL_HUNTER_API_KEY and CLEARBIT_API_KEY  in settings.py, if variables ONLY_DELIVERABLE_EMAILS, CLEARBIT_ENRICHMENT_ENABLED set to True.
6. Run migrate to create test SQLite DB.
```$ python manage.py migrate```
7. Run dev server
```$ manage.py runserver ```
### Bot Usage
1. Open another terminal tab and  activate virtualenv.
```$ source venv/bin/activate```
2. Correct *config.json* as you need. Make sure *api_url_address*  points corecctly to the working server.
3. Create fake activity for REST API by running this command. ```$ python bot.py create_activity```


**Bot after successful fake activity**
![bot](https://github.com/ddci/django_rest_social/blob/master/bot.png?raw=true)

**Simple Frontend for viewing the result:**
![bot](https://github.com/ddci/django_rest_social/blob/master/view.png?raw=true)
### REST API Available Endpoints
* /api/users/ — POST request with data fields [*email1*, *email*, *password*, *username*, *first_name (optional)*, *lastname (optional)*] returns 201 code with main info about new user (also Clearbit`s firstName or familyName);
* /api/auth/ — POST request with body [*username*,*password*] returns **JWT** token (Login);

**Next endpoints work only with JWT-token provided in Header with Bearer prefix.**
* /api/posts/ — GET/POST, POST — creates new post entity required data parameters [*title*,*content*], GET  — returns pagable list of posts;
* /api/posts/<post_id>/ — GET returns post;
* /api/posts/<post_id>/likes/ — GET/POST/DELETE, GET returns list of likes, POST/DELETE likes/unlikes post on behalf of the authenticated user;
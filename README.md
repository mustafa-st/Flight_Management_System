# flightmanager-api
<<<<<<< HEAD


=======
>>>>>>> c2e1d8f31768a007a9d605c9c8ac31c9d2b6f0d2

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy flight_manager

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Heroku

See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).

## Requirements
- [X] Models:

    <li>The user model will be extended from the AbstractUser and we will be adding additional property to it (mobile_number)</li>

    <li>Flight Model will consist of following fields:

<ul>origin</ul>
<ul>destination</ul>
<ul>flight number</ul>
<ul>departure date time</ul>
<ul>arrival date time</ul>
<ul>base fare</ul>
<ul>tax </ul></li>
<ul>provider </ul></li>

<li>Airport model will have following feilds:

<ul>iata code (string unique representation of airport)</ul>
<ul>city (string city name)</ul></li>

### The following endpoints are required in the Backend API:

- [X] User Signup
- [X] User Login (JWT authentication class to be use)
- [X] Flight Search (Public) - Flights without prices are visible on this
- [X] Flight Search with prices are available once user hit the same endpoint with login
- [X] Bonus: document all endpoints using Postman.
- [X] Booking API - API endpoint to book flights by "flight_id".
- [X] Providers API - Providers search api that gets flights data from both database and sastaticket staging.

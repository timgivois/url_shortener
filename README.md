URL Shortener
===================
Written by: Tim Givois

Basic python Django skeleton app created for shortening urls. It can easily shorten 1.44555106e17 using 10 letters. It has a Redis cache of urls that gives the shortener a fast performance when retrieving tokens. It also tracks the number of times each token is hit.

Setup & Run
-------------
For python modules installation run:

    pip install -r requirements.txt

Don't forget to run your Redis server, installation on platforms can be found on this [link.](https://redis.io/topics/quickstart)

After we have Redis running and installed Python modules, we should first make the django migration and run them.

    python manage.py makemigrations
    python manage.py migrate

If we want to run our app, we should simply run

    python manage.py runserver

Concept
-------------
This shortener relies on the concept of generating 10 random ascii letters for a new url and store them in Redis. To avoid collisions, we have on Redis both the random token and the url in order to fetch them whenever we get a new url and we want to calculate another random token. MySQL is just used for statistics.
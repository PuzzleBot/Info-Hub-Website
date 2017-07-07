# Info-Hub-Website
A website built using Python-Flask and Javascript, as part of a Computer Networks course. (2015)

The website will not work at the moment, since the database it depends on is no longer running. I will be correcting this soon, but for now just host the static version of the site.


## Hosting the website on localhost

In order to host the website, first make sure that Python-Flask is installed. Installation instructions can be found [here.](http://flask.pocoo.org/)

To host the normal version of the site with complete database and REST functionality, navigate to this directory and use the command "python host_site.py".

To host the static version with no database or REST functionality, replace "host_site.py" with "host_static.py"

The website will then be hosted on 127.0.0.1:5000, which can be accessed using any web browser.


## What is this website?

The website I've built was meant to act as a (really bad) homepage of sorts. It displays various news articles and the latest [xkcd](https://xkcd.com/) webcomic gathered from other websites using REST APIs on the front page, and has another page which allows you to search the New York Time's article database. This was basically the first site I've ever built.
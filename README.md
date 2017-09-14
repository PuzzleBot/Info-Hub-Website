# Info-Hub-Website
A website built using Python-Flask and Javascript, as part of a Computer Networks course. (2015)

Unfortunately, the full site can no longer be hosted due to the fact that the database it relies on no longer exists, and the NYT api key is no longer valid.


## Hosting the website on localhost

In order to host the website, first make sure that Python-Flask is installed. Installation instructions can be found [here.](http://flask.pocoo.org/)

To host the static version with no database or REST functionality, navigate to this directory and use "python host_static.py"

The website will then be hosted on 127.0.0.1:5000, which can be accessed using any web browser.


## What is this website?

The website I've built was meant to act as a (really bad) homepage of sorts. It displays various news articles and the latest [xkcd](https://xkcd.com/) webcomic gathered from other websites using REST APIs on the front page, and has another page which allows you to search the New York Time's article database. This was basically the first site I've ever built.

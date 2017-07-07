from flask import Flask
# Used this source for help with sending input to a server:
# http://stackoverflow.com/questions/10434599/how-can-i-get-the-whole-request-post-body-in-python-with-flask

# Used this source for help with splitting strings using a delimiter:
# http://stackoverflow.com/questions/4717074/splitting-strings-using-a-delimiter-in-python

# Used this as a guideline for HTTP methods:
# https://en.wikipedia.org/wiki/Representational_state_transfer#Example

# Used this to escape URL strings
# http://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python

# Used this to fix a strange bug that popped up concerning unicode characters in search results
# http://stackoverflow.com/questions/15321138/removing-unicode-u2026-like-characters-in-a-string-in-python2-7

from flask import render_template
from flask import url_for
from flask import request
from flask import jsonify
from flask import redirect
from flask import make_response
import os
import json
import urllib
import urllib2
import staticDB

dir = os.getcwd()   # Get the directory the html file is located in

app = Flask(__name__, template_folder=dir)


# Custom python functions
def json_parse(fileNameString):
    inputFile = open(fileNameString, "r", 0)
    fileString = inputFile.read()
    
    testLib = json.loads(fileString)
    inputFile.close()
    
    return testLib


def json_fileToLib(jsonFile):
    fileString = jsonFile.read()

    jsonLib = json.loads(fileString)
    return jsonLib


def libToDataString(jsonLib):
    dataString = 'Search results: \n'
    
    for i in jsonLib["response"]["docs"]:
        if i["web_url"] != None:
            dataString = dataString + 'Source: <a id="urlLink" href="' + i["web_url"] + '">' + i["web_url"] + '</a>\n'
        else:
            dataString = dataString + 'Source: none \n'
        
        if i["abstract"] != None:
            dataString = dataString + 'Abstract: ' + i["abstract"] + '\n'
        else:
            dataString = dataString + 'Abstract: none \n'
        
        if i["pub_date"] != None:
            dataString = dataString + 'Date published: ' + i["pub_date"] + '\n'
        else:
            dataString = dataString + 'Date published: none \n'
        
        dataString = dataString + '\n'
    
    dataString = dataString + '\n' + jsonLib["copyright"]
    return dataString

def getMostPopular(topic):
    urlResponseFile = open('static/staticExamples/mostviewed.json')
        
    NYTlib = json_fileToLib(urlResponseFile)
    
    mostPopularData = NYTlib["results"][0]["abstract"]
    mostPopularData = mostPopularData + '<br>'
    mostPopularData = mostPopularData + '<a id="urlLink" href="' + NYTlib["results"][0]["url"] + '">' + NYTlib["results"][0]["url"] + '</a>'
        
    mostPopularData = mostPopularData.encode('ascii', 'ignore')
    
    mostPopularImage = NYTlib["results"][0]["media"][0]["media-metadata"][2]["url"]
    
    return mostPopularData, mostPopularImage

def getSteamData(appID):

    if appID == '391540':
        urlResponseFile = open('static/staticExamples/undertaleNews.json')
    else:
        urlResponseFile = open('static/staticExamples/terrariaNews.json')

    STEAMlib = json_fileToLib(urlResponseFile)
    
    steamData = STEAMlib["appnews"]["newsitems"][0]["title"]
    steamData = steamData + '<br>'
    steamData = steamData + STEAMlib["appnews"]["newsitems"][0]["contents"]
    steamData = steamData + '<br>'
    steamData = steamData + '<a id="urlLink" href="' + STEAMlib["appnews"]["newsitems"][0]["url"] + '">' + STEAMlib["appnews"]["newsitems"][0]["url"] + '</a>'
    return steamData


def getXKCD(comicNumString):

    urlResponseFile = open('static/staticExamples/xkcd.json')
    XKCDlib = json_fileToLib(urlResponseFile)

    XKCDtitle = XKCDlib["safe_title"]
    XKCDcomic = XKCDlib["img"]
    XKCDflavor = XKCDlib["alt"]

    return XKCDtitle, XKCDcomic, XKCDflavor


@app.route('/unauthorized/')
def badPath():
    return 'ERROR 403: Path traversal unauthorized.'


@app.route('/static/example.json')
def staticJson():
    
    thisFile = open('static/example.json', "r", 0)
    fileString = thisFile.read()
    thisFile.close()
    
    exampleLib = json.loads(fileString);
    
    output = 'Example Search: \n'
    
    for i in exampleLib["response"]["docs"]:
        output = output + 'Source: <a id="urllink" href="' + i["web_url"] + '">' + i["web_url"] + '</a>\n'
        output = output + 'Abstract: ' + i["abstract"] + '\n'
        output = output + 'Date published: ' + i["pub_date"] + '\n'
        output = output + '\n'
    
    output = output + '\n' + exampleLib["copyright"]
    
    return render_template('static/examplePage/TextTemplate.html',input=output)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        mostPopularData, mostPopularImage = getMostPopular('technology')
        XKCDtitle, XKCDcomic, XKCDflavor = getXKCD('0')
        response = app.make_response(render_template('index.html', popData=mostPopularData, popImage=mostPopularImage, undertaleData=getSteamData('391540'), terrariaData=getSteamData('105600'), xkcdTitle=XKCDtitle, xkcdComic=XKCDcomic, xkcdSubtitle=XKCDflavor))
    if request.method == 'POST':
        # The POST method is being used for cookie management. Cookies are passed here to
        # be decrypted and used, or values are passed here to be encrypted and stored.
        if request.form.get("cookieOperation") == 'retrieve_cookie':
            # An encrypted cookie is being passed in to be decrypted.
            currentCookie = request.form.get("cookie")
            cookieColour = staticDB.decryptString(currentCookie)
            response = cookieColour
        elif request.form.get("cookieOperation") == 'set_cookie':
            # A value is being passed in to be encrypted and sent back.
            currentColour = request.form.get("backColour")
            colourCookieString = staticDB.encryptString(currentColour)
            response = colourCookieString
    
    return response


@app.route('/searchPage/', methods=['GET', 'POST'])
def searchPage():
    return render_template(url_for('static', filename='searchInputPage/searchInput.html'))



@app.route('/search/<newsDesk>/<input>', methods=['GET', 'POST'])
def searchPortal(newsDesk, input):
    
    outString = ''
    statusCode = 200
    
    # Format special characters in the URL to prevent errors, also prevents people from typing things like ' IF ' and ' OR '
    # to perform query injections
    queryInput = urllib.quote_plus(input)
    
    if request.method == 'GET':
        # Get search results from either NYT or the database
        outString = staticDB.checkCache(newsDesk, queryInput);
        
        statusCode = 200
    elif request.method == 'POST':
        # outString = 'Entry "' + input + '" created in collection "' + collectionName + '".'
        statusCode = 201
    else:
        outString = 'Unrecognized Method called'
    return render_template('static/searchPage/SearchTemplate.html', input=outString)


@app.route('/search/', methods=['GET', 'POST'])
def searchPortalBlank():
    
    input = ''
    outString = ''
    statusCode = 200
    
    # Format special characters in the URL to prevent errors, also prevents people from typing things like ' IF ' and ' OR '
    # to perform query injections
    queryInput = urllib.quote_plus(input)
    
    if request.method == 'GET':
        # Get search results from either NYT or the database
        outString = staticDB.checkCache('Technology', queryInput);
        
        statusCode = 200
    elif request.method == 'POST':
        # outString = 'Entry "' + input + '" created in collection "' + collectionName + '".'
        statusCode = 201
    else:
        outString = 'Unrecognized Method called'
    return render_template('static/searchPage/SearchTemplate.html', input=outString)



if __name__ == '__main__':
    app.run(debug=True)


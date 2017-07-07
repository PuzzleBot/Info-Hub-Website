# Used this to figure out how to test if an entry exists in a database http://stackoverflow.com/questions/13373843/how-to-check-if-record-exists-with-python-mysqdb

# SQL base code provided and authorized for use by Greg Klotz, major modifications for this application done by me

import urllib
import urllib2
import host_static


def checkCache(newsDesk, queryInput):
    output = ''

    urlResponseFile = open('static/example.json')
        
    NYTlib = host_static.json_fileToLib(urlResponseFile)
    output = host_static.libToDataString(NYTlib)
        
    output = output.encode('ascii', 'ignore')
        
    formattedOutput = urllib.quote(output);
        
    return output


def encryptString(normString):
    
    if normString == 'black':
        encryptedString = 'L4GP0RXC'
    else:
        encryptedString = '7V5AG7FB'

    return encryptedString


def decryptString(encryptedString):
    
    if encryptedString == 'L4GP0RXC':
        normString = 'black'
    else:
        normString = 'navy'

    return normString

# Used this to figure out how to test if an entry exists in a database http://stackoverflow.com/questions/13373843/how-to-check-if-record-exists-with-python-mysqdb

# SQL base code provided and authorized for use by Greg Klotz, major modifications for this application done by me

import urllib
import urllib2
import MySQLdb
import host_site

db = MySQLdb.connect(host="dursley.socs.uoguelph.ca", # our host, do not modify
                     user="tanb", # your username (same as in lab)
                     passwd="0845538", # your password (your student id number)
                     db="tanb") # name of the data base, your username, do not modify

initCur = db.cursor()
initCur.execute("INSERT INTO StringMap (input, output) VALUES ('7V5AG7FB', 'navy')")
initCur.execute("INSERT INTO StringMap (input, output) VALUES ('L4GP0RXC', 'black')")
initCur.close()


def testQuery():
    cur = db.cursor()

    #replace with your own tables once you create some
    cur.execute("INSERT INTO Nytcache (searchText, searchJson) VALUES ('//example//', 'empty')")
    cur.execute("SELECT * FROM Nytcache")


    for row in cur.fetchall() :
        print row[0]

    cur.execute("DELETE FROM Nytcache WHERE searchText='//example//'")

    cur.close()
    print "Database ready"


def checkCache(newsDesk, queryInput):
    output = ''
    cur = db.cursor()
    
    queryInput = str(MySQLdb.escape_string(queryInput))
    
    # If the search data is cached, get it from the database, otherwise pull from NYT
    cur.execute("SELECT * FROM Nytcache WHERE searchText='" + newsDesk + "/" +queryInput + "'")
    if cur.rowcount == 0 :
        apiKey = 'd6bad3c426c4053c7a16278b1267d2f9:6:72986752'
        
        if queryInput == None:
            urlString = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=' + queryInput + '&fq=news_desk:("' + newsDesk + '")&sort=newest' + '&api-key=' + apiKey
        else:
            urlString = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?fq=news_desk:("' + newsDesk + '")&sort=newest' + '&api-key=' + apiKey
        
        urlResponseFile = urllib2.urlopen(urlString)
        
        NYTlib = host_site.json_fileToLib(urlResponseFile)
        output = host_site.libToDataString(NYTlib)
        
        output = output.encode('ascii', 'ignore')
        
        formattedOutput = urllib.quote(output);
        
        # Store the search input and the formatted search results from the search
        cur.execute("INSERT INTO Nytcache (searchText, searchJson) VALUES ('" + newsDesk + "/" +queryInput + "', '" + formattedOutput + "')")
        
        print "Entry retrieved from NYT successfully"
    else :
        output = urllib.unquote(cur.fetchall()[0][1])
        print "Entry retrieved from cache successfully"
    
    cur.close()
    return output


def encryptString(normString):
    cur = db.cursor()
    
    # Default: black
    if normString == None:
        normString = 'black'
    
    normString = str(MySQLdb.escape_string(normString))
    cur.execute("SELECT input FROM StringMap WHERE output='" + normString + "'")
    
    if cur.rowcount == 0:
        encryptedString = 'L4GP0RXC'
    else:
        encryptedString = cur.fetchall()[0][0]
    
    cur.close()
    return encryptedString


def decryptString(encryptedString):
    cur = db.cursor()
    
    # Default: black
    if encryptedString == None:
        encryptedString = 'L4GP0RXC'
    
    encryptedString = str(MySQLdb.escape_string(encryptedString))
    cur.execute("SELECT output FROM StringMap WHERE input='" + encryptedString + "'")
    
    if cur.rowcount == 0:
        normString = 'black'
    else:
        normString = cur.fetchall()[0][0]
    
    cur.close()
    return normString

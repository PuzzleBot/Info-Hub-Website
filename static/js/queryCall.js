/*Used this for help with status codes: http://stackoverflow.com/questions/2955947/how-do-i-get-the-http-status-code-with-jquery*/

function successGet(outData, status){

}

/*Unused in this iteration*/
function callGet(){
    var urlString;
    
    /*Get input from text fields*/
    var searchInput = document.getElementById("searchField").value;
    
    urlString = '/redirect?input=' + searchInput;
    document.getElementById("getButton").href = urlString;

    /*Deny an empty collection field or a collection field only containing spaces
      Use .trim to reduce a string containing only whitespace into an empty string*/
     
    if(!searchInput.trim()){
        document.getElementById("statusText").innerHTML = 'Please enter search terms.';
    }
    else{
        jQuery.ajax({
                    url: urlString,
                    type: 'GET',
                    success: successGet,
                    statusCode: {
                        200: function(response){
                            document.getElementById("statusText").innerHTML = '200: OK'
                        },
                        201: function(response){
                            document.getElementById("statusText").innerHTML = '201: Created'
                        },
                        304: function(response){
                            document.getElementById("statusText").innerHTML = '304: Not Modified'
                        },
                        400: function(response){
                            document.getElementById("statusText").innerHTML = '400: Bad Request'
                        },
                        401: function(response){
                            document.getElementById("statusText").innerHTML = '401: Unauthorized'
                        },
                        404: function(response){
                            document.getElementById("statusText").innerHTML = '404: Not Found'
                        }
                    }
                    });
    }
}

function processPostColourResponse(outData, status){
    document.cookie = "branTanBackColour=" + outData + ";";
}

function processRetrColourResponse(outData, status){
    updateColour(outData);
}

function postBackColour(colourString){
    /* If the user decided to change the colour of the page, let the server know and
       give back a new encrypted cookie */
    jQuery.ajax({
                url: '/',
                type: 'POST',
                data: { backColour: colourString, cookieOperation: 'set_cookie' },
                success: processPostColourResponse
                });
}

function retrieveBackColour(colourCookie){
    /* If the user is visiting the page, give the server the colour cookie they have
       and tell the user's client what colour the background should be */
    jQuery.ajax({
                url: '/',
                type: 'POST',
                data: { cookie: colourCookie, cookieOperation: 'retrieve_cookie' },
                success: processRetrColourResponse
                });
}

function updateSearchBtnLink(){
    var urlString;
    
    /*Get input from text fields*/
    var searchInput = document.getElementById("searchField").value;
    var newsDesk = document.getElementById("deskMenu").value;
    
    if(!searchInput.trim()){
        urlString = '/search/'
        /*document.getElementById("statusText").innerHTML = 'Please enter search terms.';*/
    }
    else{
        urlString = '/search/' + newsDesk + '/' + searchInput;
        
        /*Check for an attempted path traversal in the search field*/
        if((searchInput.indexOf('/') > -1) || (searchInput.indexOf('.') > -1)){
            urlString = '/unauthorized/';
        }
        
        document.getElementById("getButton").href = urlString;
    }
    
}

function formInputURL(url, input){
    var fullURL = url + '?input=' + input;
    return formInputURL;
}


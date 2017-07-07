/* Used this guide for cookies: http://www.w3schools.com/js/js_cookies.asp 
   Used this for changing the background colour: http://www.w3schools.com/jsref/prop_style_backgroundcolor.asp
   Used this guide for cookies: http://www.w3schools.com/js/js_cookies.asp*/


/* Automatically sets the associated cookie whenever the colour changes */
function updateColour(backColourString){
    if(backColourString == 'navy'){
        document.body.style.backgroundColor = "#242E48";
        document.getElementById("navyRadio").checked = 'checked';
        postBackColour(backColourString);
    }
    else{
        /*Default: Black*/
        document.body.style.backgroundColor = "#555";
        document.getElementById("blackRadio").checked = 'checked';
        postBackColour('black');
        
    }
}


/* Sets the colour of the background based on the cookie */
function getColourCookie(){
    var cookieVarList = document.cookie.split(";");
    var currentVar;
    var splitCurrentVar;
    var colourVal;
    var i;
    
    for(i = 0; i < cookieVarList.length; i++){
        currentVar = cookieVarList[i];
        splitCurrentVar = currentVar.split("=");
        
        /*splitCurrentVar: Index 0 holds the name, index 1 holds the value*/
        if(splitCurrentVar[0] == "branTanBackColour"){
            retrieveBackColour(splitCurrentVar[1])
        }
    }
}
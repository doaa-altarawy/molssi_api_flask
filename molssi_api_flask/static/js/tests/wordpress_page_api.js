jQuery(function(){

  function getData(){
    console.log("Calling MolSSI APIs, getJSON version-------");
    jQuery.getJSON(
            //"http://api.molssi.org/test",
            "http://localhost:5000/test?callback=?",
            function(response){
                console.log("In processData..");
                console.log(response.msg);
              }
    );
  } // getData

  jQuery('#api-link').click(getData);


}); // jQuery function

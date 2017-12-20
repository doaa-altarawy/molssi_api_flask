// jQuery(document).ready(function(){
jQuery(function(){

  window.processData = function(response) {
    console.log("In processData..");
    console.log(response.msg);
  };

  function getData(){
    console.log("Calling MolSSI APIs, AJAX version-----");
    var response = jQuery.ajax({
            type: "GET",
            //url: "http://api.molssi.org/test",
            url: "http://localhost:5000/test",
            //async: false,
            dataType: "jsonp",
            data: {},
            jsonpCallback: "processData",
            success: function(data){
                //console.log("Success..., Data:", data);
            },
            fail: function(data){
                //console.error('Error ', data);
            }
        });
  }

  jQuery('#api-link2').click(getData);

}); // jQuery function

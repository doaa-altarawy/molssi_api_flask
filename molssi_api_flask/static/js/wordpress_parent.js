// <iframe id="pageContent" width="100%" height="4000px" src="http://api.molssi.org/resources_website" frameborder="0"></iframe>
function handleMessage(event) {
  var apiOrigins = ['http://api.molssi.org', 'http://localhost:5000'];
  if (jQuery.inArray(event.origin, apiOrigins)) {
    console.log("Event:", event);
    jQuery('#pageContent').get(0).height = event.data + 'px';   // adjust height
  } else{
  	console.error('Unknown origin', event.origin);
  }
}
window.onload = function() {
  window.addEventListener("message", handleMessage, false);
  console.log('this is Main wordpress Page at: ', location.host);
}

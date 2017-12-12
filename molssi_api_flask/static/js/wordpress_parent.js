// <iframe id="pageContent" width="100%" height="4000px" src="http://api.molssi.org/resources_website" frameborder="0"></iframe>
function handleMessage(event) {
    var apiOrigins = ['http://api.molssi.org', 'http://localhost:5000'];
    if (jQuery.inArray(event.origin, apiOrigins)) {
        console.log("Event from iframe:", event.data['task']);
        if (event.data['task'] == 'resize') {
            jQuery('#pageContent').get(0).height = event.data['height'] + 'px';   // adjust height
        }else if (event.data['task'] == 'scroll_top'){
            window.scrollTo(0,0);
        }
    } else{
        console.error('Unknown origin', event.origin);
    }
}
window.onload = function() {
    window.addEventListener("message", handleMessage, false);
    console.log('this is Main wordpress Page at: ', location.host);
}

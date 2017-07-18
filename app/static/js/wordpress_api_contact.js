jQuery(document).ready(function() {

    console.log("Calling Contcat api");

    // load JSON data and fill the template
    jQuery.getJSON(
        // window.API_DOMAIN +"/contact?callback=?",
        window.API_DOMAIN + "/contact",
        function(data) {
            console.log("In getJSON contact..", data);

            // Load the template
            jQuery.get(window.API_DOMAIN + '/static/templates/contact.mst',
                function(template) {
                    // var template = jQuery('#templates').html();
                    console.log("Rendering Template contact-------");
                    // console.log("The Template is: ", template);
                    var rendered = Mustache.render(template, {
                        'contacts': data
                    });
                    // console.log('rendered is: ', rendered);
                    jQuery('#contacts').html(rendered);

                    show_pages();
                }); // get template

            function show_pages() {
                /** show correct slice of the results based on
                    current active page
                **/
                var items = jQuery("#contacts section");
                //console.log(items);
                var numItems = items.length;
                var perPage = 5;
                // Only show the first `per_page` items initially.
                items.slice(perPage).hide();

                //Pagination:
                jQuery('#pagination').twbsPagination({
                    totalPages: Math.ceil(numItems / perPage),
                    itemOnPage: perPage,
                    visiblePages: 7,
                    onPageClick: function(event, pageNumber) {
                        var showFrom = perPage * (pageNumber - 1);
                        var showTo = showFrom + perPage;
                        // first hide everything...
                        items.hide()
                            // ... and then only show the appropriate rows.
                            .slice(showFrom, showTo).show();
                        // Scroll to the top!
                        //window.scrollTo(0, 0);
                    }
                });

            } // show_pages

            function sendResizeToParent() {
                var cur_height = jQuery('#page_wrapper').outerHeight(true) + 100 +
                    jQuery('#advancedSearch').outerHeight(true);
                console.log("Current hight inside getJSON: ", cur_height);
                var parentOrigin = window.WORDPRESS_DOMAIN;
                parent.postMessage(cur_height, parentOrigin);
            }

            setTimeout(sendResizeToParent, 2000);

        }); // getJSON

}); // document ready

jQuery(document).ready(function() {

    function sendResizeToParent() {
        var cur_height = jQuery('#page_wrapper').outerHeight(true) + 100 +
            jQuery('#advancedSearch').outerHeight(true);
        console.log("Current hight sendResizeToParent: ", cur_height);
        var parentOrigin = window.WORDPRESS_DOMAIN;
        parent.postMessage(cur_height, parentOrigin);
    }

    function show_pages() {
        /** show correct slice of the results based on
            current active page
        **/
        var items = jQuery("#results section");
        var numItems = items.length;
        var perPage = 7;
        // Only show the first `per_page` items initially.
        items.slice(perPage).hide();
        jQuery('p#results_count').html(numItems + ' results found');
        //Pagination:
        jQuery('#pagination').twbsPagination('destroy');  // reset previous
        if (numItems == 0){
            return;
        }
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

    // keyup search
    jQuery('#libraryName').keyup(function(event) {
        jQuery('#search_quick').trigger('click');
    });

    // add action listener
    jQuery('#search_quick, #search_adv').click(function(event) {
        jQuery('#advancedSearch').collapse('hide');
        console.log('Form submitted');
        event.preventDefault();

        // Get search parameters:
        var query_text = jQuery('#libraryName').val();
        var domain = jQuery('#domain').find(":selected").val();
        var price = jQuery('#price').find(":selected").val();
        var languages = [];
        jQuery.each(jQuery("#languages input:checked"), function(){
            languages.push.apply(languages,jQuery(this).val().split(','));
        });
        if (languages.indexOf('') != -1){
            languages = [];     // set to any language
        }
        var data = {
                query_text: query_text,  // TODO: check escaping
                domain: domain,
                languages: JSON.stringify(languages),
                price: price,
            };
        console.log('Query data: ', data);

        // query the server and show the results
        jQuery.ajax({
            // window.API_DOMAIN +"/contact?callback=?",
            url: window.API_DOMAIN + "/search",
            data: data,
            contentType: "application/json",
            //dataType: "json", # return is not JSON
            success: function(data) {             // callback
                //console.log("Returned html data", data);
                jQuery('#results').html(data);

                show_pages();

                setTimeout(sendResizeToParent, 2000);

            } // success
        }); // ajax
    });

    jQuery('#clear_search').on('click', function (e) {
        event.preventDefault();

        jQuery('#libraryName').val('');
        jQuery("#domain")[0].selectedIndex = 0;
        // unselect all languages, use prop. attr is deprecated in jQuery 1.6+
        jQuery('#languages input').prop('checked', false);
        jQuery('#languages input:first').prop('checked', true);
        jQuery('#price')[0].selectedIndex = 0;


        jQuery('p#results_count').html('');
        jQuery('#results').html('');
        jQuery('#pagination').twbsPagination('destroy');
    });
}); // document ready

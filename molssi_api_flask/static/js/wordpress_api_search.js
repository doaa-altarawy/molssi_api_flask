jQuery(document).ready(function() {

    function sendResizeToParent() {
        var cur_height = jQuery('#page_wrapper').outerHeight(true) + 100 +
            jQuery('#advancedSearch').outerHeight(true);
        console.log("Current hight inside getJSON: ", cur_height);
        var parentOrigin = window.WORDPRESS_DOMAIN;
        parent.postMessage(cur_height, parentOrigin);
    }

    function show_pages() {
        /** show correct slice of the results based on
            current active page
        **/
        var items = jQuery("#contacts section");
        var numItems = items.length;
        var perPage = 5;
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
        var query = $('#libraryName').val();
        var domain = $('#domain').find(":selected").val().split(',');
        var languages = [];
        $.each($("#languages input:checked"), function(){
            languages.push.apply(languages,$(this).val().split(','));
        });
        if (languages.indexOf('Any') != -1){
            languages = [];     // set to any langauge
        }
        var data = {
                query: query,
                domain: JSON.stringify(domain),
                languages: JSON.stringify(languages)
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
                console.log("Returned html data", data);
                jQuery('#contacts').html(data);

                show_pages();

                setTimeout(sendResizeToParent, 2000);

            } // success
        }); // ajax
    });

}); // document ready

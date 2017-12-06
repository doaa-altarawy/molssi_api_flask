jQuery(document).ready(function() {

    function send_scroll_to_parent(){
        var parentOrigin = window.WORDPRESS_DOMAIN;
        parent.postMessage({'task': 'scroll_top'}, parentOrigin);
    }

    function send_resize_to_parent() {
        var search_height = jQuery('#advancedSearch').outerHeight(true);
        if (! search_height) { search_height = 0; }
        var cur_height = jQuery('#page_wrapper').outerHeight(true) + 100 + search_height;
        console.log("Current hight sendResizeToParent: ", cur_height);
        var parentOrigin = window.WORDPRESS_DOMAIN;
        parent.postMessage({'task': 'resize', 'height': cur_height}, parentOrigin);
    }

    window.onload = search(true);

    function show_pages() {
        /** show correct slice of the results based on
            current active page
        **/
        var items = jQuery('#results').find('section');
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

        search(true);

    });

    function search(scroll_top) {
        // Get search parameters:
        var query_text = jQuery('#libraryName').val();
        var domain = jQuery('#domain').find(":checked").val();
        var price = jQuery('#price').find(":selected").val();
        var languages = [];
        jQuery.each(jQuery('#languages').find('input:checked'), function(){
            languages.push.apply(languages, jQuery(this).val().split(','));
        });
        if (languages.indexOf('') != -1){
            languages = [];     // set to any language
        }

        // QM Filters
        var qm_filters = {};
        if (domain == 'QM') {
            if (jQuery('#basis').find(":selected").val()) {
                qm_filters['basis'] = jQuery('#basis').find(":selected").val();
            }

            if (jQuery('#coverage').find(":selected").val()) {
                qm_filters['coverage'] = jQuery('#coverage').find(":selected").val();
            }

            if (jQuery('#qm_tags').find(":selected").val()) {
                qm_filters['tags'] = jQuery('#qm_tags').val();
            }
        } // QM domain
        else if (domain == 'MM') {
            // MM filters
            var mm_filters = {};
            if (jQuery('#file_formats').find(":selected").val()) {
                mm_filters['file_formats'] = jQuery('#file_formats').val();
            }
            if (jQuery('#ensembles').val()) {
                mm_filters['ensembles'] = jQuery('#ensembles').val();
            }
            if (jQuery('#qm_mm').find(":selected").val()) {
                mm_filters['qm_mm'] = jQuery('#qm_mm').find(":selected").val();
            }
            if (jQuery('#mm_tags').find(":selected").val()) {
                mm_filters['tags'] = jQuery('#mm_tags').val();
            }
        } // MM domain

        var data = {
                query_text: query_text,  // TODO: check escaping
                domain: domain,
                languages: JSON.stringify(languages),
                price: price,
                qm_filters: JSON.stringify(qm_filters),
                mm_filters: JSON.stringify(mm_filters)
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

                if (scroll_top){
                    send_scroll_to_parent();
                }
                setTimeout(send_resize_to_parent, 1500);

            } // success
        }); // ajax
    } // search


    jQuery('#domain').change(function () {
        var domain = jQuery('#domain').find(":checked").val();

        if (domain == 'MM'){
            jQuery('#mm_search_form').show();
            jQuery('#qm_search_form').hide();
        } else if (domain == 'QM') {
            jQuery('#mm_search_form').hide();
            jQuery('#qm_search_form').show();
        } else {
            jQuery('#mm_search_form').hide();
            jQuery('#qm_search_form').hide();
        }

    });

    jQuery('#languages').change(function (e) {
        var lang = jQuery(event.target);

        if (lang.val() && lang.prop('checked')) {
            jQuery('#languages').find('input:first').prop('checked', false);
        }
        else if (lang.val() && lang.prop('checked')) {
            jQuery('#languages').find('input').not(':first').prop('checked', false);
        }
    });

    function clear_search_panels(){
        // Clear basic and advanced search
        jQuery('#libraryName').val('');
        jQuery('#domain').find('input:radio:first').prop('checked', true);
        // unselect all languages, use prop. attr is deprecated in jQuery 1.6+
        jQuery('#languages').find('input').not(':first').prop('checked', false);
        jQuery('#languages').find('input:first').prop('checked', true);
        jQuery('#price')[0].selectedIndex = 0;

        jQuery('#mm_search_form').hide();
        jQuery('#qm_search_form').hide();

        jQuery('p#results_count').html('');
        jQuery('#results').html('');
        jQuery('#pagination').twbsPagination('destroy');


        // Clear MM search panel
        jQuery('#file_formats').selectpicker('deselectAll');
        jQuery('#ensembles').val('');
        jQuery('#qm_mm').val('');
        jQuery('#mm_tags').selectpicker('deselectAll');

        // Clear QM search panel
        jQuery('#basis').val('');
        jQuery('#coverage').val('');
        jQuery('#qm_tags').selectpicker('deselectAll');
    }

    jQuery('#clear_search').on('click', function (e) {
        event.preventDefault();

        clear_search_panels();
    });

}); // document ready

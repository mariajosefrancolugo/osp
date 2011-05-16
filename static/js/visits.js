function visit_paging(page) {
    $.ajax({
        url: base_url + 'visits/' + student + '/page/' + page + '/',
        success: function(data) {
            $("div#visits-animate").fadeOut('fast', function() {
                    $("div#visits-animate").html(data);
                });
            $("div#visits-animate").fadeIn('fast', function() {
                $("div#visit-paging a").each(function(index) {
                    $(this).click(function() {
                        visit_paging($(this).attr("page"));
                    });
                });
            });
        }
    });
}

$(function(){
    $("div#visit-paging a").each(function(index) {
        $(this).click(function() {
            visit_paging($(this).attr("page"));
        });
    });
});

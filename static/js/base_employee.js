$(function() {
    $('#id_query').focus(function() {
        if($(this).val() == 'search for student') {
            $(this).val('');
        }
    });
    $('#id_query').blur(function() {
        if($(this).val() == '') {
            $(this).val('search for student');
        }
    });

    $('#id_query').autocomplete({
        source: base_url + 'search/',
        minLength: 2,
        select: function(event, ui) {
            location.href = base_url + 'profile/' + ui.item.id;
        },
        position: {
            offset: '0 3'
        }
    });
});

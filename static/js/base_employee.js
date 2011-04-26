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
});

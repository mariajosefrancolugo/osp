$(function() {
    // Hard-coded string... Maybe re-work this
    $('#id_query').focus(function() {
        if ($(this).val() == 'search for student') {
            $(this).val('');
        }
    }).blur(function() {
        if ($(this).val() == '') {
            $(this).val('search for student');
        }
    }).autocomplete({
        source: base_url + 'search/',
        minLength: 2,
        select: function(event, ui) {
            // Hard-coded path... Maybe re-work this as well
            location.href = base_url + 'profile/' + ui.item.id;
        },
        position: {
            offset: '0 -1'
        }
    }).bind('paste', null, function(e) {
        if (!e.keyDown) {
            $(this).trigger('keydown');
        }
    }).data('autocomplete')._renderItem = function(ul, item) {
        return $('<li></li>')
               .data('item.autocomplete', item)
               .append('<a>' + item.label + '<br />' +
                       '<em style="color: grey;">ID Number: ' + item.desc  +
                       '</em>' + '</a>')
               .appendTo(ul);
    }
    
    $('#header form').submit(function() {
        return false;
    });
});

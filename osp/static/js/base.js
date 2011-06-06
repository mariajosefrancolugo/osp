$(function() {
    // Hard-coded paths aren't great... Maybe re-work this in the future
    var divider = "url('" + base_url + "static/img/navigation_divider.png')";

    $('#navigation ul.menu li:has(ul.submenu)').hover(function() {
        $(this).addClass('has-submenu');
        $(this).children('a.menu-link').css('background-image', 'none');
        $(this).prev('li').children('a.menu-link').css('background-image', 'none');
        $(this).children('ul').show();
    }, function() {
        $(this).removeClass('has-submenu');
        $(this).children('a.menu-link').css('background-image', divider);
        $(this).prev('li').children('a.menu-link').css('background-image', divider);
        $(this).children('ul').hide();
    });

    $('input[type=button], input[type=submit], input[type=reset]').button();

    $('.error').each(function() {
        $(this).addClass('ui-state-error ui-corner-all');
        $(this).append('<span class="ui-icon ui-icon-alert"></span>');
    });
});

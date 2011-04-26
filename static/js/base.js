$(function() {
    $('#navigation ul li:has(ul)').hover(function() {
        $(this).addClass('has-submenu');
        $(this).prev('li').children('a.menu-link').css('background-image', 'none');
        $(this).children('ul').show();
    }, function() {
        $(this).removeClass('has-submenu');
        $(this).prev('li').children('a.menu-link').css('background-image', divider);
        $(this).children('ul').hide();
    });
});

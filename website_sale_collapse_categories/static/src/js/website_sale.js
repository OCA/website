$(document).ready(function () {
    $('#o_shop_collapse_category').on('click', '.fa-chevron-right',function(){
        $(this).parent().siblings().find('.fa-chevron-down:first').click();
        $(this).parents('li').find('ul:first').show('normal');
        $(this).toggleClass('fa-chevron-down fa-chevron-right');
    });

    $('#o_shop_collapse_category').on('click', '.fa-chevron-down',function(){
        $(this).parent().find('ul:first').hide('normal');
        $(this).toggleClass('fa-chevron-down fa-chevron-right');
    });
});

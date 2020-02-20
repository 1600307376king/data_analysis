$(function () {
    // nav收缩展开
    $('.inner-li').on('click', function () {
        var parent = $(this).parent().parent();//获取当前页签的父级的父级
        var labeul = $(this).parent("li").find(">ul");
        if ($(this).parent().hasClass('open') === false) {
            //展开未展开
            $(this).css("border-left", "4px solid #08DCD2");
            $(this).find("#menuIcon").removeClass("glyphicon glyphicon-menu-left");
            $(this).find("#menuIcon").addClass("glyphicon glyphicon-menu-down");
            parent.find('ul').slideUp(300);
            parent.find("li").removeClass("open");
            parent.find('li a').removeClass("active").find(".arrow").removeClass("open");
            $(this).parent("li").addClass("open").find(labeul).slideDown(300);
            $(this).addClass("active").find(".arrow").addClass("open")
        } else {
            $(this).css("border-left", "");
            $(this).find("#menuIcon").removeClass("glyphicon glyphicon-menu-down");
            $(this).find("#menuIcon").addClass("glyphicon glyphicon-menu-left");
            $(this).parent("li").removeClass("open").find(labeul).slideUp(300);
            if ($(this).parent().find("ul").length > 0) {
                $(this).removeClass("active").find(".arrow").removeClass("open")
            } else {
                $(this).addClass("active")
            }
        }
    });
});
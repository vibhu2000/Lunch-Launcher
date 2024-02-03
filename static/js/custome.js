$(document).ready(function () {
    // scrolling -----------------------
    $(document).ready(function () {
        let scroll_link = $('.scroll');
    });
    //sticky menu while scrolling -----------------------
    window.onscroll = function () { myFunction() };

    var navbar = document.getElementById("navbar");
    var sticky = navbar.offsetTop;

    function myFunction() {
        if (window.pageYOffset >= 1) {
            navbar.classList.add("sticky")
        }
        else {
            navbar.classList.remove("sticky");
        }
    }
});
(function ($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function (e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    $(".barshown").toggleClass("d-none");
    $("#sidebarToggle").toggleClass("showarrow")
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });
  //Toggle the edit for the Number of tweets

  $("#toggleEdit").click(function () {
    $("#showEdit").toggle('fast');
    $("#showTotal").toggle('fast');
    $("#toggleEdit").toggle('fast');
  });
 //Toggle table view
 $("#toggleTable").click(function (){
  $("#tableall").toggle('fast');
  $("#opent").toggle('fast');
  $("#close").toggle('fast');
 })
  //Alter shown wordcloud
  $.fn.editCloud = function (def) {
    //Negative
    if (def == "n") {
      $("#blockwc").css("border-left", "")
      $("#blockwc").css("border-left", "0.25rem solid red")
      $("#wctitle").text("Words from negative tweets");
      $("#wcimg").attr("src", "/static/website/img/wc_n.jpg");
      $("#wcimg").attr("alt", "Word Cloud Negative");
    }
    //Uncsure
    if (def == "u") {
      $("#blockwc").css("border-left", "")
      $("#blockwc").css("border-left", "0.25rem solid #f6c23e")
      $("#wctitle").text("Words from neutral tweets");
      $("#wcimg").attr("src", "/static/website/img/wc_u.jpg");
      $("#wcimg").attr("alt", "Word Cloud Unsure");
    }
    //Positive
    if (def == "p") {
      $("#blockwc").css("border-left", "")
      $("#blockwc").css("border-left", "0.25rem solid #1cc88a")
      $("#wctitle").text("Words from positive tweets");
      $("#wcimg").attr("src", "/static/website/img/wc_p.jpg");
      $("#wcimg").attr("alt", "Word Cloud Positive");
    }
  }
  $("input[name='wc']").click(function () {
    let def = ($(this).val())
    // Do something interesting here
    $.fn.editCloud(def)
  });
  //On REady
  $(document).ready(function () {
    //Set default wordcloud
    var def = ($('#max').text()).trim();
    $.fn.editCloud(def)
    var $radios = $('input:radio[name=wc]');
    if ($radios.is(':checked') === false) {
      let output = '[value=' + def +  ']';
      $radios.filter(output).prop('checked', true).trigger("click");
    }


  });
  $(document).ready(function () {
    //Table colors

    let allCells = $("#valrow > td");

    $.each(allCells, function (index, child) {
      if (Number(child.textContent) > 0.55) {
        $(child).css("color", "green");
      }
      if (Number(child.textContent) < 0.45) {
        $(child).css("color", "red");
      }
      if (Number(child.textContent) > 0.45 && Number(child.textContent) < 0.55) {
        $(child).css("color", "#f6c23e");
      }

    });

  });
  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function () {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };

    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function (e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function () {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function (e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict

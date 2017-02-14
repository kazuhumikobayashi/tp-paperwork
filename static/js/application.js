function pluginExists(pluginName) {
    return $.fn[pluginName] != undefined;
}

$(function () {

    /*-- データテーブル --*/
    if (!pluginExists("dataTable")) {
        return;
    }

    $.extend( $.fn.dataTable.defaults, {
        language: {
            url: "/static/vendor/DataTables-1.10.13/media/i18n/Japanese.json"
        }
    });

    $('.data-table').DataTable({
      "displayLength": 5,
      "paging": true,
      "lengthChange": false,
      "searching": false,
      "ordering": true,
      "info": true,
      "autoWidth": false,
      "drawCallback": function () {
        $('.dataTables_paginate > .pagination').addClass('pagination-sm');
      }
    });
});

$(function () {

  /*-- iCheck --*/
  if (!pluginExists("iCheck")) {
      return;
  }

  $('input').iCheck({
    checkboxClass: 'icheckbox_square-purple',
    radioClass: 'iradio_square-purple',
    increaseArea: '20%' // optional
  });
});

$(function () {
  /*-- カレンダー --*/
  if (!pluginExists("datepicker")) {
    return;
  }

  $('.date').datepicker({
    format: "yyyy/mm/dd",
    language: "ja",
    autoclose: true,
    todayHighlight: true
  });
});

$(function () {

  /*-- Select2 --*/
  if (!pluginExists("select2")) {
    return;
  }

  $(".select2").select2({
    placeholder: "選択してください",
    allowClear: true
  });

});


$(function () {
  var slideToTop = $("<div />");
  slideToTop.html('<i class="fa fa-chevron-up"></i>');
  slideToTop.css({
    position: 'fixed',
    bottom: '20px',
    right: '25px',
    width: '40px',
    height: '40px',
    color: '#eee',
    'font-size': '',
    'line-height': '40px',
    'text-align': 'center',
    'background-color': '#222d32',
    cursor: 'pointer',
    'border-radius': '5px',
    'z-index': '99999',
    opacity: '.7',
    'display': 'none'
  });
  slideToTop.on('mouseenter', function () {
    $(this).css('opacity', '1');
  });
  slideToTop.on('mouseout', function () {
    $(this).css('opacity', '.7');
  });
  $('.wrapper').append(slideToTop);
  $(window).scroll(function () {
    if ($(window).scrollTop() >= 150) {
      if (!$(slideToTop).is(':visible')) {
        $(slideToTop).fadeIn(500);
      }
    } else {
      $(slideToTop).fadeOut(500);
    }
  });
  $(slideToTop).click(function () {
    $("body,html").animate({
      scrollTop: 0
    }, 500);
  });
});

$(function () {
  $('input,select,textarea').each(function(){
    $(this)
      .focusin(function(element) {
        $(this).addClass('bg-light-yellow');
      })
      .focusout(function(element) {
        $(this).removeClass('bg-light-yellow');
      });
  });

  $('.message-area').delay(4000).fadeOut();

});

var MessageBox = (function () {
  "use strict";

  var hideHandler, that = {};

  var wrapper_css = {
    "background": "#7986CB",
    "padding": "8px 30px",
    "display": "none",
    "z-index": "999999",
    "font-size": "16px"
  };

  var link_css = {
    "color": "rgba(255, 255, 255, 0.9)",
    "display": "inline-block",
    "margin-right": "10px",
    "text-decoration": "none"
  };

  var close_css = {
    "color": "#fff",
    "font-size": "20px"
  };

  var wrapper = $("<div />").css(wrapper_css);
  var link = $("<div />")
    .css(link_css);
  var close = $("<a />", {
    "class": "pull-right",
    href: "#",
    "data-placement": "left"
  }).html("&times;")
    .css(close_css)
    .click(function (e) {
      e.preventDefault();
      $(wrapper).slideUp();
    });

  that.show = function(text) {
    clearTimeout(hideHandler);

    link.html(text);

    wrapper.append(close);
    wrapper.append(link);

    $(".content-wrapper").prepend(wrapper);

    wrapper.hide(4).delay(500).slideDown();
  };

  return that;
}());

// project詳細のタブ情報を保存しておく
$(function () {
  $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
    localStorage.setItem('activeProjectTab', $(e.target).attr('href'));
  });
  var activeProjectTab = localStorage.getItem('activeProjectTab');
  if (activeProjectTab) {
    $('.nav-tabs a[href="' + activeProjectTab + '"]').tab('show');
  }
});

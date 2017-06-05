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

  $('input[type="checkbox"], input[type="radio"]').iCheck({
    checkboxClass: 'icheckbox_flat-purple',
    radioClass: 'iradio_flat-purple',
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

  $('.date-yearstart').datepicker({
    format: "yyyy/mm/dd",
    startView: 2,
    language: "ja",
    autoclose: true
  });

  $('.date-yyyymm').datepicker({
    format: "yyyy/mm",
    startView: 1,
    minViewMode: 1,
    language: "ja",
    autoclose: true
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

// 「支払いのルール」表示・非表示コントロール
$(function() {
  var FIXED = 1;
  var VARIABLE = 2;
  
  $('input').on('ifChecked', function(event){
    if ($('input[name="receipt_rule"]:checked').val() == FIXED) {
      // 固定のため、非表示
      $('#receipt-variable-area').hide('slow');
    } else if ($('input[name="receipt_rule"]:checked').val() == VARIABLE) {
      // 変動のため、表示
      $('#receipt-variable-area').show('slow');
	} else {
      // 未入力のため、非表示
      $('#receipt-variable-area').hide();
    }
  });
});


// 「請求のルール」表示・非表示コントロール
$(function() {
  var FIXED = 1;
  var VARIABLE = 2;

  $('input').on('ifChecked', function(event){
    if ($('input[name="payment_rule"]:checked').val() == FIXED) {
      // 固定のため、非表示
      $('#payment-variable-area').hide('slow');
    } else if ($('input[name="payment_rule"]:checked').val() == VARIABLE) {
      // 変動のため、表示
      $('#payment-variable-area').show('slow');
	} else {
      // 未入力のため、非表示
      $('#variable-area').hide();
    }
  });
});


// 「明細区分」表示・非表示コントロール
$(function() {
  var ENGINEER = 1;
  var WORK = 2;

  $('input').on('ifChecked', function(event){
    if ($('input[name="detail_type"]:checked').val() == ENGINEER) {
      $('.engineer-variable-area').show('slow');
      $('.work-variable-area').hide('slow');
      $('.common-variable-area').show('slow');
    } else if ($('input[name="detail_type"]:checked').val() == WORK) {
      $('.engineer-variable-area').hide('slow');
      $('.work-variable-area').show('slow');
      $('.common-variable-area').show('slow');
	}
  });
});

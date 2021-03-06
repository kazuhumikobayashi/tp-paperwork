function pluginExists(pluginName) {
    return $.fn[pluginName] != undefined;
}

function round_off(number, n){
    var pow = Math.pow(10, n);
    return Math.round(number * pow) / pow
}

function round_down(number, n){
    var pow = Math.pow(10, n);
    if(number >= 0) {
      return Math.floor(number * pow) / pow
    } else {
      return Math.ceil(number * pow) / pow
    }
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
      "order": [],
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

  $('.date').each(function () {
    $(this).datepicker({
      format: "yyyy/mm/dd",
      startDate: $(this).attr("data-date_start"),
      endDate: $(this).attr("data-date_end"),
      language: "ja",
      autoclose: true,
      todayHighlight: true
    });
  });

  $('.date-yearstart').each(function () {
    $(this).datepicker({
      format: "yyyy/mm/dd",
      startDate: $(this).attr("data-date_start"),
      endDate: $(this).attr("data-date_end"),
      startView: 2,
      language: "ja",
      autoclose: true
    });
  });

  $('.date-yyyymm').each(function () {
    $(this).datepicker({
      format: "yyyy/mm",
      startDate: $(this).attr("data-date_start"),
      endDate: $(this).attr("data-date_end"),
      startView: 1,
      minViewMode: 1,
      language: "ja",
      autoclose: true
    })
  });
});

$(function () {

  /*-- Select2 --*/
  if (!pluginExists("select2")) {
    return;
  }

  $(".select2").select2({
    placeholder: "選択してください",
    allowClear: true,
    language: {"noResults": function(){ return "検索結果がありません。";}},
    escapeMarkup: function (markup) { return markup; }
  });

});

$(function () {
    if (!pluginExists("selectpicker")) {
        return;
    }
    $(".selectpicker").selectpicker({
        "selectedText": "cat"
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
    "font-size": "22px"
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

  var error_icon = $("<i />", {
    "class": "icon fa fa-warning"
  });
  that.show_error = function(text) {
    clearTimeout(hideHandler);

    link.html(error_icon.html(" " + text));

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
    if ($('input[name="payment_rule"]:checked').val() == FIXED) {
      // 固定のため、非表示
      $('#payment-variable-area').hide('slow');
    } else if ($('input[name="payment_rule"]:checked').val() == VARIABLE) {
      // 変動のため、表示
      $('#payment-variable-area').show('slow');
	} else {
      // 未入力のため、非表示
      $('#payment-variable-area').hide();
    }
  });
});


// 「請求のルール」表示・非表示コントロール
$(function() {
  var FIXED = 1;
  var VARIABLE = 2;

  $('input').on('ifChecked', function(event){
    if ($('input[name="billing_rule"]:checked').val() == FIXED) {
      // 固定のため、非表示
      $('#billing-variable-area').hide('slow');
    } else if ($('input[name="billing_rule"]:checked').val() == VARIABLE) {
      // 変動のため、表示
      $('#billing-variable-area').show('slow');
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

$(function() {
  // 実績の請求計算
  function calculateBilling() {
    var FIXED = 1;
    var sub_hours = 0;
    var sub_money = 0;
    var estimated_money = 0;
    var adjustment = 0;
    var ROUND_DOWN = 1;
    var ROUND_OFF = 2;

    var billing_rule = $("[name=billing_rule]:checked").val();
    var work_time = $('#work_time').val();
    work_time = parseFloat(work_time.replace(/[０-９]/g,function(s){return String.fromCharCode(s.charCodeAt(0)-0xFEE0)}));
    var billing_bottom_base_hour = parseFloat($('#billing_bottom_base_hour').val());
    var billing_top_base_hour = parseFloat($('#billing_top_base_hour').val());
    var billing_per_bottom_hour = parseFloat($('#billing_per_bottom_hour').val());
    var billing_per_top_hour = parseFloat($('#billing_per_top_hour').val());
    var billing_per_month = parseFloat($('#billing_per_month').val());
    var billing_fraction_rule = parseFloat($('#billing_fraction_rule').val());
    var billing_fraction = parseFloat($('#billing_fraction').val());

    // 請求のルールが固定の場合、作業時間がいかなる場合でも請求単価が入る。
    if (($.isNumeric(work_time) && work_time !== 0) || (billing_rule === FIXED)) {

      if (work_time < billing_bottom_base_hour) {
        sub_hours = work_time - billing_bottom_base_hour;
        sub_money = sub_hours * billing_per_bottom_hour;
      } else if (billing_top_base_hour < work_time) {
        sub_hours = work_time - billing_top_base_hour;
        sub_money = sub_hours * billing_per_top_hour;
      }

      if (billing_fraction_rule === ROUND_DOWN) {
        sub_money = round_down(sub_money, billing_fraction)
      } else if (billing_fraction_rule === ROUND_OFF) {
        sub_money = round_off(sub_money, billing_fraction)
      }
      estimated_money = billing_per_month + sub_money;

    }

    $('#billing_subtraction_hours').val(sub_hours);
    $('#billing_subtraction_money').val(sub_money);
    $('#billing_estimated_money').val(estimated_money);

    adjustment = $('#billing_adjustments').val();
    adjustment = parseInt(adjustment.replace(/[０-９]/g,function(s){return String.fromCharCode(s.charCodeAt(0)-0xFEE0)})) || 0;

    $('#billing_confirmation_money').val(estimated_money + adjustment);
  }

  // 実績の請求計算
  function calculatePayment() {
    var FIXED = 1;
    var sub_hours = 0;
    var sub_money = 0;
    var estimated_money = 0;
    var adjustment = 0;
    var ROUND_DOWN = 1;
    var ROUND_OFF = 2;

    var payment_rule = $("[name=payment_rule]:checked").val();
    var work_time = $('#work_time').val();
    work_time = parseFloat(work_time.replace(/[０-９]/g,function(s){return String.fromCharCode(s.charCodeAt(0)-0xFEE0)}));
    var payment_per_month = parseFloat($('#payment_per_month').val());
    var payment_bottom_base_hour = parseFloat($('#payment_bottom_base_hour').val());
    var payment_top_base_hour = parseFloat($('#payment_top_base_hour').val());
    var payment_per_bottom_hour = parseFloat($('#payment_per_bottom_hour').val());
    var payment_per_top_hour = parseFloat($('#payment_per_top_hour').val());
    var payment_fraction_rule = parseFloat($('#payment_fraction_rule').val());
    var payment_fraction = parseFloat($('#payment_fraction').val());

    if ((($.isNumeric(work_time) && work_time !== 0) || (payment_rule === FIXED))
        && $.isNumeric(payment_per_month)) {

      if (work_time < payment_bottom_base_hour) {
        sub_hours = work_time - payment_bottom_base_hour;
        sub_money = sub_hours * payment_per_bottom_hour;
      } else if (payment_top_base_hour < work_time) {
        sub_hours = work_time - payment_top_base_hour;
        sub_money = sub_hours * payment_per_top_hour;
      }

      if (payment_fraction_rule === ROUND_DOWN) {
        sub_money = round_down(sub_money, payment_fraction)
      } else if (payment_fraction_rule === ROUND_OFF) {
        sub_money = round_off(sub_money, payment_fraction)
      }
      estimated_money = payment_per_month + sub_money;

    }

    $('#payment_subtraction_hours').val(sub_hours);
    $('#payment_subtraction_money').val(sub_money);
    $('#payment_estimated_money').val(estimated_money);

    adjustment = $('#payment_adjustments').val();
    adjustment = parseInt(adjustment.replace(/[０-９]/g,function(s){return String.fromCharCode(s.charCodeAt(0)-0xFEE0)})) || 0;

    $('#payment_confirmation_money').val(estimated_money + adjustment);
  }

  $('.auto-calc').on('blur', function () {
    calculateBilling();
    calculatePayment();
  });

  $(':submit.auto-calc').on('click', function () {
    calculateBilling();
    calculatePayment();
  });
});

// 請求済みフラグ更新
$(function() {
  $('.billing-input-flag').on('ifChanged', function(event){
    var month_id = $(this).attr("id");
    var input_flag = $(this).prop('checked') ? 1 : 0;

    $.ajax({
      type: 'POST',
      url: '/project/billing/save_flag',
      data: {month_id: month_id, input_flag: input_flag},
      dataType: 'json',
      success: function(data, dataType) {

      },
      error: function(XMLHttpRequest, textStatus, errorThrown){
        console.log(errorThrown.message);
      }
    });
  });
});


// 支払済みフラグ更新
$(function() {
  $('.payment-input-flag').on('ifChanged', function(event){
    var payment_id = $(this).attr("id");
    var input_flag = $(this).prop('checked') ? 1 : 0;

    $.ajax({
      type: 'POST',
      url: '/search/payment/save_flag',
      data: {payment_id: payment_id, input_flag: input_flag},
      dataType: 'json',
      success: function(data, dataType) {

      },
      error: function(XMLHttpRequest, textStatus, errorThrown){
        console.log(errorThrown.message);
      }
    });
  });
});


// 入金済みフラグ更新
$(function() {
  $('.deposit-input-flag').on('ifChanged', function(event){
    var month_id = $(this).attr("id");
    var input_flag = $(this).prop('checked') ? 1 : 0;

    $.ajax({
      type: 'POST',
      url: '/search/billing/save_flag',
      data: {month_id: month_id, input_flag: input_flag},
      dataType: 'json',
      success: function(data, dataType) {

      },
      error: function(XMLHttpRequest, textStatus, errorThrown){
        console.log(errorThrown.message);
      }
    });
  });
});

// formクリア
$(function() {
  $('.form-clear').bind('click', function(){
    $(':input').not(':button, :submit, :reset, :hidden, :checkbox, :radio').val('');
    if (pluginExists("iCheck")) {
      $(':checkbox, :radio').iCheck('uncheck');
    }
    $('select, textarea').val('');
    if (pluginExists("selectpicker")) {
      $('.selectpicker').selectpicker('refresh');
    }
  });
});

$("form").submit(function() {
  var self = this;
    $(":submit.save", self).prop("disabled", true);
  setTimeout(function() {
    $(":submit.save", self).prop("disabled", false);
  }, 10000);
});

$(function() {
  $('.btn-delete').click(function(event) {
    event.preventDefault();
    if($(this).hasClass('disabled')){
      return;
    }

    var $href = $(this).attr('href');
    BootstrapDialog.confirm({
      title: '削除の確認',
      message: '削除してよろしいですか？',
      type: BootstrapDialog.TYPE_DANGER,
      closable: true,
      draggable: true,
      btnCancelLabel: 'キャンセル',
      btnOKLabel: '削除する',
      btnOKClass: 'btn-danger',
      callback: function(result) {
        if(result) {
          window.location.href = $href;
        }
      }
    });
  });
});

//明細登録ページの遷移時の警告
$(function() {
  changeFlg = false;
  $('.btn-create').click(function(event) {
    event.preventDefault();

    var $href = $(this).attr('href');
    if (changeFlg) {
      BootstrapDialog.confirm({
        title: 'ページ遷移の確認',
        message: '変更した内容が破棄されますが、移動しても宜しいでしょうか？',
        closable: true,
        draggable: true,
        btnCancelLabel: 'キャンセル',
        btnOKLabel: 'OK',
        btnOKClass: 'btn-success',
        callback: function(result) {
          if(result) {
            window.location.href = $href;
          }
        }
      });
    } else {
      window.location.href = $href;
    }
  });

  //フォームの内容が変更されたらフラグを立てる
  $("input, textarea, select").change(function() {
    changeFlg = true;
  });
});


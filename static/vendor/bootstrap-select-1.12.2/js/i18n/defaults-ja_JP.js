/*!
 * Bootstrap-select v1.10.0 (http://silviomoreto.github.io/bootstrap-select)
 *
 * Copyright 2013-2016 bootstrap-select
 * Licensed under MIT (https://github.com/silviomoreto/bootstrap-select/blob/master/LICENSE)
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define(["jquery"], function (a0) {
      return (factory(a0));
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require("jquery"));
  } else {
    factory(jQuery);
  }
}(this, function (jQuery) {

(function ($) {
  $.fn.selectpicker.defaults = {
    noneSelectedText: '選択されてません',
    noneResultsText: '{0} に該当する結果がありません',
    countSelectedText: function (numSelected, numTotal) {
      return "{0} 件 選択中";
    },
    maxOptionsText: function (numAll, numGroup) {
      return [
        '最大件数に達しました。(最大 {n} 件)',
        'グループの最大件数に達しました。(最大 {n} 件)'
      ];
    },
    selectAllText: '全て選択',
    deselectAllText: '選択を解除',
    multipleSeparator: ', '
  };
})(jQuery);


}));

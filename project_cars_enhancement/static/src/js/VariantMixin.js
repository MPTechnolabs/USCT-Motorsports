odoo.define('project_cars_enhancement.VariantMixin', function (require) {
'use strict';

var VariantMixin = require('sale.VariantMixin');
const originalOnChangeCombination = VariantMixin._onChangeCombination;
VariantMixin._onChangeCombination = function (ev, $parent, combination) {
    
    const $default_code = $parent.find(".default_code");
    $default_code.text(combination['default_code']);
   
    const $kit_div = $("div#kit_div");
    const $tbody = $("tbody#kit_table_ebody");
    const $save_price = $("span#save_price");
    const $final_total = $("td#final_total");
    const $tfoot = $("#kit_table_tfoot");

    var mrp_data;
    var content = '';
    for (var i=0; i< combination['mrp_data_count']; i++ ){
        mrp_data = combination['mrp_data'][i]
        content += '<tr>'
        content += '<td>'+mrp_data['component']+'</td>'
        content += '<td>'+mrp_data['quantity']+'</td>'
        content += '<td>'+mrp_data['unit']+'</td>'
        content += '<td>'+mrp_data['list_price']+'</td>'
        content += '<td>'+mrp_data['total']+'</td>'
        content += '</tr>'
    }
    if (combination['mrp_data_count'] > 0){
        $save_price.html(combination['save_price']);
        $final_total.html(combination['final_total']);
        $tbody.html(content);
        $kit_div.css('display', '')
        $kit_div.removeClass("o_hidden");
        $tfoot.removeClass("o_hidden");
        
    }
    else
    {
        $kit_div.addClass("o_hidden");
        $tfoot.addClass("o_hidden");
        $kit_div.css('display', 'none')
    }

    originalOnChangeCombination.apply(this, [ev, $parent, combination]);
};
return VariantMixin;


});
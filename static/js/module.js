btnName = "Continue";
unexpected_close = true;

$(function() {
    $("#module-form").dialog({
        autoOpen: false,
        width: 750,
        buttons: [{
            text: btnName,
            click: function() {
                var enabled_modules = [];
                var disabled_modules = [];
                var checked = $('#module-form').find(':checked');
                $.each(checked, function(i){enabled_modules.push(checked[i].value);});
                var notchecked = $('#module-form').find(':checkbox:not(:checked)');
                $.each(notchecked, function(i){disabled_modules.push(notchecked[i].value);});
                args['module'] = JSON.stringify({'enabled': enabled_modules, 'disabled': disabled_modules});
                unexpected_close = false;
                $( this ).dialog("close");
                $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
            }
        }],
        open: function (event, ui){
            $("#module_list").append(data.module_list);
        }
    });
});


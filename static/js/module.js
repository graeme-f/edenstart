btnName = "Continue";

$(function() {
    $("#module-form").dialog({
        autoOpen: false,
        modal: true,
        buttons: [{
            text: btnName,
            click: function() {
                args['module'] = $("#module_in").val();
                $( this ).dialog("close");
                $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
            }
        }],
        open: function (event, ui){
            $("#module_list").append(data.module_list);
        }
    });
});


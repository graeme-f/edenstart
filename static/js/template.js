btnName = "Continue";
unexpected_close = true;


$(function() {
    $("#template-form").dialog({
        autoOpen: false,
        buttons: [{
            text: btnName,
            click: function() {
                args['template'] = $("#template_in").val();
                unexpected_close = false;
                $( this ).dialog("close");
                $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
            }
        }],
        open: function (event, ui){
            $("#template_in").append(data.template_options);
        }
    });
});

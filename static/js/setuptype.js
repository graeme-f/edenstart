btnName = "Continue";
args = new Object();
unexpected_close = true;

$(function() {
    $("#setup-type-form").dialog({
        autoOpen: false,
        width: 550,
        buttons: [{
            text: btnName,
            click: function() {
                args['setup_type'] = $("input:radio[name=setup_type_in]:checked").val();
                unexpected_close = false;
                $(this).dialog("close");
                $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
            }
        }],
    });
});


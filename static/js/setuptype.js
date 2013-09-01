btnName = "Continue";
args = new Object();

$(function() {
    $("#setup-type-form").dialog({
        autoOpen: false,
        width: 550,
        buttons: [{
            text: btnName,
            click: function() {
                args['setup_type'] = $("input:radio[name=setup_type_in]:checked").val();
                $(this).dialog("close");
                $.get('/'+app+'/default/setup_type', args).done(function(data){success(data)});
            }
        }],
    });
});


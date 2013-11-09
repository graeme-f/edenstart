btn1 = "Install";
btn2 = "Skip";
args = new Object();

$(function() {
    $("#missing-libs-alert").dialog({
        autoOpen: false,
        buttons: [{
            text: btn1,
            click: function() {
                $( this ).dialog("close");
                args['button'] = "install";
                $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
            }},{
            text: btn2,
            click: function() {
                $( this ).dialog("close");
                args['button'] = "skip";
                $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
            }
        }],
    });
});

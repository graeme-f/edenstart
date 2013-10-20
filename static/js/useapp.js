btnName = "Continue";
args = new Object();

$(function() {
    var appname = $("#appname_in"),
        allFields = $([]).add(appname),
        tips = $(".validateTips");
    $("#use-eden-form").dialog({
        autoOpen: false,
        width: 550,
        buttons: [{
            text: btnName,
            click: function() {
                args['appname'] = $("input:radio[name=app_name_in]:checked").val();
                $(this).dialog("close");
                $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
            }
        }],
    });
});


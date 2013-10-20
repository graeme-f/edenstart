btnName = "Continue";
args = new Object();

$(function() {
    var appname = $("#appname_in"),
        allFields = $([]).add(appname),
        tips = $(".validateTips");
    $("#app-name-form").dialog({
        autoOpen: false,
        height: 300,
        width: 350,
        buttons: [{
            text: btnName,
            click: function() {
                var bValid = true;
                allFields.removeClass( "ui-state-error" );
                bValid = bValid && checkLength( appname, "application name", 3, 16 );
                bValid = bValid && checkRegexp( appname, /^[a-z]([0-9a-z])+$/i, "Application name may consist of a-z, 0-9, begin with a letter.");
                bValid = bValid && checkRestrict( appname, "Application name already exists", data.exclude_list);
                if ( bValid ) {
                    args['appname'] = appname.val();
                    $( this ).dialog("close");
                    $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
                }
            }
        }],
        close: function() {
            allFields.val("").removeClass("ui-state-error");
        }
    });
});


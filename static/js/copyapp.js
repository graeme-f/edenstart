btnName = "Continue";
args = new Object();

$(function() {
    var appname = $("#appname_in"),
        allFields = $([]).add(appname),
        tips = $(".validateTips");
    $("#copy-eden-form").dialog({
        autoOpen: false,
        width: 550,
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
                    args['copy_appname'] = $("input:radio[name=app_name_in]:checked").val();
                    $(this).dialog("close");
                    $.get('/'+app+'/default/copy', args).done(function(data){success(data)});
                }
            }
        }],
    });
});


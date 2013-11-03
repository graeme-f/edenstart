btnName = "Continue";
nameError = "The system name needs can contain letters and spaces and be between 3 and 128 characters long."
abbrError = "The system short name needs can contain letters and spaces and be between 3 and 32 characters long."
urlError = "The url needs to be a valid URL, including the port number"


$(function() {
    var sysname = $("#sys_name_in"),
        sysabbrv = $("#sys_abbrv_in"),
        sysurl = $("#url_in"),
        allFields = $([]).add(sysname).add(sysabbrv).add(sysurl),
        tips = $(".validateTips");
    $("#sys-base-form").dialog({
        autoOpen: false,
        modal: true,
        width: 700,
        buttons: [{
            text: btnName,
            click: function() {
                var bValid = true;
                allFields.removeClass( "ui-state-error" );
                bValid = bValid && checkRegexp( sysname, /^[a-zA-Z ]{3,128}$/, nameError);
                bValid = bValid && checkRegexp( sysabbrv, /^[a-zA-Z ]{3,32}$/, abbrError);
                bValid = bValid && checkRegexp( sysurl, /^http(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:[0-9]*)$/, urlError);
                if ( bValid ) {
                    args['sys_name'] = sysname.val();
                    args['sys_abbrv'] = sysabbrv.val();
                    args['sys_url'] = sysurl.val();
                    $( this ).dialog("close");
                    $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
                }
            }
        }],
        open: function (event, ui){
            $(sysname).val(data.sys_name);
            $(sysabbrv).val(data.sys_abbrv);
            $(sysurl).val(data.sys_url);
        },
        close: function() {
            allFields.val("").removeClass("ui-state-error");
        }
    });
});

btnName = "Continue";
hostError = "Host name is invalid, it must either be a valid host name or an IP address."
portError = "The port number must be between 0 and 65535"
schemaError = "Schema name may consist of a-z, 0-9, and underscore."
userError = "The user name must be between 3 and 10 characters and can contain a letter, number or underscore"
passwordError = "The password must be between 6 and 18 characters and can contain a letter, number, hyphen or underscore"

unexpected_close = true;
args = new Object();

$(function() {
    var dbhost = $("#db_host_in"),
        dbport = $("#db_port_in"),
        dbschema = $("#db_schema_in"),
        dbuser = $("#db_user_in"),
        dbpassword = $("#db_password_in"),
        allFields = $([]).add(dbhost).add(dbport).add(dbschema).add(dbuser).add(dbpassword),
        tips = $(".validateTips");
    $("#db-connect-form").dialog({
        autoOpen: false,
        buttons: [{
            text: btnName,
            click: function() {
                var bValid = true;
                allFields.removeClass( "ui-state-error" );
                var validIpAddressRegex = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/i;
                var validHostnameRegex = /^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/i;
                var validHost = (validIpAddressRegex.test(dbhost.val()) || validHostnameRegex.test(dbhost.val()));
                if (!validHost){
                    bValid = false;
                    dbhost.addClass("ui-state-error");
                    updateTips(hostError);
                }
                bValid = bValid && checkRegexp( dbport, /([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$/i, portError);
                bValid = bValid && checkRegexp( dbschema, /^[0-9a-z_]+$/i, schemaError);
                bValid = bValid && checkRegexp( dbuser, /^[0-9a-zA-Z_]{3,10}$/i, userError);
                bValid = bValid && checkRegexp( dbpassword, /^[a-zA-Z0-9_-]{4,18}$/i, passwordError);
                if ( bValid ) {
                    args['db_host'] = dbhost.val();
                    args['db_port'] = dbport.val();
                    args['db_schema'] = dbschema.val();
                    args['db_user'] = dbuser.val();
                    args['db_password'] = dbpassword.val();
                    unexpected_close = false;
                    $( this ).dialog("close");
                    $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
                }
            }
        }],
        open: function (event, ui){
            $(dbhost).val(data.db_host);
            $(dbport).val(data.db_port);
            $(dbschema).val(data.db_schema);
            $(dbuser).val(data.db_user);
            $(dbpassword).val(data.db_password);
        },
        close: function() {
            allFields.val("").removeClass("ui-state-error");
        }
    });
});

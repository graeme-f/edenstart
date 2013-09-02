# -*- coding: utf-8 -*-
'''
    Note At various times system calls are evoked using the subprocess.pOpen
         To ensure that they work on 'Windows' systems the shell=True argument
         is required. This is a potential security issue so the use of this
         application should be restricted to trusted users.
    Note As a security measure this application can be disabled by setting
         the enabled setting in models/0.py to False
'''

app = request.application
if not settings.enabled and (request.function != "disabled"):
    redirect("/%s/default/disabled" % app)

import json
import os

def error(): return dict()
def disabled():
    if settings.enabled:
        redirect("/%s/default/index" % app)
    return dict()

# Global settings for ajax callbacks
if request.ajax:
    action = request.function
    reply = Storage()
    reply.action = action
    reply.result = True
    reply.fatal = False
    reply.dialog = False
    reply.detail = ""
    reply.advanced = ""

def index():
    if request.ajax:
#        action = request.get_vars.action
#        reply = Storage()
#        reply.action = action
#        reply.result = True
#        reply.fatal = False
#        reply.dialog = False
#        reply.detail = ""
#        reply.advanced = ""
#        if action == "start":
#            reply.next = "appname"
#            reply.dialog = "#app-name-form"
#            return json.dumps(reply)
#        elif action == "appname":
#            return appname_json(reply)
#        elif action == "git":
#            return git_json(reply)
#        elif action == "clone":
#            return clone_json(reply)
#        elif action == "python":
#            return python_json(reply)
#        elif action == "pip":
#            if request.get_vars.button == "install":
#                return pip_json(reply)
#            elif request.get_vars.button == "skip":
#                return pre_db_json(reply)
#        elif action == "install":
#            return install_json(reply)
#        elif action == "database":
#            return db_json(reply)
#        elif action == "connect":
#            return connect_json(reply)
#        elif action == "base":
#            return base_json(reply)
#        elif action == "template":
#            return template_json(reply)
#        elif action == "module":
#            return module_json(reply)
#        else:
#            reply.next = "finished"
#            return json.dumps(reply)
        pass
    else:
        try:
            # Python 2.7
            from collections import OrderedDict
        except:
            # Python 2.6
            from gluon.contrib.simplejson.ordered_dict import OrderedDict
        #session.eden_release = T("Eden release 1.0")
        session.eden_release = T("Eden trunk") # replace once we have a release
        session.fatal = None
        response.title=T("Sahana Eden Web Setup")
        actions = OrderedDict()
        actions["setup_type"] = T("Type of setup")
        actions["appname"] = T("Getting the application name")
        actions["git"] = T("Looking for git")
        actions["clone"] = T("Cloning Sahana Eden")
        actions["python"] = T("Looking for Python libraries")
        actions["pip"] = T("Looking for pip")
        actions["install"] = T("Using pip to install missing libraries")
        actions["database"] = T("Selecting the database to use")
        actions["connect"] = T("Connecting to the database")
        actions["base"] = T("Basic system settings")
        actions["template"] = T("Select the template to use")
        actions["modules"] = T("Select modules to enable")
        table = TABLE()
        for (key,value) in actions.items():
            table.append(TR(
                            TD(value, _id="%s" % key),
                            TD(IMG(_id="%s_wait" % key,
                                   _src="/%s/static/images/Waiting.png" % app),
                               IMG(_id="%s_process" % key,
                                   _src="/%s/static/images/ajax-loader.gif" % app,
                                   _class="hidden"),
                               IMG(_id="%s_pass" % key,
                                   _src="/%s/static/images/Pass.png" % app,
                                   _class="hidden"),
                               IMG(_id="%s_fail" % key,
                                   _src="/%s/static/images/Fail.png" % app,
                                   _class="hidden")
                              )
                           )
                        )
        response.basic=table
        script = """
app = "%s";
success = function(_data){
    data = $.parseJSON(_data) // Global scope so that dialog events can access it
    if (data.html) {$("#dialogs").html(data.html);};
    if (data.script){
        $.getScript(data.script,function(){dashboard_update();});
    } else {
        dashboard_update();
    }
}

dashboard_update = function(){
    if (data.subaction){
        $("#"+data.subaction+"_wait").hide();
        $("#"+data.subaction+"_process").hide();
    } else {
        $("#"+data.action+"_wait").hide();
        $("#"+data.action+"_process").hide();
    }
    if (data.result) {
        if (data.subaction){
            $("#"+data.subaction+"_pass").show();
            $("#"+data.subaction+"_fail").hide();
        } else {
            $("#"+data.action+"_pass").show();
            $("#"+data.action+"_fail").hide();
        }
    } else {
        if (data.subaction){
            $("#"+data.subaction+"_pass").hide();
            $("#"+data.subaction+"_fail").show();
        } else {
            $("#"+data.action+"_pass").hide();
            $("#"+data.action+"_fail").show();
        }
    }
    $("#detail").append("<p><b>"+data.action+":</b> "+data.detail+"</p>");
    if (data.advanced != "") {
        $("#advanced").append("<p><b>"+data.action+":</b> "+data.advanced+"</p>");
    }
    if (data.insert_basic){
        insert_basic(data.insert_basic_id, data.insert_basic_html); 
    }
    if (data.fatal){
        alert(data.fatal);
        return;
    }
    if (data.next != 'finished') {
        if (data.nextsubaction){
            $("#"+data.nextsubaction+"_wait").hide();
            $("#"+data.nextsubaction+"_process").show();
        }
        $("#"+data.next+"_wait").hide();
        $("#"+data.next+"_process").show();
        if (data.dialog){
            $(data.dialog).dialog("open")
        } else {
            $.get('/'+app+'/default/'+data.next).done(function(data){success(data)});
        }
    }
}

function insert_basic(id, html){
    $("td#"+id).append(html);
}


$.get('/'+app+'/default/start')
.done(function(data){success(data)});

$("input[name='display']").change(function(){
    if ($(this).val() == "basic"){
        $("#detail").hide();
        $("#advanced").hide();
    } else if ($(this).val() == "detail"){
        $("#detail").show();
        $("#advanced").hide();
    } else if ($(this).val() == "advanced"){
        $("#detail").show();
        $("#advanced").show();
    }
});

function updateTips( t ) {
    $(".validateTips").text(t).addClass( "ui-state-highlight" );
    setTimeout(function() {
        $(".validateTips").removeClass( "ui-state-highlight", 1500 );
    }, 500 );
}
checkLength = function( o, n, min, max ) {
    if ( o.val().length > max || o.val().length < min ) {
        o.addClass( "ui-state-error" );
        updateTips( "Length of " + n + " must be between " + min + " and " + max + "." );
        return false;
    } else {
        return true;
    }
}
checkRegexp = function (o, regexp, n) {
    if (!(regexp.test(o.val())) ) {
        o.addClass("ui-state-error");
        updateTips(n);
        return false;
    } else {
        return true;
    }
}
checkRestrict = function(o, n, exclude){
    for (i=0; i<exclude.length; i++){
        if (o.val() == exclude[i]){
            o.addClass("ui-state-error");
            updateTips(n);
            return false;
        }
    }
    return true;
}
""" % (app)
        # Add input dialogs
#        response.dialogs = DIV()
##        script = script + setup_type_dialog(app)
#        script = script + appname_dialog(app)
#        script = script + appexist_dialog(app)
#        script = script + pip_dialog(app)
#        script = script + db_type_dialog(app)
#        script = script + connect_dialog(app)
#        script = script + base_dialog(app)
#        script = script + template_dialog(app)
#        script = script + module_dialog(app)
        return dict(script=script)



def appexist_dialog(app):
    existsName = DIV(_id="app-exists-alert",
                     _title=T("Application exists")
                   )
    existsName.append(P(T("The application folder already exists. The setup will now work with this folder")))
    response.dialogs.append(existsName)
    script = """
$(function() {
    $("#app-exists-alert").dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            %s: function() {
                $( this ).dialog("close");
                $.get('/%s/default/index', args).done(function(data){success(data)});
            },
            %s: function() {
                $( this ).dialog("close");
            }
        },
    });
});
""" % (T("Continue"), app, T("Cancel"))
    return script

def pip_dialog(app):
    existsName = DIV(_id="missing-libs-alert",
                     _title=T("Missing Libraries")
                   )
    existsName.append(P(T("Some libraries that Eden uses are missing. Would you like the system to try and install them for you? To do this it is necessary to have pip installed.")))
    response.dialogs.append(existsName)
    script = """
$(function() {
    $("#missing-libs-alert").dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            %s: function() {
                $( this ).dialog("close");
                args['button'] = "install";
                $.get('/%s/default/index', args).done(function(data){success(data)});
            },
            %s: function() {
                $( this ).dialog("close");
                args['button'] = "skip";
                $.get('/%s/default/index', args).done(function(data){success(data)});
            }
        },
    });
});
""" % (T("Install"), app, T("Skip"), app)
    return script

def db_type_dialog(app):
    dbType = DIV(_id="db-type-form",
                  _title=T("Database type")
                 )
    dbType.append(P(T("Select the type of database that will be used.")))
    dbType.append(TABLE(
                        TR( TD(INPUT(_id = "dbtype_sqlite",
                             _name = "dbtype_in",
                             _type = "radio",
                             _value = "sqlite"
                            )),
                            TD(LABEL(T("Sqlite")))
                        ),
                       TR( TD(INPUT(_id = "dbtype_mysql",
                             _name = "dbtype_in",
                             _type = "radio",
                             _value = "mysql"
                            )),
                          TD(LABEL(T("MySql")))
                       ),
                       TR(TD(INPUT(_id = "dbtype_postgres",
                             _name = "dbtype_in",
                             _type = "radio",
                             _value = "postgres"
                            )),
                          TD(LABEL(T("PostgeSQL")))
                       )
                      ),
                  )
    response.dialogs.append(dbType)
    script = '''
$(function() {
    $("#db-type-form").dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            %s: function() {
                args['db_type'] = $("input:radio[name=dbtype_in]:checked").val();
                $( this ).dialog("close");
                $.get('/%s/default/index', args).done(function(data){success(data)});
            }
        },
        open: function (event, ui){
            $("input:radio[name=dbtype_in]").filter('[value="'+data.db_type+'"]').attr('checked', true); 
        }
    });
});
''' % (T("Continue"), app)
    return script

def connect_dialog(app):
    appName = DIV(_id="db-connect-form",
                  _title=T("Enter the database details")
                 )
    appName.append(P(T("Provide the details necessary to connect to the database"),
                     _class="validateTips"))
    appName.append(FORM(LABEL(T("Database host")),
                        INPUT(_id = "db_host_in",
                              _name = "db_host_in",
                              _class="text ui-widget-content ui-corner-all",
                              value = ""
                             ),
                        LABEL(T("Database port")),
                        INPUT(_id = "db_port_in",
                              _name = "db_port_in",
                              _class="text ui-widget-content ui-corner-all",
                              value = ""
                             ),
                        LABEL(T("Database schema name")),
                        INPUT(_id = "db_schema_in",
                              _name = "db_schema_in",
                              _class="text ui-widget-content ui-corner-all",
                              value = ""
                             ),
                        LABEL(T("Database username")),
                        INPUT(_id = "db_user_in",
                              _name = "db_user_in",
                              _class="text ui-widget-content ui-corner-all",
                              value = ""
                             ),
                        LABEL(T("Database password")),
                        INPUT(_id = "db_password_in",
                              _name = "db_password_in",
                              _type = "password",
                              _class="text ui-widget-content ui-corner-all",
                              value = ""
                             ),
                        )
                   )
    response.dialogs.append(appName)
    hostError = T("Host name is invalid, it must either be a valid host name or an IP address.")
    portError = T("The port number must be between 0 and 65535")
    schemaError = T("Schema name may consist of a-z, 0-9, and underscore.")
    userError = T("The user name must be between 3 and 10 characters and can contain a letter, number or underscore")
    passwordError = T("The password must be between 6 and 18 characters and can contain a letter, number, hyphen or underscore")
    script = """
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
        modal: true,
        buttons: {
            "%s": function() {
                var bValid = true;
                allFields.removeClass( "ui-state-error" );
                var validIpAddressRegex = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/i;
                var validHostnameRegex = /^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/i;
                var validHost = (validIpAddressRegex.test(dbhost.val()) || validHostnameRegex.test(dbhost.val()));
                if (!validHost){
                    bValid = false;
                    dbhost.addClass("ui-state-error");
                    updateTips("%s");
                }
                bValid = bValid && checkRegexp( dbport, /([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$/i, "%s");
                bValid = bValid && checkRegexp( dbschema, /^[0-9a-z_]+$/i, "%s");
                bValid = bValid && checkRegexp( dbuser, /^[0-9a-zA-Z_]{3,10}$/i, "%s");
                bValid = bValid && checkRegexp( dbpassword, /^[a-zA-Z0-9_-]{4,18}$/i, "%s");
                if ( bValid ) {
                    args['db_host'] = dbhost.val();
                    args['db_port'] = dbport.val();
                    args['db_schema'] = dbschema.val();
                    args['db_user'] = dbuser.val();
                    args['db_password'] = dbpassword.val();
                    $( this ).dialog("close");
                    $.get('/%s/default/index', args).done(function(data){success(data)});
                }
            }
        },
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
""" % (T("Continue"), hostError, portError, schemaError, userError, passwordError, app)
    return script

def base_dialog(app):
    appName = DIV(_id="sys-base-form",
                  _title=T("Enter the system details")
                 )
    appName.append(P(T("Provide base system details"),
                     _class="validateTips"))
    appName.append(FORM(LABEL(T("System name")),
                        INPUT(_id = "sys_name_in",
                              _name = "sys_name_in",
                              _class="text ui-widget-content ui-corner-all",
                              value = ""
                             ),
                        LABEL(T("System short name")),
                        INPUT(_id = "sys_abbrv_in",
                              _name = "sys_abbrv_in",
                              _class="text ui-widget-content ui-corner-all",
                              value = ""
                             ),
                        LABEL(T("Public URL")),
                        INPUT(_id = "url_in",
                              _name = "url_in",
                              _class="text ui-widget-content ui-corner-all",
                              value = ""
                             )
                        )
                   )
    response.dialogs.append(appName)
    nameError = T("The system name needs can contain letters and spaces and be between 3 and 128 characters long.")
    abbrError = T("The system short name needs can contain letters and spaces and be between 3 and 32 characters long.")
    urlError = T("The url needs to be a valid URL, including the port number")
    script = """
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
        buttons: {
            "%s": function() {
                var bValid = true;
                allFields.removeClass( "ui-state-error" );
                bValid = bValid && checkRegexp( sysname, /^[a-zA-Z ]{3,128}$/, "%s");
                bValid = bValid && checkRegexp( sysabbrv, /^[a-zA-Z ]{3,32}$/, "%s");
                bValid = bValid && checkRegexp( sysurl, /^http(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:[0-9]*)$/, "%s");
                if ( bValid ) {
                    args['sys_name'] = sysname.val();
                    args['sys_abbrv'] = sysabbrv.val();
                    args['sys_url'] = sysurl.val();
                    $( this ).dialog("close");
                    $.get('/%s/default/index', args).done(function(data){success(data)});
                }
            }
        },
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
""" % (T("Continue"), nameError, abbrError, urlError, app)
    return script

def template_dialog(app):
    template = DIV(_id="template-form",
                  _title=T("Template")
                 )
    template.append(P(T("Select the template that will be used.")))
    template.append(TABLE(TR(TD( LABEL(T("Template"))),
                             TD( SELECT(_id = "template_in",
                                     _name = "template_in"
                                     ))
                              )
                        )
                   )
    response.dialogs.append(template)
    script = '''
$(function() {
    $("#template-form").dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            %s: function() {
                args['template'] = $("#template_in").val();
                $( this ).dialog("close");
                $.get('/%s/default/index', args).done(function(data){success(data)});
            }
        },
        open: function (event, ui){
            $("#template_in").append(data.template_options);
        }
    });
});
''' % (T("Continue"), app)
    return script

def module_dialog(app):
    module = DIV(_id="module-form",
                  _title=T("Template")
                 )
    module.append(P(T("Select the modules that will be enabled.")))
    module.append(TABLE(TR(TD( LABEL(T("Modules"))),
                              ),
                        _id="module_list"
                        ),
                   )
    response.dialogs.append(module)
    script = '''
$(function() {
    $("#module-form").dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            %s: function() {
                args['module'] = $("#module_in").val();
                $( this ).dialog("close");
                $.get('/%s/default/index', args).done(function(data){success(data)});
            }
        },
        open: function (event, ui){
            $("#module_list").append(data.module_list);
        }
    });
});
''' % (T("Continue"), app)
    return script

def python_json(reply):
    result = check_python_libraries()
    reply.next = "database"
    libs_missing = False
    error_lib = []
    warning_lib = []
    if result["error_messages"]:
        for error in result["error_messages"]:
            error_lib.append(strip_lib(error))
            reply.detail = reply.detail + "<b>Error:</b> %s<br>" % error
            reply.advanced = reply.advanced + "<b>Error:</b> %s<br>" % error
            libs_missing = True
            reply.next = "pip"
    if result["warning_messages"]:
        for warning in result["warning_messages"]:
            warning_lib.append(strip_lib(warning))
            reply.advanced = reply.advanced + "<b>Warning:</b> %s<br>" % warning
            libs_missing = True
            reply.next = "pip"
    if libs_missing:
        session.error_lib = error_lib
        session.warning_lib = warning_lib
        table = TABLE()
        app = request.application
        for lib in error_lib:
            table.append(TR(
                            TD(IMG(_src="/%s/static/images/red_star.png" % app,
                                   _width=24, _height=24),
                               T("Install python library %s" % lib), _id="%s" % lib),
                            TD(IMG(_id="%s_wait" % lib,
                                   _src="/%s/static/images/Waiting.png" % app,
                                   _width=24, _height=24),
                               IMG(_id="%s_process" % lib,
                                   _src="/%s/static/images/ajax-loader.gif" % app,
                                   _width=24, _height=24,
                                   _class="hidden",
                                   _style="display: none"),
                               IMG(_id="%s_pass" % lib,
                                   _src="/%s/static/images/Pass.png" % app,
                                   _width=24, _height=24,
                                   _class="hidden",
                                   _style="display: none"),
                               IMG(_id="%s_fail" % lib,
                                   _src="/%s/static/images/Fail.png" % app,
                                   _width=24, _height=24,
                                   _class="hidden",
                                   _style="display: none")
                              )
                           )
                        )
        for lib in warning_lib:
            table.append(TR(
                            TD(IMG(_src="/%s/static/images/yellow_star.png" % app,
                                   _width=16, _height=16),
                               T("Install python library %s" % lib), _id="%s" % lib),
                            TD(IMG(_id="%s_wait" % lib,
                                   _src="/%s/static/images/Waiting.png" % app,
                                   _width=24, _height=24),
                               IMG(_id="%s_process" % lib,
                                   _src="/%s/static/images/ajax-loader.gif" % app,
                                   _width=24, _height=24,
                                   _class="hidden",
                                   _style="display: none"),
                               IMG(_id="%s_pass" % lib,
                                   _src="/%s/static/images/Pass.png" % app,
                                   _width=24, _height=24,
                                   _class="hidden",
                                   _style="display: none"),
                               IMG(_id="%s_fail" % lib,
                                   _src="/%s/static/images/Fail.png" % app,
                                   _width=24, _height=24,
                                   _class="hidden",
                                   _style="display: none")
                              )
                           )
                        )
        reply.insert_basic = True
        reply.insert_basic_html = table.xml()
        reply.insert_basic_id = "install"
        reply.dialog = "#missing-libs-alert"
    return json.dumps(reply)

def pip_json(reply):
    from subprocess import Popen, PIPE
    import platform
    windows = platform.system() == "Windows"
    try:
        cmd = ["pip", "--version"]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=windows)
        (myout, myerr) = p.communicate()
        if p.returncode == 0:
            reply.detail = T("Looking for pip, <b>found:</b> %s" % myout.replace('\n', '<br />'),
                             lazy = False)
            reply.advanced = myerr
        else:
            reply.fatal = T("Unable to continue, please install pip",
                            lazy=False)
            reply.detail = "%s<br>" %(reply.fatal)
            reply.advanced = "<b>command:</b>%s<br><b>exception:</b>%s<br>" % (" ".join(cmd),
                                                                               myout.replace('\n', '<br />'))
    except Exception, inst:
        reply.result = False
        reply.fatal = T("Unable to continue, please install pip",
                        lazy=False)
        reply.detail = "%s<br>" %(reply.fatal)
        reply.advanced = "<b>command:</b>%s<br><b>exception:</b>%s<br>" % (" ".join(cmd), inst)
        return json.dumps(reply)
    # Now see if the version of pip supports the --target install option
    cmd = ["pip", "install", "--target"]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=windows)
    (myout, myerr) = p.communicate()
    if "no such option" in myerr:
        reply.result = False
        reply.fatal = T("The version of pip needs to be upgraded. Use 'pip install -U pip' as admin.",
                        lazy=False)
        reply.detail = reply.detail +\
                       "<br>" +\
                       "%s<br>" %(reply.fatal)
        reply.advanced = reply.advanced +\
                         "<b>command:</b>%s<br><b>error:</b>%s<br>" % (" ".join(cmd), myerr)
    else:
        reply.detail = reply.detail +\
                       "<br>" +\
                       T("Looking for pip install --target option, <b>found:</b>", lazy = False)
        reply.next = "install"
        if session.error_lib:
            reply.nextsubaction = session.error_lib[-1]
        elif session.warning_lib:
            reply.nextsubaction = session.warning_lib[-1]
    return json.dumps(reply)

def install_json(reply):
    '''
        This function will attempt to install the missing libraries
        Because of the time it takes to install each library it will
        do one at a time and then send the result back as an json string 
    '''
    def pip_install(reply, lib, fatal):
        '''
            Function that will use pip to attempt to install the missing python library 
        '''
        from subprocess import Popen, PIPE
        import platform
        windows = (platform.system() == "Windows")

        target = os.path.join(request.env.web2py_path, "site-packages")
        cmd = ["pip", "install", "--target", target, lib]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=windows)
        (myout, myerr) = p.communicate()
        if p.returncode == 0:
            reply.detail = reply.detail + "<br>"+T("Installed <b>%s</b> library" % lib,
                                                   lazy = False)
            reply.advanced = reply.advanced +\
                            "<b>command:</b>%s<br>" % (" ".join(cmd))
        else:
            reply.detail = reply.detail + "<br>"+T("Failed to install <b>%s</b> library." % (lib),
                                                   lazy = False)
            reply.advanced = reply.advanced +\
                            "<b>command:</b>%s<br><b>error:</b>%s<br>%s<br>" % (" ".join(cmd),
                                                                          myout.replace('\n', '<br />'),
                                                                          myerr.replace('\n', '<br />'))
            if fatal:
                session.fatal = T("Failed to install all of the required libraries",
                                lazy=False)
            reply.result = False
        return reply
    # Install a required lib, if one exists
    lib = None
    if session.error_lib:
        lib = session.error_lib.pop()
        reply = pip_install(reply, lib, True)
    # Install an optional lib, if one exists
    elif session.warning_lib:
        lib = session.warning_lib.pop()
        reply = pip_install(reply, lib, False)
    if lib:
        reply.subaction = lib
        if session.error_lib:
            reply.nextsubaction = session.error_lib[-1]
        elif session.warning_lib:
            reply.nextsubaction = session.warning_lib[-1]
        reply.next = "install"
    else:
        if session.fatal:
            reply.fatal = session.fatal
            reply.result = False
        return pre_db_json(reply)
    return json.dumps(reply)


def pre_db_json(reply):
    reply.dialog = "#db-type-form"
    reply.next = "database"
    db_type = get_000_config("db_type", "sqlite")
    reply.db_type = db_type
    return json.dumps(reply)

def db_json(reply):
    db_type = request.get_vars.db_type
    session.db_type = db_type
    set_000_config("database.db_type",
                   '"%s"'%db_type,
                   comment=(db_type=="sqlite")
                  )
    reply.detail = reply.detail + T("type <b>%s</b> selected" % db_type,
                                    lazy = False)
    return pre_connect_json(reply)

def pre_connect_json(reply):
    db_type = session.db_type
    if db_type == "sqlite":
        set_000_config("database.host","",True)
        set_000_config("database.port","",True)
        set_000_config("database.database","",True)
        set_000_config("database.username","",True)
        set_000_config("database.password","",True)
        reply.next = "connect"
    elif db_type == "mysql":
        reply.dialog = "#db-connect-form"
        reply.next = "connect"
        reply.db_host = get_000_config("host", "localhost")
        reply.db_port = get_000_config("port", "3306")
        reply.db_schema = get_000_config("schema", "sahana")
        reply.db_user = get_000_config("user", "sahana")
        reply.db_password = get_000_config("password", "")
    elif db_type == "postgres":
        reply.dialog = "#db-connect-form"
        reply.next = "connect"
        reply.db_host = get_000_config("host", "localhost")
        reply.db_port = get_000_config("port", "5432")
        reply.db_schema = get_000_config("schema", "sahana")
        reply.db_user = get_000_config("user", "sahana")
        reply.db_password = get_000_config("password", "")
    return json.dumps(reply)

def connect_json(reply):
    db_type = session.db_type
    db_host = request.get_vars.db_host
    db_port = request.get_vars.db_port
    db_schema = request.get_vars.db_schema
    db_user = request.get_vars.db_user
    db_password = request.get_vars.db_password
    set_000_config("database.host",
                   '"%s"'%db_host,
                   comment=(db_type=="sqlite")
                  )
    set_000_config("database.port",
                   db_port,
                   comment=(db_type=="sqlite")
                  )
    set_000_config("database.database",
                   '"%s"'%db_schema,
                   comment=(db_type=="sqlite")
                  )
    set_000_config("database.username",
                   '"%s"'%db_user,
                   comment=(db_type=="sqlite")
                  )
    set_000_config("database.password",
                   '"%s"'%db_password,
                   comment=(db_type=="sqlite")
                  )
    # Now construct the database string
    if (db_type == "sqlite"):
        db_string = "sqlite://storage.db"
    elif (db_type == "mysql"):
        db_string = "mysql://%s:%s@%s:%s/%s" % \
                    (db_user, db_password, db_host, db_port, db_schema)
    elif (db_type == "postgres"):
        db_string = "postgres://%s:%s@%s:%s/%s" % \
                    (db_user, db_password, db_host, db_port, db_schema)
    reply = db_connect(reply, db_string)
    return json.dumps(reply)

def base_json(reply):
    sys_name = request.get_vars.sys_name
    sys_abbrv = request.get_vars.sys_abbrv
    sys_url = request.get_vars.sys_url
    set_000_config("base.system_name", 'T("%s")' % sys_name)
    set_000_config("base.system_name_short", 'T("%s")' % sys_abbrv)
    set_000_config("base.public_url", '"%s"' % sys_url)
    return pre_template_json(reply)


def pre_template_json(reply):
    reply.dialog = "#template-form"
    reply.next = "template"
    template_path = "applications/%s/private/templates" % session.appname
    dir_list = os.listdir(template_path)
    dir_list.sort()
    option_list = ""
    for file in dir_list:
        new_file = "%s/%s" % (template_path, file)
        if os.path.isdir(new_file):
            if file == "default":
                option_list = option_list\
                            + OPTION(file,
                                     _id=file,
                                     _value=file,
                                     _selected=True).xml()
            else:
                option_list = option_list\
                            + OPTION(file,
                                     _id=file,
                                     _value=file).xml()
    reply.template_options = option_list
    return json.dumps(reply)

def template_json(reply):
    set_000_config("base.template", '"%s"' % request.get_vars.template)
    return json.dumps(reply)

def module_json(reply):
    return json.dumps(reply)

def db_connect(reply, db_string):
    # attempt to connect using the string
    try:
        db = DAL(db_string)
        session.db_string = db_string
        reply.detail = reply.detail + "<br>"+T("Connection to database <b>success</b>",
                                               lazy = False)
        reply.advanced = reply.advanced +\
                        "Connection using database string <b>%s</b> succeeded<br>" % db_string
        reply.dialog = "#sys-base-form"
        reply.sys_name = get_000_config("system_name", "Sahana Eden Humanitarian Management Platform")
        reply.sys_abbrv = get_000_config("system_name_short", "Sahana Eden")
        reply.sys_url = get_000_config("public_url", "http://127.0.0.1:8000")
        reply.next = "base"
    except:
        reply.result = False
        reply.detail = reply.detail + "<br>"+T("Connection to database <b>failed</b>",
                                               lazy = False)
        reply.advanced = reply.advanced +\
                        "Connection using database string <b>%s</b> failed<br>" % db_string
        reply.dialog = "#db-type-form"
        reply.next = "database"
    return reply

def strip_lib(msg):
    needle = "unresolved dependency: "
    start = msg.find(needle) + len(needle)
    finish = msg.find(" ", start)
    lib = msg[start:finish]
    return lib

def load_000_config():
    appname = session.appname
    # Read in the 000_config file
    base_cfg_file = "applications/%s/models/000_config.py" % appname
    try:
        input = open(base_cfg_file)
        with open(base_cfg_file, "r") as file:
            data = file.readlines()
    except:
        # No file so need to copy from templates
        # NOTE this code was copied from s3_upade_check (see check_python_libraries @todo)
        template_cfg_file = "applications/%s/private/templates/000_config.py" % appname
        input = open(template_cfg_file)
        output = open(base_cfg_file, "w")
        for line in input:
            if "akeytochange" in line:
                # Generate a random hmac_key to secure the passwords in case
                # the database is compromised
                import uuid
                hmac_key = uuid.uuid4()
                line = 'deployment_settings.auth.hmac_key = "%s"' % hmac_key
            output.write(line)
        output.close()
        input.close()
        input = open(base_cfg_file)
        with open(base_cfg_file, "r") as file:
            data = file.readlines()
    return data

def get_000_config(attr, default=None):
    data = load_000_config()
    if attr[-1] != " ":
        attr = attr + " "
    value = default
    for line in data:
        if attr in line and line[0] != "#":
            endvalue =line[line.rfind("= ")+2:]
            try:
                value = endvalue.split('"')[1]
            except: # value is not a string but a number so
                value = int(endvalue)
    return value

def set_000_config(attr, value, comment=False):
    if attr[-1] != " ":
        attr = attr + " "
    # Read in the 000_config file
    appname = session.appname
    base_cfg_file = "applications/%s/models/000_config.py" % appname
    with open(base_cfg_file, "r") as file:
        data = file.readlines()
    added = False
    attr_found = False
    cnt = 0
    for line in data:
        if attr in line:
            attr_found = True
            if value and value in line:
                while data[cnt][0] == "#":
                    data[cnt] = line[1:]
                added = True
            else:
                if line[0] != "#":
                    data[cnt] = "#%s" % line
        cnt += 1
    if not comment and not added:
        if attr_found:
            cnt = 0
            for line in data:
                if attr in line:
                    data[cnt] = "settings.%s = %s\n%s" % (attr, value, line)
                    break # so it is only added once
                cnt += 1
        else:
            # add the attr at the end of the file
            data.append("settings.%s = %s\n" % (attr, value))
    with open(base_cfg_file, 'w') as file:
        file.writelines( data )

def check_python_libraries():
    ''' 
        @todo: make this a separate function in s3_upade_check so that it can be reused

        it will be called as follows:

            from gluon.shell import exec_environment
            appname = session.appname
            module = "applications/%s/modules/s3_update_check.py" % appname
            s3check = exec_environment(module)
            result = s3check.check_python_libraries()

    ''' 
    # Fatal errors
    errors = []
    # Non-fatal warnings
    warnings = []

    # -------------------------------------------------------------------------
    # Check Python libraries
    try:
        import dateutil
    except ImportError:
        errors.append("S3 unresolved dependency: python-dateutil required for Sahana to run")
    try:
        import lxml
    except ImportError:
        errors.append("S3XML unresolved dependency: lxml required for Sahana to run")
    try:
        import shapely
    except ImportError:
        warnings.append("S3GIS unresolved dependency: shapely required for GIS support")
    try:
        import xlrd
    except ImportError:
        warnings.append("S3XLS unresolved dependency: xlrd required for XLS import")
    try:
        import xlwt
    except ImportError:
        warnings.append("S3XLS unresolved dependency: xlwt required for XLS export")
    try:
        from PIL import Image
    except ImportError:
        try:
            import Image
        except ImportError:
            warnings.append("S3PDF unresolved dependency: PIL (Python Imaging Library) required for PDF export")
    try:
        import reportlab
    except ImportError:
        warnings.append("S3PDF unresolved dependency: reportlab required for PDF export")
    try:
        from osgeo import ogr
    except ImportError:
        warnings.append("S3GIS unresolved dependency: GDAL required for Shapefile support")
    try:
        import tweepy
    except ImportError:
        warnings.append("S3Msg unresolved dependency: tweepy required for non-Tropo Twitter support")
    try:
        import sunburnt
    except ImportError, inst:
        warnings.append("S3Doc unresolved dependency: sunburnt required for Full-Text Search support")
    try:
        import pyth
    except ImportError:
        warnings.append("S3Doc unresolved dependency: pyth required for RTF document support in Full-Text Search")
    try:
        import matplotlib
    except ImportError:
        msg = "S3Chart unresolved dependency: matplotlib required for charting in Survey module"
        warnings.append(msg)
    try:
        import PyRTF
    except ImportError:
        msg = "Survey unresolved dependency: PyRTF required if you want to export assessment/survey templates as a Word document"
        warnings.append(msg)
    try:
        import numpy
    except ImportError:
        warnings.append("Vulnerability unresolved dependency: numpy required for Vulnerability module support")

    return {"error_messages": errors, "warning_messages": warnings}

def start():
    if not request.ajax:
        redirect("/%s/default/index" % app)

    session.known_apps = get_known_apps() # used by appname
    session.eden_apps = get_eden_apps()   # used by use_existing
    reply.detail = "Existing web2py apps are: %s" % session.known_apps
    reply.next = "setup_type"
    reply.dialog = "#setup-type-form"
    (reply.html, reply.script) = setup_type_dialog(app)
    return json.dumps(reply)

def get_known_apps():
    known_apps = []
    ls = os.listdir("applications")
    for obj in ls:
        path = os.path.join("applications", obj)
        if os.path.isdir(path):
            if os.path.isdir(os.path.join(path, ".git")):
                known_apps.append(obj)
    return known_apps

def get_eden_apps():
    eden_apps = []
    testLine = "Sahana Eden is an Emergency Development Environment"
    ls = os.listdir("applications")
    for app in session.known_apps:
        path = os.path.join("applications", app,"ABOUT")
        if os.path.isfile(path):
            file = open(path)
            if file.read(len(testLine)) == testLine:
                eden_apps.append(app)
    return eden_apps

def setup_type():
    if not request.ajax:
        redirect("/%s/default/index" % app)

    setup_type = request.get_vars.setup_type
    session.setup_type = setup_type
    reply.detail = reply.detail + T("Setup type <b>%s</b> selected" % setup_type,
                                    lazy = False)
    (reply.html, reply.script) = appname_dialog(app)
    if session.setup_type == "use":
        reply.next = "clone"
    else:
        reply.next = "appname"
        print settings.known_apps
        reply.exclude_list = session.known_apps
        reply.dialog = "#app-name-form"
    return json.dumps(reply)

def setup_type_dialog(app):
    setup = DIV(_id="setup-type-form",
                  _title=T("Select the type of setup you want to perform")
                 )
    setup.append(TABLE(
                       TR(TD(INPUT(_id = "setup_clone",
                             _name = "setup_type_in",
                             _type = "radio",
                             _value = "clone",
                             _checked = True
                            )),
                            TD(LABEL(T("Clone from git hub")))
                       ),
                       TR(TD(INPUT(_id = "setup_copy",
                             _name = "setup_type_in",
                             _type = "radio",
                             _value = "copy"
                            )),
                          TD(LABEL(T("Copy an existing Eden install")))
                       ),
                       TR(TD(INPUT(_id = "setup_use",
                             _name = "setup_type_in",
                             _type = "radio",
                             _value = "use"
                            )),
                          TD(LABEL(T("Use an existing unused Eden install")))
                       ),
                       TR(TD(INPUT(_id = "setup_update",
                             _name = "setup_type_in",
                             _type = "radio",
                             _value = "update",
                             _disabled="disabled"
                            )),
                          TD(LABEL(T("Update an existing Eden install (requires authentication)")))
                       ),
                       TR(TD(),
                          TD(I(T("Update is not yet enabled")))
                       )
                      ),
                  )
    script = "static/js/setuptype.js"
    return (setup.xml(), script)

def appname():
    if not request.ajax:
        redirect("/%s/default/index" % app)

    setup_type = session.setup_type
    if setup_type == "clone":
        reply.next = "git"
    else:
        reply.next = "clone"
    return appname_json(reply)

def appname_dialog(app):
    appName = DIV(_id="app-name-form",
                  _title=T("Enter an application name")
                 )
    appName.append(P(T("Enter the name you will call your application"),
                     _class="validateTips"))
    appName.append(FORM(LABEL(T("Application name")),
                        INPUT(_id = "appname_in",
                              _name = "appname_in",
                              _class="text ui-widget-content ui-corner-all",
                              value = "test"
                             )
                        )
                   )
    script = "static/js/appname.js"
    return (appName.xml(), script)

def appname_json(reply):
    appname = request.get_vars.appname
    reply.detail = T("Appname will be <b>%s</b>" % appname, lazy = False)
    session.appname =  appname
    path = os.path.join("applications", appname)
    if os.path.isdir(path):
        if os.path.isdir(os.path.join(path, ".git")):
            reply.detail = reply.detail +\
                           "<br>" +\
                           T("Directory %s already exists, so %s will not be cloned" % (appname, session.eden_release),
                                            lazy = False)
            reply.dialog = "#app-exists-alert"
            reply.next = "python"
            return json.dumps(reply)
    return json.dumps(reply)

def git():
    if not request.ajax:
        redirect("/%s/default/index" % app)

    reply.next = "clone"
    return git_json(reply)

def git_json(reply):
    from subprocess import Popen, PIPE
    try:
        cmd = ["git --version"]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        (myout, myerr) = p.communicate()
        reply.detail = T("Looking for git, <b>found:</b> %s" % myout, lazy = False)
        reply.advanced = myerr
    except Exception, inst:
        reply.result = False
        reply.fatal = T("Unable to continue, please install git",
                        lazy=False)
        reply.detail = "%s<br>" %(reply.fatal)
        reply.advanced = "<b>command:</b>%s<br><b>exception:</b>%s<br>" % (" ".join(cmd), inst)
    reply.next = "clone"
    return json.dumps(reply)

def clone():
    if not request.ajax:
        redirect("/%s/default/index" % app)

    reply.next = "python"
    return get_eden_json(reply)

def get_eden_json(reply):
    if session.setup_type == "clone":
        return clone_json(reply)
    if session.setup_type == "copy":
        return copy_json(reply)

def clone_json(reply):
    from subprocess import Popen, PIPE
    try:
        appname = session.appname
        eden = session.eden_release
        cmd = ["git clone https://github.com/flavour/eden.git applications/%s" % appname]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        (myout, myerr) = p.communicate()
        retcode = p.returncode
        if retcode != 0:
            reply.result = False
            reply.fatal = T("Unable to clone %s" % eden,
                            lazy=False)
            reply.detail = T("Cloning %s into application %s:<b> Failed</b>" % (eden, appname),
                             lazy = False)
            if myerr == "":
                reply.advanced = "<b>command: </b>%s<br><b>error:</b> %s<br>" % (" ".join(cmd), myout)
            else:
                reply.advanced = "<b>command: </b>%s<br><b>error:</b> %s<br>" % (" ".join(cmd), myerr)
        else:
            reply.detail = T("Cloning %s into application %s: <br>%s" % (eden, appname, myout),
                             lazy = False)
            reply.advanced = "<b>command: </b>%s<br>" % (" ".join(cmd))
    except Exception, inst:
        reply.result = False
        reply.fatal = T("Unable to clone %s" % eden,
                        lazy=False)
        reply.detail = reply.fatal + "<br>"
        reply.advanced = "<b>command: </b>%s<br><b>exception:</b>%s<br>" % (" ".join(cmd), inst)
        reply.next = "finished"
    reply.next = "python"
    return json.dumps(reply)

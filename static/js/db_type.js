btnName = "Continue";
unexpected_close = true;
args = new Object();

$(function() {
    $("#db-type-form").dialog({
        autoOpen: false,
        buttons: [{
            text: btnName,
            click: function() {
                args['db_type'] = $("input:radio[name=dbtype_in]:checked").val();
                unexpected_close = false;
                $( this ).dialog("close");
                $.get('/'+app+'/default/'+data.next, args).done(function(data){success(data)});
            }
        }],
        open: function (event, ui){
            $("input:radio[name=dbtype_in]").filter('[value="'+data.db_type+'"]').attr('checked', true);
        }
    });
});

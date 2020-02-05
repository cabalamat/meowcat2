/* app.js */

//--------------------------------------------------------------------
/* auto update */

function pollForAutoUpdate(url, mrts){
    //console.log("pollForAutoUpdate url=" + url + " mrts=" +mrts);
    $.ajax({
        url: url,
        method: "GET",
        dataType: "json",
    }).done(function(ts){
        console.log("pollForAutoUpdate ts=" + toString(ts));
        var ts2 = ts.ts;
        if (ts2>mrts) {
            /* refresh page */
            location.reload(true);
        } else {
            /* try again 10 s later */
            setTimeout(
                function(){pollForAutoUpdate(url, mrts)}, 
                15000);
        }
    }); 
}    

//--------------------------------------------------------------------
/* starring messages */

function starClicked(mid){
    console.log("starClicked mid=" + mid);
    var url = "/x/star/" + mid;
    $.ajax({
        url: url,
        method: "POST",
        dataType: "json"
    }).done(function(d){
        
        
    });     
}    

//--------------------------------------------------------------------
/* poll for alerts */

var dynamicAlerts=false;

function getActiveAlerts(){
    console.log("getActiveAlerts()");
    $.ajax({
        url: "/x/numActiveAlerts",
        method: "GET",
        dataType: "json",
    }).done(function(retVal){
        console.log("*** getActiveAlerts retVal=" + toString(retVal));
        var numAlerts = retVal[0];
        var alertCssClass = numAlerts>0 ? "alerts" : "";
        var h = `<a href='/alerts/current'>
<span class='alert-badge ${alertCssClass}'>
    ${numAlerts} <i class='fa fa-bell'></i>
</span></a>`;
        /**/
        $('#dyn_active_alerts').html(h);
        if (dynamicAlerts) setTimeout(getActiveAlerts, 60000);
    });
}

getActiveAlerts();

//--------------------------------------------------------------------
/* editting on wikiEdit page */

function addAround(b, a) {
    /* add text before and after the selected text */
    ($("#id_source")
        .selection('insert', {text: b, mode: 'before'})
        .selection('insert', {text: a, mode: 'after'}));
}

function addTable() {
    var t = ("\nHead 1 | Head 2 | Head 3\n"
        +      "------ | ------ | ------\n"
        +      "cell 1 | cell 2 | cell 3\n"
        +      "cell 4 | cell 5 | cell 6\n");
    addAround(t, "");
}

function blockquote() {
    var sel = $('#id_source').selection(); // selected text
    var lines = sel.split("\n");
    //console.log("lines=" + toString(lines));
    var bqLines = lines.map(line => {
        return "> " + line;
    });
    //console.log("bqLines=" + toString(bqLines));
    var bqSel = bqLines.join("\n");
    $('#id_source').selection('replace', {text: bqSel});
}

function bulletList() {
    var sel = $('#id_source').selection();
    var lines = sel.split("\n");
    var rLines = lines.map(line => {
        return "* " + line;
    });
    var r = rLines.join("\n");
    $('#id_source').selection('replace', {text: r});
}

function numberedList() {
    var sel = $('#id_source').selection();
    var lines = sel.split("\n");
    var n = 1;
    var rLines = lines.map(line => {
        return (n++) + ". " + line;
    });
    var r = rLines.join("\n");
    $('#id_source').selection('replace', {text: r});
}

function monospace() {
    /* Make text monospace. If it is all on one line, suround with `...`,
    else suround with ```...``` */
    var sel = $('#id_source').selection();
    var lines = sel.split("\n");
    if (lines.length <= 1){
        addAround("`", "`");
    } else {
        addAround("\n```\n", "\n```\n");
    }
}

//--------------------------------------------------------------------

//end
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
        url: "/numActiveAlerts",
        method: "GET",
        dataType: "json",
    }).done(function(retVal){
        console.log("*** getActiveAlerts retVal=" + toString(retVal));
        var numAlerts = retVal[0];
        var alertCssClass = numAlerts>0 ? "alerts" : "";
        var h = `<a href='/alerts/active'>
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

//end
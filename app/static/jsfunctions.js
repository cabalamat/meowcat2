/* jsfunctions.js */

/*****
Some javascript utility functions
*****/

//--------------------------------------------------------------------

function ObjToSource(o){
    if (!o) return 'null';
    if (typeof(o) == "object") {
        if (!ObjToSource.check) ObjToSource.check = new Array();
        for (var i=0, k=ObjToSource.check.length ; i<k ; ++i) {
            if (ObjToSource.check[i] == o) {return '{}';}
        }
        ObjToSource.check.push(o);
    }
    if (typeof(o) == "string"){
        return JSON.stringify(o);
    }
    var k="";
    var na=typeof(o.length)== "undefined" ? 1 : 0;
    var str="";
    for(var p in o){
        if (na) k = "'"+p+ "':";
        if (typeof o[p] == "string") str += k + "'" + o[p]+"',";
        else if (typeof o[p] == "object") str += k + ObjToSource(o[p])+",";
        else str += k + o[p] + ",";
    }
    if (typeof(o) == "object")
        ObjToSource.check.pop();

    if (na)
        return "{"+str.slice(0,-1)+"}";
    else
        return "["+str.slice(0,-1)+"]";
}

function toString(ob){
    /* convert an object to a string */
    return ObjToSource(ob);
}

//--------------------------------------------------------------------
/* functions on objects and arrays */

function dokv(ob, doSomething){
    /* do on keys and values
    */
    for (var property in ob) {
        if (ob.hasOwnProperty(property)) {
            var value = ob[property];
            doSomething(property, value);
        }
    }
}

function get(ob, key, value){
    /* If object (ob) has a property (key), then return it, else
    return (value)
    */
    if (ob.hasOwnProperty(key))
        return ob[key];
    else
        return value;
}

function contains(haystack, needle){
    for (var i=0; i<haystack.length; i++){
        if (haystack[i]===needle) return true;
    }
    return false;
}

function remove(a, item){
    /* remove all occurrances of (item) from array (a) */
    return a.filter(el => el!==item);
}


function including(a, item) {
    /* return an array like (a) but containing item (item).
    If it alrady contains it, just return (a).
    Else return a new array with (item) in it.
    */
    if (contains(a, item)) {
        return a;
    } else {
        var clone = a.slice(0);
        clone.push(item);
        return clone;
    }
}

function makeIdDict(obs){
    /*
    obs::[Object] has an 'id' key
    returns::{str:Object} where the keys are the ids
        from (obs)
    */
    var idDict = {};
    obs.forEach(ob => {
        var id = get(ob, 'id', "");
        if (id !== ""){
            idDict[id] = ob;
        }
    });
    return idDict;
}

function minimum(a){
    /* return the minimum value in an array */
    if (a.length===0) return null;
    var min;
    var first = true;
    a.forEach(e => {
        if (first){
            min = e;
        } else {
            if (e < min) min = e;
        }
        first = false;
    });
    return min;
}

//--------------------------------------------------------------------
/* functions on strings */

function removeSpaces(s) {
    /* return a string like (s) but with all spaces removed */
    return s.replace(/ /g, "");
}

//--------------------------------------------------------------------

/* end */

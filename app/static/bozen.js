/* bozen.js
   ========

Javascript for use with the Bozen library.
*/

//--------------------------------------------------------------------
/* date picker fields */

$(".bz-DateField").datepicker({
    dateFormat: 'yy-M-d',
    firstDay: 1,
});

$('.bz-DateTimeField').datetimepicker({
    dateFormat: 'yy-M-dd',
});


//--------------------------------------------------------------------
/* Tiny MCE -- WYSIWYG text editor */

tinymce.init({
    selector: '.wysiwyg',
    content_css: '/static/wizzy.css'
});

//--------------------------------------------------------------------

function deleteEntity(name, id){
    console.log("deleteEntity " + name + ", " + id);
    var msg = ("Do you really want to delete "
        + name + "?");
    bootbox.confirm(msg, function(result) {
        if (result) {
            reallyDeleteEntity(name, id);
        }
    });
}

function reallyDeleteEntity(name, id){
    console.log("reallyDeleteEntity " + id);
    document.getElementById("delete_record").value = "1";
    document.forms['theForm'].submit();
}

//--------------------------------------------------------------------


/*end*/

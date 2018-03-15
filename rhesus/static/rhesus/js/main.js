

$(document).ready(function(){
     /* Sort table */
    $("table.tablesorter").tablesorter({
        theme: "bootstrap",
        widthFixed: true,
        widgets: ['uitheme', 'zebra'],
        headerTemplate: '{content} {icon}'
    });

    $('[data-toggle=popover]').popover();
    $('[data-toggle=tooltip]').tooltip();
    $('input[type=text]').on('click', function() {return $(this).select()});
    $('textarea').on('click', function() {return $(this).select()});
    // $('textarea').on('click', function() {return $(this).select()});

    // Toggle modal
    $('body').on('hidden.bs.modal', '.modal',function(){return $(this).removeData('bs.modal')});
 });
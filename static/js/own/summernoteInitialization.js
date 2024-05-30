$(document).ready(function () {
    // Initializing Summernote for element with ID "material_text"
    $("#id_material_text").summernote({
        'width': '100%',
        'height': '240',
    });
    // Fixes for parameter differences in Bootstrap5
    let buttons = $('.note-editor button[data-toggle="dropdown"]');

    buttons.each((key, value) => {
        $(value).on('click', function (e) {
            $(this).attr('data-bs-toggle', 'dropdown')
            $(this).data('id', 'dropdownMenu');
        })
    })
});
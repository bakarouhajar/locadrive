$(document).ready(function() {
  $('input[type="checkbox"]').change(function() {
    var rental_id = $(this).data('rental-id');
    var field_name = $(this).attr('name');
    var field_value = $(this).is(':checked') ? 1 : 0;

    $.ajax({
      url: '/employee/update_field/',
      type: 'POST',
      data: {
        'rental_id': rental_id,
        'field_name': field_name,
        'field_value': field_value,
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
      },
      success: function(response) {
        console.log(response);
      },
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });
});

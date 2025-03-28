$(document).ready(function() {
    $('#yearLevelRow, #semesterRow').hide();
        
// Units Control System
function updateUnits() {
    const lec = parseInt($('#lec_units').val()) || 0;
    const lab = parseInt($('#lab_units').val()) || 0;
    $('#units').val(lec + lab);
}

function updateConstraints() {
    const lec = parseInt($('#lec_units').val()) || 0;
    const lab = parseInt($('#lab_units').val()) || 0;

    // Set max values based on current input
    $('#lec_units').attr('max', 3 - lab);
    $('#lab_units').attr('max', 3 - lec);
    
    // Validate current values
    if (lec > 3 - lab) $('#lec_units').val(3 - lab);
    if (lab > 3 - lec) $('#lab_units').val(3 - lec);
}

function handleUnitChange(input, direction) {
    const currentValue = parseInt(input.val()) || 0;
    const otherInput = input.attr('id') === 'lec_units' ? $('#lab_units') : $('#lec_units');
    const otherValue = parseInt(otherInput.val()) || 0;
    
    let newValue = currentValue;
    
    if (direction === 'up') {
        newValue = Math.min(currentValue + 1, 3 - otherValue);
    } else {
        newValue = Math.max(currentValue - 1, 0);
    }
    
    input.val(newValue);
    updateConstraints();
    updateUnits();
}

// Button click handlers
$('.increment').on('click', function() {
    const input = $(this).closest('.input-group').find('input[type="text"]');
    handleUnitChange(input, 'up');
});

$('.decrement').on('click', function() {
    const input = $(this).closest('.input-group').find('input[type="text"]');
    handleUnitChange(input, 'down');
});

// Input change handlers
$('#lec_units, #lab_units').on('input', function() {
    let value = parseInt($(this).val()) || 0;
    const otherId = $(this).attr('id') === 'lec_units' ? '#lab_units' : '#lec_units';
    const otherValue = parseInt($(otherId).val()) || 0;
    
    // Clamp value between 0 and (3 - otherValue)
    value = Math.min(Math.max(value, 0), 3 - otherValue);
    $(this).val(value);
    
    updateConstraints();
    updateUnits();
});

// Initial setup
updateConstraints();
updateUnits();

  // Initialize select2 for prerequisites.
  $('#prerequisites').select2({
    placeholder: "Select prerequisites",
    allowClear: true,
    width: '100%'
  });

  
  // Toggle Year Level and Semester based on Subject Type.
  function toggleSubjectFields() {
    var type = $('#subject_type').val().toUpperCase();
    if (type === 'MINOR') {
      $('#yearLevelRow, #semesterRow').hide();
    } else {
      $('#yearLevelRow, #semesterRow').show();
    }
  }
  $('#subject_type').change(toggleSubjectFields);
  toggleSubjectFields();





});
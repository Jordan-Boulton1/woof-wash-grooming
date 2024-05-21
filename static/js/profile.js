// Prevents the POST from running again on refresh or back button.
if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
}

document.addEventListener("DOMContentLoaded", function() {
  // Selecting elements
  const editButtons = document.querySelectorAll('.editBtn');
  const addPetButton = document.getElementById('addPetButton');
  const cancelButtons = document.querySelectorAll('.cancelBtn');
  const deletePetButtons = document.querySelectorAll('.deletePetBtn');
  const dateField = document.getElementById("start_date");
  const petField = document.getElementById("id_pet");
  const serviceField = document.getElementById("id_service");
  const description = document.getElementById("id_description");
  const dateFieldIcon = document.getElementById("start-date-icon");
  const appointmentIdField = document.getElementById("appointment_id");
  const petIdField = document.getElementById("pet_id");
  const cancelAppointmentIdField = document.getElementById("cancel_appointment_id");
  const deletePetIdField = document.getElementById("pet_id");
  const confirmCancelButton = document.getElementById("confirmCancelButton");
  const confirmDeletePetButton = document.getElementById("confirmDeletePetButton");
  const addPetModal = document.getElementById("addPetModal");
  const editPetButtons = document.querySelectorAll('.editPetBtn');

  // Handling tab triggers
  const triggerTabList = document.querySelectorAll('#v-tabs-tab button')
  triggerTabList.forEach(triggerEl => {
    const tabTrigger = new bootstrap.Tab(triggerEl)

    triggerEl.addEventListener('click', event => {
      event.preventDefault()
      tabTrigger.show()

    })
  })

  // Handle cancel buttons
  cancelButtons.forEach(function(btn) {
    const appointmentModal = document.getElementById("confirmCancelAppointmentModal");
    btn.addEventListener('click', function() {
      const appointmentId = btn.getAttribute('id');

      const modal = new bootstrap.Modal(appointmentModal);
      modal.show();
      confirmCancelButton.addEventListener("click", function() {
        cancelAppointmentIdField.value = appointmentId;
        let form = document.getElementById("cancelAppointmentForm");
        form.action = form.action.replace('/0/', '/' + appointmentId + '/');
        form.submit();
      });
    });
  });

  // Handle edit buttons
  editButtons.forEach(function(btn) {
    const appointmentModal = document.getElementById("editAppointmentModal");
    btn.addEventListener('click', function() {
      const appointmentId = btn.getAttribute('id');

      renderFlatPickr();
      renderCalendarIcon(dateFieldIcon, dateField);
      appointmentIdField.innerHTML = "";
      fetch(`/api/appointment/${appointmentId}/`)
      .then((response) => response.json())
      .then((data) => {
        const appointment = data.appointment

        setDefaultOption(dateField, appointment.start_date_time)
        setDefaultOption(description, appointment.description);
        setDefaultSelectOption(petField, appointment.pet.id);
        setDefaultSelectOption(serviceField, appointment.service.id);
        appointmentIdField.value = appointmentId;
      })

      const modal = new bootstrap.Modal(appointmentModal);
      modal.show();


    });
  });

  // Show add pet modal
  addPetButton.addEventListener('click', function() {
    const modal = new bootstrap.Modal(addPetModal);
    modal.show();
  });

  document.getElementById('saveChangesButton').addEventListener('click', function (event) {
        const editAppointmentForm = document.getElementById('editAppointmentForm');
        const editAppointmentFormData = new FormData(editAppointmentForm);
        const startDateTime = editAppointmentFormData.get('start_date_time');
        const convertedDateTime = convertDateTimeFormat(startDateTime);
        editAppointmentFormData.set('start_date_time', convertedDateTime);

        document.getElementById('editAppointmentFormErrors').innerHTML = '';

        fetch(editAppointmentForm.action, {
            method: 'POST',
            body: editAppointmentFormData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');
            const errorMessages = doc.querySelectorAll('#editAppointmentFormErrors .alert');

            const errorDiv = document.getElementById('editAppointmentFormErrors');
            errorMessages.forEach(error => {
                errorDiv.appendChild(error);
            });

            if (errorMessages.length === 0) {
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

   });

  // Handle add pet submit
document.getElementById('addPetSubmitButton').addEventListener('click', function(event) {
    event.preventDefault();
    const form = document.getElementById('addPetForm');
    const formData = new FormData(form);

    document.getElementById('petFormErrors').innerHTML = '';

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, 'text/html');
        const errorMessages = doc.querySelectorAll('#petFormErrors .alert');

        const errorDiv = document.getElementById('petFormErrors');
        errorMessages.forEach(error => {
            errorDiv.appendChild(error);
        });

        if (errorMessages.length === 0) {
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

 editPetButtons.forEach(function(btn) {
    const editPetModal = document.getElementById("editPetModal");
    btn.addEventListener('click', function() {
      const petId = btn.getAttribute('id');

      petIdField.innerHTML = "";
      fetch(`/api/pet/${petId}/`)
      .then((response) => response.json())
      .then((data) => {
        const pet = data.pet
        petIdField.value = petId;
          const petNameField = document.getElementById("edit_pet_name");
          const petBreedField = document.getElementById("edit_pet_breed");
          const petAgeField = document.getElementById("edit_pet_age");
          const petMedicalNotesField = document.getElementById("edit_medical_notes");
          setDefaultOption(petNameField, pet.name)
          setDefaultOption(petBreedField, pet.breed);
          setDefaultOption(petAgeField, pet.age);
          setDefaultOption(petMedicalNotesField, pet.medical_notes);
      })

      const modal = new bootstrap.Modal(editPetModal);
      modal.show();


    });
  });

 document.getElementById('editPetButton').addEventListener('click', function (event) {
        const editPetForm = document.getElementById('editPetForm');
        const editPetFormData = new FormData(editPetForm);

        document.getElementById('editPetFormErrors').innerHTML = '';

        fetch(editPetForm.action, {
            method: 'POST',
            body: editPetFormData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');
            const errorMessages = doc.querySelectorAll('#editPetFormErrors .alert');

            const errorDiv = document.getElementById('editPetFormErrors');
            errorMessages.forEach(error => {
                errorDiv.appendChild(error);
            });

            if (errorMessages.length === 0) {
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

   });

  // Handle delete buttons
  deletePetButtons.forEach(function(btn) {
    const deletePetModal = document.getElementById("confirmDeletePetModal");
    btn.addEventListener('click', function() {
      const petid = btn.getAttribute('id');
      const modal = new bootstrap.Modal(deletePetModal);
      modal.show();
      confirmDeletePetButton.addEventListener("click", function() {
        deletePetIdField.value = petid;
        let form = document.getElementById("deletePetForm");
        form.action = form.action.replace('/0/', '/' + petid + '/');
        form.submit();
      });

    });
  });
});

// Render Flatpickr date-time picker
function renderFlatPickr() {
  flatpickr('#start_date', {
    "dateFormat": "d-m-Y H:i",
    "enableTime": true
  });
}

// Render calendar icon
function renderCalendarIcon(icon, dateField) {
  icon.addEventListener("click", function(event) {
    event.preventDefault();
    dateField._flatpickr.open()
  });
}

// Set default option for field
function setDefaultOption(field, value) {
  field.value = value;
}

// Set default select option for field
function setDefaultSelectOption(field, id) {
  for (let i = 0; i < field.options.length; i++) {
    let option = field.options[i];
    if (option.value == id) {
      option.selected = true;
      break;
    }
  }
}

function convertDateTimeFormat(dateTimeStr) {
    // Assuming the incoming date format is "d-m-Y H:i"
    // Convert it to "Y-m-d H:i"
    const [datePart, timePart] = dateTimeStr.split(' ');
    const [day, month, year] = datePart.split('-');
    return `${year}-${month}-${day} ${timePart}`;
}
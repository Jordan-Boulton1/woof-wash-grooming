// Prevents the POST from running again on refresh or back button.
if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

document.addEventListener("DOMContentLoaded", function () {
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
    });
  });

  // Handle cancel appointment
  handleConfirmationModal(
    "confirmCancelAppointmentModal",
    "cancelAppointmentForm",
    cancelButtons,
    confirmCancelButton,
    cancelAppointmentIdField);

  // Handle edit appointment
  handleFormSubmit(
    "saveChangesButton",
    "editAppointmentForm",
    "editAppointmentFormErrors")

  // Handle edit appointment modal
  editButtons.forEach(function (btn) {
    const appointmentModal = document.getElementById("editAppointmentModal");
    btn.addEventListener('click', function () {
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
  addPetButton.addEventListener('click', function () {
    const modal = new bootstrap.Modal(addPetModal);
    modal.show();
  });

  // Handle add pet
  handleFormSubmit(
    "addPetSubmitButton",
    "addPetForm",
    "petFormErrors")

  // Handle edit pet modal
  editPetButtons.forEach(function (btn) {
    const editPetModal = document.getElementById("editPetModal");
    btn.addEventListener('click', function () {
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

  // Handle edit pet
    handleFormSubmit(
    "editPetButton",
    "editPetForm",
    "editPetFormErrors");

  // Handle delete pet
  handleConfirmationModal(
      "confirmDeletePetModal",
      "deletePetForm",
      deletePetButtons,
    confirmDeletePetButton,
      deletePetIdField);
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
  icon.addEventListener("click", function (event) {
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
function handleConfirmationModal(modal, confirmationForm, triggerButtons, confirmationButton, idField) {
  triggerButtons.forEach(function (btn) {
    const confirmationModal = document.getElementById(modal);
    btn.addEventListener('click', function (event) {
      event.preventDefault();
      const id = btn.getAttribute('id');

      const modal = new bootstrap.Modal(confirmationModal);
      modal.show();

      confirmationButton.addEventListener("click", function () {
        idField.value = id;
        let form = document.getElementById(confirmationForm);
        form.action = form.action.replace('/0/', '/' + id + '/');
        form.submit();
      });
    });
  });
}
function handleFormSubmit(submitButton, submitForm, formErrorContainer) {
  document.getElementById(submitButton).addEventListener('click', function (event) {
    event.preventDefault();
    const form = document.getElementById(submitForm);
    const formData = new FormData(form);
    const formType = formData.get("form_type");

    if (formType === 'edit_appointment_form') {
      const startDateTime = formData.get('start_date_time');
      const convertedDateTime = convertDateTimeFormat(startDateTime);
      formData.set('start_date_time', convertedDateTime);
    }

    document.getElementById(formErrorContainer).innerHTML = '';
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
        const errorMessages = doc.querySelectorAll(`#${formErrorContainer} .alert`);

        const errorDiv = document.getElementById(formErrorContainer);
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
  })
}
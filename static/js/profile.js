// Check if the browser supports the replaceState method
if (window.history.replaceState) {
    // Replace the current history state with a new one to prevent form resubmission
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
  const triggerTabList = document.querySelectorAll('#v-tabs-tab button');

  // Loop through each tab button
  triggerTabList.forEach(triggerEl => {
    const tabTrigger = new bootstrap.Tab(triggerEl);

    // Add a click event listener to each tab button
    triggerEl.addEventListener('click', event => {
      event.preventDefault();
      tabTrigger.show();
    });
  });


  // Handle cancel appointment
  handleConfirmationModal(
    "confirmCancelAppointmentModal",
    "cancelAppointmentForm",
    cancelButtons,
    confirmCancelButton,
    cancelAppointmentIdField
  );

  // Handle edit appointment
  handleFormSubmit(
    "saveChangesButton",
    "editAppointmentForm",
    "editAppointmentFormErrors"
  );

  // Handle edit appointment modal
  editButtons.forEach(function (btn) {
    // Get the modal element for editing appointments
    const appointmentModal = document.getElementById("editAppointmentModal");
    // Add a click event listener to each edit button
    btn.addEventListener('click', function () {
      // Get the appointment ID from the buttons attribute
      const appointmentId = btn.getAttribute('id');

      // Initialize Flatpickr date-time picker
      renderFlatPickr();
      // Render the calendar icon for the date field
      renderCalendarIcon(dateFieldIcon, dateField);
      // Clear the appointment ID field
      appointmentIdField.innerHTML = "";
      // Fetch appointment data from the API
      fetch(`/api/appointment/${appointmentId}/`)
        .then((response) => response.json())
        .then((data) => {
          const appointment = data.appointment;

          // Set default options for the form fields with fetched data
          setDefaultOption(dateField, appointment.start_date_time);
          setDefaultOption(description, appointment.description);
          setDefaultSelectOption(petField, appointment.pet.id);
          setDefaultSelectOption(serviceField, appointment.service.id);
          // Set the appointment ID in the hidden field
          appointmentIdField.value = appointmentId;
        });

      // Show the modal for editing appointments
      const modal = new bootstrap.Modal(appointmentModal);
      modal.show();
    });
  });

  // Show add pet modal
  addPetButton.addEventListener('click', function () {
    // Get the modal element for adding a pet
    const modal = new bootstrap.Modal(addPetModal);
    // Show the modal for adding a pet
    modal.show();
  });

  // Handle add pet
  handleFormSubmit(
    "addPetSubmitButton",
    "addPetForm",
    "petFormErrors"
  );

  // Handle edit pet modal
  editPetButtons.forEach(function (btn) {
    // Get the modal element for editing pets
    const editPetModal = document.getElementById("editPetModal");
    // Add a click event listener to each edit pet button
    btn.addEventListener('click', function () {
      // Get the pet ID from the button's attribute
      const petId = btn.getAttribute('id');

      // Clear the pet ID field
      petIdField.innerHTML = "";
      // Fetch pet data from the API
      fetch(`/api/pet/${petId}/`)
        .then((response) => response.json())
        .then((data) => {
          const pet = data.pet
          // Set default options for the form fields with the fetched pet data
          petIdField.value = petId;
          const petNameField = document.getElementById("edit_pet_name");
          const petBreedField = document.getElementById("edit_pet_breed");
          const petAgeField = document.getElementById("edit_pet_age");
          const petMedicalNotesField = document.getElementById("edit_medical_notes");
          setDefaultOption(petNameField, pet.name)
          setDefaultOption(petBreedField, pet.breed);
          setDefaultOption(petAgeField, pet.age);
          setDefaultOption(petMedicalNotesField, pet.medical_notes);
        });

      // Show the modal for editing pets
      const modal = new bootstrap.Modal(editPetModal);
      modal.show();
    });
  });

  // Handle edit pet form submission
    handleFormSubmit(
    "editPetButton",
    "editPetForm",
    "editPetFormErrors"
    );

  // Handle delete pet
  handleConfirmationModal(
      "confirmDeletePetModal",
      "deletePetForm",
      deletePetButtons,
      confirmDeletePetButton,
      deletePetIdField
  );
});

// Render Flatpickr date-time picker
function renderFlatPickr() {
  flatpickr('#start_date', {
    "dateFormat": "d-m-Y H:i",
    "enableTime": true,
    "minDate": "today",
    "disable": [
        // Disable weekends
        function(date) {
            return (date.getDay() === 0 || date.getDay() === 6);

        }
    ],
    "minTime": "08:00",
    "maxTime": "17:00",
  });
}

/**
 * Render calendar icon to trigger opening of the Flatpickr date-time picker.
 *
 * @param icon - The calendar icon element.
 * @param dateField - The input field associated with the Flatpickr date-time picker.
 */
function renderCalendarIcon(icon, dateField) {
  // Add a click event listener to the calendar icon
  icon.addEventListener("click", function (event) {
    event.preventDefault();

    // Open the Flatpickr date-time picker
    dateField._flatpickr.open()
  });
}

/**
 * Set the default value for a given field.
 *
 * @param field - The field element.
 * @param value - The default value to be set.
 */
function setDefaultOption(field, value) {
  // Set the value of the field to the provided value
  field.value = value;
}

/**
 * Set the default selected option for a given select field based on the provided ID.
 *
 * @param field - The select field element.
 * @param id - The ID of the option to be selected.
 */
function setDefaultSelectOption(field, id) {
  for (let i = 0; i < field.options.length; i++) {
    let option = field.options[i];
    if (option.value == id) {
      option.selected = true;
      break;
    }
  }
}

/**
 * Convert the format of a date-time string from "d-m-Y H:i" to "Y-m-d H:i".
 *
 * @param dateTimeStr - The date-time string in "d-m-Y H:i" format.
 * @returns The date-time string converted to "Y-m-d H:i" format.
 */
function convertDateTimeFormat(dateTimeStr) {
  const [datePart, timePart] = dateTimeStr.split(' ');
  const [day, month, year] = datePart.split('-');
  return `${year}-${month}-${day} ${timePart}`;
}

/**
 * Handle the confirmation modal for various actions triggered by specific buttons.
 *
 * @param modal - The ID of the confirmation modal element.
 * @param confirmationForm - The ID of the form associated with the confirmation action.
 * @param triggerButtons - The NodeList of buttons that trigger the confirmation modal.
 * @param confirmationButton - The confirmation button within the modal.
 * @param idField - The hidden input field storing the ID associated with the action.
 */
function handleConfirmationModal(modal, confirmationForm, triggerButtons, confirmationButton, idField) {
  // Iterate over each trigger button
  triggerButtons.forEach(function (btn) {
    // Get the confirmation modal
    const confirmationModal = document.getElementById(modal);
    // Add click event listener to the trigger button
    btn.addEventListener('click', function (event) {
      event.preventDefault();
      const id = btn.getAttribute('id');

      // Show the confirmation modal
      const modal = new bootstrap.Modal(confirmationModal);
      modal.show();

      // Add click event listener to the confirmation button within the modal
      confirmationButton.addEventListener("click", function () {
        idField.value = id;
        let form = document.getElementById(confirmationForm);
        // Update the form action URL to include the ID
        form.action = form.action.replace('/0/', '/' + id + '/');
        form.submit();
      });
    });
  });
}

/**
 * Handle form submission asynchronously.
 *
 * @param submitButton - The ID of the submit button.
 * @param submitForm - The ID of the form to be submitted.
 * @param formErrorContainer - The ID of the container to display form errors.
 */
function handleFormSubmit(submitButton, submitForm, formErrorContainer) {
  // Add click event listener to the submit button
  document.getElementById(submitButton).addEventListener('click', function (event) {
    event.preventDefault();
    const form = document.getElementById(submitForm);
    const formData = new FormData(form);
    const formType = formData.get("form_type");

    // If the form type is edit_appointment_form, convert the date-time format
    if (formType === 'edit_appointment_form') {
      const startDateTime = formData.get('start_date_time');
      const convertedDateTime = convertDateTimeFormat(startDateTime);
      formData.set('start_date_time', convertedDateTime);
    }

    // Clear the form error container
    document.getElementById(formErrorContainer).innerHTML = '';

    // Send a fetch request to the form action URL with form data
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
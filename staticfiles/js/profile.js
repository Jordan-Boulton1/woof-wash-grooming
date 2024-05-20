// Execute when the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Selecting elements
  const editButtons = document.querySelectorAll('.editBtn');
  const addPetButton = document.getElementById('addPetButton');
  const cancelButtons = document.querySelectorAll('.cancelBtn');
  const dateField = document.getElementById("start_date");
  const petField = document.getElementById("id_pet");
  const serviceField = document.getElementById("id_service");
  const description = document.getElementById("id_description");
  const dateFieldIcon = document.getElementById("start-date-icon");
  const appointmentIdField = document.getElementById("appointment_id");
  const cancelAppointmentIdField = document.getElementById("cancel_appointment_id");
  const confirmCancelButton = document.getElementById("confirmCancelButton");
  const appointmentModal = document.getElementById("addPetModal");
  const addPetSubmitButton = document.getElementById("addPetSubmitButton");

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

      document.getElementById('saveChangesButton').addEventListener('click', function () {
        console.log(appointmentIdField.value);
        document.getElementById('editAppointmentForm').submit();
      });
    });
  });

  // Show add pet modal
  addPetButton.addEventListener('click', function() {
    const modal = new bootstrap.Modal(appointmentModal);
    modal.show();
  });

  // Handle add pet submit
  addPetSubmitButton.addEventListener("click", function() {
    document.getElementById('addPetForm').submit();
  })
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
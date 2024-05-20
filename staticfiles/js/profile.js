document.addEventListener("DOMContentLoaded", function() {
  const editButtons = document.querySelectorAll('.editBtn');
  const cancelButtons = document.querySelectorAll('.cancelBtn');
  const dateField = document.getElementById("start_date");
  const petField = document.getElementById("id_pet");
  const serviceField = document.getElementById("id_service");
  const description = document.getElementById("id_description");
  const dateFieldIcon = document.getElementById("start-date-icon");
  const appointmentIdField = document.getElementById("appointment_id");
  const cancelAppointmentIdField = document.getElementById("cancel_appointment_id");
  const confirmCancelButton = document.getElementById("confirmCancelButton")


  const triggerTabList = document.querySelectorAll('#v-tabs-tab button')
  triggerTabList.forEach(triggerEl => {
    const tabTrigger = new bootstrap.Tab(triggerEl)

    triggerEl.addEventListener('click', event => {
      event.preventDefault()
      tabTrigger.show()
    })
  })

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
});

function renderFlatPickr() {
   flatpickr('#start_date', {
       "dateFormat": "d-m-Y H:i",
       "enableTime": true
    });
}

function renderCalendarIcon(icon, dateField) {
  icon.addEventListener("click", function(event) {
    event.preventDefault();
    dateField._flatpickr.open()
  });
}


function setDefaultOption(field, value) {
    field.value = value;
}

function setDefaultSelectOption(field, id) {
    for (let i = 0; i < field.options.length; i++) {
        let option = field.options[i];
        if (option.value == id) {
            option.selected = true;
            break;
        }
    }
}
document.addEventListener("DOMContentLoaded", function() {
  const editButtons = document.querySelectorAll('.editBtn');
  const dateField = document.getElementById("start_date");
  const timeField = document.getElementById("id_start_time");
  const petField = document.getElementById("id_pet");
  const serviceField = document.getElementById("id_service");
  const description = document.getElementById("id_description");
  const dateFieldIcon = document.getElementById("start-date-icon");
  const editAppointmentBtn = document.getElementById("edit-appointment");
  const appointmentIdField = document.getElementById("appointment_id");

  editButtons.forEach(function(btn) {
    const appointmentModal = document.getElementById("editAppointmentModal");
    btn.addEventListener('click', function() {
      const appointmentId = btn.getAttribute('id');
   
      renderFlatPickr();
      renderCalendarIcon(dateFieldIcon, dateField);
      timeField.innerHTML = "";
      appointmentIdField.innerHTML = "";
      fetch(`/api/appointment/${appointmentId}/`)
      .then((response) => response.json())
      .then((data) => {
            const appointment = data.appointment
            setDefaultOption(dateField, appointment.start_date)
            setDefaultOption(description, appointment.description);
            setDefaultSelectOption(petField, appointment.pet.id);
            setDefaultSelectOption(serviceField, appointment.service.id);
            addDateChangeHandler(dateField, timeField, appointment.start_time);
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
  fetch(`/api/available-appointment-dates/`)
  .then((response) => response.json())
  .then((appointments) => {
    flatpickr('#start_date', {
      "dateFormat": "d-m-Y",
      "enable": appointments.map((x) => new Date(x))
    });    
  });
}
function renderCalendarIcon(icon, dateField) {
  icon.addEventListener("click", function(event) {
    event.preventDefault();
    dateField._flatpickr.open()
  });
}

function addDateChangeHandler(dateField, timeField, defaultTime) {
  createOptionElement(timeField, defaultTime, defaultTime);
  dateField.addEventListener("change", function() {
    const selectedDate = dateField.value;

    if (selectedDate) {
        fetch(`/api/available-times/${selectedDate}/`)
            .then((response) => response.json())
            .then((times) => {
                timeField.innerHTML = "";
                setDefaultOption(timeField, "Select a time");
                times.forEach((time) => {
                   createOptionElement(timeField, time, time);
                });
            })
            .catch((error) => console.error("Error fetching available times:", error));
    } else {
        timeField.innerHTML = "";
    }
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

function createOptionElement(timeField, value, text) {
  const option = document.createElement("option");
  option.value = value;
  option.text = text;
  timeField.appendChild(option);
}
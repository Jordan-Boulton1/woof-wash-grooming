var editButtons = document.querySelectorAll('.editBtn');
  editButtons.forEach(function(btn) {
     var appointmentModal = document.getElementById("editAppointmentModal");
    btn.addEventListener('click', function() {
      var appointmentId = btn.getAttribute('id');
      console.log(appointmentId)
      
      var modal = new bootstrap.Modal(appointmentModal);
      modal.show();
    });
  });
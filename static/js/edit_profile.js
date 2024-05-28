if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}
document.addEventListener("DOMContentLoaded", function () {
  const deleteUserBtn = document.getElementById('deleteUserBtn');
  const deleteUserMdodal = document.getElementById('confirmDeleteProfileModal');
  const confirmDeleteUser = document.getElementById('confirmDeleteUserButton');

// Show delete user modal
  deleteUserBtn.addEventListener('click', function () {
    const modal = new bootstrap.Modal(deleteUserMdodal);
    modal.show();
    const hiddenUserIdInput = deleteUserMdodal.getElementsByClassName('hidden_input')
    const user_id = hiddenUserIdInput[0].getAttribute('id');
    confirmDeleteUser.addEventListener("click", function () {
        let form = document.getElementById('deleteUserForm');
        form.action = form.action.replace('/0/', '/' + user_id + '/');
        form.submit();
      });
  });
});
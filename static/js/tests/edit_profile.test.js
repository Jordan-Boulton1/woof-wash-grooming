import { editProfile } from '../edit_profile.js';

// Mocking window.history.replaceState
beforeAll(() => {
  Object.defineProperty(window.history, 'replaceState', {
    writable: true,
    value: jest.fn(),
  });
});

// Mocking document.getElementById
beforeEach(() => {
  document.body.innerHTML = `
    <button id="deleteUserBtn">Delete User</button>
    <div id="confirmDeleteProfileModal">
      <input type="hidden" class="hidden_input" id="userId" value="123">
      <button id="confirmDeleteUserButton">Confirm Delete</button>
    </div>
    <form id="deleteUserForm" action="/delete/0/" method="post"></form>
  `;
});

// Mocking bootstrap modal
class Modal {
  show() {
    document.getElementById('confirmDeleteProfileModal').classList.add('show');
  }
}

global.bootstrap = {
  Modal: Modal
};

// Mocking form submit
HTMLFormElement.prototype.submit = jest.fn();
test('editProfile adds event listeners', () => {
  editProfile();

  // Simulate click on delete user button
  document.getElementById('deleteUserBtn').click();

  // Check if modal is shown
  expect(document.getElementById('confirmDeleteProfileModal').classList).toContain('show');

  // Simulate click on confirm delete user button
  document.getElementById('confirmDeleteUserButton').click();

  // Check if form action is updated
  expect(document.getElementById('deleteUserForm').getAttribute('action')).toBe('http://localhost/delete/userId/');

  // Check if form is submitted
  expect(HTMLFormElement.prototype.submit).toHaveBeenCalled();
});

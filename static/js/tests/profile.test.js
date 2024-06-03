/**
 * @jest-environment jsdom
 */

const { delayBeforeReroute } = require('../shared.js');

const { setDefaultOption, setDefaultSelectOption, handleFormSubmit, convertDateTimeFormat, handleMessageRendering } = require('../profile.js');


// Mock dependencies
jest.mock('../shared.js', () => ({
  delayBeforeReroute: jest.fn(),
  handleMessageRendering: jest.fn(),
  convertDateTimeFormat: jest.fn((datetime) => datetime),
  handleFormSubmit: jest.requireActual('../profile.js').handleFormSubmit,
}));
test('sets the default value for a form field', () => {
  document.body.innerHTML = `<input id="testField" value="">`;
  const field = document.getElementById('testField');

  setDefaultOption(field, 'testValue');

  expect(field.value).toBe('testValue');
});

test('sets the default selected option for a select field', () => {
  document.body.innerHTML = `
    <select id="testSelect">
      <option value="1">Option 1</option>
      <option value="2">Option 2</option>
      <option value="3">Option 3</option>
    </select>`;
  const field = document.getElementById('testSelect');

  setDefaultSelectOption(field, '2');

  expect(field.value).toBe('2');
});

test('converts date-time format from d-m-Y H:i to Y-m-d H:i', () => {
  const input = '03-06-2024 15:30';
  const output = convertDateTimeFormat(input);

  expect(output).toBe('2024-06-03 15:30');
});

describe('handleFormSubmit', () => {
  beforeEach(() => {
    // Setting up the document body
    document.body.innerHTML = `
      <form id="testForm" action="/submit">
        <input name="start_date_time" value="03-06-2024 15:30">
        <input name="form_type" value="edit_appointment_form">
      </form>
      <div id="testFormErrors"></div>
      <button id="testSubmitButton"></button>`;

    // Resetting fetch mocks
    fetch.resetMocks();
  });

  test('handles form submission', async () => {
    // Mocking fetch response
    fetch.mockResponseOnce('<div class="alert"></div>');

    // Calling handleFormSubmit and triggering the submit button click
    handleFormSubmit('testSubmitButton', 'testForm', 'testFormErrors');
    document.getElementById('testSubmitButton').click();

    // Waiting for all microtasks to complete
    await Promise.resolve();

    // Assertions
    expect(fetch).toHaveBeenCalledWith('http://localhost/submit', expect.anything());
  });
});

describe('handleMessageRendering', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div id="testFormErrors"></div>`;
  });

  test('renders form messages', () => {
    const data = `
      <div id="testFormErrors">
        <div class="alert">Error message</div>
        <div class="alert alert-success">Success message</div>
      </div>`;

    handleMessageRendering('testFormErrors', data);

    const errorsContainer = document.getElementById('testFormErrors');
    expect(errorsContainer.innerHTML).toContain('Error message');
    expect(errorsContainer.innerHTML).toContain('Success message');
  });
});
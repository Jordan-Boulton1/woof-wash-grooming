/**
 * @jest-environment jsdom
 */

const { delayBeforeReroute } = require('../shared.js');

// Mock the delayBeforeReroute function
jest.mock('../shared.js', () => ({
  delayBeforeReroute: jest.fn(),
}));

describe('login.js', () => {
  beforeAll(() => {
    // Mock window.history.replaceState
    if (!window.history.replaceState) {
      window.history.replaceState = jest.fn();
    } else {
      jest.spyOn(window.history, 'replaceState').mockImplementation(jest.fn());
    }
  });

  beforeEach(() => {
    // Reset the mock functions before each test
    jest.clearAllMocks();
    document.body.innerHTML = '';
  });

  test('should call replaceState to prevent form resubmission on page reload', () => {
    // Import the login.js file to run its code
    require('../login.js');

    // Check if replaceState was called with the correct arguments
    expect(window.history.replaceState).toHaveBeenCalledWith(null, null, window.location.href);
  });

  test('should call delayBeforeReroute with the root URL after DOMContentLoaded', () => {
    // Simulate DOMContentLoaded event
    document.dispatchEvent(new Event('DOMContentLoaded'));

    // Check if delayBeforeReroute was called with the correct argument
    expect(delayBeforeReroute).toHaveBeenCalledWith('/');
  });
});

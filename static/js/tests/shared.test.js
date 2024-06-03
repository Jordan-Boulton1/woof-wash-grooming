/**
 * @jest-environment jsdom
 */

import { delayBeforeReroute } from '../shared.js';

describe('shared.js', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.clearAllTimers();
    jest.restoreAllMocks(); // Restore all mocks to their original implementations
  });

  describe('delayBeforeReroute', () => {
    test('should not redirect if there are no success messages', () => {
      document.body.innerHTML = ``;
      const location = 'http://example.com';

      // Mock setTimeout
      jest.spyOn(window, 'setTimeout');

      delayBeforeReroute(location);

      expect(setTimeout).not.toHaveBeenCalled();
    });
  });

  describe('DOMContentLoaded event listener', () => {
    test('should hide parent element when close button is clicked', () => {
      document.body.innerHTML = `
        <div class="alert">
          <button class="close">Close</button>
        </div>
      `;

      // Simulate DOMContentLoaded event
      document.dispatchEvent(new Event('DOMContentLoaded'));

      const closeButton = document.querySelector('.close');
      closeButton.click();

      const alertDiv = closeButton.parentElement;
      expect(alertDiv.style.display).toBe('none');
    });
  });
});

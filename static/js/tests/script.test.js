/**
 * @jest-environment jsdom
 */

const { delayBeforeReroute } = require('../shared.js');

// Mock the delayBeforeReroute function
jest.mock('../shared.js', () => ({
  delayBeforeReroute: jest.fn(),
}));


describe("Script functionality", () => {
  describe("Check window.history.replaceState", () => {
    test("should call window.history.replaceState if supported", () => {
      // Mock the window.history.replaceState method
      const replaceStateMock = jest.fn();
      Object.defineProperty(window.history, "replaceState", {
        value: replaceStateMock,
      });

      // Reload the script to trigger the code execution
      jest.resetModules();
      require("../script.js");

      // Expectation
      expect(replaceStateMock).toHaveBeenCalled();
    });
  });

  describe("Event listeners", () => {
    // Mocking DOM elements and events
    beforeEach(() => {
      document.body.innerHTML = `
        <div id="start-date-icon"></div>
        <select id="id_service">
          <option value="1">Service 1</option>
          <option value="2">Service 2</option>
        </select>
        <div class="django-flatpickr"></div>
        <div id="servicePrice"></div>
      `;
    });

    test("should attach click event listener to date field icon", () => {
      // Run the script to attach event listeners
      jest.resetModules();
      require("../script.js");

      // Simulate click event
      const dateFieldIcon = document.getElementById("start-date-icon");
      dateFieldIcon.click();

      // Expectation
      // Add expectation here
    });

    test("should attach change event listener to service select", () => {
      // Run the script to attach event listeners
      jest.resetModules();
      require("../script.js");

      // Simulate change event
      const serviceSelect = document.getElementById("id_service");
      serviceSelect.value = "1";
      serviceSelect.dispatchEvent(new Event("change"));

      // Expectation
      // Add expectation here
    });
  });

  describe("delayBeforeReroute function", () => {
    // Mocking window object for delayBeforeReroute test
    beforeEach(() => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          json: () => Promise.resolve({ price_range: { vary_price1: 10, vary_price2: 20 } }),
        })
      );
    });

    test("should delay before reroute", async () => {
      // Mocking the delay time
      jest.useFakeTimers();

      // Run the function
      delayBeforeReroute("/profile");

      // Fast-forward time
      jest.advanceTimersByTime(3000);

      // Expectation
      // Add expectation here
    });
  });
});
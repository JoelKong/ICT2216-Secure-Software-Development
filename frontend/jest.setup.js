import { TextEncoder, TextDecoder } from "util";

global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

beforeAll(() => {
  // Suppress console logs during tests
  jest.spyOn(console, "error").mockImplementation(() => {});

  // The below 2 lines are commented out to avoid suppressing errors and warnings.
  // jest.spyOn(console, "log").mockImplementation(() => {});
  // jest.spyOn(console, "warn").mockImplementation(() => {});
});

afterAll(() => {
  jest.restoreAllMocks();
});

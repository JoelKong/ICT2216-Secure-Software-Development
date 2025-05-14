import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import LoginForm from "../../components/auth/LoginForm";

// Mock constants
jest.mock("../../const", () => ({
  API_ENDPOINT: "http://localhost:5000",
  LOGIN_ROUTE: "api/login",
}));

// Login form test cases
describe("LoginForm Component", () => {
  const mockSetIsSignup = jest.fn();
  const mockSetModal = jest.fn();
  const mockSetRateLimit = jest.fn();
  const mockRateLimit = { attempts: 0, cooldown: false };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Check if rendered properly
  test("renders login form correctly", () => {
    render(
      <LoginForm
        setIsSignup={mockSetIsSignup}
        setModal={mockSetModal}
        rateLimit={mockRateLimit}
        setRateLimit={mockSetRateLimit}
      />
    );

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /log in/i })).toBeInTheDocument();
  });

  // Check if theres an error when fields are empty
  test("displays error when fields are empty", async () => {
    render(
      <LoginForm
        setIsSignup={mockSetIsSignup}
        setModal={mockSetModal}
        rateLimit={mockRateLimit}
        setRateLimit={mockSetRateLimit}
      />
    );

    fireEvent.submit(screen.getByTestId("loginform"));

    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message: "All fields are required",
      });
    });
  });

  // Check if rate limiting works
  test("handles rate limiting correctly", async () => {
    render(
      <LoginForm
        setIsSignup={mockSetIsSignup}
        setModal={mockSetModal}
        rateLimit={{ attempts: 5, cooldown: true }}
        setRateLimit={mockSetRateLimit}
      />
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /log in/i }));

    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message:
          "Too many attempts. Please wait a short while before trying again.",
      });
    });
  });

  // Test to ensure API request is not sent when rate limiting occurs
  test("does not send API request when rate limiting occurs for login page", async () => {
    global.fetch = jest.fn();

    render(
      <LoginForm
        setIsSignup={mockSetIsSignup}
        setModal={mockSetModal}
        rateLimit={{ attempts: 5, cooldown: true }}
        setRateLimit={mockSetRateLimit}
      />
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /log in/i }));

    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message:
          "Too many attempts. Please wait a short while before trying again.",
      });
    });

    expect(global.fetch).not.toHaveBeenCalled();

    global.fetch.mockRestore();
  });

  // Test if login sends data to the server
  test("sends login data to the server", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ message: "Login successful" }),
      })
    );

    render(
      <LoginForm
        setIsSignup={mockSetIsSignup}
        setModal={mockSetModal}
        rateLimit={mockRateLimit}
        setRateLimit={mockSetRateLimit}
      />
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "Password123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /log in/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:5000/api/login",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            email: "test@example.com",
            password: "Password123!",
          }),
        })
      );
    });

    global.fetch.mockRestore();
  });

  // Test if server error is handled correctly
  test("displays error when server returns an error", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ error: "Invalid credentials" }),
      })
    );

    render(
      <LoginForm
        setIsSignup={mockSetIsSignup}
        setModal={mockSetModal}
        rateLimit={mockRateLimit}
        setRateLimit={mockSetRateLimit}
      />
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "WrongPassword" },
    });
    fireEvent.click(screen.getByRole("button", { name: /log in/i }));

    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message: "Invalid credentials",
      });
    });

    global.fetch.mockRestore();
  });
});

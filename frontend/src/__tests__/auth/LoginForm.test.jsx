import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import { MemoryRouter } from "react-router-dom";
import LoginForm from "../../components/auth/LoginForm";
import { GlobalContext } from "../../utils/globalContext";

// Mock constants
jest.mock("../../const", () => ({
  API_ENDPOINT: "http://localhost:5000",
  LOGIN_ROUTE: "api/login",
}));

describe("LoginForm Component", () => {
  // Mock States
  const mockSetIsSignup = jest.fn();
  const mockSetModal = jest.fn();
  const mockSetRateLimit = jest.fn();
  const mockSetAuth = jest.fn();
  const mockRateLimit = { attempts: 0, cooldown: false };

  // Get global states from global context
  const renderWithContext = (ui, contextOverrides = {}) => {
    const contextValue = {
      setModal: mockSetModal,
      rateLimit: mockRateLimit,
      setRateLimit: mockSetRateLimit,
      setAuth: mockSetAuth,
      ...contextOverrides,
    };
    return render(
      <GlobalContext.Provider value={contextValue}>
        <MemoryRouter>{ui}</MemoryRouter>
      </GlobalContext.Provider>
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Render login form correctly
  test("renders login form correctly", () => {
    renderWithContext(<LoginForm setIsSignup={mockSetIsSignup} />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /log in/i })).toBeInTheDocument();
  });

  // Validation when fields are empty
  test("displays error when fields are empty", async () => {
    renderWithContext(<LoginForm setIsSignup={mockSetIsSignup} />);
    fireEvent.submit(screen.getByTestId("loginform"));
    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message: "All fields are required",
      });
    });
  });

  // If rate limit attempts reach dont send api request
  test("does not send API request when rate limiting occurs for login page", async () => {
    global.fetch = jest.fn();
    renderWithContext(<LoginForm setIsSignup={mockSetIsSignup} />, {
      rateLimit: { attempts: 5, cooldown: true },
    });
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

  // Sending of data to backend server
  test("sends login data to the server", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ message: "Login successful" }),
      })
    );
    renderWithContext(<LoginForm setIsSignup={mockSetIsSignup} />);
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

  // If server returns an error display it
  test("displays error when server returns an error", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ error: "Invalid credentials" }),
      })
    );
    renderWithContext(<LoginForm setIsSignup={mockSetIsSignup} />);
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

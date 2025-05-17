import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import SignupForm from "../../components/auth/SignupForm";
import { MemoryRouter } from "react-router-dom";

// Mock constants
jest.mock("../../const", () => ({
  API_ENDPOINT: "http://localhost:5000",
  SIGNUP_ROUTE: "api/signup",
}));

// Sign up form test cases
describe("SignupForm Component", () => {
  const mockSetIsSignup = jest.fn();
  const mockSetModal = jest.fn();
  const mockSetRateLimit = jest.fn();
  const mockSetAuth = jest.fn();
  const mockRateLimit = { attempts: 0, cooldown: false };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Check if rendered properly
  test("renders signup form correctly", () => {
    render(
      <MemoryRouter>
        <SignupForm
          setIsSignup={mockSetIsSignup}
          setModal={mockSetModal}
          rateLimit={mockRateLimit}
          setRateLimit={mockSetRateLimit}
          setAuth={mockSetAuth}
        />
      </MemoryRouter>
    );

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText("Password:")).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /sign up/i })
    ).toBeInTheDocument();
  });

  // Check if password match validation is successful
  test("displays error when passwords do not match", async () => {
    render(
      <MemoryRouter>
        <SignupForm
          setIsSignup={mockSetIsSignup}
          setModal={mockSetModal}
          rateLimit={mockRateLimit}
          setRateLimit={mockSetRateLimit}
          setAuth={mockSetAuth}
        />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" },
    });

    fireEvent.change(screen.getByLabelText("Password:"), {
      target: { value: "Password123!" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "DifferentPassword123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message: "Passwords do not match.",
      });
    });
  });

  // Test if rate limiting works for signup
  test("handles rate limiting correctly during signup", async () => {
    render(
      <MemoryRouter>
        <SignupForm
          setIsSignup={mockSetIsSignup}
          setModal={mockSetModal}
          rateLimit={{ attempts: 5, cooldown: true }}
          setRateLimit={mockSetRateLimit}
          setAuth={mockSetAuth}
        />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" },
    });

    fireEvent.change(screen.getByLabelText("Password:"), {
      target: { value: "Password123!" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "Password123!" },
    });

    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

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
  test("does not send API request when rate limiting occurs for signup page", async () => {
    global.fetch = jest.fn();

    render(
      <MemoryRouter>
        <SignupForm
          setIsSignup={mockSetIsSignup}
          setModal={mockSetModal}
          rateLimit={{ attempts: 5, cooldown: true }}
          setRateLimit={mockSetRateLimit}
          setAuth={mockSetAuth}
        />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" },
    });

    fireEvent.change(screen.getByLabelText("Password:"), {
      target: { value: "Password123!" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "Password123!" },
    });

    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

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

  // Test if email regex validation works
  test("displays error for invalid email format", async () => {
    render(
      <MemoryRouter>
        <SignupForm
          setIsSignup={mockSetIsSignup}
          setModal={mockSetModal}
          rateLimit={mockRateLimit}
          setRateLimit={mockSetRateLimit}
          setAuth={mockSetAuth}
        />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "invalid-email" },
    });
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" },
    });

    fireEvent.change(screen.getByLabelText("Password:"), {
      target: { value: "Password123!" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "Password123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message: "Please enter a valid email address",
      });
    });
  });

  // Test if password format validation works
  test("displays error for invalid password format", async () => {
    render(
      <MemoryRouter>
        <SignupForm
          setIsSignup={mockSetIsSignup}
          setModal={mockSetModal}
          rateLimit={mockRateLimit}
          setRateLimit={mockSetRateLimit}
          setAuth={mockSetAuth}
        />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" },
    });
    // Invalid password (e.g., too short or missing special character)
    fireEvent.change(screen.getByLabelText("Password:"), {
      target: { value: "pass" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "pass" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message:
          "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.",
      });
    });
  });

  // Test if signup sends data to the server
  test("sends signup data to the server", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ message: "Sign up was successful!" }),
      })
    );

    render(
      <MemoryRouter>
        <SignupForm
          setIsSignup={mockSetIsSignup}
          setModal={mockSetModal}
          rateLimit={mockRateLimit}
          setRateLimit={mockSetRateLimit}
          setAuth={mockSetAuth}
        />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" },
    });
    fireEvent.change(screen.getByLabelText("Password:"), {
      target: { value: "Password123!" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "Password123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:5000/api/signup",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            email: "test@example.com",
            username: "testuser",
            password: "Password123!",
            confirmPassword: "Password123!",
          }),
        })
      );
    });

    global.fetch.mockRestore();
  });

  // Test if server error is handled correctly during signup
  test("displays error when server returns an error during signup", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ error: "Email already in use." }),
      })
    );

    render(
      <MemoryRouter>
        <SignupForm
          setIsSignup={mockSetIsSignup}
          setModal={mockSetModal}
          rateLimit={mockRateLimit}
          setRateLimit={mockSetRateLimit}
          setAuth={mockSetAuth}
        />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" },
    });
    fireEvent.change(screen.getByLabelText("Password:"), {
      target: { value: "Password123!" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "Password123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

    await waitFor(() => {
      expect(mockSetModal).toHaveBeenCalledWith({
        active: true,
        type: "fail",
        message: "Email already in use.",
      });
    });

    global.fetch.mockRestore();
  });
});

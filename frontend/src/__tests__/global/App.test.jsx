import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import App from "../../App";
import { MemoryRouter } from "react-router-dom";

// Mock constants
jest.mock("../../const", () => ({
  API_ENDPOINT: "http://localhost:5000",
}));

jest.mock("../../utils/upgradeMembership", () => ({
  stripe_publishable_key: "test_key",
}));

// Mock fetch for user profile
const mockFetchUser = (user = null, ok = true) => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok,
      json: () => Promise.resolve(user ? { user } : {}),
    })
  );
};

describe("App Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  test("renders AuthPage when not authenticated", async () => {
    mockFetchUser();
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>
    );
    await waitFor(() =>
      expect(
        screen.getByText(/The Leonardo Discussion Room/i)
      ).toBeInTheDocument()
    );
  });

  test("redirects to /posts and renders HomePage when authenticated", async () => {
    const user = {
      username: "testuser",
      email: "test@example.com",
      membership: "basic",
      profile_picture: "",
      created_at: "2024-01-01T00:00:00Z",
      post_limit: 2,
    };
    localStorage.setItem("access_token", "testtoken");
    mockFetchUser(user);
    render(
      <MemoryRouter initialEntries={["/posts"]}>
        <App />
      </MemoryRouter>
    );
    await waitFor(() =>
      expect(screen.getByText(/Welcome, testuser/i)).toBeInTheDocument()
    );
    expect(
      screen.getByText(/You are currently on basic plan/i)
    ).toBeInTheDocument();
  });
});

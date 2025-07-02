import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import App from "../../App";
import { MemoryRouter } from "react-router-dom";
import { GlobalContext } from "../../utils/globalContext"; // ADD THIS

// Mock constants
jest.mock("../../const", () => ({
  API_ENDPOINT: "http://localhost:5000",
}));

jest.mock("../../utils/upgradeMembership", () => ({
  stripe_publishable_key: "test_key",
}));

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

  test("redirects to /posts and renders HomePage when authenticated", async () => {
    const user = {
      username: "testuser",
      email: "test@example.com",
      membership: "basic",
      profile_picture: "",
      created_at: "2024-01-01T00:00:00Z",
      post_limit: 2,
    };

    // Simulate token already set
    localStorage.setItem("access_token", "testtoken");

    mockFetchUser(user);

    const contextValue = {
      auth: {
        isAuthenticated: true,
        token: "testtoken",
        user,
      },
      setAuth: jest.fn(),
      rateLimit: { attempts: 0, cooldown: false },
      setRateLimit: jest.fn(),
      setModal: jest.fn(),
      getAuthToken: () => "testtoken",
      updateAuthToken: jest.fn(),
      handleLogout: jest.fn(),
    };

    render(
      <GlobalContext.Provider value={contextValue}>
        <MemoryRouter initialEntries={["/posts"]}>
          <App />
        </MemoryRouter>
      </GlobalContext.Provider>
    );

    await waitFor(() =>
      expect(screen.getByText(/Welcome, testuser/i)).toBeInTheDocument()
    );
    expect(
      screen.getByText(/You are currently on basic plan/i)
    ).toBeInTheDocument();
  });
});

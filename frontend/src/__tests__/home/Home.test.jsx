import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import HomePage from "../../pages/home/Home";
import { GlobalContext } from "../../utils/globalContext";
import { MemoryRouter, useNavigate } from "react-router-dom";
import upgradeMembership from "../../utils/upgradeMembership";

// Mocks
jest.mock("../../const", () => ({
  API_ENDPOINT: "http://localhost:5000",
}));
jest.mock("../../utils/upgradeMembership", () => jest.fn());
jest.mock("react-router-dom", () => {
  const actual = jest.requireActual("react-router-dom");
  return {
    ...actual,
    useNavigate: jest.fn(),
  };
});

// Helper to render with context
const renderWithContext = (
  ui,
  {
    auth = {
      user: {
        username: "testuser",
        membership: "basic",
        post_limit: 2,
      },
      token: "testtoken",
      isAuthenticated: true,
    },
  } = {}
) => {
  return render(
    <GlobalContext.Provider value={{ auth }}>
      <MemoryRouter>{ui}</MemoryRouter>
    </GlobalContext.Provider>
  );
};

describe("HomePage", () => {
  // Make sure there is plan and post limit
  test("renders user's plan and post limit for basic user", () => {
    renderWithContext(
      <HomePage
        searchTerm=""
        scrollContainerRef={{ current: document.createElement("div") }}
      />
    );
    expect(
      screen.getByText(/You are currently on basic plan/i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/You can create 2 posts today/i)
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", {
        name: /Upgrade to premium plan to enjoy unlimited posting/i,
      })
    ).toBeInTheDocument();
  });

  // render correct text for premium user
  test("renders correct text for premium user", () => {
    renderWithContext(
      <HomePage
        searchTerm=""
        scrollContainerRef={{ current: document.createElement("div") }}
      />,
      {
        auth: {
          user: {
            username: "premiumuser",
            membership: "premium",
            post_limit: 999,
          },
          token: "testtoken",
          isAuthenticated: true,
        },
      }
    );
    expect(
      screen.getByText(/You are currently on premium plan/i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/You can create unlimited posts/i)
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /Upgrade to premium/i })
    ).not.toBeInTheDocument();
  });

  test("renders welcome message with username", () => {
    renderWithContext(
      <HomePage
        searchTerm=""
        scrollContainerRef={{ current: document.createElement("div") }}
      />
    );
    expect(screen.getByText(/Welcome, testuser/i)).toBeInTheDocument();
  });

  test("renders Create Post button", () => {
    renderWithContext(
      <HomePage
        searchTerm=""
        scrollContainerRef={{ current: document.createElement("div") }}
      />
    );
    expect(
      screen.getByRole("button", { name: /Create Post/i })
    ).toBeInTheDocument();
  });

  test("calls navigate when Create Post button is clicked", () => {
    const mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);

    renderWithContext(
      <HomePage
        searchTerm=""
        scrollContainerRef={{ current: document.createElement("div") }}
      />
    );
    fireEvent.click(screen.getByRole("button", { name: /Create Post/i }));
    expect(mockNavigate).toHaveBeenCalledWith("/create-posts");
  });

  test("calls upgradeMembership when upgrade button is clicked", () => {
    const upgradeMembership = require("../../utils/upgradeMembership");
    renderWithContext(
      <HomePage
        searchTerm=""
        scrollContainerRef={{ current: document.createElement("div") }}
      />
    );
    fireEvent.click(
      screen.getByRole("button", {
        name: /Upgrade to premium plan to enjoy unlimited posting/i,
      })
    );
    expect(upgradeMembership).toHaveBeenCalled();
  });
});

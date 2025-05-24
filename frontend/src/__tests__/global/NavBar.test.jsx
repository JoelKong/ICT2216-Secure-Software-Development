import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import NavBar from "../../components/global/NavBar";
import { GlobalContext } from "../../utils/globalContext";
import { MemoryRouter } from "react-router-dom";

// Mocks
jest.mock("../../utils/upgradeMembership", () => jest.fn());
const mockUpgradeMembership = require("../../utils/upgradeMembership");

const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => {
  const actual = jest.requireActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

const renderWithContext = (
  ui,
  {
    auth = {
      user: {
        username: "testuser",
        membership: "basic",
        profile_picture: "",
      },
      token: "testtoken",
      isAuthenticated: true,
    },
    setAuth = jest.fn(),
  } = {}
) => {
  return render(
    <GlobalContext.Provider value={{ auth, setAuth }}>
      <MemoryRouter>{ui}</MemoryRouter>
    </GlobalContext.Provider>
  );
};

describe("NavBar", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  test("renders Home link and SearchBar", () => {
    renderWithContext(<NavBar setSearchTerm={jest.fn()} />);
    expect(screen.getByText("Home")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText(/Search discussions by topic/i)
    ).toBeInTheDocument();
  });

  test("shows user icon if no profile picture", () => {
    renderWithContext(<NavBar setSearchTerm={jest.fn()} />);
    expect(screen.getByRole("button")).toBeInTheDocument();
  });

  test("opens and closes dropdown on user icon click", () => {
    renderWithContext(<NavBar setSearchTerm={jest.fn()} />);
    const userBtn = screen.getByRole("button");
    fireEvent.click(userBtn);
    expect(screen.getByText(/View my profile/i)).toBeInTheDocument();
    fireEvent.click(userBtn);
    expect(screen.queryByText(/View my profile/i)).not.toBeInTheDocument();
  });

  test("navigates to profile when 'View my profile' is clicked", () => {
    renderWithContext(<NavBar setSearchTerm={jest.fn()} />);
    fireEvent.click(screen.getByRole("button"));
    fireEvent.click(screen.getByText(/View my profile/i));
    // Should use anchor, so no navigate call, but link is present
    expect(screen.getByText(/View my profile/i).closest("a")).toHaveAttribute(
      "href",
      "/profile"
    );
  });

  test("calls upgradeMembership when upgrade button is clicked for basic user", () => {
    renderWithContext(<NavBar setSearchTerm={jest.fn()} />);
    fireEvent.click(screen.getByRole("button"));
    fireEvent.click(screen.getByText(/Upgrade to premium/i));
    expect(mockUpgradeMembership).toHaveBeenCalled();
  });

  test("does not show upgrade button for premium user", () => {
    renderWithContext(<NavBar setSearchTerm={jest.fn()} />, {
      auth: {
        user: {
          username: "premiumuser",
          membership: "premium",
          profile_picture: "",
        },
        token: "testtoken",
        isAuthenticated: true,
      },
    });
    fireEvent.click(screen.getByRole("button"));
    expect(screen.queryByText(/Upgrade to premium/i)).not.toBeInTheDocument();
  });

  test("logs out and navigates to / when Logout is clicked", () => {
    const setAuth = jest.fn();
    renderWithContext(<NavBar setSearchTerm={jest.fn()} />, { setAuth });
    fireEvent.click(screen.getByRole("button"));
    fireEvent.click(screen.getByText(/Logout/i));
    expect(setAuth).toHaveBeenCalledWith({
      isAuthenticated: false,
      token: null,
      user: null,
    });
    expect(mockNavigate).toHaveBeenCalledWith("/");
    expect(localStorage.getItem("access_token")).toBeNull();
  });
});

import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import Modal from "../../components/global/Modal";

// Check if modal component renders properly
describe("Modal Component", () => {
  test("renders success message", () => {
    render(<Modal modal={{ type: "pass", message: "Success!" }} />);
    expect(screen.getByText("Success!")).toBeInTheDocument();
    expect(screen.getByText("Success!")).toHaveClass("bg-green-400");
  });

  test("renders failure message", () => {
    render(<Modal modal={{ type: "fail", message: "Error occurred!" }} />);
    expect(screen.getByText("Error occurred!")).toBeInTheDocument();
    expect(screen.getByText("Error occurred!")).toHaveClass("bg-red-200");
  });
});

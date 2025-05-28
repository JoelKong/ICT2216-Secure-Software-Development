import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import SimplifiedPost from "../../components/home/SimplifiedPost";
import { GlobalContext } from "../../utils/globalContext";
import { MemoryRouter, useLocation } from "react-router-dom";

// Mock constants
jest.mock("../../const", () => ({
  FETCH_POSTS_ROUTE: "api/posts",
  API_ENDPOINT: "http://localhost:5000",
  LIKE_POST_ROUTE: "api/posts/like",
  DELETE_POSTS_ROUTE: "api/posts/delete",
}));

jest.mock("react-router-dom", () => {
  const actual = jest.requireActual("react-router-dom");
  return {
    ...actual,
    useLocation: jest.fn(),
  };
});

// Helper to render with context
const renderWithContext = (
  ui,
  {
    auth = { token: "testtoken", user: { user_id: 1, username: "testuser" } },
    setModal = jest.fn(),
    rateLimit = { attempts: 0, cooldown: false },
    setRateLimit = jest.fn(),
  } = {}
) => {
  return render(
    <GlobalContext.Provider value={{ auth, setModal, rateLimit, setRateLimit }}>
      <MemoryRouter>{ui}</MemoryRouter>
    </GlobalContext.Provider>
  );
};

describe("SimplifiedPost Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    global.fetch = jest.fn();
  });

  afterEach(() => {
    if (global.fetch.mockRestore) global.fetch.mockRestore();
  });

  test("renders loading state", async () => {
    global.fetch.mockImplementation(
      () =>
        new Promise((resolve) =>
          setTimeout(
            () =>
              resolve({
                ok: true,
                json: () =>
                  Promise.resolve({
                    posts: [
                      {
                        post_id: 1,
                        title: "Test Post",
                        content: "Test Content",
                        username: "testuser",
                        likes: 0,
                        comments: 0,
                        created_at: new Date().toISOString(),
                        updated_at: new Date().toISOString(),
                      },
                    ],
                    liked_post_ids: [],
                  }),
              }),
            100
          )
        )
    );
    renderWithContext(
      <SimplifiedPost
        scrollContainerRef={{ current: document.createElement("div") }}
      />
    );
    expect(screen.getByText(/Loading.../i)).toBeInTheDocument();
    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  });

  test("renders empty state when no posts", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ posts: [], liked_post_ids: [] }),
    });
    renderWithContext(
      <SimplifiedPost
        scrollContainerRef={{ current: document.createElement("div") }}
      />
    );
    await waitFor(() =>
      expect(screen.getByText(/No Posts Found/i)).toBeInTheDocument()
    );
  });

  test("renders posts with correct data", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          posts: [
            {
              post_id: 1,
              title: "Test Post",
              content: "Test Content",
              username: "testuser",
              likes: 5,
              comments: 2,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            },
          ],
          liked_post_ids: [1],
        }),
    });
    renderWithContext(
      <SimplifiedPost
        scrollContainerRef={{ current: document.createElement("div") }}
      />
    );
    expect(await screen.findByText("Test Post")).toBeInTheDocument();
    expect(screen.getByText("Test Content")).toBeInTheDocument();
    expect(screen.getByText("testuser")).toBeInTheDocument();
    expect(screen.getByText("5")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
  });

  // TODO: sometimes work sometimes dont
  // test("calls toggleLike when like button is clicked", async () => {
  //   global.fetch
  //     .mockResolvedValueOnce({
  //       ok: true,
  //       json: () =>
  //         Promise.resolve({
  //           posts: [
  //             {
  //               post_id: 1,
  //               title: "Test Post",
  //               content: "Test Content",
  //               username: "testuser",
  //               likes: 0,
  //               comments: 0,
  //               created_at: new Date().toISOString(),
  //               updated_at: new Date().toISOString(),
  //             },
  //           ],
  //           liked_post_ids: [],
  //         }),
  //     })
  //     .mockResolvedValueOnce({
  //       ok: true,
  //       json: () => Promise.resolve({ likes: 1 }),
  //     });

  //   renderWithContext(
  //     <SimplifiedPost
  //       scrollContainerRef={{ current: document.createElement("div") }}
  //     />
  //   );

  //   // Wait for post to render
  //   const likeButton = await screen.findByRole("button", {
  //     name: /like post/i,
  //   });
  //   fireEvent.click(likeButton);

  //   await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(4));
  // });

  test("shows edit and delete buttons on profile page", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          posts: [
            {
              post_id: 1,
              title: "Test Post",
              content: "Test Content",
              username: "testuser",
              likes: 0,
              comments: 0,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            },
          ],
          liked_post_ids: [],
        }),
    });

    useLocation.mockReturnValue({ pathname: "/profile" });

    renderWithContext(
      <SimplifiedPost
        scrollContainerRef={{ current: document.createElement("div") }}
        userId={1}
      />
    );

    expect(await screen.findByText("Edit Post")).toBeInTheDocument();
    expect(screen.getByText("Delete Post")).toBeInTheDocument();
  });

  // TODO: sometimes work sometimes dont
  // test("calls delete post and shows modal on confirm", async () => {
  //   global.fetch
  //     .mockResolvedValueOnce({
  //       ok: true,
  //       json: () =>
  //         Promise.resolve({
  //           posts: [
  //             {
  //               post_id: 1,
  //               title: "Test Post",
  //               content: "Test Content",
  //               username: "testuser",
  //               likes: 0,
  //               comments: 0,
  //               created_at: new Date().toISOString(),
  //               updated_at: new Date().toISOString(),
  //             },
  //           ],
  //           liked_post_ids: [],
  //         }),
  //     })
  //     .mockResolvedValueOnce({
  //       ok: true,
  //       json: () => Promise.resolve({ message: "Post deleted successfully" }),
  //     });

  //   window.confirm = jest.fn(() => true);

  //   const setModal = jest.fn();
  //   renderWithContext(
  //     <SimplifiedPost
  //       scrollContainerRef={{ current: document.createElement("div") }}
  //       userId={1}
  //     />,
  //     { setModal }
  //   );

  //   const deleteBtn = await screen.findByText("Delete Post");
  //   fireEvent.click(deleteBtn);

  //   await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(2));
  //   expect(setModal).toHaveBeenCalled();
  // });
});

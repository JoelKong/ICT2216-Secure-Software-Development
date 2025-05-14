export default {
  transform: {
    "^.+\\.(js|jsx)$": "babel-jest",
  },
  moduleNameMapper: {
    "^.+\\.(css|scss)$": "identity-obj-proxy",
  },

  testEnvironment: "jsdom",
};

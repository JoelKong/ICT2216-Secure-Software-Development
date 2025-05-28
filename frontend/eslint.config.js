import js from "@eslint/js";
import globals from "globals";
import pluginReact from "eslint-plugin-react";
import pluginJest from "eslint-plugin-jest";
import { defineConfig } from "eslint";
export default defineConfig({
  files: ["**/*.{js,mjs,cjs,jsx}"],
  plugins: {
    react: pluginReact,
    jest: pluginJest,
  },
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:jest/recommended",
  ],
  languageOptions: {
    ecmaVersion: 2022,
    sourceType: "module",
    globals: {
      ...globals.browser,
      ...globals.jest,
    },
  },
  settings: {
    react: {
      version: "detect",
    },
  },
});

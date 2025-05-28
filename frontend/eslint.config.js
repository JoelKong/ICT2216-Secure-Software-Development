import js from "@eslint/js";
import globals from "globals";
import pluginReact from "eslint-plugin-react";
import pluginJest from "eslint-plugin-jest";
import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    plugins: { js, react: pluginReact, jest: pluginJest },
    extends: [
      "js/recommended",
      "plugin:react/recommended",
      "plugin:jest/recommended",
    ],
    languageOptions: {
      globals: { ...globals.browser, ...globals.jest },
    },
  },
  {
    files: ["**/__tests__/**/*.{js,jsx}"],
    extends: ["plugin:jest/recommended"],
  },
]);

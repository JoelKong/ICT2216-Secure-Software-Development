import js from "@eslint/js";
import globals from "globals";
import pluginReact from "eslint-plugin-react";
import pluginJest from "eslint-plugin-jest";
import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    plugins: { js },
    extends: ["js/recommended"],
  },
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    languageOptions: { globals: { ...globals.browser, ...globals.jest } },
  },
  pluginReact.configs.flat.recommended,
  {
    files: ["**/__tests__/**/*.{js,jsx}"],
    plugins: { jest: pluginJest },
    extends: ["plugin:jest/recommended"],
  },
]);

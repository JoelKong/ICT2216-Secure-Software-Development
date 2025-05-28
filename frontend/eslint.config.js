import js from "@eslint/js";
import globals from "globals";
import pluginReact from "eslint-plugin-react";
import pluginJest from "eslint-plugin-jest";

export default [
  js.configs.recommended,
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    plugins: {
      react: pluginReact,
      jest: pluginJest,
    },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.jest,
      },
    },
    rules: {
      ...pluginReact.configs.recommended.rules,
      ...pluginJest.configs.recommended.rules,
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
];

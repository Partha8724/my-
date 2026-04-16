import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          950: "#060915",
          900: "#0B1227",
          700: "#1E2E6A",
          500: "#4E8CFF",
          300: "#6AF0F8"
        }
      },
      boxShadow: {
        glow: "0 0 40px rgba(78, 140, 255, 0.35)"
      }
    }
  },
  plugins: []
};

export default config;

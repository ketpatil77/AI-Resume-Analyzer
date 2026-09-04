import type { Config } from "tailwindcss";
import forms from "@tailwindcss/forms";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Clash Display", "DM Sans", "sans-serif"],
        sans: ["DM Sans", "sans-serif"]
      },
      borderRadius: {
        card: "8px"
      },
      boxShadow: {
        card: "0 18px 50px rgba(0, 0, 0, 0.22)"
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        },
        spin: {
          to: { transform: "rotate(360deg)" }
        }
      },
      animation: {
        fadeUp: "fadeUp 0.45s ease-out both",
        spin: "spin 0.9s linear infinite"
      }
    }
  },
  plugins: [forms]
} satisfies Config;

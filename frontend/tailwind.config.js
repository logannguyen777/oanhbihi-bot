/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}", // nếu dùng Vue hoặc React/TS
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#fcd9b6',
          DEFAULT: '#f97316', // màu cam chính
          dark: '#c2410c',
        },
        secondary: {
          light: '#ffeccc',
          DEFAULT: '#fb923c', // màu cam phụ
          dark: '#ea580c',
        },
        background: '#fff7ed',
        text: '#7c2d12',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        oanhbihi: {
          primary: "#f97316",
          secondary: "#fb923c",
          accent: "#fcd34d",
          neutral: "#292524",
          "base-100": "#fff7ed",
          info: "#3ABFF8",
          success: "#22c55e",
          warning: "#facc15",
          error: "#ef4444",
        },
      },
    ],
  },
}

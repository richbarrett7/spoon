/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    relative: true,
    files: [
      './src/**/*.html',
      './public/assets/js/src/**/*.js',
    ]
  },
  theme: {
    extend: {
      colors: {
        'spoon-yellow': '#ffc762',
        'spoon-blue': '#28d2d1',
        'spoon-orange': '#ff7f4c',
        'spoon-burnt-orange': '#e49e6e',
        'spoon-dark-blue': '#549ed6',
        'spoon-green': '#35ce7f',
        'spoon-pale-yellow': '#f4e0a6', 
        'spoon-alt-blue': '#00b3e4'
      },
    },
  },
  plugins: [],
  darkMode: 'selector',
}
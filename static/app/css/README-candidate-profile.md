# Candidate Profile Styling

## File Structure

```
static/app/css/
├── candidate-profile.scss   # Source SCSS file with Tailwind directives
└── candidate-profile.css    # Compiled CSS file (used in production)
```

## Overview

The candidate profile page uses **Tailwind CSS** combined with custom SCSS for tooltip and form styling. The styles are organized in separate files for better maintainability.

## Features

### 1. **Tooltip System**
- Info icons positioned on the right side of input fields
- Hover tooltips with smooth animations
- Responsive positioning (switches side on mobile)
- Beautiful dark theme with arrow indicators

### 2. **Error Messages**
- Displayed **below** the input field (not inline)
- Gradient background with red accent border
- Slide-down animation on appearance
- Icon with descriptive text
- Full-width layout for better visibility

### 3. **Input Styling**
- Smaller, more compact inputs (14px font, optimized padding)
- Focus states with blue ring
- Error states with red border and ring
- Consistent spacing and transitions

### 4. **Responsive Design**
- Mobile-first approach
- Tooltip repositioning on small screens
- Stacked layout for input + icon on mobile

## Using SCSS (Optional)

If you want to modify the styles using SCSS:

### Prerequisites

Install Sass compiler:

```bash
npm install -g sass
# or
pip install libsass
```

### Compile SCSS to CSS

```bash
# Watch for changes and auto-compile
sass --watch static/app/css/candidate-profile.scss:static/app/css/candidate-profile.css

# One-time compilation
sass static/app/css/candidate-profile.scss static/app/css/candidate-profile.css

# Minified production version
sass static/app/css/candidate-profile.scss:static/app/css/candidate-profile.min.css --style compressed
```

### Using with Tailwind CSS

If you want full Tailwind integration:

1. **Install Tailwind CSS**:
```bash
npm install -D tailwindcss
npx tailwindcss init
```

2. **Configure tailwind.config.js**:
```javascript
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

3. **Create input CSS file**:
```css
/* static/app/css/tailwind-input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@import 'candidate-profile.scss';
```

4. **Build CSS**:
```bash
npx tailwindcss -i static/app/css/tailwind-input.css -o static/app/css/candidate-profile.css --watch
```

## Quick Start (No Build Required)

The project already includes:
- ✅ Compiled CSS file (`candidate-profile.css`)
- ✅ Tailwind CDN loaded in HTML
- ✅ All styles ready to use

**You don't need to compile anything** unless you want to modify the SCSS source.

## HTML Structure

Error messages are positioned correctly:

```html
<div class="form-group">
  <label>Field Name</label>
  <div class="input-with-tooltip">
    <input type="text" name="field">
    <span class="info-tooltip">
      <i class="fas fa-info-circle"></i>
      <span class="tooltip-text">Help text here</span>
    </span>
  </div>
  <!-- Error message appears HERE, below the input -->
  {% if form.field.errors %}
    <div class="error-message">
      <i class="fas fa-exclamation-circle"></i> 
      {{ form.field.errors.0 }}
    </div>
  {% endif %}
</div>
```

## Customization

### Change Tooltip Colors

Edit `candidate-profile.scss` or `.css`:

```scss
.info-tooltip .tooltip-text {
  background-color: #1f2937; // Change this
  color: #ffffff;            // And this
}
```

### Change Error Message Style

```scss
.error-message {
  border-left: 4px solid #ef4444;  // Border color
  color: #b91c1c;                  // Text color
  background: linear-gradient(...); // Background
}
```

### Adjust Input Size

```scss
.form-group input {
  font-size: 14px;      // Text size
  padding: 10px 14px;   // Inner spacing
}
```

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (iOS/Android)

## Notes

- The CSS file is already production-ready
- Tailwind CSS is loaded via CDN for quick setup
- SCSS file is provided for developers who want to customize
- All animations use CSS transitions (no JavaScript required)

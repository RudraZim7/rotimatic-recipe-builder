# Rotimatic Recipe Builder

A web-based recipe editor and JSON generator for Rotimatic recipes. This tool allows you to visually edit recipe parameters and export them in JSON format.

## Features

- 🎯 **Recipe Selection**: Choose from 10 pre-loaded recipes
- ✏️ **Interactive Editing**: Modify recipe parameters directly in the browser
- 👁️ **JSON Preview**: View formatted JSON before downloading
- 💾 **Download**: Export modified recipes as JSON files
- 📋 **Copy to Clipboard**: Quick copy of JSON data
- 🔒 **Change Validation**: Ensures at least one modification before download
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Available Recipes

- Crisp Roti
- Jowar Bhakri
- Makkai Bhakri
- Masala Poori
- Missi Bhakri
- Multigrain Poori
- Multigrain Roti
- Plain Poori
- TGR Poori
- Tortilla Wraps

## Project Structure

```
Rotimatic Recipe Builder/
├── rotimatic-recipe-builder.html    # Main application
├── generate_html_files.py            # Python script to generate HTML forms
├── README.md                         # This file
├── HTML Files/                       # Individual recipe HTML forms
│   ├── crisp_roti.html
│   ├── jowar_bhakri.html
│   ├── makkai_bhakri.html
│   └── ...
└── Recipes/                          # Original JSON recipes
    ├── Crisp_Roti.json
    ├── Jowar_Bhakri.json
    ├── Makkai_Bhakri.json
    └── ...
```

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Edge, Safari)
- Python 3.x (for running local web server)

### Installation

1. Clone or download this repository
2. Navigate to the project directory

### Running the Application

Due to browser security restrictions with local files, you need to run a local web server:

#### Option 1: Using Python

```bash
# Navigate to the project directory
cd "Rotimatic Recipe Builder"

# Start a local web server
python -m http.server 8000
```

Then open your browser and go to:
```
http://localhost:8000/rotimatic-recipe-builder.html
```

#### Option 2: Using Node.js (http-server)

```bash
# Install http-server globally (one time)
npm install -g http-server

# Run the server
http-server -p 8000
```

Then open: `http://localhost:8000/rotimatic-recipe-builder.html`

## Usage

### Editing a Recipe

1. **Select a Recipe**: Choose a recipe from the dropdown menu
2. **Wait for Loading**: The recipe form will load in the iframe
3. **Modify Values**: Edit any parameter in the form (at least one change required)
4. **Preview or Download**:
   - Click **Preview JSON** to view the formatted JSON
   - Click **Download JSON** to save the file directly

### Preview Modal Features

- **View JSON**: See formatted, readable JSON output
- **Copy to Clipboard**: Copy the entire JSON with one click
- **Download**: Save the JSON file from the preview
- **Close**: Click X, press Escape, or click outside the modal

### Validation Rules

- A recipe must be selected before preview/download
- At least one field must be modified from the original values
- All changes are tracked automatically

## Recipe JSON Structure

Each recipe contains:

- **Basic Info**: Recipe ID, name, version, description
- **Quality Control**: Quality options, size settings, softness parameters
- **Settings**: 
  - Roast levels and temperatures
  - Oil levels
  - Thickness parameters (heating, dispensing, adaptive DAK)
- **Process Steps**: Mixing, doughing, stabilizing, rounding, pressing, roasting, etc.

## Development

### Generating HTML Forms

The `generate_html_files.py` script converts JSON recipes into HTML forms:

```bash
python generate_html_files.py
```

This will regenerate all HTML files in the `HTML Files/` directory based on the JSON files in `Recipes/`.

### Customization

- **Styling**: Modify the CSS in the `<style>` section of `rotimatic-recipe-builder.html`
- **Recipe Fields**: Edit the JSON files in `Recipes/` and regenerate HTML forms
- **Validation**: Adjust the change tracking logic in the JavaScript section

## Browser Compatibility

- ✅ Chrome/Edge (Chromium): Full support
- ✅ Firefox: Full support
- ✅ Safari: Full support
- ⚠️ Internet Explorer: Not supported

## Troubleshooting

### "Could not generate JSON" Error

**Cause**: Browser security restrictions when opening files directly with `file://` protocol.

**Solution**: Always run through a local web server (see Installation section).

### Preview/Download Button Not Working

**Cause**: No changes made to the recipe.

**Solution**: Modify at least one field value before attempting to preview or download.

### Iframe Not Loading

**Possible causes**:
- Files not in correct directory structure
- Web server not running
- Browser cache issues

**Solution**: 
- Verify all files are in place
- Clear browser cache and refresh
- Check browser console (F12) for error messages

## License

© Zimplistic - Internal Tool

## Support

For issues or questions, contact the development team.

---

**Note**: This tool is designed for internal use with Rotimatic recipe development and testing.

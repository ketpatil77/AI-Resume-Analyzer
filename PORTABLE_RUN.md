# Portable Run

Use `START.bat` on Windows after extracting the zip.

What it does:

- Uses normal Windows PowerShell. PowerShell 7 is not required.
- Downloads portable Node.js into `.portable` if Node is missing from the project.
- Installs project dependencies with `npm ci` when `package-lock.json` is present.
- Falls back to a clean `npm install` if the lockfile install fails.
- Reuses existing downloads and `node_modules` on later runs.
- Finds a free local port starting at `5173`.
- Opens the app in the browser and runs Vite.

Zip rule:

- Zip the whole `AI-Resume-Analyzer` folder.
- Do not include `node_modules`, `.portable`, `.venv`, `.pip-cache`, or `dist`.
- On the next Windows machine, extract anywhere and double-click `START.bat`.
- Internet is required on first run so the launcher can download Node.js and npm packages.

Manual reset:

If a dependency install gets corrupted, delete `node_modules` and run `START.bat` again. The launcher will reinstall everything.

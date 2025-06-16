# 🧹 SSS Data File Cleaner

A Windows-friendly, GUI-based application for validating and cleaning SSS (Social Security System) upload files. Built with Python, Tkinter, and pandas, this tool compares final and upload `.txt/.csv` files, highlights mismatches, and outputs cleaned data and audit reports.

---

## 📦 Features

* 🧠 Smart field-level comparison using `SSS_Number` as key
* 📁 Auto-creates `OUTPUT` and `REPORT` directories
* 💬 GUI with tooltips, keyboard shortcuts, and animated toast notifications
* 🔍 Live filtering of results
* 🧾 Saves detailed mismatch reports and cleaned upload files

---

## 📁 Folder Structure

```
├── HRA.py                 # Main script
├── OUTPUT/                # Cleaned upload files
├── REPORT/                # Mismatch reports
├── assets/                # (optional for future icons/images)
└── dist/                  # Auto-generated when converted to EXE
```

---

## 🛠️ Installation

###  Install Required Packages

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install manually:

```bash
pip install pandas pillow ttkthemes
```

---

## 🚀 Running the Tool

Run directly via Python:

```bash
python HRA.py
```

---

## 🔍 How It Works (Developer-Level Code Overview)

### 🧱 High-Level Architecture

* **GUI Layer**: Built using Tkinter, styled with `ttkthemes`, all encapsulated in the `DataCleanerGUI` class.
* **Business Logic Layer**: Data validation, diffing, and cleaning handled by independent functions (like `read_data_file`, `compare_dataframes`, etc).
* **I/O Management**: Uses `pandas` for loading/saving data and `Pathlib` for OS-independent file handling.

---

### ✨ GUI Class Breakdown: `DataCleanerGUI`

This class wraps the Tkinter root window and manages layout and event handling.

Key components:

* `__init__()` initializes layout, style, and binds buttons.
* `_create_widgets()` arranges all UI components using a structured layout: header, file selectors, options, results, and footer.
* `_process_files()` is the handler for the "Validate & Clean" button — it invokes the entire backend pipeline.

Subcomponents:

* `ButtonWithIcon`: Custom Tkinter Button with base64 icon embedding.
* `ToolTip`: Tooltip implementation on hover.
* `Toast`: Non-blocking notification system.
* `LoadingSpinner`: Canvas-based loading animation.

---

### 📂 Core Functional Blocks

#### `read_data_file(file_path)`

Purpose: Load SSS text/CSV file with flexible encoding fallback and validate column structure.

Highlights:

* Tries encodings in order: `utf-8`, `cp1252`, `latin1`, `utf-16`.
* Parses data into DataFrame with strict column names.
* Checks for:

  * Invalid numeric `Amount`
  * Duplicate `SSS_Number`

#### `compare_dataframes(raw_df, upload_df)`

Purpose: Detect mismatches and differences in aligned SSS rows.

Logic:

* Uses vectorized `pandas.merge()` with suffixes.
* Iterates over all columns except `SSS_Number` to compare values.
* Outputs:

  * `mismatch_report`: field-wise value differences
  * `missing_records`: raw entries not in upload
  * `extra_records`: upload entries not in raw

#### `clean_upload_file(raw_df, upload_df, extra_records, output_path)`

Purpose: Clean the upload file by removing non-matching records and syncing raw values.

* Removes all rows in upload that don't exist in raw.
* Overwrites all columns with raw data **except** `Amount`.
* Saves cleaned file to versioned path inside `OUTPUT/`.

#### `save_mismatch_report(...)`

Purpose: Combine all mismatch/missing/extra data into a CSV report.

* Adds a timestamp to filename.
* Combines three report types into one DataFrame.
* Saves to `REPORT/mismatch_report_<timestamp>.csv`

#### `main(...)`

Orchestration entrypoint for headless batch execution.

Steps:

1. Loads both files.
2. Calls `compare_dataframes`.
3. Cleans file using `clean_upload_file`.
4. Saves report using `save_mismatch_report`.
5. Logs stats and results to terminal (or GUI via overridden `print`).

#### `ensure_app_folders()`

Ensures `OUTPUT/` and `REPORT/` directories are present in runtime directory.
Used before file writing in both script and EXE mode.

---

### ⚙️ Application Modes

* **Development Mode**: Runs via Python, paths resolved with `__file__`.
* **EXE Bundle Mode**: Uses `sys._MEIPASS` for bundled resource access (PyInstaller-compatible).

---

## 🧪 Shortcuts and User Guide

| Action           | Shortcut |
| ---------------- | -------- |
| Open Final File  | Ctrl+O   |
| Open Upload File | Ctrl+U   |
| Validate & Clean | Ctrl+P   |
| Save Log         | Ctrl+S   |
| Show Help        | F1       |
| Filter Results   | Ctrl+F   |

---

## 📤 Output Files

* **Cleaned Upload** → `OUTPUT/filename_cleaned_vX.txt`
* **Mismatch Report** → `REPORT/mismatch_report_filename_vYYYYMMDD_HHMMSS.csv`

---

## 📦 Convert to Executable (Windows)

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build Executable

```bash
pyinstaller --noconsole --onefile --add-data "assets;assets" HRA.py
```

> If you’re not using external files like icons or images, you can simplify:

```bash
pyinstaller --noconsole --onefile HRA.py
```

### Step 3: Locate the Executable

Check `dist/HRA.exe`. You can now share it with users without requiring Python.

---

## 🛯️ Troubleshooting

| Problem                          | Solution                                                                |
| -------------------------------- | ----------------------------------------------------------------------- |
| GUI freezes during large files   | Wait — uses Tkinter update cycles                                       |
| "File encoding error"            | Check file is `.csv/.txt` and not Excel                                 |
| App window too small on high-DPI | Right-click EXE → Properties → Compatibility → Change high DPI settings |

---

## 🙌 Credits

* Built with 💙 by \[Your Name]
* Icon base64s from `https://icons8.com`
* UI inspired by modern Microsoft design system

---

## 🛡️ License

MIT License

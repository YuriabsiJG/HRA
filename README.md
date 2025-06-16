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

## 🔍 How It Works 

### 🧠 Expert Code Architecture & Flow

This project adheres to a layered, modular design that separates concerns between UI, processing logic, and I/O operations. It’s structured for maintainability and extensibility — with the following architectural components:

---

### 📐 Architecture Layers

| Layer           | Description                                                                  |
| --------------- | ---------------------------------------------------------------------------- |
| **UI Layer**    | `DataCleanerGUI` class encapsulates the GUI logic using Tkinter and ttk.     |
| **Logic Layer** | Stateless, functional utilities for parsing, validating, comparing, writing. |
| **I/O Layer**   | File encoding, folder creation, and safe read/write operations.              |

---

### 🧰 GUI System Design (`DataCleanerGUI`)

The entire graphical interface is managed via `DataCleanerGUI`, a class that encapsulates the lifecycle of the Tkinter window.

**Key Responsibilities:**

* Initializes themed layout using `ttkthemes.vista`.
* Renders sections: header, file inputs, results, footer.
* Hooks action buttons (e.g., Browse, Validate, Save) to corresponding back-end logic.
* Uses custom controls:

  * `ButtonWithIcon` for consistent styling + embedded base64 icons.
  * `Toast` for non-blocking feedback.
  * `ToolTip` for enhanced UX.
  * `LoadingSpinner` to indicate asynchronous work.

**Design Patterns Used:**

* Inversion of Control: Backend functions are injected into GUI handlers.
* MV-ish Pattern: Although not a full MVVM, logic and view are clearly decoupled.

---

### 🧪 Backend Logic Breakdown

All core business logic is abstracted into stateless functions — making them independently testable.

#### 🔹 `read_data_file(file_path)`

Handles robust multi-encoding loading using pandas.

* Auto-detects encoding (UTF-8, Windows-1252, Latin1, UTF-16).
* Validates structure: exact 11-column, semicolon-delimited format.
* Verifies uniqueness of `SSS_Number`.
* Cleans strings, strips invisible characters, validates `Amount`.

> ⚠ Returns `None` on parse failure to allow graceful upstream error handling.

#### 🔹 `compare_dataframes(raw_df, upload_df)`

Performs vectorized diffing on all aligned fields (except `Amount`):

* Uses `pandas.merge()` to align based on `SSS_Number`.
* Extracts:

  * Row-level mismatches
  * Records missing from upload
  * Extra records in upload

Output: A structured diff for downstream reporting and correction.

#### 🔹 `clean_upload_file(...)`

Cleans the upload file by enforcing schema parity:

* Filters out extra SSS Numbers.
* Retains original `Amount` values from the upload.
* Overwrites remaining fields with values from the raw file.
* Auto-generates a versioned filename (e.g., `*_cleaned_v2.txt`).

#### 🔹 `save_mismatch_report(...)`

Logs all mismatch metadata into a timestamped CSV file.

* Categorizes records: Mismatch / Missing / Extra.
* Uses `pandas.concat` to unify them into one exportable frame.
* Versioned to prevent accidental overwrite of previous audits.

#### 🔹 `main(...)`

Single-entry orchestration function.

Flow:

```
read → compare → clean → save report → log
```

Also used by the GUI layer via function injection to `print()` — redirecting output into a Tkinter Text widget for real-time feedback.

#### 🔹 `ensure_app_folders()`

\[PLACEHOLDER: DEVELOPER DOCUMENTATION FOR SSS DATA CLEANER]

This Python code defines a GUI application for cleaning and validating SSS (Social Security System) data files. It's structured as a desktop application using the tkinter library for the graphical user interface, pandas for data manipulation, and pathlib and os for file system operations.

---

### 1. Imports and Helper Functions

#### Import Statements

* **pandas as pd**: For powerful data manipulation and analysis.
* **os, io, sys, pathlib.Path**: For file system operations.
* **tkinter**, **tkinter.ttk**, **tkinter.filedialog**, **tkinter.messagebox**: GUI components.
* **ttkthemes**: Modern themes for ttk widgets.
* **PIL.Image, PIL.ImageTk**: For GUI image rendering.
* **base64**: Decoding icon image data.
* **uuid.uuid4**: For generating unique identifiers (though not explicitly used).

#### Functions:

* `get_base_path()`, `get_app_path()` - Handles relative paths for resources.
* `ensure_app_folders()` - Creates `OUTPUT` and `REPORT` folders if they don't exist.
* `ICONS` dictionary - Stores icons in base64 format for use in GUI buttons.

---

### 2. GUI Helper Classes

* **Toast**: Transient message notification (bottom right corner).
* **ButtonWithIcon**: Custom button class supporting icon + text.
* **ToolTip**: Hover-help tooltip window.
* **LoadingSpinner**: Visual processing animation using canvas.

---

### 3. `DataCleanerGUI` Class (Main Application Logic)

#### `__init__()`

* Sets up main window, styles, variables, and GUI widgets.
* Uses `ttkthemes` for modern look.
* Initializes `tk.StringVar()` for user-selected files and status.

#### \_configure\_styles()

* Customizes ttk styles for theming consistency.

#### \_create\_keyboard\_shortcuts()

* Adds hotkeys for common actions (Ctrl+O, Ctrl+P, F1).

#### \_create\_tooltips()

* Assigns contextual hover-tooltips.

#### \_show\_help()

* Displays help modal (shortcuts, instructions).

#### \_create\_widgets()

* Main GUI layout builder:

  * Header
  * File Selector Cards
  * Options Card (future use)
  * Results Viewer (`tk.Text` + `ttk.Scrollbar`)
  * Bottom Bar: action buttons
  * Status Bar

#### \_update\_status()

* Updates footer status bar.

#### File Selectors:

* `_browse_raw_file()`, `_browse_upload_file()`

  * Uses `askopenfilename()`
  * Shows Toasts and updates status

#### \_process\_files()

* Core handler for data validation
* Handles GUI state changes (spinner, button disable, stdout redirection)
* Calls the `main()` function

#### \_save\_log()

* Saves `results_text` content to text file

#### \_filter\_results()

* Filters results log based on input

#### \_clear\_results()

* Clears both the result log and filter

#### \_open\_output\_folder() / \_open\_report\_folder()

* Opens folders in Windows Explorer

---

### 4. Data Processing Functions

#### read\_data\_file(file\_path)

* Tries multiple encodings to load semi-colon-separated text
* Verifies format, dtypes, and nulls
* Strips whitespace, filters out unreadable chars
* Warns for duplicates and invalid amounts

#### compare\_dataframes(raw\_df, upload\_df)

* Finds missing, extra, and mismatching records
* Returns structured report for GUI/logging

#### clean\_upload\_file(raw\_df, upload\_df, extra\_records, output\_path)

* Removes extras
* Aligns cleaned data to raw data (except Amount column)
* Saves cleaned file in `OUTPUT` folder

#### save\_mismatch\_report(...)

* Saves discrepancies to CSV report (timestamped filename)

#### main(...)

* Orchestrator:

  * Load files
  * Run comparisons
  * Save report
  * Save cleaned output
  * Log processing summary

---

### 5. Main Entry Point

```python
if __name__ == "__main__":
    ensure_app_folders()
    root = tk.Tk()
    app = DataCleanerGUI(root)
    root.mainloop()
```

---

### Flow Summary

1. **Launch** GUI via `__main__`
2. **User selects files** via "Browse"
3. **Click Validate & Clean**

   * Spinner shows
   * Processing happens via `main()`
4. **Output**:

   * Cleaned file saved
   * CSV report generated
   * Log appears in GUI
5. **User actions**:

   * Filter log, save log, open folders

---

\[END PLACEHOLDER - Insert Real Implementation/Code Here as Needed]


Ensures directory safety for:

* `OUTPUT/`: Cleaned files
* `REPORT/`: Audit files

Supports both CLI and PyInstaller bundle contexts via `sys._MEIPASS` & `__file__`.

---

### ⚙️ Runtime Modes

* **Script Mode**: Executed via `python HRA.py`, using local paths.
* **Bundled Mode**: Supports PyInstaller packaging via frozen executable check (`sys.frozen`).

---

### 🔄 Extensibility Notes

The codebase is intentionally built with extensibility in mind:

* **Themed UI**: Swappable with other `ttkthemes` without code changes.
* **Validation Logic**: Modular — easy to add additional column rules or reporting.
* **Localization-Ready**: Encodings, tooltips, and labels are centralized.
* **Testability**: All core logic is function-based and decoupled from GUI state.

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



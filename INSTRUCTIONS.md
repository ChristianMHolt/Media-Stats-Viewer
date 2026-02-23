# Media Stats Viewer - High Performance Search

This document explains how to compile the C++ search backend and bundle the application with Nuitka.

## 1. Prerequisites

You need a C++ compiler and Python development headers.
- **Windows**: Install Visual Studio Build Tools (ensure "Desktop development with C++" is selected).
- **Python**: Ensure you have Python 3.8+ installed.

## 2. Compiling the C++ Extension

To achieve zero-lag search performance, you must compile the `fast_search` extension.

1.  Open a terminal (Command Prompt or PowerShell) in the project directory.
2.  Install `pybind11`:
    ```bash
    pip install pybind11
    ```
3.  Compile the extension in-place:
    ```bash
    python setup.py build_ext --inplace
    ```
    On Windows, this will generate a file like `fast_search.cp312-win_amd64.pyd`.

## 3. Running the Application

Once compiled, you can run the application normally:
```bash
python app.py
```
If the extension is not compiled or fails to load, the application will automatically fallback to a slower Python implementation of the search logic.

## 4. Bundling with Nuitka

To create a standalone executable that includes the compiled C++ extension:

1.  Install Nuitka:
    ```bash
    pip install nuitka zstandard
    ```

2.  Run the Nuitka compilation command. The key is to include the `customtkinter` package and ensuring the `.pyd` file is picked up (usually automatic if in the same directory, but `--include-module` can help if not).

    **Command:**
    ```bash
    nuitka --standalone --onefile --enable-plugin=tk-inter --include-package=customtkinter --windows-console-mode=disable --include-data-file=fast_search.cp312-win_amd64.pyd=fast_search.pyd app.py
    ```
    *Note: Replace `fast_search.cp312-win_amd64.pyd` with the actual name of the generated file on your system.*

    Alternatively, if you want Nuitka to compile the extension along with the main program (less common for pybind11 but possible), you might just rely on Nuitka finding the import. However, including the pre-compiled `.pyd` as a data file or binary is often safer.

    **Recommended Approach:**
    Keep the `.pyd` next to the executable or use `--include-data-file` to bundle it.
    If you use `--onefile`, Nuitka unpacks data files to a temporary directory. You might need to adjust `app.py` to look for the module in `sys._MEIPASS` or similar if you are doing manual loading, but since we use `import fast_search`, standard Nuitka bundling usually works if the module is in the path during compilation.

    **Simpler Nuitka Command (if .pyd is in folder):**
    ```bash
    nuitka --standalone --enable-plugin=tk-inter --include-package=customtkinter app.py
    ```
    Nuitka should detect the `import fast_search` and include the `.pyd` file automatically if it's in the python path (current directory).

## 5. Troubleshooting

- **"Module not found"**: Ensure the `.pyd` file is in the same directory as `app.py`.
- **Search is slow**: If the C++ extension failed to load, the app uses Python fallback. Check the console for import errors (though the app suppresses them gracefully, you can remove the try/except block temporarily to debug).

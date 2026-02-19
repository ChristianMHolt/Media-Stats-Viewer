# Media Library Tracker

A simple application to track and visualize your media library statistics based on folder naming conventions.

## Features
- **Smart Parsing**: Automatically extracts Name, Group, Resolution, Source, Video Codec, and Audio Codec from folder names like `Title [Group][1080p][BD][H.264][AAC]`.
- **Season Support**: Handles nested season folders and metadata overrides (e.g., Season 1 is 1080p, but Season 2 is 4K).
- **Modern UI**: Clean, responsive interface to browse your collection.

## Prerequisites
- **Python 3.8+**
- **Node.js 16+** (and npm)

## Quick Start (with Test Data)

If you don't have a media library to test with yet, you can generate one:

1.  **Generate Dummy Library**:
    ```bash
    python3 generate_dummy_library.py
    ```
    This creates a `dummy_library` folder in the root directory.

2.  **Start the Backend**:
    ```bash
    uvicorn backend.main:app --reload
    ```

3.  **Start the Frontend** (in a new terminal):
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

4.  **Open the App**:
    - Go to `http://localhost:5173` in your browser.
    - Enter `dummy_library` (or the full path to it) in the search box and click **Scan**.

## Detailed Installation

### Backend Setup (API)

1.  Navigate to the project root:
    ```bash
    cd media-library-tracker
    ```

2.  (Optional) Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  Run the server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Frontend Setup (UI)

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```
    The UI will be available at `http://localhost:5173`.

## Usage

1.  Enter the absolute path to your media folder (e.g., `C:\Media\Anime` or `/mnt/share/Movies`).
2.  Click **Scan**.
3.  The app will list all found media items with their parsed details.

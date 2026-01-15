# WoodCraft Custom Manufacturing Website

This is a complete prototype for a wood manufacturing company with a User-facing calculator and an Admin management panel.

## Features

- **User Side:**
  - View products
  - Calculate costs based on dimensions and wood type
  - Real-time price updates

- **Admin Side:**
  - Secure Login (default: `admin`/`admin`)
  - Dashboard
  - Manage Wood Types (Add/Delete)
  - Manage Sub-types & Prices (Add/Delete)
  - Manage Homepage Products (Add/Delete)
  - Update Labor Costs

## Setup Instructions

### 1. Prerequisites
- Python 3.x installed
- `pip` (Python package manager)

### 2. Installation

1.  Open a terminal in this folder.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Database
The application uses SQLite. The database file `wood_manufacturing.db` will be automatically created when you run the application for the first time, using the `schema.sql` file.

### 4. Running the App

1.  Start the Flask server:
    ```bash
    python app.py
    ```
2.  Open your browser and navigate to:
    - Homepage: `http://127.0.0.1:5000/`
    - Admin Panel: `http://127.0.0.1:5000/admin/login`

### 5. Default Credentials
- **Username:** `admin`
- **Password:** `admin`

## Project Structure

- `app.py`: Main backend application file (Flask).
- `schema.sql`: Database structure.
- `templates/`: HTML files for frontend.
- `static/`: CSS and Javascript files.

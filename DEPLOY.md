# How to Deploy for Free (0 Cost)

Since your project uses **Flask** and **SQLite**, here are the two best options for 0-cost deployment.

---

## Option 1: Render.com (Easiest "Git Push" Flow)
*Best for: Quick demos.*
*Warning: On the free tier, your database will reset (lose data) if the app restarts.*

1.  **Push your code to GitHub:**
    *   Create a repository on GitHub.
    *   Push all these files to it.

2.  **Deploy on Render:**
    *   Go to [dashboard.render.com](https://dashboard.render.com/) and Sign Up/Login.
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repository.
    *   **Settings:**
        *   **Name:** `wood-manufacturing` (or similar)
        *   **Runtime:** `Python 3`
        *   **Build Command:** `pip install -r requirements.txt`
        *   **Start Command:** `gunicorn app:app`
        *   **Instance Type:** `Free`
    *   Click **Create Web Service**.

3.  **Done!** Render will build and give you a URL (e.g., `https://wood-app.onrender.com`).

---

## Option 2: PythonAnywhere (Best for Data Persistence)
*Best for: Keeping your Wood/Product data saved permanently.*

1.  **Sign Up:**
    *   Go to [www.pythonanywhere.com](https://www.pythonanywhere.com/) and create a "Beginner" (Free) account.

2.  **Upload Code:**
    *   Go to the **Files** tab.
    *   Upload your files (`app.py`, `schema.sql`, `requirements.txt`) and folders (`templates`, `static`).
    *   *Tip: You can also open a "Bash" console there and `git clone` your repo.*

3.  **Install Dependencies:**
    *   Open a **Bash** console from the Dashboard.
    *   Run: `pip3.10 install -r requirements.txt --user` (Replace 3.10 with your python version if needed).

4.  **Configure Web App:**
    *   Go to the **Web** tab.
    *   Click **Add a new web app**.
    *   Select **Flask** -> **Python 3.10** (or latest).
    *   **Path:** Ensure it points to your `/home/yourusername/mysite/app.py`.

5.  **Database Config:**
    *   Since PythonAnywhere keeps files persistent, your `wood_manufacturing.db` will be created and **saved** forever.

6.  **Reload:**
    *   Click the **Reload** button on the Web tab. Your site is live at `yourusername.pythonanywhere.com`.

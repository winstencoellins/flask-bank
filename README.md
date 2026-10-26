# Simple Bank (Flask)

A beginner-friendly banking web app. There is **no login** and **no database**.
An admin can see every user, add users, and record deposits and withdrawals.
All data is stored in CSV files.

## What you need

- Python 3 installed on your computer
- A web browser (Chrome, Firefox, Safari, etc.)

## How to run the app

Open a terminal (or Command Prompt / PowerShell on Windows) and follow these steps.

### 1. Go into the project folder

```bash
cd banking_app
```

### 2. Create a virtual environment

A virtual environment is a private folder for this project's Python packages.
That way Flask is installed only for this app, not for your whole computer.

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

After it is activated, you should see `(venv)` at the start of your terminal line.

### 3. Install Flask

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
python app.py
```

You should see something like: `Running on http://127.0.0.1:5001`

### 5. Open it in your browser

Visit: [http://127.0.0.1:5001](http://127.0.0.1:5001)

If the terminal says "Address already in use", another program is using that port.
Open `app.py`, find `port=5001`, change it to another number (for example `5002`), save, and run `python app.py` again.

To stop the app, go back to the terminal and press `Ctrl + C`.

## Sample users

The app starts with three users you can click on:

| Username | Password   | Balance |
|----------|------------|---------|
| alice    | alice123   | 1000.00 |
| bob      | bob456     | 250.50  |
| charlie  | charlie789 | 0.00    |

## Project files

- `app.py` — Python backend (reads/writes CSV files and handles pages)
- `data/users.csv` — all users
- `data/transactions.csv` — all deposits and withdrawals
- `templates/` — HTML pages (Jinja templates)
- `static/style.css` — styling
- `static/script.js` — small amount of JavaScript for forms

## Note about passwords

Passwords are stored as plain text in `users.csv` **only so beginners can see how the data is saved**. Never store real passwords this way.

## Deploy to Vercel

Deploy the **`banking_app`** folder, not the repo root. Vercel looks for Flask's `app.py` in the project root it builds.

**Important:** CSV files do not persist on Vercel the way they do on your computer. Deposits may work for a short time, then reset. That is normal for this lab app on Vercel. For long-term data, a host with a real disk (Railway, Render, PythonAnywhere) is a better fit.

### Option A — Vercel website (Git)

1. Push this project to GitHub.
2. Go to [vercel.com/new](https://vercel.com/new) and import the repo.
3. Set **Root Directory** to `banking_app`.
4. Leave the framework as Flask (Vercel should detect it from `app.py` and `requirements.txt`).
5. Click Deploy.

### Option B — Vercel CLI

```bash
cd banking_app
npx vercel
```

The first time, log in if asked, then accept the defaults. Use `npx vercel --prod` for a production URL.

After it is live, open the site and click **Instructions** in the top-right for the lab notes.

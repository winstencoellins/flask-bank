# Lab: Build Your Own Simple Banking Web App

**Build this yourself.** Do not copy the example app in `banking_app/`. That folder is a finished demo for your instructor. Your job is to design your own Flask app that stores data in CSV files.

This document tells you **what the app must do**, **how the CSV files should look**, and **small samples that teach the idea**. The samples are incomplete on purpose. You still have to plan the pages, the functions, and the file layout.

> **Explore on your own.** This lab includes tools and ideas that may **not** have been taught in class (for example: the `csv` module, `flash()` messages, Jinja template inheritance, `datetime` timestamps, JavaScript `confirm()`, or creating files if they are missing). You still need to **implement those parts**. Look them up, try the concept samples below, read Flask's docs, and ask questions if you get stuck. Needing to research something is part of the assignment, not a reason to skip it.

---

## Goal

Make a tiny banking admin tool:

- There is **no login**. The person using the app is an admin who can see every user.
- There is **no database**. Save everything in `.csv` files using Python's built-in `csv` module (do not use pandas).
- The frontend is **plain HTML, CSS, and vanilla JavaScript**. No React, Vue, Bootstrap, or Tailwind.
- Use **Flask** and **Jinja templates** to render pages.

---

## Rules (keep the code beginner-friendly)

- Prefer simple functions and `for` loops.
- Avoid classes.
- The only decorators you need are Flask routes, such as `@app.route("/")`.
- Skip list comprehensions unless they are very short and easy to read.
- Add comments that explain what each part does.
- When the app starts, create the CSV files (with header rows) if they do not exist yet.

---

## Suggested project structure

You may name folders differently, but this layout works well:

```text
your_bank_app/
├── app.py
├── data/
│   ├── users.csv
│   └── transactions.csv
├── templates/
│   ├── base.html
│   ├── index.html
│   └── user_detail.html
└── static/
    ├── style.css
    └── script.js
```

Also include a `requirements.txt` with just `Flask`.

---

## How the CSV files should look

A CSV file is a spreadsheet saved as plain text. The **first row is the header** (column names). Every row after that is one record. Columns are separated by commas.

### 1. `data/users.csv`

Columns (in this order):

| Column     | Meaning                                      | Example      |
|------------|----------------------------------------------|--------------|
| `id`       | Unique number for this user                  | `1`          |
| `username` | Login name. Must be unique.                  | `alice`      |
| `password` | Stored as plain text **for this lab only**   | `alice123`   |
| `balance`  | Current money, with 2 decimal places         | `1000.00`    |

Example file:

```csv
id,username,password,balance
1,alice,alice123,1000.00
2,bob,bob456,250.50
3,charlie,charlie789,0.00
```

Notes:

- Put **2–3 sample users** in the file so the dashboard has data on first run.
- Keep money as text with 2 decimal places, like `250.50` not `250.5`.
- Never use real people's real passwords. Plain-text passwords are only for learning.

### 2. `data/transactions.csv`

Columns (in this order):

| Column          | Meaning                                         | Example                 |
|-----------------|-------------------------------------------------|-------------------------|
| `id`            | Unique number for this transaction              | `1`                     |
| `user_id`       | The `id` of the user this row belongs to        | `1`                     |
| `type`          | Either `deposit` or `withdrawal`                | `deposit`               |
| `amount`        | How much money moved, 2 decimal places          | `100.00`                |
| `balance_after` | The user's balance after this transaction       | `1100.00`               |
| `timestamp`     | When it happened, format `YYYY-MM-DD HH:MM:SS`  | `2026-10-23 15:20:22`   |

Example file (header only is fine at first):

```csv
id,user_id,type,amount,balance_after,timestamp
```

Example after Alice (user `id` 1) deposits `100.00` and her new balance is `1100.00`:

```csv
id,user_id,type,amount,balance_after,timestamp
1,1,deposit,100.00,1100.00,2026-10-23 15:20:22
```

Example after she then withdraws `50.00`:

```csv
id,user_id,type,amount,balance_after,timestamp
1,1,deposit,100.00,1100.00,2026-10-23 15:20:22
2,1,withdrawal,50.00,1050.00,2026-10-23 15:21:03
```

Rules for these files:

- `type` must be exactly `deposit` or `withdrawal`.
- `user_id` must match a user's `id` in `users.csv`.
- New transactions are **appended** (added at the bottom). Newest rows are last in the file.
- On the user page, show history **newest first** (you can reverse the list after reading it).

---

## Features you must build

### 1. Dashboard page — `/`

- Show the total number of users at the top.
- Show a table of all users: **ID**, **Username**, **Password**, **Balance**, and a **View Details** link.
- Include a form to add a new user: username, password, starting balance (default `0`).
- If the username already exists, do **not** add the user. Show an error message.

### 2. User detail page — `/user/<id>`

- Show that user's username, password, and current balance.
- A deposit form (amount + button).
- A withdrawal form (amount + button).
- A table of that user's transactions (newest first): Date/Time, Type, Amount, Balance After.
- A **Back to Dashboard** link.

### 3. Deposit and withdrawal logic

- Amount must be a **positive number**. Show an error otherwise.
- Withdrawal must **not** be larger than the current balance. Show an error if it is.
- After a successful deposit or withdrawal:
  1. update that user's `balance` in `users.csv`
  2. add a new row to `transactions.csv`
- Use Flask's `flash()` for success and error messages.

### 4. JavaScript (small and simple)

- Before a money form submits, check that the amount is a number greater than `0`. Use `alert()` if it is not.
- Before a withdrawal submits, use `confirm()` so the admin can cancel.
- Optional: a button on the dashboard that shows or hides passwords.

### 5. CSS

- One file: `static/style.css`.
- Keep it clean: centered page, tables with borders, green deposit button, red withdrawal button, styled success/error messages.
- Display money with 2 decimal places.

---

## Implementation hints (not the full answer)

Think in this order:

1. **Create empty CSV files with headers** when the app starts.
2. **Write helper functions** that only talk to files, for example:
   - `read_users()`
   - `save_users(users)`
   - `find_user_by_id(user_id)`
   - `read_transactions_for_user(user_id)`
   - `add_transaction(user_id, type, amount, balance_after)`
3. **Then write Flask routes** that call those helpers.
4. **After a form POST**, redirect back to a page (do not stay on the POST URL). This avoids the browser asking to "resubmit the form" if someone refreshes.

Useful route sketch:

| URL                     | Method     | Job                                      |
|-------------------------|------------|------------------------------------------|
| `/`                     | GET        | Show dashboard                           |
| `/add_user`             | POST       | Create a user, then redirect to `/`      |
| `/user/<user_id>`       | GET        | Show one user and their history          |
| `/user/<user_id>/deposit`   | POST   | Add money, then redirect to that user    |
| `/user/<user_id>/withdraw`  | POST   | Remove money, then redirect to that user |

Other reminders:

- CSV values come in as **strings**. Convert balance with `float(...)` before you do math. Save it back with `"{:.2f}".format(amount)`.
- To make a new `id`, look at the highest existing id and add `1`. If the file has no rows yet, start at `1`.
- Flask needs a `secret_key` before `flash()` will work.
- Put a comment at the top of `app.py` that plain-text passwords are only for learning and must never be used in a real app.

---

## Concept samples

These snippets teach **one idea at a time**. They are not your banking app. Copy the *idea*, then write your own code.

### Sample A — smallest Flask page

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
```

### Sample B — read a CSV into a list of dictionaries

`csv.DictReader` turns each row into a dictionary, using the header as keys.

```python
import csv

def read_rows(path):
    rows = []
    with open(path, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

# Example row after reading:
# {"id": "1", "username": "alice", "password": "alice123", "balance": "1000.00"}
```

### Sample C — write the whole list back to the CSV

When you change a user's balance, it is often easiest to rewrite the whole users file.

```python
import csv

def save_rows(path, rows, fieldnames):
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
```

### Sample D — append one new transaction

Deposits and withdrawals add a **new line**. You do not need to rewrite the whole transactions file.

```python
import csv

def append_row(path, row, fieldnames):
    with open(path, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(row)
```

### Sample E — create the file with a header if it is missing

```python
import csv
import os

def ensure_file(path, header):
    folder = os.path.dirname(path)
    if folder != "" and not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(path):
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
```

### Sample F — HTML form that sends data to Flask

```html
<form action="/add_user" method="post">
    <label>
        Username
        <input type="text" name="username" required>
    </label>
    <button type="submit">Add User</button>
</form>
```

In Flask, read the submitted value with:

```python
from flask import request

username = request.form.get("username", "").strip()
```

### Sample G — flash a message, then redirect

```python
from flask import Flask, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "change-this-in-your-app"

@app.route("/do_something", methods=["POST"])
def do_something():
    flash("It worked!", "success")
    return redirect(url_for("home"))
```

In the template:

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### Sample H — Jinja loop to build a table

```html
<p>Total users: {{ total_users }}</p>

<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Balance</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
        <tr>
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>${{ "%.2f"|format(user.balance|float) }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

`{{ "%.2f"|format(user.balance|float) }}` prints money with 2 decimal places, such as `10.50`.

### Sample I — check an amount in JavaScript before submit

```javascript
function validateAmount(form) {
    var amountInput = form.querySelector('input[name="amount"]');
    var amount = parseFloat(amountInput.value);

    if (isNaN(amount) || amount <= 0) {
        alert("Please enter an amount greater than 0.");
        return false;
    }

    return true;
}
```

```html
<form action="/deposit" method="post" onsubmit="return validateAmount(this);">
    <input type="number" name="amount" step="0.01">
    <button type="submit">Deposit</button>
</form>
```

For withdrawals, call `validateAmount` first, then `confirm("Are you sure?")`.

### Sample J — today's timestamp

```python
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Example: 2026-10-23 15:20:22
```

---

## How to run your app

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install Flask
python app.py
```

Open the address Flask prints, usually `http://127.0.0.1:5000`.

On many Macs, port `5000` is already used by AirPlay. If you see "Address already in use", run on another port:

```python
app.run(debug=True, port=5001)
```

---

## Checklist before you submit

- [ ] `users.csv` has the correct header and at least 2 sample users
- [ ] `transactions.csv` has the correct header
- [ ] Dashboard lists every user and can add a new one
- [ ] Duplicate usernames are rejected
- [ ] User page can deposit and withdraw
- [ ] Invalid amounts and overdrafts show an error
- [ ] Successful money moves update **both** CSV files
- [ ] Transaction table shows that user's history, newest first
- [ ] Money is shown with 2 decimal places
- [ ] Comments explain the code in your own words

Design your own page layout and function names. Matching the CSV columns and the features above is what matters.

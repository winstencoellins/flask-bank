# =============================================================================
# Simple Banking System (Flask)
# =============================================================================
# IMPORTANT (for students):
# Storing passwords in plain text is ONLY for learning purposes.
# Never do this in a real application. Real apps hash and salt passwords
# so the original password cannot be read from a file or database.
# =============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
import shutil
from datetime import datetime

# Create the Flask app object. This is the heart of the web application.
app = Flask(__name__)

# Flask needs a secret key to use flash() messages (the green/red alerts).
# In a real app this would be a long random string kept private.
app.secret_key = "beginner-banking-app-secret-key"

# Always reload HTML after a deposit/withdrawal so the new balance shows up.
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# -----------------------------------------------------------------------------
# File paths
# -----------------------------------------------------------------------------
# __file__ is the path of this app.py file. Using it means the CSV files are
# always found next to the app, even if you start Python from another folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STARTER_DATA_DIR = os.path.join(BASE_DIR, "data")

# Vercel Functions cannot save files forever. On Vercel we write to /tmp
# so deposits still work for a short demo. Locally we use the data/ folder.
if os.environ.get("VERCEL"):
    DATA_DIR = "/tmp/bank-data"
else:
    DATA_DIR = STARTER_DATA_DIR

USERS_FILE = os.path.join(DATA_DIR, "users.csv")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")


# =============================================================================
# CSV helper functions
# These functions are the only place that talks to the .csv files.
# The routes below call these helpers instead of opening files themselves.
# =============================================================================

def ensure_csv_files_exist():
    """Create the data folder and CSV files (with header rows) if missing."""
    # Make the data folder if it does not exist yet.
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # If we are on Vercel, copy the starter CSV files into /tmp first.
    copy_starter_csv_if_needed("users.csv", USERS_FILE)
    copy_starter_csv_if_needed("transactions.csv", TRANSACTIONS_FILE)

    # Create users.csv with column names if the file is not there.
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "password", "balance"])

    # Create transactions.csv with column names if the file is not there.
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "user_id", "type", "amount", "balance_after", "timestamp"])


def copy_starter_csv_if_needed(filename, dest_path):
    """Copy a starter CSV from data/ when the live file does not exist yet."""
    starter_path = os.path.join(STARTER_DATA_DIR, filename)
    if os.path.exists(dest_path):
        return
    if os.path.exists(starter_path) and starter_path != dest_path:
        shutil.copy(starter_path, dest_path)


def read_instructions_text():
    """Read the lab instructions markdown file."""
    # Prefer the file in the repo root when running locally.
    # On Vercel, only the copy inside banking_app/ is available.
    possible_paths = [
        os.path.join(BASE_DIR, "..", "INSTRUCTIONS.md"),
        os.path.join(BASE_DIR, "INSTRUCTIONS.md")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
    return "Instructions file was not found."


def clean_row(row):
    """Strip extra spaces from CSV keys and values so ids match reliably."""
    cleaned = {}
    for key in row:
        if key is None:
            continue
        value = row[key]
        if value is None:
            value = ""
        cleaned[key.strip()] = str(value).strip()
    return cleaned


def read_users():
    """Read every user from users.csv and return a list of dictionaries."""
    users = []
    with open(USERS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned = clean_row(row)
            if cleaned.get("id", "") != "":
                users.append(cleaned)
    return users


def save_users(users):
    """Write the full list of users back to users.csv (overwrites the file)."""
    with open(USERS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "username", "password", "balance"]
        )
        writer.writeheader()
        for user in users:
            writer.writerow(user)


def find_user_by_id(user_id):
    """Return the user dictionary with this id, or None if not found."""
    users = read_users()
    for user in users:
        if user["id"] == str(user_id):
            return user
    return None


def find_user_by_username(username):
    """Return the user dictionary with this username, or None if not found."""
    users = read_users()
    for user in users:
        if user["username"] == username:
            return user
    return None


def get_next_id(rows):
    """Return one more than the highest id in a list of CSV rows."""
    if len(rows) == 0:
        return 1

    highest = 0
    for row in rows:
        if row.get("id", "") == "":
            continue
        row_id = int(row["id"])
        if row_id > highest:
            highest = row_id
    return highest + 1


def update_user_balance(user_id, new_balance):
    """Change one user's balance in users.csv and save the file."""
    users = read_users()
    updated = False
    for user in users:
        if user["id"] == str(user_id):
            # Store money with 2 decimal places, e.g. 10.50
            user["balance"] = "{:.2f}".format(new_balance)
            updated = True
    save_users(users)
    return updated


def read_all_transactions():
    """Read every transaction from transactions.csv."""
    transactions = []
    with open(TRANSACTIONS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned = clean_row(row)
            if cleaned.get("id", "") != "":
                transactions.append(cleaned)
    return transactions


def save_transactions(transactions):
    """Write the full list of transactions back to transactions.csv."""
    with open(TRANSACTIONS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "user_id", "type", "amount", "balance_after", "timestamp"]
        )
        writer.writeheader()
        for row in transactions:
            writer.writerow(row)


def read_transactions_for_user(user_id):
    """Return this user's transactions, newest first."""
    matching = []
    all_transactions = read_all_transactions()
    for row in all_transactions:
        if row["user_id"] == str(user_id):
            matching.append(row)

    # New rows are added at the bottom of the CSV, so reverse to show newest first.
    matching.reverse()
    return matching


def add_transaction(user_id, transaction_type, amount, balance_after):
    """Append one new deposit or withdrawal row to transactions.csv."""
    transactions = read_all_transactions()
    new_id = get_next_id(transactions)

    # Example timestamp: 2026-10-23 15:30:01
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_row = {
        "id": str(new_id),
        "user_id": str(user_id),
        "type": transaction_type,
        "amount": "{:.2f}".format(amount),
        "balance_after": "{:.2f}".format(balance_after),
        "timestamp": timestamp
    }
    transactions.append(new_row)
    save_transactions(transactions)


def parse_amount(raw_value):
    """
    Turn form text into a positive number.
    Returns the number if valid, or None if it is not a valid amount.
    """
    try:
        amount = float(raw_value)
    except (TypeError, ValueError):
        return None

    if amount <= 0:
        return None

    # Keep money to 2 decimal places (cents).
    return round(amount, 2)


def redirect_after_post(endpoint, **values):
    """
    After a form is submitted, send the browser to a GET page.
    Code 303 means "always use GET next", so the new balance is loaded.
    """
    return redirect(url_for(endpoint, **values), code=303)


# =============================================================================
# Flask routes (the pages and form actions)
# =============================================================================

@app.before_request
def prepare_data_files():
    """Make sure the CSV files exist before every page load."""
    ensure_csv_files_exist()


@app.after_request
def stop_browser_from_caching(response):
    """Stop the browser from showing an old balance after a deposit."""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def dashboard():
    """Home page: list all users and a form to add a new user."""
    users = read_users()
    total_users = len(users)
    return render_template("index.html", users=users, total_users=total_users)


@app.route("/add_user", methods=["POST"])
def add_user():
    """Handle the 'Add User' form from the dashboard."""
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    starting_balance_text = request.form.get("balance", "0").strip()

    # Username and password cannot be empty.
    if username == "" or password == "":
        flash("Username and password are required.", "error")
        return redirect_after_post("dashboard")

    # Do not allow two users to have the same username.
    existing_user = find_user_by_username(username)
    if existing_user is not None:
        flash("That username already exists. Please choose another.", "error")
        return redirect_after_post("dashboard")

    # Starting balance is optional; if left blank we use 0.
    if starting_balance_text == "":
        starting_balance_text = "0"

    try:
        starting_balance = float(starting_balance_text)
    except ValueError:
        flash("Starting balance must be a number.", "error")
        return redirect_after_post("dashboard")

    if starting_balance < 0:
        flash("Starting balance cannot be negative.", "error")
        return redirect_after_post("dashboard")

    starting_balance = round(starting_balance, 2)

    users = read_users()
    new_user = {
        "id": get_next_id(users),
        "username": username,
        "password": password,
        "balance": "{:.2f}".format(starting_balance)
    }
    users.append(new_user)
    save_users(users)

    flash("User '" + username + "' was added successfully.", "success")
    return redirect_after_post("dashboard")


@app.route("/user/<user_id>")
def user_detail(user_id):
    """Show one user's info, deposit/withdraw forms, and transaction history."""
    user = find_user_by_id(user_id)
    if user is None:
        flash("User not found.", "error")
        return redirect_after_post("dashboard")

    transactions = read_transactions_for_user(user_id)
    return render_template("user_detail.html", user=user, transactions=transactions)


@app.route("/user/<user_id>/deposit", methods=["POST"])
def deposit(user_id):
    """Add money to a user's balance and record the transaction."""
    user = find_user_by_id(user_id)
    if user is None:
        flash("User not found.", "error")
        return redirect_after_post("dashboard")

    amount = parse_amount(request.form.get("amount"))
    if amount is None:
        flash("Please enter a positive number for the deposit amount.", "error")
        return redirect_after_post("user_detail", user_id=user_id)

    current_balance = float(user["balance"])
    new_balance = round(current_balance + amount, 2)

    updated = update_user_balance(user_id, new_balance)
    if not updated:
        flash("Could not update this user's balance.", "error")
        return redirect_after_post("user_detail", user_id=user_id)

    add_transaction(user_id, "deposit", amount, new_balance)

    flash("Deposited $" + "{:.2f}".format(amount) + " successfully.", "success")
    return redirect_after_post("user_detail", user_id=user_id)


@app.route("/user/<user_id>/withdraw", methods=["POST"])
def withdraw(user_id):
    """Remove money from a user's balance (if they have enough) and record it."""
    user = find_user_by_id(user_id)
    if user is None:
        flash("User not found.", "error")
        return redirect_after_post("dashboard")

    amount = parse_amount(request.form.get("amount"))
    if amount is None:
        flash("Please enter a positive number for the withdrawal amount.", "error")
        return redirect_after_post("user_detail", user_id=user_id)

    current_balance = float(user["balance"])

    # A user cannot withdraw more money than they currently have.
    if amount > current_balance:
        flash("Withdrawal failed: amount is greater than the current balance.", "error")
        return redirect_after_post("user_detail", user_id=user_id)

    new_balance = round(current_balance - amount, 2)

    updated = update_user_balance(user_id, new_balance)
    if not updated:
        flash("Could not update this user's balance.", "error")
        return redirect_after_post("user_detail", user_id=user_id)

    add_transaction(user_id, "withdrawal", amount, new_balance)

    flash("Withdrew $" + "{:.2f}".format(amount) + " successfully.", "success")
    return redirect_after_post("user_detail", user_id=user_id)


@app.route("/instructions")
def instructions():
    """Show the lab instructions inside the app."""
    text = read_instructions_text()
    return render_template("instructions.html", text=text)


# =============================================================================
# Start the app
# =============================================================================

# Make sure the CSV files exist when the app starts.
ensure_csv_files_exist()

if __name__ == "__main__":
    # debug=True reloads the app when you save files and shows error pages.
    # Turn this off if you ever put the app on the public internet.
    #
    # Port 5001 is used because on many Macs port 5000 is already taken
    # by AirPlay Receiver. If 5001 is busy too, try another number.
    app.run(debug=True, port=5001)

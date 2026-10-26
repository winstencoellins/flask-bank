// Beginner-friendly JavaScript for the banking app.
// These functions are called from the HTML with onsubmit="..." and onclick="..."

// Check that the amount typed in a form is a number greater than 0.
// Return false to stop the form from submitting.
function validateAmount(form) {
    var amountInput = form.querySelector('input[name="amount"]');
    var amount = parseFloat(amountInput.value);

    if (isNaN(amount) || amount <= 0) {
        alert("Please enter an amount greater than 0.");
        return false;
    }

    return true;
}

// Used by the withdrawal form.
// First validate the amount, then ask "Are you sure?" with confirm().
function confirmWithdrawal(form) {
    if (!validateAmount(form)) {
        return false;
    }

    // confirm() shows OK / Cancel. OK returns true, Cancel returns false.
    var ok = confirm("Are you sure you want to withdraw this amount?");
    return ok;
}

// Show or hide passwords in the dashboard table.
function togglePasswords() {
    var cells = document.querySelectorAll(".password-cell");
    var button = document.getElementById("toggle-passwords");
    var i;
    var cell;
    var currentlyHidden;

    if (cells.length === 0) {
        return;
    }

    // Look at the first cell to decide whether we are showing or hiding.
    currentlyHidden = cells[0].getAttribute("data-hidden") === "true";

    for (i = 0; i < cells.length; i++) {
        cell = cells[i];
        if (currentlyHidden) {
            cell.textContent = cell.getAttribute("data-password");
            cell.setAttribute("data-hidden", "false");
        } else {
            cell.textContent = "••••••";
            cell.setAttribute("data-hidden", "true");
        }
    }

    if (currentlyHidden) {
        button.textContent = "Hide Passwords";
    } else {
        button.textContent = "Show Passwords";
    }
}

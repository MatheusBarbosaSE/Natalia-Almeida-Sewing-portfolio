from flask import Flask, render_template, request, redirect, url_for, session
import os
import csv
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Secret key for session management
app.secret_key = os.urandom(24)

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

# Services page route
@app.route("/services")
def services():
    return render_template("services.html")

# About page route
@app.route("/about")
def about():
    return render_template("about.html")

# Contact page route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save form data to a CSV file
        with open("messages.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write header if the file is empty
            file.seek(0)
            if file.tell() == 0:
                writer.writerow(["Name", "Email", "Phone", "Message", "DateTime"])

            # Write the form data
            writer.writerow([name, email, phone, message, date_time])

        # Show success message after submission
        success_message = "Mensagem enviada com sucesso!"
        return render_template("contact.html", success=success_message)

    return render_template("contact.html")

# Login page route (for protected access)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        # Check if the password is correct
        if password == "admin123":
            session["authenticated"] = True
            return redirect(url_for("messages"))
        else:
            error = "Senha incorreta. Tente novamente."
            return render_template("login.html", error=error)

    return render_template("login.html")

# Messages page route (protected)
@app.route("/messages")
def messages():
    # Check if the user is authenticated
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    data = []

    try:
        # Read CSV file
        with open("messages.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)  # Read header row

            for row in reader:
                data.append(row)
    except FileNotFoundError:
        header = []
        data = []

    return render_template("messages.html", header=header, data=data)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

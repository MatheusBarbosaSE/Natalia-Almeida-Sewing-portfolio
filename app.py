from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        # Save form data to a CSV file
        with open("messages.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Check if the file is empty and write the header
            file.seek(0)
            if file.tell() == 0:
                writer.writerow(["Name", "Email", "Phone", "Message"])

            # Write the submitted form data as a new row
            writer.writerow([name, email, phone, message])

        success_message = "Mensagem enviada com sucesso!"
        return render_template("contact.html", success=success_message)

    return render_template("contact.html")

@app.route("/messages")
def messages():
    data = []

    try:
        with open("messages.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)  # Read header row

            for row in reader:
                data.append(row)
    except FileNotFoundError:
        header = []
        data = []

    return render_template("messages.html", header=header, data=data)

if __name__ == "__main__":
    app.run(debug=True)

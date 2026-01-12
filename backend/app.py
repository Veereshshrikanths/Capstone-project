from flask import Flask, render_template, request, redirect
from db_config import get_db

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]
        email = request.form["email"]

        try:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (name, phone, address, email) VALUES (%s, %s, %s, %s)",
                (name, phone, address, email)
            )

            print(" ROWS INSERTED:", cursor.rowcount)

            conn.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            print(" LAST INSERT ID:", cursor.fetchone())

            cursor.close()
            conn.close()

            return "INSERT OK – CHECK DATABASE NOW"

        except Exception as e:
            return f" ERROR: {e}"

    return render_template("login.html")


@app.route("/users")
def users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("users.html", users=users)


if __name__ == "__main__":
    app.run(debug=False)

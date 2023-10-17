from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = "muhlisasri"
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "hire.muhlis@gmail.com"
app.config["MAIL_PASSWORD"] = "wcmkufpeoscqfdat"

db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(80))
    email = db.Column(db.String(80))
    nowa = db.Column(db.String(80))
    tgl_lahir = db.Column(db.Date)
    status = db.Column(db.String(80))

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST" :
        nama = request.form["nama"]
        email = request.form["email"]
        nowa = request.form["nowa"]
        tgl_lahir = request.form["date"]
        tgl_lahir_conv = datetime.strptime(tgl_lahir, "%Y-%m-%d") # Konversi tanggal agar dapat terbaca oleh sqlite
        status = request.form["status"]

        # # Create a new Form object and add it to the database
        form_data = Form(nama=nama, email=email, nowa=nowa, tgl_lahir=tgl_lahir_conv, status=status)
        db.session.add(form_data)
        db.session.commit()

        message_body = f"Terima kasih atas pendaftarannya, {nama}. "\
                       f"Berikut adalah data anda : {nama} \n {nowa} \n "
        message = Message(subject="Registrasi Berhasil",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        flash(f"Terima kasih {nama}, formulirmu berhasil dikirim", "sukses")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
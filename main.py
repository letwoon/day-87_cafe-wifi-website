from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)

##Connect to Database
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
Bootstrap(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

class AddCafe(FlaskForm):
    name = StringField(label="Cafe Name", validators=[DataRequired()])
    img_url = StringField(label="Cafe Picture", validators=[DataRequired()])
    map_url = StringField(label="Map Url", validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired()])
    seats = StringField(label="Seats", validators=[DataRequired()])
    coffee_price = StringField(label="Coffee Price", validators=[DataRequired()])
    has_toilet = BooleanField(label="Restroom")
    has_wifi = BooleanField(label="Wifi")
    has_sockets = BooleanField(label="Sockets")
    can_take_calls = BooleanField(label="Call Reservation")
    submit = SubmitField(label="Add Cafe")

@app.route("/")
def home():
    all_cafe = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafe)


@app.route("/add", methods=["GET","POST"])
def add_cafe():
    form = AddCafe()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            img_url=form.img_url.data,
            map_url=form.map_url.data,
            location=form.location.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            has_toilet=bool(form.has_toilet.data),
            has_wifi=bool(form.has_wifi.data),
            can_take_calls=bool(form.can_take_calls.data),
            has_sockets=bool(form.has_sockets.data)
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)

@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

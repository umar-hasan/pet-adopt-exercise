from flask import Flask, request, render_template, redirect
from models import Pet, db, connect_db
from forms import AddPetForm, EditPetForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def home():
    pets = Pet.query.all()
    return render_template("index.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_form():
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        return redirect("/")
    else:
        form.age.data = 0
        return render_template("add-pet.html", form=form)

@app.route("/pet/<int:id>", methods=["GET", "POST"])
def show_pet(id):
    pet = Pet.query.get(id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo_url.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect(f"/pet/{id}")
    return render_template("pet.html", form=form, pet=pet)

@app.route("/pet/<int:id>/delete", methods=["POST"])
def delete_pet(id):
    Pet.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect("/")
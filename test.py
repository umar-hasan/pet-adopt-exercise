from unittest import TestCase
from app import app
from flask import Flask
from models import Pet, db
from forms import AddPetForm, EditPetForm


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class PetAdoptTest(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        db.session.rollback()

    def test_1_page_render(self):
        home = self.client.get("/")
        add = self.client.get("/add")

        self.assertEqual(home.status_code, 200)
        self.assertEqual(add.status_code, 200)

    def test_2_add_pet(self):
        post_res = self.client.post("/add", data={"name": "Catty", "species": "cat", "photo_url": "https://c.files.bbci.co.uk/12A9B/production/_111434467_gettyimages-1143489763.jpg", "age": "2", "notes": "Test content"})
        res = self.client.get("/")

        html = res.get_data(as_text=True)

        self.assertEqual(post_res.status_code, 302)
        self.assertIn("Catty", html)
        self.assertIn("is available!", html)

    def test_3_delete_pet(self):
        post_res = self.client.post("/pet/1/delete")

        html = post_res.get_data(as_text=True)

        self.assertEqual(post_res.status_code, 302)
        self.assertNotIn("Catty", html)
import unittest
import re

from Starline import create_app, db, bcrypt
from Starline.models import Admin

app = create_app()
db.init_app(app)


class Setup(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            # Create admin
            password = bcrypt.generate_password_hash("demo")
            admin = Admin(email="demo", password=password)
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


class LoginLogout(Setup, unittest.TestCase):
    def _login(self, app, email, password):
        return self.app.post(
            "/login",
            data=dict(email="demo", password="demo"),
            follow_redirects=True,
        )

    def _logout(self, app):
        return self.app.get("/logout", follow_redirects=True)

    def test_login_load(self):
        response = self.app.get("/login")
        self.assertEqual(response.status_code, 200)
        print("Login page loaded successfully")

    def test_login_logout(self):
        response = self._login(app, email="bob@aol.com", password="PoopyButthole01")
        self.assertIn(b"Demo", response.data)

        response = self._logout(app)
        self.assertIn(b"Login", response.data)
        print("Login and logout working successfully")


class FlashMessages(Setup, unittest.TestCase):
    def test_bad_login(self):
        response = self.app.post(
            "/login",
            data=dict(email="bob@aol.com", password="Pooutthole01"),
            follow_redirects=True,
        )
        self.assertTrue(
            re.search(
                "Login Unsuccessful. Please check email and password",
                response.get_data(as_text=True),
            )
        )

    print("Bad login successful")


if __name__ == "__main__":
    unittest.main()

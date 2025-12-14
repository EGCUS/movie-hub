from locust import HttpUser, TaskSet, task

from core.environment.host import get_host_for_locust_testing
from core.locust.common import fake, get_csrf_token


class SignupBehavior(TaskSet):
    def on_start(self):
        self.signup()

    @task
    def signup(self):
        response = self.client.get("/signup")
        csrf_token = get_csrf_token(response)

        response = self.client.post(
            "/signup", data={"email": fake.email(), "password": fake.password(), "csrf_token": csrf_token}
        )
        if response.status_code != 200:
            print(f"Signup failed: {response.status_code}")


class LoginBehavior(TaskSet):
    def on_start(self):
        self.ensure_logged_out()
        self.login()

    @task
    def ensure_logged_out(self):
        response = self.client.get("/logout")
        if response.status_code != 200:
            print(f"Logout failed or no active session: {response.status_code}")

    @task
    def login(self):
        response = self.client.get("/login")
        if response.status_code != 200 or "Login" not in response.text:
            print("Already logged in or unexpected response, redirecting to logout")
            self.ensure_logged_out()
            response = self.client.get("/login")

        csrf_token = get_csrf_token(response)

        response = self.client.post(
            "/login", data={"email": "user1@example.com", "password": "1234", "csrf_token": csrf_token}
        )
        if response.status_code != 200:
            print(f"Login failed: {response.status_code}")


class AuthUser(HttpUser):
    tasks = [SignupBehavior, LoginBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()


class EmailVerificationBehavior(TaskSet):
    """Simula el flujo de registro seguido por intentos de validación de correo.

    Dado que el código de verificación real se guarda en la sesión del servidor y
    normalmente se envía por correo, aquí simulamos el flujo y realizamos envíos
    de claves incorrectas para ejercitar la ruta de validación.
    """

    def on_start(self):
        # Crear usuario nuevo y dejar la sesión con la verificación pendiente
        self.signup()

    def signup(self):
        resp = self.client.get("/signup")
        csrf = get_csrf_token(resp)
        self._email = fake.email()
        self._password = fake.password()
        self.client.post(
            "/signup",
            data={"email": self._email, "password": self._password, "csrf_token": csrf},
            name="POST /signup",
        )

    @task(3)
    def submit_wrong_validation_key(self):
        # Accede al formulario de validación y envía una clave errónea
        resp = self.client.get("/email_validation")
        csrf = get_csrf_token(resp)
        self.client.post(
            "/email_validation",
            data={"key": "000000", "csrf_token": csrf},
            name="POST /email_validation (wrong)",
        )


# Añadimos el comportamiento de verificación al conjunto de tareas del usuario
AuthUser.tasks.append(EmailVerificationBehavior)

from locust import HttpUser, task, between
import random


class ShopUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        with self.client.post(
            "/login/",
            json={"username": "testuser", "password": "testpass123"},
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Login failed: {resp.status_code}")

    @task(1)
    def view_home(self):
        self.client.get("/")

    @task(3)
    def view_products(self):
        self.client.get("/products/")

    @task(5)
    def view_product_detail(self):
        pk = random.randint(1, 20)
        self.client.get(f"/products/{pk}/", name="/products/[id]/")

    @task(2)
    def view_profile(self):
        self.client.get("/profile/")

    @task(1)
    def view_missing_product(self):
        with self.client.get(
            "/products/9999/",
            name="/products/[missing]/",
            catch_response=True,
        ) as resp:
            if resp.status_code == 404:
                resp.success()
            else:
                resp.failure(f"Expected 404, got {resp.status_code}")

# locust -f locustfile.py --host http://127.0.0.1:8000 --headless -u 50 -r 1 -t 2m --html=report2.html
# locust -f locustfile.py --host http://127.0.0.1:8000
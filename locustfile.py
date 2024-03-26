from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_main_page(self):
        self.client.get("http://aditya.discworld.cc/")

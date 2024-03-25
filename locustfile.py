import os
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    # Set a default wait time if none is provided
    wait_time = between(1, 5)

    @task
    def load_main_page(self):
        # Get the host from an environment variable
        self.client.get(os.getenv("LOCUST_HOST_URL", "http://aditya.discworld.cc/"))

# The HOST_URL, USERS, SPAWN_RATE, and RUN_TIME can be passed as environment variables

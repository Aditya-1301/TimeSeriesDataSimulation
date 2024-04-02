import multiprocessing
import time
import random
from locust.env import Environment
from locustfile import WebsiteUser

host_url = "http://aditya.discworld.cc/"
max_users = 1_000_000_000
env = Environment(user_classes=[WebsiteUser], host=host_url)
env.create_web_ui("127.0.0.1", 8089)
env.create_local_runner()


def start_locust_instance(duration, users_per_second, sleep_time=0):
    """
    Function to start a locust instance. This function can be customized to include parameters for user count, spawn rate, etc.
    """

    env.runner.start(user_count=max_users, spawn_rate=users_per_second)

    time.sleep(duration)

    env.runner.quit()


def process_one():
    while True:
        start_locust_instance(60, 50)


def process_two():
    while True:
        start_locust_instance(120, 50, 180)


def process_three():
    random.seed(time.time() + multiprocessing.get_ident())
    while True:
        run_time = random.randint(30, 60)
        sleep_time = 300 - run_time
        start_locust_instance(run_time, 100, sleep_time)


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=process_one)
    p2 = multiprocessing.Process(target=process_two)
    p3 = multiprocessing.Process(target=process_three)

    p1.start()
    p2.start()
    time.sleep(180)
    p3.start()

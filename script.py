import threading
import time
import random
from locust.env import Environment
from locustfile import WebsiteUser

running = True

host_url = "http://aditya.discworld.cc/"
env = Environment(user_classes=[WebsiteUser], host=host_url)
env.create_web_ui("127.0.0.1", 8089)
env.create_local_runner()


def start_locust(max_users, duration, users_per_second, start_timer=0):
    while running:
        time.sleep(start_timer)
        env.runner.start(user_count=max_users, spawn_rate=users_per_second)
        time.sleep(duration)
        env.runner.quit()


def thread_one():
    while running:
        if not thread1.is_alive():
            print("Thread 1 is not alive. Restarting...")
        start_locust(500_000, 60, 500)


def thread_two():
    while running:
        if not thread2.is_alive():
            print("Thread 2 is not alive. Restarting...")
        start_locust(100_000, 120, 500, 30)


def thread_three():
    random.seed(time.time() + threading.get_ident())
    while running:
        if not thread3.is_alive():
            print("Thread 3 is not alive. Restarting...")
        # interval = 300
        duration = random.randint(30, 60)
        start_locust(50_0000, duration, 1000, 60)


thread1 = threading.Thread(target=thread_one, name='Thread 1')
thread2 = threading.Thread(target=thread_two, name='Thread 2')
thread3 = threading.Thread(target=thread_three, name='Thread 3')

thread1.daemon = True
thread2.daemon = True
thread3.daemon = True

thread1.start()
thread2.start()
thread3.start()

try:
    thread1.join()
    thread2.join()
    thread3.join()
except KeyboardInterrupt:
    running = False
    thread1.join()
    thread2.join()
    thread3.join()
    print("Simulation stopped by user.")

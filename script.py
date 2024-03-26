import threading
import time
import random
from locust.env import Environment
from locustfile import WebsiteUser

# import os
# import signal

running = True

# def signal_handler(signum, frame):
#     global running
#     print('Received shutdown signal. Stopping threads...')
#     running = False
#
#
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)

host_url = "http://aditya.discworld.cc/"
max_users = 1_000_000_000
env = Environment(user_classes=[WebsiteUser], host=host_url)
env.create_web_ui("127.0.0.1", 8089)
env.create_local_runner()


def start_locust(duration, users_per_second, thread_name):
    while running:
        # locust_command = (
        #     f"locust -f locustfile.py --autostart "
        #     f"-u {max_users} -r {users_per_second} "
        #     f"-t {duration}s "
        #     f"-H {host_url} "
        #     # f"--web-host 127.0.0.1 "
        #     # f"--web-port 8089"
        # )
        # print(f"[{thread_name}] Running Locust command: {locust_command}")
        # os.system(locust_command)
        # print(f"[{thread_name}] Locust run completed.")

        env.runner.start(user_count=max_users, spawn_rate=users_per_second)

        time.sleep(duration)

        env.runner.quit()


def thread_one():
    while running:
        if not thread1.is_alive():
            print("Thread 1 is not alive. Restarting...")
        start_locust(60, 500, 'Thread 1')


def thread_two():
    while running:
        if not thread2.is_alive():
            print("Thread 2 is not alive. Restarting...")
        start_locust(120, 500, 'Thread 2')
        time.sleep(180)


def thread_three():
    while running:
        if not thread3.is_alive():
            print("Thread 3 is not alive. Restarting...")
        interval = 300
        duration = random.randint(30, 60)
        start_locust(duration, 1000, 'Thread 3')
        time.sleep(interval - duration)


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

import threading
import time
import random
from locust.env import Environment
from locustfile import WebsiteUser

running = threading.Event()
running.set()  # Initially set to True
host_url = "http://aditya.discworld.cc/"
env = Environment(user_classes=[WebsiteUser], host=host_url)
env.create_web_ui("127.0.0.1", 8089)
env.create_local_runner()


def start_locust(max_users, duration, users_per_second, start_timer=0):
    print("Starting Locust")
    time.sleep(start_timer)
    print("Starting Locust after delay")
    env.runner.start(user_count=max_users, spawn_rate=users_per_second)
    print("Locust started")
    time.sleep(duration)
    print("Stopping Locust")
    env.runner.quit()


def thread_function(max_users, duration, users_per_second, start_timer=0):
    while running.is_set():
        print(
            f"Starting Locust with {max_users} users, {duration} seconds, {users_per_second} users/s, {start_timer} seconds delay.")
        start_locust(max_users, duration, users_per_second, start_timer)


# Use a factory function to create thread instances with different parameters
def create_thread(name, max_users, duration, users_per_second, start_timer=0):
    return threading.Thread(target=thread_function, args=(max_users, duration, users_per_second, start_timer),
                            name=name, daemon=True)


thread1 = create_thread(name='Thread 1',
                        max_users=500_000,
                        duration=60,
                        users_per_second=70)
thread2 = create_thread(name='Thread 2',
                        max_users=100_000,
                        duration=120,
                        users_per_second=100,
                        start_timer=30)
random.seed(time.time() + threading.get_ident())
thread3 = create_thread(name='Thread 3',
                        max_users=50_0000,
                        duration=random.randint(30, 60),
                        users_per_second=100,
                        start_timer=60)

thread1.start()
thread2.start()
thread3.start()

try:
    # Main thread waits for keyboard interrupt
    thread1.join()
    thread2.join()
    thread3.join()
except KeyboardInterrupt:
    # running.clear()  # Stops all threads
    thread1.join()
    thread2.join()
    thread3.join()
    print("Simulation stopped by user.")

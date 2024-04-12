import threading
import time
import random
from locust.env import Environment
from locustfile import WebsiteUser

# running = threading.Event()
# running.set()  # Initially set to True


def start_locust(max_users, duration, users_per_second, start_timer=0, web_port=8089):
    host_url = "http://aditya.discworld.cc/"
    env = Environment(user_classes=[WebsiteUser], host=host_url)
    env.create_web_ui("127.0.0.1", web_port)
    env.create_local_runner()
    print("Starting Locust")
    time.sleep(start_timer)
    print("Starting Locust after delay")
    env.runner.start(user_count=max_users, spawn_rate=users_per_second)
    print("Locust started")
    time.sleep(duration)
    print("Stopping Locust")
    env.runner.quit()


def thread_function(max_users, duration, users_per_second, start_timer=0, web_port=8089):
    running = threading.Event()
    running.set()  # Initially set to True
    while running.is_set():
        print(
            f"Starting Locust with {max_users} users, {duration} seconds, {users_per_second} users/s, {start_timer} seconds delay. UI port: {web_port}")
        start_locust(max_users, duration, users_per_second, start_timer, web_port)
        running.clear()


# Use a factory function to create thread instances with different parameters
def create_thread(name, max_users, duration, users_per_second, start_timer=0, web_port=8089):
    return threading.Thread(target=thread_function, args=(max_users, duration, users_per_second, start_timer, web_port),
                            name=name, daemon=True)


thread1 = create_thread(name='Thread 1',
                        max_users=500_000,
                        duration=60,
                        users_per_second=70,
                        web_port=8089)
thread2 = create_thread(name='Thread 2',
                        max_users=100_000,
                        duration=120,
                        users_per_second=100,
                        start_timer=30,
                        web_port=8090)
thread3 = create_thread(name='Thread 3',
                        max_users=50_0000,
                        duration=random.randint(30, 60),
                        users_per_second=100,
                        start_timer=60,
                        web_port=8091)

thread1.start()
thread2.start()
thread3.start()

try:
    # Main thread waits for keyboard interrupt
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    thread1.join()
    thread2.join()
    thread3.join()
    print("Simulation stopped by user.")

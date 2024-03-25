# import threading
# import time
# import random
# import os
# import signal
#
#
# # Flag to control the running of threads
# running = True
#
#
# # Function to handle signal for graceful shutdown
# def signal_handler(signum, frame):
#     global running
#     print('Received shutdown signal. Stopping threads...')
#     running = False
#
#
# # Register the signal handler for SIGINT (Ctrl+C)
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)
#
#
# host_url = "http://aditya.discworld.cc/"
#
#
# def simulate_locust_run_with_file(duration, users_per_second, host, thread_name):
#     while running:
#         # Set environment variables for the locustfile
#         os.environ["LOCUST_HOST_URL"] = host
#
#         locust_command = (
#             f"locust -f locustfile.py --headless "
#             f"-u {users_per_second} -r {users_per_second} "
#             f"--run-time {duration}s "
#             f"--host {host} "
#             f"--web-host 0.0.0.0 "
#             f"--web-port 8089"
#         )
#
#         print(f"[{thread_name}] Running Locust command: {locust_command}")
#         os.system(locust_command)
#         print(f"[{thread_name}] Locust run completed.")
#
#
# # The thread function that runs the locust simulation repeatedly with a fixed interval
# def fixed_interval_thread(interval, duration, users_per_second, thread_name):
#     while running:
#         simulate_locust_run_with_file(duration, users_per_second, host_url, thread_name)
#         time.sleep(interval)
#
#
# # The thread function that runs the locust simulation repeatedly with a random interval
# def random_interval_thread(min_duration, max_duration, users_per_second, thread_name):
#     while running:
#         interval = 300
#         duration = random.randint(min_duration, max_duration)
#         simulate_locust_run_with_file(duration, users_per_second, host_url, thread_name)
#         time.sleep(interval - duration)
#
#
# # Starting the threads
# thread1 = threading.Thread(target=fixed_interval_thread, args=(60, 60, 1000, 'Thread 1'))
# thread2 = threading.Thread(target=fixed_interval_thread, args=(180, 120, 1000, 'Thread 2'))
# thread3 = threading.Thread(target=random_interval_thread, args=(30, 60, 500, 'Thread 3'))
#
# # Set threads as daemons, so they end when the main thread ends
# thread1.daemon = True
# thread2.daemon = True
# thread3.daemon = True
#
# # Start the threads
# thread1.start()
# thread2.start()
# thread3.start()
#
# try:
#     thread1.join()
#     thread2.join()
#     thread3.join()
# except KeyboardInterrupt:
#     running = False
#     thread1.join()
#     thread2.join()
#     thread3.join()
#     print("Simulation stopped by user.")
#
# # Run the threads for a short while then stop (for demonstration purposes)
# # time.sleep(1000000)  # The threads run in the background
# # print("Simulation done.")  # In practice, the script would run indefinitely or until stopped manually
#
# # Normally the script would just continue running, but here we stop it to avoid an infinite loop in this environment
# # In a real-world scenario, you might have an event that, when set, stops the loop inside the threads.


import threading
import time
import random
import os
import signal

# Flag to control the running of threads
running = True


# Function to handle signal for graceful shutdown
def signal_handler(signum, frame):
    global running
    print('Received shutdown signal. Stopping threads...')
    running = False


# Register the signal handler for SIGINT (Ctrl+C) and SIGTERM
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

host_url = "http://aditya.discworld.cc/"


def simulate_locust_run_with_file(duration, users_per_second, host, thread_name):
    while running:
        # Set environment variables for the locustfile
        os.environ["LOCUST_HOST_URL"] = host
        locust_command = (
            f"locust -f locustfile.py --headless "
            f"-u {users_per_second} -r {users_per_second} "
            f"--run-time {duration}s "
            f"--host {host} "
            f"--web-host 127.0.0.1 "
            f"--web-port 8089"
        )
        print(f"[{thread_name}] Running Locust command: {locust_command}")
        os.system(locust_command)
        print(f"[{thread_name}] Locust run completed.")


# Adjusted thread functions
def thread_one():
    while running:
        simulate_locust_run_with_file(60, 500, host_url, 'Thread 1')


def thread_two():
    while running:
        simulate_locust_run_with_file(120, 500, host_url, 'Thread 2')
        time.sleep(180)


def thread_three():
    # Wait for Thread 2 to run for its 2 minutes before starting
    while running:
        interval = 300
        duration = random.randint(30, 60)
        simulate_locust_run_with_file(duration, 1000, host_url, 'Thread 3')
        time.sleep(interval - duration)


# Starting the threads
thread1 = threading.Thread(target=thread_one)
thread2 = threading.Thread(target=thread_two)
thread3 = threading.Thread(target=thread_three)

# Set threads as daemons
thread1.daemon = True
thread2.daemon = True
thread3.daemon = True

# Start the threads
thread1.start()
thread2.start()
thread3.start()

# Join threads to the main thread
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

# Daemon to run processes in the background
import time
import sys, signal
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


print("Daemon up and running")

# TODO run cronjobs here
while True:
    print("Daemon still running")
    time.sleep(60)

print("Daemon down")

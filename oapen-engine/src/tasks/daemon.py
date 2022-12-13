# Daemon to run processes in the background
import time

print("Daemon up and running")

# TODO run cronjobs here
while True:
    print("Daemon still running")
    time.sleep(60 * 2)

print("Daemon down")
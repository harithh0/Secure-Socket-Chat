from time import sleep

counter = 0
while True:
    if counter != 10:
        print("\r", "user typing ...", end="")
        sleep(0.2)
        counter += 1
    else:
        break

print("\r", end="")

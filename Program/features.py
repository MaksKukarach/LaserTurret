from time import sleep
from random import randint

# Робот начинает хаотично двигаться, имитируя танец
def dance(serial_port):
    for i in range(10):
        X = randint(0, 180)
        Y = randint(0, 180)
        serial_port.write(str.encode(f"X{X}Y{Y}"))
        print(f'Dancing: {X}, {Y}')
        sleep(0.5)
from Raspberry.final.CAR import CAR  # 载入机器人库
from pynput import keyboard
import time
import threading

top_servo_angle = 50
# bottom_servo_angle = 145
clbrobot = CAR()  # 实例化机器人对象
# clbrobot.set_servo_angle(10, bottom_servo_angle)  # 底座舵机 90
clbrobot.set_servo_angle(9, top_servo_angle)  # 顶部舵机 145

speed = 60
t = 0
current_key = None
last_press_time = 0


def on_press(key):
    global current_key, last_press_time, top_servo_angle

    last_press_time = time.time()

    try:
        if key == keyboard.Key.left and current_key == "left":
            return
        if key == keyboard.Key.right and current_key == "right":
            return
        if key.char == current_key:
            return

        current_key = key.char

        print('Alphanumeric key pressed: {0} '.format(key.char))

        if key.char == "w":
            clbrobot.t_up(speed, t)
        elif key.char == "a":
            clbrobot.move_left(speed, t)  # 机器人左移
        elif key.char == "s":
            clbrobot.t_down(speed, t)  # 机器人后退
        elif key.char == "d":
            clbrobot.move_right(speed, t)  # 机器人右移
        elif key.char == "q":
            clbrobot.forward_left(speed, t)  # 机器人前左斜
        elif key.char == "r":
            top_servo_angle -= 5
            clbrobot.set_servo_angle(9, top_servo_angle)  # 顶部舵机 145
        elif key.char == "f":
            top_servo_angle += 5
            clbrobot.set_servo_angle(9, top_servo_angle)  # 顶部舵机 145

    except AttributeError:

        print('special key pressed: {0}'.format(key))

        if key == keyboard.Key.left:
            clbrobot.turnLeft(speed, t)  # 机器人左转
            current_key = "left"
        elif key == keyboard.Key.right:
            clbrobot.turn_right(speed, t)  # 机器人右转
            current_key = "right"


def on_release(key):
    global current_key, last_press_time
    print('Key released: {0}'.format(key))
    current_key = None
    # last_press_time = time.time()
    # clbrobot.t_stop(t)

    if key == keyboard.Key.esc:
        # Stop listener
        clbrobot.t_stop(t)
        # return False


def release():
    print("before while")
    while True:
        if time.time() - last_press_time > 0.2 and current_key is None:
            clbrobot.t_stop(0)


def keyborad_listener():
    pass


if __name__ == "__main__":
    x = threading.Thread(target=release)
    x.start()
    # threading.Thread(target=keyborad_listener)

    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # try:
    #     while True:
    #         clbrobot.t_up(50, 3)  # 机器人前进
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.t_down(50, 3)  # 机器人后退
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.turnLeft(50, 3)  # 机器人左转
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.turnRight(50, 3)  # 机器人右转
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.moveLeft(50, 3)  # 机器人左移
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.moveRight(50, 3)  # 机器人右移
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.forward_Left(50, 3)  # 机器人前左斜
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.backward_Right(50, 3)  # 机器人后右斜
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.forward_Right(50, 3)  # 机器人前右斜
    #         clbrobot.t_stop(1)  # 机器人停止
    #         clbrobot.backward_Left(50, 3)  # 机器人后左斜
    #         clbrobot.t_stop(5)  # 机器人停止
    # except KeyboardInterrupt:
    #     clbrobot.t_stop(0)  # 机器人停止
    #     GPIO.cleanup()

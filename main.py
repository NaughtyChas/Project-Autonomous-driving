import time
from CAR import CAR
from pynput import keyboard
import cv2

last_press_time = 0

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    speed = 99
    t = 0
    current_key = None
    car = CAR()
    last_press_time = 0

    if not capture.isOpened():
        print("Cannot open camera")
        exit()

    is_camera_open = True

    while True:
        if is_camera_open:
            ret, frame = capture.read()
            if not ret:
                print("ERROR,Can't receive frame(stream end?), Exiting...")
                break

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        tm = time.strftime('%Y,%m,%d %H %M %S')
        if key == ord('c'):
            filename = tm + '.jpg'
            cv2.imwrite(filename, frame)

        if key == ord('p'):
            is_camera_open = not is_camera_open

        if key == ord('w'):
            print('w')
            car.t_up(speed, 0)
        if key == ord('s'):
            print('s')
            car.t_down(speed, 0)
        if key == ord('a'):
            print('a')
            car.move_left(speed, 0)
        if key == ord('d'):
            print('d')
            car.move_right(speed, 0)
        if key == ord(' '):
            print('stopped')
            car.t_stop(0)
        if key == ord('k'):
            print('turn left')
            car.turn_left(speed,0)
        if key == ord('l'):
            print('turn right')
            car.turn_right(speed,0)

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


        if key == 27:
            break

    capture.release()
    cv2.destroyAllWindows()

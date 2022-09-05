import cv2
import torch
import numpy as np
from my_car import MyCar
from tracks_training import Net

device = torch.device("cpu")
net = Net().to(device)
net.train(False)
net.load_state_dict(torch.load(f"parameters/resnet18_eXX.pth", map_location=device))  # 模型权重路径


def auto_drive_with_nn(image: np.ndarray):
    with torch.no_grad():
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_LINEAR)  # 缩放成 224 * 224
        image = np.transpose(image, (2, 0, 1))  # 将RGB通道移到最前面
        image = image.reshape(1, 3, 224, 224)  # 重塑成 batch_size * channel * width * height 形式
        image = torch.tensor(image / 255, dtype=torch.float).to(device)  # 将值从 0-255 映射到 0-1 并转成 tensor
        outputs = net(image)
        _, predicted = torch.max(outputs.data, 1)
        moving_status = predicted.item()
        return moving_status


def main():
    car = MyCar()
    speed = 40
    capture = cv2.VideoCapture(0)

    while True:
        ret, input_frame = capture.read()
        if not ret:
            print("Error open camera.")
            break

        moving_status = auto_drive_with_nn(input_frame)

        if moving_status == 0:
            car.t_up(speed)
        elif moving_status == 1:
            car.turn_left(speed)
        elif moving_status == 2:
            car.turn_right(speed)

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

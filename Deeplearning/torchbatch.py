import time
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as fun
import torch.optim as optim

Device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

Transform = transforms.Compose([
    transforms.ToTensor(),
])


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.resnet = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.DEFAULT)
        self.resnet = nn.Sequential(*list(self.resnet.children())[:-1])
        self.fc1 = nn.Linear(512, 100)
        self.fc2 = nn.Linear(100, 10)

    def forward(self, x):
        f512 = self.resnet(x)
        f512 = f512.view(-1, 512)
        f100 = self.fc1(f512)
        f100 = fun.relu(f100)
        f10 = self.fc2(f100)
        f10 = fun.softmax(f10)
        return f10


def train_model(batch_size: int, start_epoch: int, end_epoch: int, model_name: str):
    train_set = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=Transform)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=4)

    net = Net().to(Device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    if start_epoch >= 1:
        net.load_state_dict(torch.load(f"parameters/{model_name}_e{start_epoch}.pth"))

    for epoch in range(start_epoch + 1, end_epoch + 1):
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data[0].to(Device), data[1].to(Device)
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            if i % 10 == 0:
                print(f"epoch {epoch}, batch {i}, loss = {loss.item()}")
        torch.save(net.state_dict(), f"parameters/{model_name}_e{epoch}.pth")


def test_model(batch_size: int, epoch: int, model_name: str):
    test_set = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=Transform)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=True, num_workers=4)

    net = Net().to(Device)
    if epoch >= 1:
        net.load_state_dict(torch.load(f"parameters/{model_name}_e{epoch}.pth"))

    correct, total = 0, 0
    with torch.no_grad():
        for data in test_loader:
            inputs, labels = data[0].to(Device), data[1].to(Device)
            outputs = net(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f"Accuracy of epoch {epoch} = {100 * correct // total} %")


if __name__ == '__main__':
    print(Device)

    test_model(batch_size=256, epoch=0, model_name="resnet18")

    for e in range(1, 11):
        start_time = time.time()
        train_model(batch_size=256, start_epoch=e - 1, end_epoch=e, model_name="resnet18")
        end_time = time.time()
        print(f"Training time for epoch {e} = {end_time - start_time:.2f}s")
        test_model(batch_size=256, epoch=e, model_name="resnet18")

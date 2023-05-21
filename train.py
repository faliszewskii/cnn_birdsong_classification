import pandas as pd
import torch
import torchvision.transforms as transforms
from torch import nn
from torch.utils.data import DataLoader

from BirdsongDataset import BirdsongDataset
from Net import Net
import torch.optim as optim


if __name__ == "__main__":

    batch_size = 4
    num_workers = 2
    data_source = "./spectrograms"
    train_data_annotations = "train_data.csv"
    test_data_annotations = "test_data.csv"
    classes_file = "classes.csv"

    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((300, 300)),
        transforms.ToTensor(),
        transforms.Normalize((0.5), (0.5))
    ])

    train_set = BirdsongDataset(data_source, train_data_annotations, transform=transform)
    train_loader = DataLoader(dataset=train_set, shuffle=True, batch_size=batch_size, num_workers=num_workers)

    test_set = BirdsongDataset(data_source, test_data_annotations, transform=transform)
    test_loader = DataLoader(dataset=test_set, shuffle=False, batch_size=batch_size, num_workers=num_workers)

    classes = pd.read_csv(classes_file)

    #dataset_example(train_loader, classes, batch_size)

    net = Net(len(classes))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    train_count = len(train_loader)

    for epoch in range(2):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}, train_count: {train_count}')
                running_loss = 0.0

    print('Finished Training')
    output_net = './trained_net.pth'
    torch.save(net.state_dict(), output_net)
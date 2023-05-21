import pandas as pd
import torch
import torchvision
from torch.utils.data import DataLoader
from tqdm import tqdm

from BirdsongDataset import BirdsongDataset
import torchvision.transforms as transforms
from NetV2 import Net
from test_dataset import imshow

if __name__ == "__main__":
    trained_model = "trained_net_v2.pth"
    data_source = "./spectrograms"
    test_data_annotations = "test_data.csv"
    classes_file = "classes.csv"
    batch_size = 4
    num_workers = 2
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5), (0.5))
    ])

    classes = pd.read_csv(classes_file)
    net = Net(len(classes))
    net.load_state_dict(torch.load(trained_model))

    test_set = BirdsongDataset(data_source, test_data_annotations, transform=transform)
    test_loader = DataLoader(dataset=test_set, shuffle=False, batch_size=batch_size, num_workers=num_workers)
    # print images
    dataiter = iter(test_loader)
    images, labels = next(dataiter)
    imshow(torchvision.utils.make_grid(images))
    print('GroundTruth: ', ' '.join(f'{classes.iloc[int(labels[j]), 0]:5s}' for j in range(4)))

    outputs = net(images)

    _, predicted = torch.max(outputs, 1)

    print('Predicted: ', ' '.join(f'{classes.iloc[int(predicted[j]), 0]:5s}'for j in range(4)))

    correct = 0
    total = 0
    # since we're not training, we don't need to calculate the gradients for our outputs
    with torch.no_grad():
        for data in tqdm(test_loader):
            images, labels = data
            # calculate outputs by running images through the network
            outputs = net(images)
            # the class with the highest energy is what we choose as prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy of the network on the test images: {100 * correct // total} %')
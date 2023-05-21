import numpy as np
import torch
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd

import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from tqdm import tqdm

from BirdsongDataset import BirdsongDataset
from Net import Net

y_pred = []
y_true = []

trained_model = "trained_net.pth"
data_source = "./spectrograms"
test_data_annotations = "test_data.csv"
classes_file = "classes.csv"
batch_size = 4
num_workers = 2
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((300, 300)),
    transforms.ToTensor(),
    transforms.Normalize((0.5), (0.5))
])
test_set = BirdsongDataset(data_source, test_data_annotations, transform=transform)
test_loader = DataLoader(dataset=test_set, shuffle=False, batch_size=batch_size, num_workers=num_workers)

# constant for classes
classes = pd.read_csv(classes_file)
classes_headers = tuple(classes.iloc[int(i), 0] for i in range(len(classes)))

net = Net(len(classes))
net.load_state_dict(torch.load(trained_model))
# iterate over test data
for inputs, labels in tqdm(test_loader):
    output = net(inputs)  # Feed Network

    output = (torch.max(torch.exp(output), 1)[1]).data.cpu().numpy()
    y_pred.extend(output)  # Save Prediction

    labels = labels.data.cpu().numpy()
    y_true.extend(labels)  # Save Truth


threshold = 0.05
# Build confusion matrix
cf_matrix = confusion_matrix(y_true, y_pred)
df_cm = pd.DataFrame(cf_matrix / np.sum(cf_matrix, axis=1)[:, None], index=[i for i in classes_headers],
                     columns=[i for i in classes_headers])
labels = pd.DataFrame(cf_matrix / np.sum(cf_matrix, axis=1)[:, None], index=[i for i in classes_headers],
                     columns=[i for i in classes_headers])
labels = labels.applymap(lambda x: f"{x:.2f}" if x > threshold else '')
plt.figure(figsize=(24, 16))
#sn.set(font_scale=1.2)
heatmap = sn.heatmap(
    df_cm,
    #cmap="mako",
    square=True,
    annot=labels,
    annot_kws={'fontsize':12, 'color': '#8A8A8A'},
    fmt='',
    linewidth=0.01,
    linecolor="#4A4A4A"
)
plt.savefig('output.png')
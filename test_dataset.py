import matplotlib.pyplot as plt
import numpy as np
import torchvision


# functions to show an image


def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


def dataset_example(loader, classes, batch_size):
    # get some random training images
    dataiter = iter(loader)
    images, labels = next(dataiter)

    # show images
    imshow(torchvision.utils.make_grid(images))
    # print labels
    print(' '.join(f'{classes.iloc[int(labels[j]), 0]:5s}' for j in range(batch_size)))

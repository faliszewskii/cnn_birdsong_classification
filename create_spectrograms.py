import os
from concurrent.futures import ThreadPoolExecutor

import librosa
import numpy
import skimage


def scale_minmax(X, min=0.0, max=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled


def spectrogram_image(y, sr, out, hop_length, n_mels):
    # use log-melspectrogram
    mels = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels,
                                          n_fft=hop_length * 2, hop_length=hop_length)
    mels = numpy.log(mels + 1e-9)  # add small number to avoid log(0)

    # min-max scale to fit inside 8-bit range
    img = scale_minmax(mels, 0, 255).astype(numpy.uint8)
    img = numpy.flip(img, axis=0)  # put low frequencies at the bottom in image
    img = 255 - img  # invert. make black==more energy

    # save as PNG
    skimage.io.imsave(out, img)


def create_spectrogram(path, i, subdir_output, hop_length, n_mels, time_steps):

    y, sr = librosa.load(path, offset=1.0, duration=10.0, sr=22050)
    out = os.path.join(subdir_output, file[:-3] + "png")
    # extract a fixed length window
    start_sample = 0  # starting at beginning
    length_samples = time_steps * hop_length
    window = y[start_sample:start_sample + length_samples]

    # convert to PNG
    spectrogram_image(window, sr=sr, out=out, hop_length=hop_length, n_mels=n_mels)
    print("Processed file {}/{}: {}".format(i, total_files, path))


if __name__ == '__main__':
    # settings
    hop_length = 512  # number of samples per time-step in spectrogram
    n_mels = 224  # number of bins in spectrogram. Height of image
    time_steps = 224  # number of time-steps. Width of image

    input_dir = 'snippets'
    output_dir = 'spectrograms'

    # traverse the directory structure and identify audio files
    total_files = sum(len(files) for _, _, files in os.walk(input_dir))
    processed_files = 0

    for subdir, dirs, files in os.walk(input_dir):
        # create the corresponding output subdirectory
        subdir_output = os.path.join(output_dir, os.path.relpath(subdir, input_dir))
        if not os.path.exists(subdir_output):
            os.makedirs(subdir_output)
        for file in files:
            with ThreadPoolExecutor() as executor:
                path = os.path.join(input_dir, os.path.relpath(subdir, input_dir), file)
                executor.submit(create_spectrogram, path, processed_files, subdir_output, hop_length, n_mels, time_steps)
                processed_files += 1

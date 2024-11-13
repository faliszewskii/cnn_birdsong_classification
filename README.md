# CNN Birdsong Classification
Birdsong classification using Convolutional Neural Network

## Data preprocessing
The dataset to train and test the neural network was created from scratch using data available through the API at [xeno-canto.org](https://xeno-canto.org/). 150 recordings were downloaded from Poland of each species that had a sufficient number of recordings in the territory of Poland. The website provides recordings in MP3 or WAV format, so those that were in MP3 format were converted to WAV format.
The input files were cut into three-second chunks and transformed into spectrograms, an example of which is shown in Figure 2. The Fourier transform window size is 512 samples. The process is shown in Figure 1.

<p align="center">
  <img src="https://github.com/faliszewskii/cnn-birdsong-classification/assets/74872004/5b32cd77-40ab-4bcd-a761-2c2a6b658262" alt="process" width="600" />
  <p align = "center"><i>Figure 1 - Preprocessing process of downloaded data. The downloaded files, which can be in MP3 format, are first converted to WAV format and then cut into fragments and converted to spectrogram.</i></p>
</p>

<p align="center">  
  <img src="https://github.com/faliszewskii/cnn-birdsong-classification/assets/74872004/00c8ceb1-b4b3-4320-9aa6-7cd727ac47e4" alt="Black Woodpecker birdsong spectrogram" width="200"/>
  <p align="center"><i>Figure 2 - Example of the resulting spectrogram which is the input for the neural network.</i> </p>
</p>

The main justification for choosing such a short time of 3 seconds is research indicating that the curve of human sound recognition accuracy from sound length flattens out around 3 seconds, and that experiments training convolutional neural networks on sound tracks  achieved good results for this duration [1] [2]. 

The Fourier transform approach was chosen because research on human hearing has shown that the brain decomposes a continuous sound wave into individual frequencies (with an emphasis on low frequencies), from which the neurons responsible for sound recognition are able to extract increasingly detailed information [3].

## Struktura sieci
The data set was split into 80% training data and 20% test data. There were a total of 48 species and therefore classes to classify. Before the image was sent to the network, it was converted to greyscale, scaled to 300x300 pixels and normalised. The network used is presented in Figure 3, and its configuration was as follows:
1. convolution layer 1 input channel, 6 output channels, 5x5 kernel (ReLU activation function).
2. maxPooling layer, size 2x2, step 2
Convolution layer 6 input channels, 16 output channels, 5x5 kernel (ReLU activation function).
ReLU activation).
4. maxPooling layer, size 2x2, step 2
5. tensor flattening to one dimension
6. linear layer with ReLu activation func. 82944 → 120
7. linear layer with activation func. ReLu 120 → 84
8. linear layer with ReLu activation func. 84 → 48

<p align="center">  
  <img src="https://github.com/faliszewskii/cnn-birdsong-classification/assets/74872004/ba54c947-2a63-4da9-86b7-1c4acfce6df3" alt="Black Woodpecker birdsong spectrogram" width="1000"/>
  <p align="center"><i>Figure 3 - Neural network structure recognising bird species.</i> </p>
</p>

## Results
The trained neural network correctly classified the spectrogram 58% of the time based on the test set. Figure 4 shows the confusion matrix of the trained network. 58% is a good result, given that the probability of correctly randomly classifying a spectrogram into 48 classes is about 2%. Furthermore, the single recording that we would like to identify can last up to several minutes resulting in dozens of 3-second fragments whose spectrogram is classified. Thanks to that, the resulting species can be selected as the one most frequently attributed to the fragments analysed.

<p align="center">  
  <img src="https://github.com/faliszewskii/cnn-birdsong-classification/assets/74872004/144e829e-ce89-4a32-a424-c0cc6ad31ab9" alt="Black Woodpecker birdsong spectrogram" width="1000"/>
  <p align="center"><i>Figure 4 - Confusion table for the trained network with labelled cells starting with a value of 0.05. The OY axis shows the actual species and the OX axis shows the species predicted by the neural network.</i> </p>
</p>

## Conclusions
The objective of the task was achieved with good results. Nevertheless, there are aspects of the solution that can be developed. For example, the quality of the data set could be improved by removing
fragments that contain silence or random noise. It is also worth mentioning that the chosen network may not necessarily be the best for this application. Various network configurations were tested during the task, although on the one hand there was a computer memory problem with networks that were too deep, and on the other hand there was a problem with the quality of the results with highly compressed spectrograms. Time limitation was also an issue as training process can take a great amount of time.

## Bibliography

- [1] G. Tzanetakis and P. Cook. Musical genre classification of audio signals. IEEE Transactions
on Speech and Audio Processing, 10(5):293-302, 2002.
- [2] Honglak Lee, Peter Pham, Yan Largman, and Andrew Ng. Unsupervised feature learning for
audio classification using convolutional deep belief networks. In Y. Bengio, D. Schuurmans,
J. Lafferty, C. Williams, and A. Culotta, editors, Advances in Neural Information Processing
Systems, volume 22, pages 1096-1104. Curran Associates, Inc., 2009.
- [3] Mingwen Dong. Convolutional neural network achieves human-level accuracy in music genre
classification. Feb 2018.

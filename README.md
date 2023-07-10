# CNN Birdsong Classification
Birdsong classification using Convolutional Neural Network

## Preprocessing danych
Zestaw danych do wytrenowania i przetestowania sieci neuronowej został stworzony od zera na
podstawie danych dostępnych za pośrednictwem API w [xeno-canto.org](https://xeno-canto.org/). Pobrano po 150 nagrań z Polski każdego gatunku, który
posiadał wystarczającą liczbę nagrań na terenie Polski. Strona udostępnia nagrania w formacie
MP3 lub WAV, więc te, które były w formacie MP3, zostały przekonwertowane na format WAV.
Pliki wejściowe zostały pocięte na trzysekundowe fragmenty oraz przekształcone w spektrogramy,
których przykład pokazano na rysunku 1. Rozmiar okna przekształcenia Fouriera to 512 próbek. Proces przedstawiono na rysunku 2.
<p align="center">
  <img src="https://github.com/faliszewskii/cnn-birdsong-classification/assets/74872004/5b32cd77-40ab-4bcd-a761-2c2a6b658262" alt="process" width="600" />
  <p align = "center"><i>Rysunek 1 - Proces preprocessingu pobranych danych. Pobrane pliki, które mogą być w formacie MP3 są
najpierw konwertowane na format WAV, a następnie cięte na fragmenty i konwertowane na spektrogram.</i></p>
</p>

<p align="center">  
  <img src="https://github.com/faliszewskii/cnn-birdsong-classification/assets/74872004/00c8ceb1-b4b3-4320-9aa6-7cd727ac47e4" alt="Black Woodpecker birdsong spectrogram" width="200"/>
  <p align="center"><i>Rysunek 2 - Przykład wynikowego spektrogramu będącego wejściem dla sieci neuronowej.</i> </p>
</p>

Głównym usprawiedliwieniem wyboru tak krótkiego czasu 3 sekund są badania wskazujące,
że krzywa dokładności rozpoznawania dźwięku przez człowieka od jego długości ulega spłaszczeniu
w okolicach 3 sekund oraz to, że eksperymenty trenujące splotowe sieci neuronowe na ścieżkach
dźwiękowych osiągały dobre wyniki dla tego czasu [1] [2]. 

Podejście wykorzystujące przekształcenie Fouriera zostało wybrane, ponieważ badania nad ludzkim słuchem wykazały, że mózg rozkłada ciągłą falę
dźwiękową na poszczególne częstotliwości (z naciskiem na częstotliwości niskie), z których neurony
odpowiedzialne za rozpoznawanie dźwięków są w stanie wyodrębnić coraz to bardziej szczegółowe informacje [3].

## Struktura sieci
Zestaw danych został podzielony na 80% danych treningowych oraz 20% danych testowych. Wszystkich gatunków, a więc klas do klasyfikacji było łącznie 48. Przed wysłaniem obrazu do sieci, obraz
był przekształcany do skali szarości, skalowany do formatu 300x300 pikseli i normalizowany. Wykorzystana sieć zaprezentowana została na rysunku 3, a jej konfiguracja była następująca:
1. Warstwa konwolucyjna 1 kanał wejściowy, 6 kanałów wyjściowych, kernel 5x5 (funkcja aktywacji ReLU).
2. Warstwa MaxPooling, rozmiar 2x2, krok 2
3. Warstwa konwolucyjna 6 kanałów wejściowych, 16 kanałów wyjściowych, kernel 5x5 (funkcja
aktywacji ReLU).
4. Warstwa MaxPooling, rozmiar 2x2, krok 2
5. Spłaszczenie tensora do jednego wymiaru
6. Warstwa liniowa z f. aktywacji ReLu 82944 → 120
7. Warstwa liniowa z f. aktywacji ReLu 120 → 84
8. Warstwa liniowa z f. aktywacji ReLu 84 → 48

<p align="center">  
  <img src="https://github.com/faliszewskii/cnn-birdsong-classification/assets/74872004/ba54c947-2a63-4da9-86b7-1c4acfce6df3" alt="Black Woodpecker birdsong spectrogram" width="1000"/>
  <p align="center"><i>Rysunek 3 - Struktura sieci neuronowej rozpoznająca gatunki ptaków.</i> </p>
</p>

## Wyniki

Wytrenowana sieć neuronowa poprawnie klasyfikowała spektrogram w 58% przypadków na podstawie zbioru testowego. Na rysunku 4 pokazana została tablica pomyłek (ang. Confusion matrix)
wytrenowanej sieci. 58% to bardzo dobry wynik, biorąc pod uwagę, że prawdopodobieństwo poprawnej losowej klasyfikacji spektrogramu do 48 klas jest równe około 2%. Ponadto, pojedyncze
nagranie, które chcielibyśmy zidentyfikować może trwać do kilku minut co daje kilkadziesiąt 3-sekundowych fragmentów, których spektrogram jest klasyfikowany. Wtedy jako wynikowy gatunek
może zostać wybrany ten, który został najczęściej przypisywany badanym fragmentom.

<p align="center">  
  <img src="https://github.com/faliszewskii/cnn-birdsong-classification/assets/74872004/144e829e-ce89-4a32-a424-c0cc6ad31ab9" alt="Black Woodpecker birdsong spectrogram" width="1000"/>
  <p align="center"><i>Rysunek 4 - Tablica pomyłek dla wyuczonej sieci z oznaczonymi kamórkami zaczynając od wartości 0.05. Na osi OY widnieją gatunki rzeczywiste, a na osi OX gatunki przewidziane przez sieć neuronową.</i> </p>
</p>

## Wnioski
Udało się osiągnąć cel zadania z bardzo dobrym wynikiem. Niemniej jednak, są aspekty rozwiązania, które można rozwinąć. Przykładowo można ulepszyć jakość zestawu danych poprzez usunięcie
fragmentów, które w całości zawierają ciszę albo szum. Warto również wspomnieć, że wybrana sieć niekoniecznie może być najlepsza do tego zastosowania. Podczas realizacji zadania zostały
przetestowane różne konfiguracje sieci, aczkolwiek z jednej strony pojawiał się problem pamięci
operacyjnej komputera przy sieciach zbyt głębokich, a z drugiej strony pojawiał się problem jakości wyników przy mocno skompresowanych spektrogramach.

## Bibliografia

- [1] G. Tzanetakis and P. Cook. Musical genre classification of audio signals. IEEE Transactions
on Speech and Audio Processing, 10(5):293-302, 2002.
- [2] Honglak Lee, Peter Pham, Yan Largman, and Andrew Ng. Unsupervised feature learning for
audio classification using convolutional deep belief networks. In Y. Bengio, D. Schuurmans,
J. Lafferty, C. Williams, and A. Culotta, editors, Advances in Neural Information Processing
Systems, volume 22, pages 1096-1104. Curran Associates, Inc., 2009.
- [3] Mingwen Dong. Convolutional neural network achieves human-level accuracy in music genre
classification. Feb 2018.

# Custom Vision vs Own Model for object detection

### Skład zespołu
1. Ivan Prakapets,
2. Aliaksandr Karolik,
3. Jakub Korczakowski,
4. Piotr Rosa,
5. Bartosz Puszkarski.

### Opis projektu
Celem projektu jest zapoznanie się z usługą Custom Vision w Azure [start](https://azure.microsoft.com/en-us/services/cognitive-services/custom-vision-service/) oraz porównanie z własnym wyborem modelu dla wykrywanie obiektów. [dokumentacja do startu Custom Vision](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier).

Usługa Custom Vision jest częścią chmurowych usług Cognitive Services na platformie Azure.

### Zbiory danych

W celu porówniania działania onu serwisów planujemy sprawdzić trzy zbiory danych, różnią się one wielkością. Wszystkie z nich zawierają obrazy wraz z otagowanymi obiektami (tagi w plikach `.xml` lub `.txt`).

- Monkey, Cat and Dog detection (30 MB) - https://www.kaggle.com/tarunbisht11/yolo-animal-detection-small,
- street object detection dataset (228 MB) - https://www.kaggle.com/fantacher/bd-street-object-detection-dataset,
- Labeled Surgical Tools and Images (734 MB) - https://www.kaggle.com/dilavado/labeled-surgical-tools.

Zbiorem referncyjnym w zadaniu detekcji obiektów jest zbiór COCO (https://cocodataset.org/#home). Jeśli zasoby dostępne na Azure umożliwią nam to planujemy użycie także tego zbioru.

### Funkcjonalności
Nasz projekt będzie rozpoznawał, wykrywał obiekty.
Zaskres danych (należy wybrać):
  1. Rozpoznawanie oznakowania ekologicznego np. [przyklad zdjecia](https://www.spg-pack.com/blog/wp-content/uploads/2019/10/semitipo-1024x506-1024x506.jpg)
  2. Zwierzę
  3. Produkty żywności
  4. Samochody
  5. Popularne marki (brendy) Cola, Nike i td.
  
### Diagram
![alt text](wykres.png "Design")


### Stos technologiczny
- Microsoft Azure Storage Blocks,
- Azure Machine Learning Services,
- Microsoft Azure Custom Vision,
- Microsoft Azure Machine Learning Compute Cluster
- Python3, PyTorch, NumPy, SciPy,


### Kamienie milowe
1. Diagramy architektury oraz określenie zakresu prac i funkcjonalności.
2. ...

### Harmonogram

| Lp. | Data | Zadanie | 
| -------- | ------------- | ------------------------------------------------- |
| 1        | 26.11.2020          | P2 - przedstawienie architektury projektu i tworzonych artefaktów                                |
| 2    | 10.12.2020 | P3 - check-point|                                                              |
| 3   | 07.01.2021 | P4 |
| 4   | 14.01.2021 | P5 - middle-check point |
| 5   | 21.01.2021 | P6 |
| 6   | 28.01.2021 | P7 - prezentacja projektów                                   |                                                              |




### Przydatne materiały

Object detection w Custom Vision - https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/get-started-build-detector

Deep Learning na Azure - https://github.com/Microsoft/HyperdriveDeepLearning
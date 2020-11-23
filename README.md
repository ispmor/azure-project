# Custom Vision vs Own Model for object detection

### Opis projektu
Celem projektu jest zapoznanie się z usługą Custom Vision w Azure [start](https://azure.microsoft.com/en-us/services/cognitive-services/custom-vision-service/) oraz porównanie z własnym wyborem modelu dla wykrywanie obiektów. [dokumentacja do startu Custom Vision](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier).

Usługa Custom Vision jest częścią chmurowych usług Cognitive Services na platformie Azure.

### Funkcjonalności
Nasz projekt będzie rozpoznawał, wykrywał obiekty.
Zaskres danych (należy wybrać):
  1. Rozpoznawanie oznakowania ekologicznego np. [przyklad zdjecia](https://www.spg-pack.com/blog/wp-content/uploads/2019/10/semitipo-1024x506-1024x506.jpg)
  2. Zwierzę
  3. Produkty żywności
  4. Samochody
  5. Popularne marki (brendy) Cola, Nike i td.
  
### Wstępną architekturę (diagram)

### Stos technologiczny
Oprócz Custom Vision, mozna będzie uzyć [tu](https://azure.microsoft.com/en-us/services/media-services/video-indexer/) Video indexer. Może indeksować filmy, rozpoznaje twarze, nastroje (które pojawiają się na osi czasu), obiekty i tekst na ekranie. Można będzie brać dane z video, ale to do przymyślenia.

### Harmonogram

| Lp. | Data | Zadanie | 
| -------- | ------------- | ------------------------------------------------- |
| 1        | 26.11.2020          | przedstawienie architektury projektu i tworzonych artefaktów                                |

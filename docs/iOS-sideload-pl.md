# SSP na iPhonie/iPadzie: pobieranie i sideload

To jest eksperymentalny port. Eksport projektu Xcode jest sprawdzony; działanie
na prawdziwym urządzeniu wymaga jeszcze testów.

## 1. Pobierz IPA

1. Wejdź w [buildy iOS](https://github.com/h4z3fyx/sound-space-plus/actions/workflows/build-ios.yml).
2. Otwórz zakończony zielonym znakiem build zawierający zadanie `build-ios`.
3. Na dole strony, w **Artifacts**, pobierz **Rhythia-iOS-unsigned**.
   GitHub może wymagać zalogowania. Artefakt pojawia się dopiero po udanym buildzie
   i jest dostępny przez ograniczony czas.
4. Rozpakuj ZIP na komputerze. W środku jest **Rhythia-unsigned.ipa**.
   Tego pliku użyj w Sideloadly. `Rhythia-Xcode` zawiera projekt dla programistów,
   a nie gotową aplikację do sideloadu.

Jeżeli przy ostatnim buildzie jest czerwony znak albo nie ma artefaktu IPA,
plik nie został zbudowany — samo pobranie kodu jako ZIP nie wystarczy.

## 2. Podpisz Apple ID i zainstaluj przez Sideloadly

Potrzebujesz komputera Windows lub Mac, kabla USB, Apple ID i urządzenia iOS.
Nie musisz kupować konta deweloperskiego, żeby przetestować aplikację na własnym telefonie.

1. Pobierz **Sideloadly wyłącznie z [sideloadly.io](https://sideloadly.io/)**
   i zainstaluj wersję dla swojego komputera.
2. Na Windows zainstaluj wymagane przez Sideloadly wersje iTunes i iCloud
   z linków na jego oficjalnej stronie. Obecna instrukcja Sideloadly wymaga wersji
   ze strony Apple, a nie Microsoft Store. Na Macu pomiń ten krok.
3. Podłącz odblokowanego iPhone'a/iPada przez USB. Na urządzeniu wybierz
   **Zaufaj temu komputerowi** i wpisz kod blokady.
4. Uruchom Sideloadly. Wybierz telefon w polu urządzenia.
5. Przeciągnij **Rhythia-unsigned.ipa** do okna Sideloadly.
6. Wpisz swoje **Apple ID** i kliknij **Start**. Hasło i ewentualny kod 2FA
   podaj w oknie Sideloadly zgodnie z jego komunikatami. Nie wysyłaj ich na czacie.
7. Poczekaj na zakończenie instalacji. Sideloadly pobierze profil deweloperski
   i podpisze aplikację Twoim Apple ID — nie potrzebujesz osobnego pliku certyfikatu.
8. Jeśli iOS zgłosi niezaufanego dewelopera: otwórz **Ustawienia → Ogólne →
   VPN i zarządzanie urządzeniem**, wybierz wpis swojego Apple ID i wybierz **Zaufaj**.
9. Na iOS/iPadOS 16 lub nowszym włącz **Ustawienia → Prywatność i ochrona →
   Tryb dewelopera**, jeśli urządzenie tego wymaga. Uruchom ponownie telefon
   i potwierdź włączenie. Ta opcja może pojawić się dopiero po instalacji aplikacji
   deweloperskiej. Nazwy pozycji zależą od wersji i języka systemu.
10. Otwórz **Rhythia** na telefonie.

### Darmowe Apple ID: ważne ograniczenia

- Podpis zwykle wygasa po **7 dniach**. Odśwież instalację przez Sideloadly
  przed wygaśnięciem albo zainstaluj ponownie ten sam plik, używając tego samego konta.
  Sideloadly ma też funkcję automatycznego odświeżania; wymaga działającego komputera
  i połączenia z urządzeniem.
- Apple ogranicza liczbę aktywnych aplikacji i identyfikatorów przy darmowym koncie.
  Jeśli Sideloadly zgłosi limit, postępuj według jego komunikatu.
- Zachowaj to samo konto i identyfikator aplikacji przy aktualizacjach. Przed
  usunięciem aplikacji zrób kopię danych w **Pliki → Na moim iPhonie/iPadzie → Rhythia**;
  usunięcie aplikacji może usunąć jej dane.
- To nie jest instalacja z App Store ani TestFlight. Niepodpisanego IPA nie da się
  zainstalować samym kliknięciem w Safari.

## Alternatywa: podpis bezpośrednio w Xcode

Na Macu pobierz artefakt **Rhythia-Xcode**, rozpakuj wszystkie pliki razem,
otwórz `Rhythia.xcodeproj`, wybierz target **Rhythia → Signing & Capabilities**,
włącz **Automatically manage signing**, wybierz własny **Team** i unikalny
**Bundle Identifier**. Zastąp eksportowy Team ID `0000000000` swoim zespołem.
Wybierz podłączony telefon i kliknij **Run**.
Pełna instrukcja budowania znajduje się w [iOS.md](iOS.md).

Oficjalna instrukcja Apple dotycząca zaufania aplikacjom:
[Instalowanie niestandardowych aplikacji](https://support.apple.com/en-us/102109).

# Système d'authentification d'utilisateurs par NFC

Ce projet démontre comment utiliser un Arduino avec un module NFC PN532 pour authentifier des utilisateurs via des tags NFC. L'Arduino lit l'identifiant unique (UID) d'un tag NFC et l'envoie à un script Python exécuté sur un ordinateur portable pour un traitement ultérieur.

## Matériel requis
- Arduino Uno R3
- Module NFC PN532 (par exemple, le shield RFID VMA211)
- Tags NFC (par exemple, Mifare Classic 1K)
- Câble USB pour Arduino

## Logiciels requis
- Arduino IDE
- Python 3.x
- Bibliothèque `pyserial` (pour le script Python)

## Installation

### 1. Configuration de l'Arduino
1. Connectez le module NFC PN532 à votre Arduino.
2. Téléversez le sketch Arduino fourni sur votre Arduino à l'aide de l'Arduino IDE.

   ```cpp
   #include "PN532.h"
   #include <SPI.h>

   #define PN532_CS 10
   PN532 nfc(PN532_CS);

   void setup(void) {
       Serial.begin(9600);
       Serial.println("Système d'authentification NFC");

       nfc.begin();
       uint32_t versiondata = nfc.getFirmwareVersion();
       if (!versiondata) {
           Serial.println("Carte PN53x non détectée");
           while (1); // Arrêt
       }
       nfc.SAMConfig(); // Configurer le PN532 pour lire les tags
   }

   void loop(void) {
       uint32_t id;
       id = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A);

       if (id != 0) {
           Serial.print("Tag NFC détecté avec UID : ");
           Serial.println(id);

           delay(2000); // Attendre avant de scanner le prochain tag
       }
   }
   ```
### librairie arduino
   utilisation de la librairie PN532 pour lire les uids des Tags NFC. Celle-ci a été modifier légerment pour enlever les debugs sur la communication en série.

### fonctionement
  La communication se fait grace au port série de l'arduino, le script python tourne sur le  PC client afin de recevoir les différents uid des tags NFC.

#include "PN532.h"
#include <SPI.h>

#define PN532_CS 10
PN532 nfc(PN532_CS);



void setup(void) {
    Serial.begin(9600);
    Serial.println("NFC User Authentication System");

    nfc.begin();
    uint32_t versiondata = nfc.getFirmwareVersion();
    if (!versiondata) {
        Serial.println("Didn't find PN53x board");
        while (1); // Halt
    }
    nfc.SAMConfig(); // Configure the PN532 to read tags
}

void loop(void) {
    uint32_t id;
    id = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A);

    if (id != 0) {
        Serial.print("Detected NFC Tag with UID: ");
        Serial.println(id);

        delay(2000); // Wait before scanning the next tag
    }
}
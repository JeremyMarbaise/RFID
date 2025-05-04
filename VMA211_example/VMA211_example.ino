#include "PN532.h"
#include <SPI.h>

#define PN532_CS 10
PN532 nfc(PN532_CS);
uint8_t keys[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; // Default key for Mifare Classic
const uint8_t BLOCK_NUMBER = 4; // Block to store client ID (avoid block 0-3)

void setup(void) {
    Serial.begin(115200);
    Serial.println("NFC Client ID Manager");
    
    nfc.begin();
    uint32_t versiondata = nfc.getFirmwareVersion();
    if (!versiondata) {
        Serial.println("PN532 not found");
        while (1);
    }
    nfc.SAMConfig();
}

void loop(void) {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        
        if (command == "READ") {
            readClientId();
        }
        else if (command.startsWith("WRITE:")) {
            String clientId = command.substring(6);
            clientId.trim();
            writeClientId(clientId);
        }
    }
}

void readClientId() {
    uint32_t id;
 
    id = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A);

    if (id != 0) {
        if (nfc.authenticateBlock(1, id, BLOCK_NUMBER, KEY_A, keys)) {
            uint8_t data[17];
            if (nfc.readMemoryBlock(1, BLOCK_NUMBER, data)) {
                String clientId = "";
                for (int i = 0; i < 16; i++) {
                    if (data[i] == 0) break;
                    clientId += (char)data[i];
                }
                data[16]='\0';
                Serial.print("CLIENT_ID:");
                Serial.println(clientId);
            }
        }
    }
    delay(1000);
}

void writeClientId(String clientId) {
    uint32_t id;
    id = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A);
    
    if (id != 0) {
        if (nfc.authenticateBlock(1, id, BLOCK_NUMBER, KEY_A, keys)) {
            uint8_t data[16] = {0};
            for (int i = 0; i < 16 && i < clientId.length(); i++) {
                data[i] = clientId[i];
            }

            if (nfc.writeMemoryBlock(1, BLOCK_NUMBER, data)) {
                Serial.println("WRITE_SUCCESS");
            } else {
                Serial.println("WRITE_FAILED");
            }
        }
    }
    delay(1000);
}

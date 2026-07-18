const uint8_t RELAY_1 = 14;
const uint8_t RELAY_2 = 27;
const uint8_t RELAY_3 = 26;
const uint8_t RELAY_4 = 25;

const bool RELAY_ACTIVE_LOW = true;

void setRelay(uint8_t pin, bool enabled) {
  if (RELAY_ACTIVE_LOW) {
    digitalWrite(pin, enabled ? LOW : HIGH);
  } else {
    digitalWrite(pin, enabled ? HIGH : LOW);
  }
}

void allRelaysOff() {
  setRelay(RELAY_1, false);
  setRelay(RELAY_2, false);
  setRelay(RELAY_3, false);
  setRelay(RELAY_4, false);
}

void activateOnly(uint8_t relayPin) {
  allRelaysOff();
  setRelay(relayPin, true);
}

void setup() {
  Serial.begin(115200);

  pinMode(RELAY_1, OUTPUT);
  pinMode(RELAY_2, OUTPUT);
  pinMode(RELAY_3, OUTPUT);
  pinMode(RELAY_4, OUTPUT);
  allRelaysOff();

  Serial.println("Flower AIoT relay controller ready");
}

void loop() {
  if (!Serial.available()) {
    return;
  }

  char command = Serial.read();
  switch (command) {
    case '1':
      activateOnly(RELAY_1);
      Serial.println("Relay 1 ON");
      break;
    case '2':
      activateOnly(RELAY_2);
      Serial.println("Relay 2 ON");
      break;
    case '3':
      activateOnly(RELAY_3);
      Serial.println("Relay 3 ON");
      break;
    case '4':
      activateOnly(RELAY_4);
      Serial.println("Relay 4 ON");
      break;
    case '0':
      allRelaysOff();
      Serial.println("All relays OFF");
      break;
    default:
      Serial.println("Unknown command ignored");
      break;
  }
}

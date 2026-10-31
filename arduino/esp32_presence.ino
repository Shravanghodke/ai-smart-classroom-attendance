// Optional presence indicator for the AI-based attendance prototype.
// Wiring: PIR OUT -> GPIO 27, PIR VCC -> 3V3 (check your module), GND -> GND.
// This sketch reports presence over Serial; it does not identify students.

const int PIR_PIN = 27;
const int LED_PIN = 2;  // Common onboard LED pin on many ESP32 boards; verify your board.

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("Smart Classroom presence monitor ready");
}

void loop() {
  const bool motionDetected = digitalRead(PIR_PIN) == HIGH;
  digitalWrite(LED_PIN, motionDetected ? HIGH : LOW);

  if (motionDetected) {
    Serial.println("PRESENCE_DETECTED");
  } else {
    Serial.println("NO_PRESENCE");
  }
  delay(1000);
}

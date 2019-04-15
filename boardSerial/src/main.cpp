#include <Arduino.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {

//  Serial.print("S");
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
                // read the incoming byte:
                // say what you got:
                Serial.write(Serial.read());
                // Serial.print(Serial.read(),HEX);
  }
}

#include <Arduino.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // int pulse_id=1;
  // if (Serial.available() > 0) {
  //     Serial.print( "P27," + (String)pulse_id + "1\n");
  //     delay (5000);
  //     Serial.print( "P27," + (String)pulse_id + "0\n");
  //     pulse_id = pulse_id + 1;
  //     delay(5000)
  // }


  Serial.write("P27, 1, 1\n");
  delay(5000);
  Serial.write("P27, 1, 0 \n");
  delay(5000);
  Serial.write("P27, 2, 1 \n");
  delay(5000);
  Serial.write("P27, 2, 0 \n");
  delay(5000);
  Serial.write("P27, 3, 1 \n");
  delay(5000);
  Serial.write("P27, 3, 0 \n");
  delay(5000);
}

/*
 */
#include <servo.h>
void setup() {
    int lecteur = A0;
    Servo servomoteur;
    servomoteur.attach(9);
    servomoteur.write(90);
}

void loop() {
  delayMicroseconds(5);
  if (analogRead(lecteur) > 1){
      servomoteur.write(140)
  }
  else {
    servomoteur.write(90)
  }
}

#include <Servo.h>

// Crear objetos Servo
Servo thumb, ind, middle, ring, pinky;

// Pines compatibles con Arduino UNO (PWM)
int thumb_pin = 3;
int index_pin = 5;
int middle_pin = 6;
int ring_pin = 9;
int pinky_pin = 10;

int fingers[5] = {0, 0, 0, 0, 0};
String data = "";

void setup() {
  thumb.attach(thumb_pin);
  ind.attach(index_pin);
  middle.attach(middle_pin);
  ring.attach(ring_pin);
  pinky.attach(pinky_pin);

  Serial.begin(9600);
  stopAll();  // Asegura que todos los servos inicien detenidos
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    parseData(data);
    controlFingers();
  }

  delay(50); // Evita saturar el puerto
}

void parseData(String inputData) {
  int index = 0, start = 0;
  int commaIndex = inputData.indexOf(',');

  while (commaIndex >= 0 && index < 5) {
    fingers[index] = inputData.substring(start, commaIndex).toInt();
    start = commaIndex + 1;
    commaIndex = inputData.indexOf(',', start);
    index++;
  }

  if (index < 5) {
    fingers[index] = inputData.substring(start).toInt();
  }
}

void controlFingers() {
  moveFinger(thumb, fingers[0]);
  moveFinger(ind, fingers[1]);
  moveFinger(middle, fingers[2]);
  moveFinger(ring, fingers[3]);
  moveFinger(pinky, fingers[4]);
}

void moveFinger(Servo &servo, int state) {
  if (state == 1) {
    servo.write(87);     // Giro MUY lento a la izquierda
    delay(70);           // Tiempo de giro corto (aprox 3°)
    servo.write(90);     // Detener
  } else {
    servo.write(93);     // Giro MUY lento a la derecha
    delay(70);           
    servo.write(90);     // Detener
  }
}

void stopAll() {
  thumb.write(90);
  ind.write(90);
  middle.write(90);
  ring.write(90);
  pinky.write(90);
}

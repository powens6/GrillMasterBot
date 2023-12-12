#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  Serial.begin(115200);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(50);  // Analog servos run at ~50 Hz updates
  delay(10);
}

void loop() {
  if (Serial.available() >= 8) {
    int pulselengths[4];
    for (int i = 0; i < 4; i++) {
      pulselengths[i] = Serial.parseInt();
    }

    // Set pulse lengths for each servo
    pwm.setPWM(0, 0, pulselengths[0]); // Servo 1
    pwm.setPWM(1, 0, pulselengths[1]); // Servo 2
    pwm.setPWM(2, 0, pulselengths[2]); // Servo 3
    pwm.setPWM(3, 0, pulselengths[3]); // End Effector
  }
} 
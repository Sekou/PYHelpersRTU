// Multi-accelerometer readings from Adafruit MPU6050
// S. Diane, 2024

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

const int NUM=3;
Adafruit_MPU6050 mpus[NUM];
int pins[]={GPIO_NUM_2, GPIO_NUM_4, GPIO_NUM_5};

void startPin(int ind)
{
  pinMode(pins[ind], OUTPUT);
  digitalWrite(pins[ind], LOW); //enable
  // Try to initialize!
  if (!mpus[ind].begin()) {
    Serial.print("Failed to find MPU6050 chip ");
    Serial.println(ind);
    while (1) {delay(10);}
  }
  
  Serial.print("MPU6050 ");
  Serial.print(ind);
  Serial.println(" found!");
  
  //mpus[ind].setAccelerometerRange(MPU6050_RANGE_8_G);
  //mpus[ind].setGyroRange(MPU6050_RANGE_500_DEG);

  mpus[ind].setAccelerometerRange(MPU6050_RANGE_8_G);
  mpus[ind].setGyroRange(MPU6050_RANGE_500_DEG);
  mpus[ind].setFilterBandwidth(MPU6050_BAND_21_HZ);

  digitalWrite(pins[ind], HIGH); //disable
}

void setup(void) {
  Serial.begin(115200);
  while (!Serial) delay(10); // waiting while console opens
  Serial.println("Adafruit MPU6050 test!");

  for(int i=0;i<NUM;i++)
    digitalWrite(pins[i], HIGH); //disable

  for(int i=0;i<NUM;i++){
    startPin(i);
    delay(20);
  }
}

void printIMU(int ind) {
  digitalWrite(pins[ind], LOW); //enable
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpus[ind].getEvent(&a, &g, &temp);
  digitalWrite(pins[ind], HIGH); //disable

  /* Print out the values 
  Serial.print("IMU ind: ");
  Serial.print(ind);
  Serial.print(", Acceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");*/

  /* Print out the values */
  Serial.print(a.acceleration.x);
  Serial.print(", ");
  Serial.print(a.acceleration.y);
  Serial.print(", ");
  Serial.print(a.acceleration.z);
  Serial.print(", ");
  Serial.print(g.gyro.x);
  Serial.print(", ");
  Serial.print(g.gyro.y);
  Serial.print(", ");
  Serial.print(g.gyro.z);
  Serial.print(", ");
}

void loop() {
   for(int i=0;i<NUM;i++)
    printIMU(i);
  
  Serial.println("");
  delay(25);
}



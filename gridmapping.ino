//pin definitions
const int motor1Pin1 = 5; // Example motor 1 control pin 1
const int motor1Pin2 = 6; // Example motor 1 control pin 2
const int motor2Pin1 = 9; // Example motor 2 control pin 1
const int motor2Pin2 = 10; // Example motor 2 control pin 2

const int trig = 7;
const int echo = 8;


char fromPi;

void setup() {
  //pin configurations
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

  Serial.begin(9600);
}

void right() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
}

void left() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

void forward() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

void backward() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
}

void stopmotors() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
}

void getultradata() {
  long sum = 0; 

  for (int i = 0; i < 10; i++) { 
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);

    long duration = pulseIn(echo, HIGH);
    long distance = duration * 0.034 / 2; 
    sum += distance; 
  }

  long finalDistance = sum / 10; 
  Serial.println(finalDistance); 
}


void loop() {
  delay(15);
  if (Serial.available() > 0) {
    fromPi = Serial.read();

    if (fromPi == 'F') {
      forward();
    } else if (fromPi == 'B') {
      backward();
    } else if (fromPi == 'R') {
      right();
    } else if (fromPi == 'L') {
      left();
    } else if (fromPi == 'S') {
      stopmotors();
    }else if (fromPi == 'U'){
      stopmotors();
      getultradata();
    }
    } 
  
  Serial.flush();
  

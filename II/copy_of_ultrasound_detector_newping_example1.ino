// Ignore this first bit but don't delete or change it
// this bit is usually hidden inside 
// #import <NewPing.h>
// But I can't hide it in TinkerCad. 
class NewPing {
  public:
    NewPing(int TRIGGER_PIN, int ECHO_PIN, int MAX_DISTANCE ){
      trigPin=TRIGGER_PIN;
      echoPin=ECHO_PIN;
      maxDistance=MAX_DISTANCE;

      pinMode(trigPin,OUTPUT);
      pinMode(echoPin,INPUT);
    }

    int ping_cm(){
      // Clears the trigPin
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      // Sets the trigPin on HIGH state for 10 micro seconds
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      // Reads the echoPin, returns the sound wave travel time in microsecond
      long duration = pulseIn(echoPin, HIGH);
      // Calculating the distance
      int distance =  duration*0.034/2;
      // Checks out of range
      if (distance>maxDistance){
        distance=0;
      }
      return(distance);
    }

  private:
    int trigPin;
    int echoPin;
    int maxDistance;
};
// this is the bit you can modify



#define TRIGGER_PIN  9  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     8  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 100 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
#define GREEN 5
#define YELLOW 4
#define RED 3
#define BLUE 2

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
int cm;
void setup() {
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(RED, OUTPUT);
}

void loop() {
  delay(50);                     // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  delay(50);
  cm = sonar.ping_cm();
  Serial.println(cm);
if(cm > 49){
    digitalWrite(RED,LOW);
    digitalWrite(YELLOW,LOW);
    digitalWrite(GREEN,LOW);
    digitalWrite(BLUE,HIGH);
  }else if(cm > 30){
    digitalWrite(RED,LOW);
    digitalWrite(YELLOW,LOW);
    digitalWrite(GREEN,HIGH);
    digitalWrite(BLUE,LOW);
  }else if(cm > 20){
    digitalWrite(RED,LOW);
    digitalWrite(YELLOW,HIGH);
    digitalWrite(GREEN,LOW);
    digitalWrite(BLUE,LOW);
  }else if(cm != 0 && cm > 0){
    digitalWrite(RED,HIGH);
    digitalWrite(YELLOW,LOW);
    digitalWrite(GREEN,LOW);
    digitalWrite(BLUE,LOW);
  }else{
  	digitalWrite(RED,LOW);
  	digitalWrite(YELLOW,LOW);
  	digitalWrite(BLUE,LOW);
  	digitalWrite(GREEN,LOW);
  }
}
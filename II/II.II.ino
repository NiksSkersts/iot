// bibliotēka LCD vadībai
#include <LiquidCrystal.h>
const int ELEMENT_COUNT_MAX = 21;
int i = 0;
//šķidro kristālu displeja pieslēgvietas
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
//Temperatūras sensora pieslēgvieta
const int tempSensorPin = A0;
int storage_array[ELEMENT_COUNT_MAX];
//nolasītā temperatūras sensora vērtība
int tempSensVal = 0;
//nolasītā vērtība pārveidota uz voltiem
float volts = 0;
//volti pārveidoti uz celsija grādiem
float temp = 0;
float average (int * array, int len)  // assuming array is int.
{
  long sum = 0L ;  // sum will be larger than an item, long for safety.
  for (int i = 0 ; i < len ; i++)
    sum += array [i] ;
  return  ((float) sum) / len ;  // average will be fractional, so float may be appropriate.
}
void setup()
{
  //temperatūras sensora pieslēgvietas stāvokļa noteikšana
  pinMode(tempSensorPin, INPUT);
  //displeja nodefinēšana, (16 rakstzīmes, 2 rindas)
  lcd.begin(16, 2);
  //teksta izvadīšana LCD
  lcd.print("Digital");
  //kursora novietošana otrās rindas sākumā
  lcd.setCursor(0, 1);
  //teksta izvadīšana LCD
  lcd.print("thermometer");
  //pauze 5 sekundes
  delay(5000);
}
void loop()
{
  //temperatūras sensora vērtības nolasīšana
  tempSensVal = analogRead(tempSensorPin);
  //nolasītās vērtības pārveidošana uz voltiem
  volts = (tempSensVal / 1024.0) * 5.0;
  //iegūtās vērtības pārveidošana uz celsija grādiem
  temp = (volts - 0.5) * 100;
  storage_array[i] = temp;
  i++;
  if (i == ELEMENT_COUNT_MAX) {
    i = 0;
    int avg = average(storage_array, ELEMENT_COUNT_MAX);
    lcd.clear();
    //kursora novietošana pirmās rindas sākumā
    lcd.setCursor(0, 0);
    lcd.print("Temperature: ");
    lcd.setCursor(0, 1);
    lcd.print(avg);
    lcd.print(" ");
    //grādu simbola "◦" izvadīšana LCD
    lcd.print((char)223);
    lcd.print("C");
    delay(2000);
  }
}

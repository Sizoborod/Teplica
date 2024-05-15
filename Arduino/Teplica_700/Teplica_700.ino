// Видеообзоры и уроки работы с ARDUINO и ESP8266 на http://iomoio.ru

#include <PCF8574.h>
#include <ESP8266WiFi.h>                  // Библиотека для создания Wi-Fi подключения (клиент или точка доступа)
#include <WiFiClient.h>                   // Библиотека для связи с сетевыми хостами (локальными и интернет)
// Библиотека для работы с временем
#include <ArduinoJson.h>                  // Библиотека для разбора JSON
#include "DHT.h"
#include <LiquidCrystal_PCF8574.h>
LiquidCrystal_PCF8574 lcd(0x27);
PCF8574 PCF(0x26);
#include "ADS1X15.h"
ADS1115 ADS(0x48);

/*
  const char* ssid = "TP-Link_182C";
  const char* password = "5090748900";*/


const char* ssid = "Tp-Link";
const char* password = "9278512183";
String token = "bXgLsghZdNVDUDM";

int timetesting = 100;// время тестирования устройств

int timesend = 0;
int timeloop = 0;


WiFiClient client;                        // Создаём объект для работы с удалёнными хостами
/*
   ВЫХОДЫ
   d1 экран scl
   d2 экран sda
   d5 Насос
   d6 Подогрев
   d7 Вентилятор
   d8 Подсветка

   ВХОДЫ
   освешеность А0
   влажность А1
   Влажность А2
   уровень воды А4
   Температура внутри D2
   Температура снаружи D5

*/
#define DHTPIN_in D3
#define DHTPIN_out D4
#define DHTTYPE DHT11
DHT dht_in(DHTPIN_in, DHTTYPE);
DHT dht_out(DHTPIN_out, DHTTYPE);
#define pin_Pump 4
#define pin_Heat 5
#define pin_Led 6
#define pin_Fan 7

void OFF_Led();
void ON_Heat();
void OFF_Heat();
void ON_Pump();
void OFF_Pump();
void ON_Fan();
void OFF_Fan();
void ON_Led();
int Moisture_1;
int Moisture_2;
int Light;
int Temp_in;
int Temp_out;
int Humidity_in;
int Humidity_out;
int Level_water;
int fan = 0;
int pump = 0;
int heat = 0;
int led = 0;
int f_fan = 0;
int f_pump = 0;
int f_heat = 0;
int f_led = 0;
int light_on = 65;
int heat_on = 15;
int heat_off = 25;
int fan_on = 25;
int pump_on = 60;
int water = 60;
int control = 0;
int delta_send = 300;
int delta_loop = 30;
int sending = 0;
bool rebut = false;

int timeup = 0;
const char* up[]  = {
  "|",     // 0
  "/",     // 1
  "-",     // 2
  "\\",     // 3
  "|",     // 4
  "/",     // 5
  "-",     // 6
  "\\",    // 7
};


void OFF_Led() {
  PCF.write(pin_Led, 1);
}
void ON_Heat() {
  PCF.write(pin_Heat, 0);
}
void OFF_Heat() {
  PCF.write(pin_Heat, 1);
}
void ON_Pump() {
  PCF.write(pin_Pump, 0);
}
void OFF_Pump() {
  PCF.write(pin_Pump, 1);
}
void ON_Fan() {
  PCF.write(pin_Fan, 0);
}
void OFF_Fan() {
  PCF.write(pin_Fan, 1);
}
void ON_Led() {
  PCF.write(pin_Led, 0);
}
void setup() {
  OFF_Led();
  OFF_Heat();
  OFF_Pump();
  OFF_Fan();

  Serial.begin(9600);                                         // Инициализируем вывод данных на серийный порт со скоростью 9600 бод
  Serial.println("\n\n");

  Wire.begin();
  ADS.begin();

  dht_in.begin();
  dht_out.begin();
  pinMode(DHTPIN_in, INPUT);
  pinMode(DHTPIN_out, INPUT);

  WiFi.begin(ssid, password);                                 // Соединяемся с WiFi-сетью
  lcd.begin(20, 4);// у нас экран 16 столбцов на 2 строки
  lcd.setBacklight(255); //установить яркость подсветки на максимум
  lcd.clear(); // очистить экран и установить курсор в позицию 0, 0
  lcd.print("Rucheek");// печатаем нужную строку
  lcd.setCursor(4, 1);// переводим курсор в нужную позицию
  lcd.print("Teplica 7.0");// печатаем нужную строку
  delay(2000);// Initialize the LED_BUILTIN pin as an output
  while (WiFi.status() != WL_CONNECTED)                       // Пока соединение не установено
    delay(500);                                               //  делаем задержку в пол секунды, пока соединение не установится
  Serial.print(WiFi.localIP());
  lcd.setCursor(0, 2);
  lcd.print("Connect Wi-Fi");// печатаем нужную строку
  lcd.setCursor(0, 3);// переводим курсор в нужную позицию
  lcd.print(WiFi.localIP());// печатаем нужную строку
  delay(2000);


  testingsystem(timetesting);                                 // запускаем тестирование реле на работу. Должна прощелкать четырмя реле
  int count_connect = 0;
  while (!TimeAndWeather() || count_connect < 5)                                   // Синхронизируем время микроконтроллера с реальным временем и получаем информацию о погоде
  {
    delay(1000);
    count_connect = count_connect + 1;
  }
  lcd.clear();
}

void loop() {

  delay(1000);
  readSensors();

  if (Light < light_on  || f_led) {
    ON_Led();
    led = 1;
  } else {
    OFF_Led();
    led = 0;
  }
  if ((Temp_in > heat_on) && (Temp_in < heat_off)  || f_heat) {
    ON_Heat();
    heat = 1;

  } else {
    OFF_Heat();
    heat = 0;
  }
  if ( ((Moisture_1 + Moisture_2) / 2  < pump_on) && (Level_water > 20) || f_pump) {
    ON_Pump();
    pump = 1;
    lcd.begin(20, 4);// у нас экран 16 столбцов на 2 строки
    lcd.setBacklight(255); //установить яркость подсветки на максимум
    lcd.clear(); // очистить экран и установить курсор в позицию 0, 0
    rebut = true;
  } else {
    OFF_Pump();
    pump = 0;
    if (rebut) {
      lcd.begin(20, 4);// у нас экран 16 столбцов на 2 строки

      lcd.setBacklight(255); //установить яркость подсветки на максимум
      lcd.clear(); // очистить экран и установить курсор в позицию 0, 0
    }
    rebut = false;
  }

  if ((Temp_in > Temp_out) && (fan_on <= Temp_in) || f_fan) {
    ON_Fan();
    fan = 1;
  } else {
    OFF_Fan();
    fan = 0;
  }
  timeloop += 1;
  timesend += 1;
  timeup += 1;
  if (timeloop >= delta_loop - sending) {
    timeloop = 0;
    int count_connect = 0;
    while (!TimeAndWeather() || count_connect < 5)                                   // Синхронизируем время микроконтроллера с реальным временем и получаем информацию о погоде
    {
      delay(1000);
      count_connect = count_connect + 1;
    }

  }
  if (timesend >= delta_send) {
    timesend = 0;

    sendSensors();
  }
  printDisplayParam();
  printserial();
  lcd.setCursor(15, 0);
  lcd.print(up[timeup]);
  if (timeup >= 7) {
    timeup = 0;
  }

}

bool TimeAndWeather () {                                               // Функция синхронизации времени работы программы с реальным временем и получения информации о погоде
  if (client.connect("teplica.pythonanywhere.com", 80)) {                                   // Если удаётся установить соединение с указанным хостом (Порт 443 для https)
    client.println("GET /update/bXgLsghZdNVDUDM HTTP/1.1\r\nHost: teplica.pythonanywhere.com\r\nConnection: close\r\n\r\n"); // Отправляем параметры запроса
    delay(200);                                                             // Даём серверу время, чтобы обработать запрос
    char endOfHeaders[] = "\r\n\r\n";

    Serial.println("endOfHeaders=");
    // Системные заголовки ответа сервера отделяются от остального содержимого двойным переводом строки
    if (!client.find(endOfHeaders)) {                                       // Отбрасываем системные заголовки ответа сервера
      Serial.println("Invalid response");                                   // Если ответ сервера не содержит системных заголовков, значит что-то пошло не так
      return false;                                                         // и пора прекращать всё это дело
    }
    const size_t capacity = 750;                                            // Эта константа определяет размер буфера под содержимое JSON (https://arduinojson.org/v5/assistant/)
    DynamicJsonBuffer jsonBuffer(capacity);                                 // Инициализируем буфер под JSON

    JsonObject& root = jsonBuffer.parseObject(client);                      // Парсим JSON-модержимое ответа сервера
    client.stop();                                                          // Разрываем соединение с сервером
    //Serial.println(root);                                   // Если ответ сервера не содержит системных заголовков, значит что-то пошло не так
    if (root["light_on"].as<String>().toInt() != 0 || root["heat_on"].as<String>().toInt()) {
      light_on = root["light_on"].as<String>().toInt();
      heat_on =  root["heat_on"].as<String>().toInt();
      heat_off =  root["heat_off"].as<String>().toInt();
      fan_on =  root["heat_on"].as<String>().toInt();
      pump_on =  root["pump_on"].as<String>().toInt();
      f_pump =  root["pump"].as<String>().toInt();
      f_heat =  root["heat"].as<String>().toInt();
      f_led =  root["led"].as<String>().toInt();
      f_fan =  root["fan"].as<String>().toInt();
      water =  root["water"].as<String>().toInt();
      control =  root["control"].as<String>().toInt();
      delta_send =  root["delta_send"].as<String>().toInt();
      delta_loop =  root["delta_loop"].as<String>().toInt();
      sending =  root["sending"].as<String>().toInt();
      lcd.setCursor(15, 2);
      lcd.print("R");

    }
    else {
      lcd.setCursor(15, 2);
      lcd.print("L");
    }


    // печатаем нужную строку
    //delay(5000);
    jsonBuffer.clear();                                                     // Очищаем буфер парсера JSON

    // Синхронизируем время

    return true;
  }
  return false;
}

unsigned long StringToULong(String Str) {                     // Эта функция преобразует String в unsigned long
  unsigned long ULong = 0;
  for (int i = 0; i < Str.length(); i++) {                    // В цикле посимвольно переводим строку в unsigned long
    char c = Str.charAt(i);
    if (c < '0' || c > '9') break;
    ULong *= 10;
    ULong += (c - '0');
  }
  return ULong;
}



String leadNull(int digits) {                                   // Функция добавляет ведущий ноль
  String out = "";
  if (digits < 10)
    out += "0";
  return out + String(digits);
}


void testingsystem(int testing) {

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("t |");
  lcd.setCursor(0, 1);
  lcd.print("e |");
  lcd.setCursor(0, 2);
  lcd.print("s |");
  lcd.setCursor(0, 3);
  lcd.print("t |");
  lcd.setCursor(3, 0);
  lcd.print("Pump testing-OFF");
  lcd.setCursor(3, 1);
  lcd.print("Heat testing-OFF");
  lcd.setCursor(3, 2);
  lcd.print("Led testing-OFF");
  lcd.setCursor(3, 3);
  lcd.print("Fan testing-OFF");
  delay(1000);
  lcd.setCursor(16, 0);
  lcd.print("ON ");
  ON_Pump();
  delay(testing);
  //lcd.setCursor(16, 0);
  //lcd.print("OFF");
  OFF_Pump();
  delay(1000);
  lcd.setCursor(16, 1);
  lcd.print("ON ");
  ON_Heat();
  delay(testing);
  //lcd.setCursor(16, 1);
  //lcd.print("OFF");
  OFF_Heat();
  delay(1000);
  lcd.setCursor(15, 2);
  lcd.print("ON ");
  ON_Led();
  delay(testing);
  //lcd.setCursor(15, 2);
  //lcd.print("OFF");
  OFF_Led();
  delay(1000);
  lcd.setCursor(15, 3);
  lcd.print("ON ");
  ON_Fan();
  delay(testing);
  //lcd.setCursor(15, 3);
  //lcd.print("OFF");
  OFF_Fan();
  delay(1000);


}
void printserial() {
  Serial.print(" light_on = ");
  Serial.print(light_on);
  Serial.print(" heat_on = ");
  Serial.print(heat_on);
  Serial.print(" heat_off = ");
  Serial.print(heat_off);
  Serial.print(" fan_on = ");
  Serial.println(fan_on);
  Serial.print(" pump_on = ");
  Serial.print(pump_on);
  Serial.print(" f_pump = ");
  Serial.print(f_pump);
  Serial.print(" f_heat = ");
  Serial.println(f_heat);
  Serial.print(" f_led = ");
  Serial.print(f_led);
  Serial.print(" f_fan = ");
  Serial.print(f_fan);
  Serial.print(" water = ");
  Serial.print(water);
  Serial.print(" control = ");
  Serial.print(control);
  Serial.print(" delta_send = ");
  Serial.print(delta_send);
  Serial.print(" delta_loop = ");
  Serial.print(delta_loop);
  Serial.print(" sending = ");
  Serial.println(sending);



  Serial.print("\tMoisture_1 = ");
  Serial.print(Moisture_1);
  Serial.print("\tMoisture_2 = ");
  Serial.print(Moisture_2);
  Serial.print("\tLight = ");
  Serial.println(Light);
  Serial.print("\tTemp_in = ");
  Serial.print(Temp_in);
  Serial.print("\tHumidity_in = ");
  Serial.println(Humidity_in);
  Serial.print("\tTemp_out = ");
  Serial.print(Temp_out);
  Serial.print("\tHumidity_out = ");
  Serial.println(Humidity_out);
  Serial.print("\tLevel_water = ");
  Serial.println(Level_water);



}




void testloop() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("main program");
  lcd.setCursor(0, 1);
  lcd.print("timeloop = ");
  lcd.print(timeloop);
  lcd.setCursor(0, 2);
  lcd.print("timesend = ");
  lcd.println(timesend);
  Serial.print("Петля номер - timeloop = ");
  Serial.print(timeloop);
  Serial.print(" timesend = ");
  Serial.println(timesend);
  if (timeloop >= delta_loop) {
    timeloop = 0;
    lcd.setCursor(0, 3);
    lcd.print("Update loop");
    Serial.println("Обнуляем loop");
    //readSensors();
  }
  if (timesend >= delta_send) {
    timesend = 0;
    lcd.setCursor(0, 4);
    lcd.print("Update send");
    Serial.println("Обнуляем send");
    //sendSensors();
  }
}


void readSensors() {
  Wire.begin();
  ADS.begin();

  dht_in.begin();
  dht_out.begin();


  ADS.setGain(0);

  int16_t val_0 = ADS.readADC(0);
  int16_t val_1 = ADS.readADC(1);
  int16_t val_2 = ADS.readADC(2);
  int16_t val_3 = ADS.readADC(3);

  float f = ADS.toVoltage(1);  //  voltage factor

  Serial.print("\tAnalog0: "); Serial.print(val_0); Serial.print('\t'); Serial.println(val_0 * f, 3);
  Serial.print("\tAnalog1: "); Serial.print(val_1); Serial.print('\t'); Serial.println(val_1 * f, 3);
  Serial.print("\tAnalog2: "); Serial.print(val_2); Serial.print('\t'); Serial.println(val_2 * f, 3);
  Serial.print("\tAnalog3: "); Serial.print(val_3); Serial.print('\t'); Serial.println(val_3 * f, 3);
  Serial.println();

  Moisture_1 = 100 - val_1 * f * 100 / 5.05;
  Moisture_2 = 100 - val_2 * f * 100 / 5.05;
  Light = 100 - val_0 * f * 100 / 5.05;
  Temp_in = dht_in.readTemperature();
  Humidity_in = dht_in.readHumidity();
  if (Temp_in > 100) {
    Temp_in = 0;
    Humidity_in = 0;
  }
  Temp_out = dht_out.readTemperature();
  Humidity_out = dht_out.readHumidity();
  if (Temp_out > 100) {
    Temp_out = 0;
    Humidity_out = 0;
  }
  Level_water = val_3 * f * 100 / 5.05;;
}

void sendSensors() {
  if (client.connect("teplica.pythonanywhere.com", 80)) {
    // Если удаётся установить соединение с указанным хостом (Порт 443 для https)
    String url = "GET /add_sensors?";
    url += "token=" + token;
    url += "&t_in=";
    url += Temp_in;
    url += "&t_out=";
    url += Temp_out;
    url += "&h_in=";
    url += Humidity_in;
    url += "&h_out=";
    url += Humidity_out;
    url += "&mois1=";
    url += Moisture_1;
    url += "&mois2=";
    url += Moisture_2;
    url += "&water=";
    url += Level_water;
    url += "&light=";
    url += Light;
    url += "&pump=";
    url += pump;
    url += "&heat=";
    url += heat;
    url += "&led=";
    url += led;
    url += "&fan=";
    url += fan;
    url += " HTTP/1.1\r\nHost: teplica.pythonanywhere.com\r\nConnection: close\r\n\r\n";
    Serial.println(url);
    client.println(url); // Отправляем параметры запроса
    //delay(500);
    lcd.setCursor(15, 2);
    lcd.print("S");// Даём серверу время, чтобы обработать запрос

  }
}

void printDisplayParam() {

  lcd.setCursor(0, 3);
  lcd.print("t");
  //lcd.print("in");
  lcd.print(leadNull(Temp_in));
  lcd.print("C");
  lcd.print(leadNull(Humidity_in));
  lcd.print("%");
  lcd.print("/");
  lcd.print(leadNull(Temp_out));
  lcd.print("C");
  lcd.print(leadNull(Humidity_out));
  lcd.print("%-");
  //lcd.print("(");
  lcd.print(leadNull(heat_on));
  lcd.print("/");
  lcd.print(leadNull(heat_off));
  //lcd.print(")");
  //lcd.print(leadNull(Humidity_in));
  //lcd.print("/");
  //lcd.print(leadNull(Humidity_out));



  lcd.setCursor(0, 0);
  lcd.print("Led-");
  lcd.print(leadNull(Light));
  lcd.print("(");
  lcd.print(leadNull(light_on));
  lcd.print(")");
  lcd.setCursor(0, 1);
  lcd.print("Moi-");
  lcd.print(leadNull((Moisture_1 + Moisture_2) / 2));
  lcd.print("(");
  lcd.print(leadNull(pump_on));
  lcd.print(")");
  lcd.setCursor(0, 2);
  lcd.print("H2O-");
  lcd.print(leadNull(Level_water));
  lcd.print("(");
  lcd.print(leadNull(water));
  lcd.print(")");


  lcd.setCursor(16, 0);
  lcd.print("PHLF");
  lcd.setCursor(15, 1);
  if (control > 0) {
    lcd.print("M");
  } else {
    lcd.print("A");
  }
  lcd.print(f_pump);
  lcd.print(f_heat);
  lcd.print(f_led);
  lcd.print(f_fan);
  lcd.setCursor(16, 2);
  lcd.print(pump);
  lcd.print(heat);
  lcd.print(led);
  lcd.print(fan);
  lcd.setCursor(11, 0);
  lcd.print("     ");
  lcd.setCursor(11, 0);
  lcd.print(delta_send);
  lcd.setCursor(11, 1);

  lcd.print("    ");
  lcd.setCursor(11, 1);
  lcd.print(delta_loop);
  lcd.setCursor(11, 2);
  lcd.print("    ");
  lcd.setCursor(11, 2);
  lcd.print(sending);
  /*
    lcd.print("on=");
    lcd.print(heat_on);
    lcd.print("off=");
    lcd.print(heat_off);
    lcd.setCursor(0, 1);// переводим курсор в нужную позицию
    lcd.print("p=");
    lcd.print(pump_on);
    lcd.print(" p");
    lcd.print(pump);
    lcd.print("h");
    lcd.print(heat);
    lcd.print("l");
    lcd.print(led);
    lcd.print("f");
    lcd.print(fan);
  */
}

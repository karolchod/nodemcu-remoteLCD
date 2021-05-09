/**
 * Displays text sent over the serial port (e.g. from the Serial Monitor) on
 * an attached LCD.
 */
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <NTPClient.h>

#define WIFI_SSID "AAA"	//Please enter your wifi ssid
#define WIFI_PASS "AAA" //Please enter valid wifi password
#define UDP_PORT 4210	//Port used by device

WiFiUDP UDP;
char packet[255];

const long utcOffsetInSeconds = 3600;     //UTC+1, utc+0 = 0 (=utc*3600)
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int buzzer=14;	//pin used for buzzer
bool exitFromNTPCLOCK; //first time we need to act like we gone out from NTP loop, used also in scrolling text function
int packetSize;

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  lcd.begin();
  lcd.backlight();
  
  // Initialize the serial port at a speed of 9600 baud
  Serial.begin(115200);
  pinMode(buzzer, OUTPUT);//buzzer
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  
  // Connecting to WiFi...
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  // Loop while WiFi is not connected
  lcd.setCursor(0,0);
  lcd.print(WIFI_SSID);
  int conCount=0;
  while (WiFi.status() != WL_CONNECTED)
  {
    if(conCount==16){
      lcd.clear();
      conCount=0;
    }
    lcd.setCursor(conCount,1);
    lcd.print('.');
    digitalWrite(LED_BUILTIN, LOW);
    delay(200);
    Serial.print(".");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    conCount++;
  }
  lcd.clear();
  // Connected to WiFi
  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  lcd.setCursor(0,0);
  lcd.print(WiFi.localIP());
 
  // Begin listening to UDP port
  UDP.begin(UDP_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(UDP_PORT);
  lcd.setCursor(0,1);
  lcd.print(UDP_PORT);
  for(int i=0;i<10;i++){
    lcd.setCursor(6+i,1);
    lcd.print('.');
    delay(500);
  }
  lcd.clear(); 
  exitFromNTPCLOCK=0; //first time we need to act like we gone out from NTP loop
  packetSize=0;

//------------after connection, it starts showing NTP clock
  //lcd.clear();
  timeClient.begin();
  while(1){
      packetSize=UDP.parsePacket();
      if(packetSize)
        break;
      timeClient.update();
      String czas=timeClient.getFormattedTime();
      //Serial.println(czas);
      lcd.setCursor(0,0);
      lcd.print("    "+czas);
      delay(300);
    }
    timeClient.end();  
    lcd.clear();
    exitFromNTPCLOCK=1;
//---------------------
// any packet 
}

void loop()
{

  // If packet received...
  if(exitFromNTPCLOCK==1){
    exitFromNTPCLOCK=0;
  }else{
    packetSize = UDP.parsePacket();
  }
  
  //if (Serial.available() > 0) {
  if (packetSize) {
    Serial.print("Received packet! Size: ");
    Serial.println(packetSize);
    int len = UDP.read(packet, 255);
    if (len > 0)
    {
      packet[len] = '\0';
    }
    Serial.print("Packet received: ");
    Serial.println(packet);
    
    String text = packet;// s1 is String type variable.
    //Serial.print("Received Data => ");
    //Serial.println(text);//display same received Data back in serial monitor.
    //delay(100);
    if (text!="") {
      int wiersz=0;
      //text[text.length()-1]='\0';
      //lcd.clear();
      //lcd.print(text);
      if(text[0]=='0'||text[0]=='1'||text[0]=='2'||text[0]=='3'){
        if(text[0]=='0')
          wiersz=0;
        else if (text[0]=='1')
          wiersz=1;
        else if (text[0]=='2')
          wiersz=2;
        else if (text[0]=='3')
          wiersz=3;
        clearLCDLine(wiersz%2);
        lcd.setCursor(0, wiersz%2);
        if (wiersz==0||wiersz==1||text.length()<=17){
          //if(text.length()<=17){
            if(text[0]=='2')
              wiersz=0;
            else if (text[0]=='3')
              wiersz=1;
            for(int i=1;i<text.length();i++){ //for use with python, use  i<text.length()-1 for serial monitor input (debugging)
              if(i<=16){
                lcd.setCursor(i-1,wiersz);
                lcd.print(text[i]);
              }
            }
          }
        else{   //when lane type is 2 lub 3 and more than 16 characters
            
            UpdateLCDDisplay(text,750);// text sliding, with velocity in ms
        }
      } 
      //else
      //else if(text[0]=='3'){  //TODO: what if both lanes are more than 16 characters?
      //  clearLCDLine(0);
      //  clearLCDLine(1);
      //}
      else if(text[0]=='9'){//clear screen
        clearLCDLine(0);
        clearLCDLine(1);
      }
      else if(text[0]=='7'){//backlight on
        lcd.backlight();
      }
      else if(text[0]=='8'){//backlight off
        lcd.noBacklight();
      }
      else if(text[0]=='6'){ //beep with buzzer
        int ilosc=0; //number of double beeps
        if(text[1]=='1')
          ilosc=1;
        else if (text[1]=='2')
          ilosc=2;
        else if (text[1]=='3')
          ilosc=3;
        else if (text[1]=='4')
          ilosc=4;
         else if (text[1]=='5')
          ilosc=4;
         else if (text[1]=='6')
          ilosc=6;
         else if (text[1]=='7')
          ilosc=7;
         else if (text[1]=='8')
          ilosc=8;
         else if (text[1]=='9')
          ilosc=9;
         
        if(ilosc>0&&ilosc<=9){
          for(int i=0;i<ilosc;i++){
            tone(buzzer, 4000); //generate sound 4000Hz at buzzer pin  
            delay(100);  
            noTone(buzzer);
            delay(100);
            tone(buzzer, 4000); //generate sound 4000Hz at buzzer pin  
            delay(100);  
            noTone(buzzer);
            delay(700);
          }
        }
      }
      else if (text[0]=='5'){ //show online clock with time live from NTP server
        lcd.clear();
        timeClient.begin();
        while(1){
          packetSize=UDP.parsePacket();
          if(packetSize)
            break;
          timeClient.update();
          String czas=timeClient.getFormattedTime();
          //Serial.println(czas);
          lcd.setCursor(0,0);
          lcd.print("    "+czas);
          delay(300);
        }
        timeClient.end();  
        lcd.clear();
        exitFromNTPCLOCK=1;
      }
      //else
      // Serial.println("wrong lane type"); 
    }
  }
}

void clearLCDLine(int line)
{               
  lcd.setCursor(0,line);
  for(int n = 0; n < 16; n++) // 20 indicates symbols in line. For 2x16 LCD write - 16
  {
    lcd.print(" ");
  }
}

void UpdateLCDDisplay(String LargeTextRaw,int speed){
  //text conversion to correct form
  String LargeText=LargeTextRaw.substring(1);
  LargeText=LargeText+" -  ";
  int iLineNumber=0;
  int iCursor = 0;
  if(LargeTextRaw[0]=='2')
    iLineNumber=0;
  else
    iLineNumber=1;

while(1){  
  
  packetSize=UDP.parsePacket();
  if(packetSize)
    break;
  
  int iLenOfLargeText = LargeText.length();     // Calculate lenght of string.
  if (iCursor == (iLenOfLargeText - 1) )        // Reset variable for rollover effect.
  {
    iCursor = 0;
  }
  //lcd.clear();
  lcd.setCursor(0,iLineNumber);
  
  if(iCursor < iLenOfLargeText - 16)            // This loop exicuted for normal 16 characters.
  {
    for (int iChar = iCursor; iChar < iCursor + 16 ; iChar++)
    {
      lcd.print(LargeText[iChar]);
    }
  }
  else
  {
    for (int iChar = iCursor; iChar < (iLenOfLargeText - 1) ; iChar++)  //  This code takes care of printing charecters of current string.
    {
      lcd.print(LargeText[iChar]);
    }
    for (int iChar = 0; iChar <= 16 - (iLenOfLargeText - iCursor); iChar++) //  Reamining charecter will be printed by this loop.
    {
      lcd.print(LargeText[iChar]);   
    }
  }
  iCursor++;
  delay(speed); 
}
exitFromNTPCLOCK=1;
}

#include <M5StickC.h>

#define VIB_MOTOR_PIN 0 // Changed from GPIO 36 (input-only) to GPIO 0 (safe for output)
#define BUZZER_PIN 26   // Buzzer pin

int currentBPM = 0; // Stores received BPM

void showInfo(const char *beatLabel)
{
  M5.Lcd.setCursor(10, 10);
  M5.Lcd.setTextColor(WHITE, BLACK);
  M5.Lcd.setTextSize(2);
  M5.Lcd.printf("BPM: %d\n", currentBPM);

  M5.Lcd.setCursor(10, 40);
  M5.Lcd.printf("Beat: %s", beatLabel);
}

void setup()
{
  M5.begin();
  M5.Lcd.setRotation(3);
  M5.Lcd.fillScreen(BLACK);
  Serial.begin(115200);

  pinMode(VIB_MOTOR_PIN, OUTPUT);
  ledcAttachPin(BUZZER_PIN, 0); // Buzzer PWM
  ledcSetup(0, 2000, 8);        // 2kHz, 8-bit resolution
}

void loop()
{
  if (Serial.available())
  {
    if (Serial.peek() == '#')
    {
      Serial.read(); // Consume '#'
      currentBPM = Serial.parseInt();
      M5.Lcd.fillScreen(BLACK);
      showInfo("Waiting...");
      Serial.printf("Updated BPM: %d\n", currentBPM);
      return;
    }

    char beatType = Serial.read();

    if (beatType == 'S')
    {
      M5.Lcd.fillScreen(RED);
      showInfo("SAM");
      Serial.printf("Beat: SAM | BPM: %d\n", currentBPM);
      ledcWrite(0, 200);
      delay(150);
      ledcWrite(0, 0);
    }
    else if (beatType == 'K')
    {
      M5.Lcd.fillScreen(BLUE);
      showInfo("KHALI");
      Serial.printf("Beat: KHALI | BPM: %d\n", currentBPM);
      ledcWrite(0, 80);
      delay(80);
      ledcWrite(0, 0);
    }
    else if (beatType == 'B')
    {
      M5.Lcd.fillScreen(ORANGE);
      showInfo("THALI");
      Serial.printf("Beat: THALI | BPM: %d\n", currentBPM);
      ledcWrite(0, 120);
      delay(50);
      ledcWrite(0, 0);
    }
  }
}
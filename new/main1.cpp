#include <M5StickC.h>

#define BUZZER_PIN 26

int bpm = 120;
int timeSignature = 4;
bool useMetronome = false;
bool modeSelected = false;

void showBPM()
{
    M5.Lcd.setCursor(10, 10);
    M5.Lcd.setTextColor(WHITE, BLACK);
    M5.Lcd.setTextSize(2);
    M5.Lcd.print("BPM: ");
    M5.Lcd.print(bpm);
}

void playBeat(int beatNum)
{
    if (beatNum == 1)
    {
        M5.Lcd.fillScreen(RED);
        ledcWrite(0, 200);
    }
    else
    {
        M5.Lcd.fillScreen(ORANGE);
        ledcWrite(0, 100);
    }
    showBPM();
    delay(100);
    ledcWrite(0, 0);
}

void setup()
{
    M5.begin();
    M5.Lcd.setRotation(3);
    M5.Lcd.fillScreen(BLACK);
    Serial.begin(115200);
    ledcAttachPin(BUZZER_PIN, 0);
    ledcSetup(0, 2000, 8);

    M5.Lcd.setTextSize(2);
    M5.Lcd.setCursor(10, 30);
    M5.Lcd.println("A: Song Beat");
    M5.Lcd.setCursor(10, 50);
    M5.Lcd.println("B: Metronome");
}

void loop()
{
    M5.update();

    if (!modeSelected)
    {
        if (M5.BtnA.wasPressed())
        {
            useMetronome = false;
            modeSelected = true;
            M5.Lcd.fillScreen(BLACK);
        }
        if (M5.BtnB.wasPressed())
        {
            useMetronome = true;
            modeSelected = true;
            M5.Lcd.fillScreen(BLACK);

            Serial.println("Enter BPM:");
            while (Serial.available() == 0)
                delay(100);
            bpm = Serial.parseInt();

            Serial.println("Enter Time Signature:");
            while (Serial.available() == 0)
                delay(100);
            timeSignature = Serial.parseInt();
        }
    }

    if (useMetronome)
    {
        float beatInterval = 60000.0 / bpm;
        int beatCount = 1;

        playBeat(beatCount);
        beatCount = (beatCount % timeSignature) + 1;
        delay(beatInterval - 100);
    }
    else
    {
        if (Serial.available())
        {
            if (Serial.peek() == '#')
            {
                Serial.read();
                bpm = Serial.parseInt();
                M5.Lcd.fillScreen(BLACK);
                showBPM();
                return;
            }

            char beatType = Serial.read();

            if (beatType == 'S')
            {
                M5.Lcd.fillScreen(RED);
                showBPM();
                ledcWrite(0, 200);
                delay(150);
                ledcWrite(0, 0);
            }
            else if (beatType == 'K')
            {
                M5.Lcd.fillScreen(BLUE);
                showBPM();
                ledcWrite(0, 80);
                delay(80);
                ledcWrite(0, 0);
            }
            else if (beatType == 'B')
            {
                M5.Lcd.fillScreen(ORANGE);
                showBPM();
                ledcWrite(0, 120);
                delay(50);
                ledcWrite(0, 0);
            }
        }
    }
}

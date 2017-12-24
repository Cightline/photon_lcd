// This #include statement was automatically added by the Particle IDE.
#include <ArduinoJson.h>

// This #include statement was automatically added by the Particle IDE.
#include <adafruit-serial-rgb-lcd.h>

// This #include statement was automatically added by the Particle IDE.
// https://github.com/colinodell/AdafruitSerialRGBLCD
#include <adafruit-serial-rgb-lcd.h>



SerialRGBLCD lcd;



int data_is_set = -1;
int d = 5000;

String temp_f; 
String weather;
bool   alert_is_current = false;
String alert_message = "none";
String l_one = "";
String l_two = "";

String messages[5]; 
String titles[5];
bool   alerts[5];
int    last_used_index = 0;

// https://www.hackster.io/TheReddest/photon-powered-lcd-forecast-and-time-display-32bab4
// https://github.com/menan/SparkJson/blob/master/firmware/examples/JsonParserExample/JsonParserExample.ino
int update(String arg)
{
    display_message("updating...", "");
    data_is_set = 0;
    
    StaticJsonBuffer<200> jb;
    JsonObject& text        = jb.parseObject((char*)arg.c_str());
    //JsonObject& text = jb.parseObject(arg);
    
    String new_message = "n/a msg";
    String new_title   = "n/a title";
    bool   is_alert    = false;
    String a           = "0";
    
            
    if (!text.success())
    {
         new_message = "can't parse";
         new_title   = "ERROR";
    }
    
    
    else
    {
         new_message      = text["message"].asString();
         new_title        = text["title"].asString();
         a                = text["is_alert"].asString();
        
        if (a == "1")
        {
            is_alert = true;
        }
    }
    
    
    // Make the index roll over to 0 again. 
    if (last_used_index == 5)
    {
        last_used_index = 0;
    }

    messages[last_used_index] = new_message;
    titles[last_used_index]   = new_title;
    alerts[last_used_index]   = is_alert;
    last_used_index           = last_used_index + 1;
    data_is_set               = 1;
    
    return data_is_set;
}



void display_message(String line_one, String line_two)
{
    if (line_one != l_one or line_two != l_two)
    {
        lcd.clear();
        delay(200);
        lcd.home();
        lcd.print(line_one);
        lcd.setCursor(1,2);
        lcd.print(line_two);
        l_one = line_one;
        l_two = line_two;
    }
    
}

void set_normal_color()
{
    lcd.setBacklightColor(255, 51, 51);
}

void set_alert_color()
{
    lcd.setBacklightColor(255, 0, 0);
}


void setup() 
{
    // Photon's RGB
    //RGB.control(true);
    //RGB.brightness(0);
    //RGB.color(0, 0, 0);
    //delay(1000);
    
    
    lcd.begin(9600);
    lcd.setContrast(220);
    lcd.setBrightness(220);
    set_normal_color();
    lcd.setAutoscroll(false);
    Particle.function("update", update);
    

}

void loop() 
{
    if (WiFi.ready() != true)
    {
        display_message("no connection", "");
    }
    
    
    
    if (data_is_set != 1)
    {
        display_message("waiting...", "");
    }
    
    
    else
    {
        for (int i = 0; i < 5; i++)
        {
            if (titles[i].length() > 0 && messages[i].length() > 0)
            {
                if (alerts[i] == true)
                {
                    set_alert_color();
                    display_message(titles[i], messages[i]);
                    delay(d);
                    
                    
                }
                else
                {
                    set_normal_color();
                    display_message(titles[i], messages[i]);
                    delay(d);
                }
            
            }
            
        }
        
        
 
    }
    
   
}

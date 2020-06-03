#include <Servo.h>
#include <SPI.h>

Servo IndexFinger;
Servo MiddleFinger;
Servo RingFinger;
Servo Pinky;
Servo Thumb;
Servo Wrist;

static int index;

static int ThumbPrev = 90;
static int RingPrev = 180;

static int PinkyPrev = 180;
static int IndexPrev = 180;
static int MiddlePrev = 90;


void fingercalc(int);
void PinkyMove(int);
void RingMove(int);
void MiddleMove(int);
void IndexMove(int);
void ThumbMove(int);

void setup (void)
{  
  Serial.begin(9600); 
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  SPI.attachInterrupt();
  
  IndexFinger.attach(9);
  MiddleFinger.attach(11);
  RingFinger.attach(3);
  Pinky.attach(5);
  Thumb.attach(6);
  //Wrist.attach(10);
  
  Pinky.write(180);
  MiddleFinger.write(90);
  RingFinger.write(180);
  IndexFinger.write(180);
  Thumb.write(90);
}

ISR (SPI_STC_vect)
{
  byte c = SPDR;
  fingercalc(c);
}  

// main loop - do nothing, wait for interrupt
void loop (void)
{ 

}

void fingercalc(int val)
{
  int val2 = val>>5;
  int val3;
  Serial.println(" ");
  Serial.print("SPI Raw ");
  Serial.println(val);
  Serial.print("ID ");
  Serial.print(val2);
  Serial.print(" ");
  
  switch(val2)
  {
    int y;
    case 0:
        val3 = val;
        if((val3>=0)&&(val3<=8))
        {
           y = 90;
           Pinky.write(y);
           Serial.print("PinkyAngle ");
           Serial.print(y);
           PinkyPrev = y;
        }
        if((val3>8)&&(val3<=12))
        {
           y = 100;
           Pinky.write(y);
           Serial.print("PinkyAngle ");
           Serial.print(y);
           PinkyPrev = y;
        }
        if((val3>12)&&(val3<=18))
        {
           y = 120;
           Pinky.write(y);
           Serial.print("PinkyAngle ");
           Serial.print(y);
           PinkyPrev = y;
        } 
        if((val3>18)&&(val3<=22))
        {
           y = 140;
           Pinky.write(y);
           Serial.print("PinkyAngle ");
           Serial.print(y);
           PinkyPrev = y;
        }
        if((val3>22)&&(val3<=25))
        {
           y = 160;
           Pinky.write(y);
           Serial.print("PinkyAngle ");
           Serial.print(y);
           PinkyPrev = y;
        }
        if((val3>25)&&(val3<=31))
        {
           y = 180;
           Pinky.write(y);
           Serial.print("PinkyAngle ");
           Serial.print(y);
           PinkyPrev = y;
        } 
        else
          Pinky.write(PinkyPrev);
        break;
        
    case 1:
        val3 = val - 32;
        if((val3>=0)&&(val3<=8))
        {
           y = 90;
           RingFinger.write(y);
           Serial.print("RingFinger ");
           Serial.println(y);
           RingPrev = y;
        }
        if((val3>8)&&(val3<=12))
        {
           y = 100;
           RingFinger.write(y);
           Serial.print("RingFinger ");
           Serial.println(y);
           RingPrev = y;
        }
        if((val3>12)&&(val3<=18))
        {
           y = 120;
           RingFinger.write(y);
           Serial.print("RingFinger ");
           Serial.println(y);
           RingPrev = y;
        } 
        if((val3>18)&&(val3<=22))
        {
           y = 140;
           RingFinger.write(y);
           Serial.print("RingFinger ");
           Serial.println(y);
           RingPrev = y;
        }
        if((val3>22)&&(val3<=25))
        {
           y = 160;
           RingFinger.write(y);
           Serial.print("RingFinger ");
           Serial.println(y);
           RingPrev = y;
        }
        if((val3>25)&&(val3<=31))
        {
           y = 180;
           RingFinger.write(y);
           Serial.print("RingFinger ");
           Serial.println(y);
           RingPrev = y;
        } 
        else
          RingFinger.write(RingPrev);
        break;
    
    case 2:
        val3 = val - 64;
        if((val3>=0)&&(val3<=8))
        {
           y = 90;
           MiddleFinger.write(y);
           Serial.print("MiddleFinger ");
           Serial.println(y);
           MiddlePrev = y;
        }
        if((val3>8)&&(val3<=12))
        {
           y = 100;
           MiddleFinger.write(y);
           Serial.print("MiddleFinger ");
           Serial.println(y);
           MiddlePrev = y;
        }
        if((val3>12)&&(val3<=18))
        {
           y = 120;
           MiddleFinger.write(y);
           Serial.print("MiddleFinger ");
           Serial.println(y);
           MiddlePrev = y;
        } 
        if((val3>18)&&(val3<=22))
        {
           y = 140;
           MiddleFinger.write(y);
           Serial.print("MiddleFinger ");
           Serial.println(y);
           MiddlePrev = y;
        }
        if((val3>22)&&(val3<=25))
        {
           y = 160;
           MiddleFinger.write(y);
           Serial.print("MiddleFinger ");
           Serial.println(y);
           MiddlePrev = y;
        }
        if((val3>25)&&(val3<=31))
        {
           y = 180;
           MiddleFinger.write(y);
           Serial.print("MiddleFinger ");
           Serial.println(y);
           MiddlePrev = y;
        } 
        else
          MiddleFinger.write(MiddlePrev);
        break;
    
    case 4:
        val3 = val - 128;
        if((val3>=0)&&(val3<=8))
        {
           y = 90;
           IndexFinger.write(y);
           Serial.print("IndexFinger ");
           Serial.println(y);
           IndexPrev = y;
        }
        if((val3>8)&&(val3<=12))
        {
           y = 100;
           IndexFinger.write(y);
           Serial.print("IndexFinger ");
           Serial.println(y);
           IndexPrev = y;
        }
        if((val3>12)&&(val3<=18))
        {
           y = 120;
           IndexFinger.write(y);
           Serial.print("IndexFinger ");
           Serial.println(y);
           IndexPrev = y;
        } 
        if((val3>18)&&(val3<=22))
        {
           y = 140;
           IndexFinger.write(y);
           Serial.print("IndexFinger ");
           Serial.println(y);
           IndexPrev = y;
        }
        if((val3>22)&&(val3<=25))
        {
           y = 160;
           IndexFinger.write(y);
           Serial.print("IndexFinger ");
           Serial.println(y);
           IndexPrev = y;
        }
        if((val3>25)&&(val3<=31))
        {
           y = 180;
           IndexFinger.write(y);
           Serial.print("IndexFinger ");
           Serial.println(y);
           IndexPrev = y;
        } 
        else
          IndexFinger.write(IndexPrev);
        break;

    case 7:
        val3 = val - 224;
        if((val3>=0)&&(val3<=8))
        {
           y = 90;
           Thumb.write(y);
           Serial.print("Thumb ");
           Serial.println(y);
           ThumbPrev = y;
        }
        if((val3>8)&&(val3<=12))
        {
           y = 100;
           Thumb.write(y);
           Serial.print("Thumb ");
           Serial.println(y);
           ThumbPrev = y;
        }
        if((val3>12)&&(val3<=18))
        {
           y = 120;
           Thumb.write(y);
           Serial.print("Thumb ");
           Serial.println(y);
           ThumbPrev = y;
        } 
        if((val3>18)&&(val3<=22))
        {
           y = 140;
           Thumb.write(y);
           Serial.print("Thumb ");
           Serial.println(y);
           ThumbPrev = y;
        }
        if((val3>22)&&(val3<=25))
        {
           y = 160;
           Thumb.write(y);
           Serial.print("Thumb ");
           Serial.println(y);
           ThumbPrev = y;
        }
        if((val3>25)&&(val3<=31))
        {
           y = 180;
           Thumb.write(y);
           Serial.print("Thumb ");
           Serial.println(y);
           ThumbPrev = y;
        } 
        else
          Thumb.write(ThumbPrev);
        break;


  }
}

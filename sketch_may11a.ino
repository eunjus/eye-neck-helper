#include <Servo.h>
 
Servo servo1;  //servo 객체를 만들어준다 (최대8개 생성 가능)
Servo servo2;
Servo servo3; 
Servo servo4;

int pos1 = 105;
int pos2 = 105;    
int pos3 = 85;    
int pos4 = 90;   // servo motor 회전각도 변수 선언

void setup()
{
  Serial.begin(9600);
  servo1.attach(12);  //servo motor 연결핀 설정(디지털 12번핀)
  servo2.attach(10);  //servo motor 연결핀 설정(디지털 10번핀)
  servo3.attach(13);  //servo motor 연결핀 설정(디지털 13번핀)
  servo4.attach(11);  //servo motor 연결핀 설정(디지털 11번핀)

}
  
void loop()
{
  
  while(Serial.available()){
  int sig=Serial.read();
  
  switch(sig){
  case'1':               
    servo1.write(pos1++);//pos 변수의 각도만큼 움직여라 (1도씩증가)
    servo2.write(pos2++); 
    sig=NULL;
    break;     
  case'2':
    servo1.write(pos1--);//pos 변수의 각도만큼 움직여라 (1도씩감소)
    servo2.write(pos2--);  
    sig=NULL;
    break;
  case'3':
    servo3.write(pos3--);//pos 변수의 각도만큼 움직여라 (1도씩증가)
    servo4.write(pos4--); 
    sig=NULL;
    break;     
  case'4':
    servo3.write(pos3++);//pos 변수의 각도만큼 움직여라 (1도씩감소)
    servo4.write(pos4++); 
    sig=NULL;
    break;     
   case'5':
    sig =NULL;
    break;
  }
 }
}

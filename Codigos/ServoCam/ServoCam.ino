#include <Servo.h>
#include <SoftwareSerial.h>

//Declaramos el servo
Servo servo;

//Declaramos las variables 

char dato; //el dato que recime/manda el puerto serial 
int angulo = 90; //El angulo del servomotor 

void setup() {
  Serial.begin(9600);//Velocidad de comunicacion del puerto COM#
  Serial.setTimeout(5);//Cada cuanto timepo recibe datos/manda datos (5ms)
  servo.attach(7);//Pin en el que se conecta el servo al arduino
  servo.write(angulo);// el servo siempre se inicia en el centro=90 grados
}

void loop() {
  while(Serial.available()){
    dato = Serial.read();
    delay(10);
    Serial.println(dato);
    switch(dato){
      case 'd':
      //Gira servo hacia la derecha
      angulo = angulo + 2;
      servo.write(angulo);
      break;
      
      case 'i':
      //Gira servo hacia la izquierda
      angulo = angulo - 2;
      servo.write(angulo);
      break;
      
      case 'p':
      //Parar el servo
      angulo = angulo;
      servo.write(angulo);
      break;
      }
   }
 }
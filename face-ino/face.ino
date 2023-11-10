#include <LiquidCrystal.h>

LiquidCrystal lcd(2,3,4,5,6,7); // Conexiones de los pines al LCD
int valor_dato = 0;

void setup() {
  lcd.begin(16, 2); // Inicializa el LCD con 16 columnas y 2 filas
  lcd.clear();      // Limpia la pantalla
  Serial.begin(9600); // Inicializa la comunicación serial
}

void loop() {
  if (Serial.available()) {
    valor_dato = Serial.read();
    if (valor_dato == '1')
    {
      lcd.setCursor(0,0);
      lcd.clear();
      lcd.print("PERMITIR");
    }
    else if (valor_dato == '0')
    {
      lcd.setCursor(0,0);
      lcd.print("NO PERMITIR");
    }
  }
}



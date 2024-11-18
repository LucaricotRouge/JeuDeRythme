const int buttonPin = 7; // Pin auquel le bouton est connecté
int buttonState = 0;
const int ledPerfect = 10;
const int ledGood = 11;
const int ledMiss = 12;

void setup() {
  Serial.begin(9600); // Initialiser la communication série à 9600 bps
  pinMode(buttonPin, INPUT_PULLUP); // Configurer le pin comme entrée avec pull-up
  pinMode(ledPerfect, OUTPUT);
  pinMode(ledGood, OUTPUT);
  pinMode(ledMiss, OUTPUT);
}

void loop() {
  buttonState = digitalRead(buttonPin);
  
  // Vérifier si le bouton est appuyé (LOW signifie appuyé avec INPUT_PULLUP)
  if (buttonState == LOW) {
    Serial.println("BUTTON_PRESSED"); // Envoyer un message à Python
    delay(200); // Anti-rebond pour éviter les lectures multiples
  }
  // Vérifier s'il y a des données reçues depuis le port série
  if (Serial.available() > 0) {
    String result = Serial.readStringUntil('\n');

    // Éteindre toutes les LED avant de gérer le nouveau résultat
    digitalWrite(ledPerfect, LOW);
    digitalWrite(ledGood, LOW);
    digitalWrite(ledMiss, LOW);

    if (result == "Perfect") {
      digitalWrite(ledPerfect, HIGH); // Allumer la LED verte
    } else if (result == "Good") {
      digitalWrite(ledGood, HIGH);    // Allumer la LED jaune
    } else if (result == "Miss") {
      digitalWrite(ledMiss, HIGH);    // Allumer la LED rouge
    }
  }
}



int buzzer = 8;
int state = 0;  // 0 = stop, 1 = sleepy, 2 = yawn

void setup() {
    pinMode(buzzer, OUTPUT);
    Serial.begin(9600);  // Initialize the serial communication
}

void loop() {
    if (Serial.available()) {
        String input = Serial.readString();  // Read the input from the serial monitor
        input.trim();                        // Remove leading and trailing whitespaces

        if (input.equals("sleepy")) {
            state = 1;  // Set state to play tones
        } else if (input.equals("yawn")) {
            // Additional behavior for "yawn" input
            state = 2;  // Set state to play tones
        } else if (input.equals("stop")) {
            state = 0;  // Set state to stop playing tones
        }
    }

    if (state == 0) {
        noTone(buzzer);  // Stop the sound
    }

    else if (state == 1) {
        tone(buzzer, 500);
        delay(1000);
        tone(buzzer, 1000);
        delay(1000);
    } else if (state == 2) {
        tone(buzzer, 100);
        delay(1000);
        tone(buzzer, 200);
        delay(1000);
        noTone(buzzer);
        delay(3000);
    }
}
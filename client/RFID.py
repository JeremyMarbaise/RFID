import serial

# Configure the serial port
ser = serial.Serial('COM10', 9600)  # Replace 'COM3' with your Arduino's port

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(line)  # Print the received message
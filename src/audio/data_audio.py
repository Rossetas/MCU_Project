# bibliotecas
import serial
import time
import csv
import numpy as np
from scipy.io.wavfile import write

# config
PORT = '/dev/ttyACM0'
BAUDRATE = 9600
DURATION_SECONDS = 3
SAMPLERATE = 16000

# inputs
class_label = input("Nombre de la clase (ej: ladrido): ")
num_samples = int(input("¿Cuantas muestras a grabar?: "))

# serial
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Conectado a {PORT}")
    time.sleep(2)
except Exception as e:
    print("Error al conectar:", e)
    exit()

for sample_num in range(1, num_samples + 1):
    input(f"\nPresiona ENTER para grabar muestra {sample_num}/{num_samples}...")

    print("Grabando...")
    samples = []
    start_time = time.time()

    while time.time() - start_time < DURATION_SECONDS:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                value = int(line)
                samples.append(value)
        except:
            continue

    wav_filename = f"{class_label}_{sample_num:02d}.wav"
    csv_filename = f"{class_label}_{sample_num:02d}.csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for s in samples:
            writer.writerow([s])

    samples_np = np.array(samples, dtype=np.int16)
    write(wav_filename, SAMPLERATE, samples_np)

    print(f"Muestra {sample_num} guardada: {wav_filename}, {csv_filename}")

ser.close()
print("\nGrabacion completa.")



# bibliotecas
import serial
import time
import csv
import numpy as np
from scipy.io.wavfile import write
import os

# config
PORT = '/dev/ttyACM0'
BAUDRATE = 230400
DURATION_SECONDS = 4
SAMPLERATE = 16000
TARGET_SAMPLES = SAMPLERATE * DURATION_SECONDS
GAIN = 2  # ganancia

def suavizar(signal, ventana=9):
    return np.convolve(signal, np.ones(ventana)/ventana, mode='same')

# entrada de clase
class_label = input("Nombre de la clase (ej: ladrido): ").strip().lower()
num_samples = int(input("¿Cuantas muestras a grabar?: "))

# directorio para guardar
base_dir = "data"
class_dir = os.path.join(base_dir, class_label)
os.makedirs(class_dir, exist_ok=True)

# abrir puerto serial
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Conectado a {PORT} a {BAUDRATE} baudios.")
    time.sleep(2)
except Exception as e:
    print("Error al conectar:", e)
    exit()

# grabacion por muestra
for sample_num in range(1, num_samples + 1):
    input(f"\nPresiona ENTER para grabar muestra {sample_num}/{num_samples} de '{class_label}'...")

    print("-> Grabando...")
    samples = []

    while len(samples) < TARGET_SAMPLES:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                value = int(line)
                samples.append(value)
        except:
            continue

    print(f"{len(samples)} muestras capturadas.")

    # nombres de archivo
    wav_filename = os.path.join(class_dir, f"{class_label}_{sample_num:02d}.wav")
    csv_filename = os.path.join(class_dir, f"{class_label}_{sample_num:02d}.csv")

    # guardar CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for s in samples:
            writer.writerow([s])

    # procesar y guardar WAV
    samples_np = np.array(samples, dtype=np.int16)
    samples_np = suavizar(samples_np).astype(np.int16)
    samples_np = np.clip(samples_np * GAIN, -32768, 32767)
    write(wav_filename, SAMPLERATE, samples_np)

    print(f"Muestra {sample_num} guardada: {os.path.basename(wav_filename)}")

# cerrar puerto serial
ser.close()
print("\nGrabacion finalizada.")



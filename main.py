import time
import codebug
import random
import pyaudio
import numpy as np


def generate_random_number(min, max):
    return random.randint(min, max)


def generate_random_numbers(pcs, min=0, max=5):
    return [generate_random_number(min, max) for _ in range(pcs)]


def get_bar_height(number):
    bar_height = 0
    for _ in range(number):
        bar_height <<= 1
        bar_height |= 1
    return bar_height


def get_bars(numbers):
    return [mirror_byte(get_bar_height(number), 5) for number in numbers]


def mirror_byte(number, bits):
    mirrored_number = 0
    for _ in range(8):
        mirrored_number <<= 1
        mirrored_number |= number & 0x01
        number >>= 1
    return mirrored_number >> (8 - bits)


def append_to_buffer(buffer, size_of_buffer, value):
    if len(buffer) < size_of_buffer:
        buffer.append(value)
    else:
        buffer = buffer[1:]
        buffer.append(value)
    return buffer


def open_mic_stream(rate, chunk):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    return audio, stream


def close_mic_stream(audio, stream):
    stream.stop_stream()
    stream.close()
    audio.terminate()


def print_terminal_visualization(value):
    if value == 0:
        print('.')
    else:
        print('#' * value)


def main():
    CHUNK = 2**11
    RATE = 44100
    
    values = []
    size_of_numbers = 10

    audio, stream = open_mic_stream(RATE, CHUNK)
    code_bug = codebug.CodeBug()
    try:
        while True:
            code_bug.clear_screen()
            
            data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
            peak = np.average(np.abs(data))*2
            value = int(20 * peak / 2**16)
            
            values = append_to_buffer(values, size_of_numbers, value)
            bars = get_bars(values)[:5]
            
            print_terminal_visualization(value)
            code_bug.set_screen(bars)
    except KeyboardInterrupt:
        pass
    finally:
        close_mic_stream(audio, stream)

    



if __name__ == "__main__":
    main()
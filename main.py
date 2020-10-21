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


def main():
    

    CHUNK = 2**11
    RATE = 44100

    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                frames_per_buffer=CHUNK)



    numbers = []
    size_of_numbers = 10

    try:
        while True:
            code_bug = codebug.CodeBug()
            code_bug.clear_screen()
            
            random_number = generate_random_number(0, 5)
            numbers = append_to_buffer(numbers, size_of_numbers, random_number)
            print(numbers)

            for i in range(int(10*44100/1024)): #go for a few seconds
                data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
                peak=np.average(np.abs(data))*2
                bars="#"*int(50*peak/2**16)
                print("%04d %05d %s"%(i,peak,bars))

            bars = get_bars(numbers)[:5]
            print(bars)
            
            code_bug.set_screen(bars)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


    



if __name__ == "__main__":
    main()
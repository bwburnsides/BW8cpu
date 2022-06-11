from pprint import pprint

# Read raw file
with open("notes.txt") as f:
    notes = [line.strip().split() for line in f.readlines()]

notes = {line[0]: float(line[1]) for line in notes}

f_width = 11
div = 8

for crystal in sorted([1843.20, 6144, 1000, 524.288, 500, 1544]):
    print(f"Reference Crystal {crystal} kHz")
    crystal *= 1000
    frequencies = []
    for b in range(1, 2**f_width):
        frequencies.append((crystal / div) / b)

    print("Audible frequencies: ", sum(f < 20_000 for f in frequencies))

    notes_deltas = {k: min(abs(v - f) for f in frequencies) for k, v in notes.items()}

    print("Largest note deviation: ", max(notes_deltas.values()))
    print("Smallest note deviation: ", min(notes_deltas.values()))
    print("Highest frequency: ", max(frequencies))
    print("Lowest frequency: ", min(frequencies))
    print()

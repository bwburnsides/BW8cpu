def parallel_resistance(*resistances: float) -> float:
    return 1 / sum(1 / res for res in resistances)


def voltage_div_get_r1(v0: float, v1: float, r2: float) -> float:
    return (r2 * (v0 - v1)) / v1


ans = parallel_resistance(1500, 680)

voltages = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

resistors = []
for volt in voltages:
    if volt != 0:
        resistors.append(voltage_div_get_r1(5, volt, 75))
    else:
        resistors.append(0)

with open("resistor_vals.txt") as f:
    raw_resistor_vals = f.read().splitlines()

resistor_vals = []
for r in raw_resistor_vals:
    try:
        resistor_vals.append(float(r))
    except ValueError:
        if r[-1] == "K":
            resistor_vals.append(float(r[:-1]) * 1_000)
        elif r[-1] == "M":
            resistor_vals.append(float(r[:-1]) * 1_000_000)

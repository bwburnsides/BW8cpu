import matplotlib.pyplot as plt
import numpy as np
from math import sin, exp


def Ap(x):
    return 5 * (MAX_AMPLITUDE) * exp(x * (MAX_AMPLITUDE / 25))
    return (1 / 500) * x * x


def An(x):
    return (-1 / 500) * x * x


def Dp(x):
    return 3 * exp(x * (-3 / 90))


def Dn(x):
    return (3 * exp(x * (2 / 150))) - 2 * MAX_AMPLITUDE


MAX_AMPLITUDE = 2
SUSTAIN_PERC = 0.8
SUSTAIN_TIME = 35
x = np.arange(0, 200, 0.1).tolist()

Ap_curve = [Ap(i) for i in x]
An_curve = [An(i) for i in x]
ATTACK_END = min(idx for idx, _ in enumerate(x) if Ap_curve[idx] >= MAX_AMPLITUDE)


print(x[ATTACK_END], Ap_curve[ATTACK_END])
# exit()

Dp_curve = [Dp(i) for i in x]
Dn_curve = [Dn(i) for i in x]
DECAY_END = (
    min(
        idx
        for idx, _ in enumerate(x)
        if Dp_curve[idx] <= (MAX_AMPLITUDE * SUSTAIN_PERC)
    )
    + ATTACK_END
)

print(len(x))
print(ATTACK_END)
print(DECAY_END)


def f(x):
    y = []
    for i, v in enumerate(x):
        if i <= ATTACK_END:
            y.append(min(Ap_curve[i], max(An_curve[i], MAX_AMPLITUDE)) * sin(v))
        elif i <= (ATTACK_END + DECAY_END):
            y.append(
                min(
                    Dp_curve[i],
                    max(Dn_curve[i], MAX_AMPLITUDE * SUSTAIN_PERC),
                )
                * sin(v)
            )
        else:
            y.append(MAX_AMPLITUDE * sin(v))
    return y


# Attack Curves
plt.plot(x, Ap_curve)
# plt.plot(x[0:ATTACK_END], Ap_curve[0:ATTACK_END])
# plt.plot(x[0:ATTACK_END], An_curve[0:ATTACK_END])

# Decay Curves
# plt.plot(x[ATTACK_END:DECAY_END], Dp_curve[ATTACK_END:DECAY_END])
plt.plot(x, Dp_curve)
# plt.plot([i + x[ATTACK_END] for i in x][0:DECAY_END], Dp_curve[0:DECAY_END])
# plt.plot([i + x[ATTACK_END] for i in x][0:DECAY_END], Dn_curve[0:DECAY_END])

# Sustain Curves
# plt.plot(x[DECAY_END:], [MAX_AMPLITUDE * SUSTAIN_PERC for _ in x][DECAY_END:])

# Func
# plt.plot(x, f(x))

plt.grid()
# plt.xlim([0, 100])
# plt.ylim([-15, 15])
plt.show()
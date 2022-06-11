import matplotlib.pyplot as plt
import numpy as np
from math import sin, floor, pi


def y_intercept(m, pt):
    return (-m * pt[0]) + pt[1]


x = np.arange(0, 200, 0.1).tolist()

MAX_AMPLITUDE = 2
SUSTAIN_PERC = 0.60
ATTACK_TIME = 30
DECAY_TIME = 45
SUSTAIN_TIME = 80
RELEASE_TIME = 30

SUSTAIN_VOL = MAX_AMPLITUDE * SUSTAIN_PERC

MAX_X = 200
X_STEP = 0.1

X = np.arange(0, MAX_X, X_STEP).tolist()

attack_slope = MAX_AMPLITUDE / ATTACK_TIME
attack_curve = [x * attack_slope for x in X]

a_end_idx = min(idx for idx, _ in enumerate(X) if attack_curve[idx] >= MAX_AMPLITUDE)
a_endpoint = (X[a_end_idx], attack_curve[a_end_idx])

decay_slope = ((MAX_AMPLITUDE * SUSTAIN_PERC) - MAX_AMPLITUDE) / DECAY_TIME
decay_b = y_intercept(decay_slope, a_endpoint)
decay_curve = [(x * decay_slope) + decay_b for x in X]

d_end_idx = min(idx for idx, _ in enumerate(X) if decay_curve[idx] <= SUSTAIN_VOL)
d_endpoint = X[d_end_idx], decay_curve[d_end_idx]

sustain_curve = [SUSTAIN_VOL for _ in X]

s_start_time = d_endpoint[0]
s_end_time = s_start_time + SUSTAIN_TIME
s_end_idx = min(idx for idx, x in enumerate(X) if x >= s_end_time)
s_endpoint = X[s_end_idx], sustain_curve[s_end_idx]

release_slope = (-SUSTAIN_VOL) / RELEASE_TIME
release_b = y_intercept(release_slope, s_endpoint)
release_curve = [(x * release_slope) + release_b for x in X]

r_end_idx = min(idx for idx, _ in enumerate(X) if release_curve[idx] <= 0)

print(attack_slope)
print(decay_slope)
print(SUSTAIN_VOL)
print(release_slope)


def f(D, g=sin):
    Y = []
    for i, x in enumerate(D):
        a = min(attack_curve[i], MAX_AMPLITUDE) * g(x)
        d = min(decay_curve[i], MAX_AMPLITUDE) * g(x)
        s = min(sustain_curve[i], MAX_AMPLITUDE) * g(x)
        r = min(release_curve[i], MAX_AMPLITUDE) * g(x)
        y = MAX_AMPLITUDE * g(x)

        if i <= a_end_idx:
            Y.append(a)
        elif i <= d_end_idx:
            Y.append(d)
        elif i <= s_end_idx:
            Y.append(s)
        elif i <= r_end_idx:
            Y.append(r)
        else:
            Y.append(y)

    return Y


plt.plot(X[0:a_end_idx], attack_curve[0:a_end_idx])
plt.plot(X[a_end_idx:d_end_idx], decay_curve[a_end_idx:d_end_idx])
plt.plot(X[d_end_idx:s_end_idx], sustain_curve[d_end_idx:s_end_idx])
plt.plot(X[s_end_idx:r_end_idx], release_curve[s_end_idx:r_end_idx])

plt.plot(X[:r_end_idx], f(X)[:r_end_idx])

plt.grid()
plt.xlim([0, X[r_end_idx]])
plt.xlabel("Time")
plt.ylabel("Volume")
plt.title("ADSR Envelope with Linear ADR")
plt.show()

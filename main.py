from matplotlib import pyplot as plt
import json
from datetime import datetime


def smooth(l, n=1):
    """ Takes a list and returns it smoothed as the prof asked 
        l: list to smooth
        n: number of elements used to make the mean """

    # per n grandi (n>50) l'inizio e la fine si vede che sono brutti
    if n < 1:
        # chiude il loop
        return 1

    # inserisce la prima parte che viene saltata
    # smoothing con n=n/10 perchè non sia troppo brutto
    new_l = [] + smooth(l[:n], n=int(n/10))

    for i in range(n, len(l) - n):
        # temp list su cui calcolare la media
        temp_list = l[i-n:i+n+1]

        # media
        mean = sum(temp_list) / len(temp_list)
        new_l.append(mean)

    # inserisce l'ultima parte che viene saltata
    # stessa cosa dell'inizio
    new_l += smooth(l[-n:], n=int(n/10))

    return new_l


def smooth2(l):
    """ Stessa funzione senza la variabile 'n' """
    new_l = []
    new_l.append(l[0])

    for i in range(1, len(l) - 1):
        value = (l[i-1] + l[i] + l[i+1]) / 3
        new_l.append(value)

    new_l.append(l[-1])
    return new_l


# point 1.1
with open("market-cap.json") as f:
    dic = json.load(f)["values"]

v = [x["y"] for x in dic]

# point 1.2
plt.plot(smooth(v, n=100))

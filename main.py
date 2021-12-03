from matplotlib import pyplot as plt
from datetime import datetime
import json


def mean(l):
    """ Mean of a list """
    return sum(l) / len(l)


def jsonr(filename):
    """ Json read function """
    with open(filename) as f:
        return json.load(f)


def plotsetup(title, ylab="", xlab="", xtick=4, ytick=8):
    """ Plot setup function to avoid redundance """
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    ax.yaxis.set_major_locator(plt.MaxNLocator(8))
    plt.title(title)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.grid()


def smooth4(l, n=15):
    """ Takes a list and returns it smoothed
        In the range (1, n) each mean must be done with that number of elements
        Official function to be used
    """

    # creates new list
    new_l = []
    # appends first element
    new_l.append(l[0])

    for i in range(1, len(l)-1):

        # corrected_n is the range around the 'i'th element
        # it is not always equal to 'n' because in the first and last 'n' elements
        # it is equal to the largest possible range
        if i < n:
            corrected_n = i
        elif len(l) - i < n:
            corrected_n = len(l) - i
        else:
            corrected_n = n

        # temp list with the elements used to calculate the mean
        temp_l = l[i-corrected_n:i+corrected_n+1]
        new_l.append(mean(temp_l))

    # appends last element
    new_l.append(l[-1])

    return new_l


MC = jsonr("market-cap.json")
DIFF = jsonr("difficulty.json")
REV = jsonr("miners-revenue.json")
# plt.figure(dpi=600)


""" part 1 task 1 """

# data set up
values = [x["y"] for x in MC["values"]]
timestamps = [datetime.fromtimestamp(x["x"]) for x in MC["values"]]

plotsetup("Market capitalization", ylab="USD")

plt.plot(timestamps, values, color="black")
plt.savefig("part1_task1.png", dpi=600)

plt.cla()

""" part 1 task 2 """

plotsetup("Market capitalization (smoothed)", ylab="USD")

plt.plot(timestamps, smooth4(values), color="black")
plt.plot(timestamps, values, color="black", alpha=0.2)
plt.savefig("part1_task2.png", dpi=600)

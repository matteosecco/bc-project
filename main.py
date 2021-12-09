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


def plotsetup(title, ylab="", xlab="", xtick=4, ytick=8, ylab2=""):
    """ Plot-setup function to avoid redundance
        Returns 'fig' and 'ax' in case they are needed for specific purposes"""
    
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(plt.MaxNLocator(xtick))
    ax.yaxis.set_major_locator(plt.MaxNLocator(ytick))
    plt.title(title)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    
    # sets 'ax2' only when specified
    if ylab2 != "":
        ax2 = ax.twinx()
        ax2.set_ylabel(ylab2)
        ax2.xaxis.set_major_locator(plt.MaxNLocator(xtick))
        ax2.yaxis.set_major_locator(plt.MaxNLocator(ytick))
    else:
        # returned empty if not used
        ax2 = ""

    plt.grid()

    return fig, ax, ax2


def getval(data):
    """ Gets data in the format found in ["values"] (dict with x, y keys) 
        and returns a tuple containing the two lists (x, y)
    """

    return [x["y"] for x in data], [datetime.fromtimestamp(x["x"]) for x in data]


def smooth(l, n=15):
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


def norm(l, n=1):
    """ Normalize a list so that it starts from 'n' """

    # moltiplicatore
    molt = n / l[0]

    return [e*molt for e in l]


# unpack all data in 6 lists and cuts the last two
mc_values, mc_ts = getval(jsonr("market-cap.json")["values"])
diff_values, diff_ts = getval(jsonr("difficulty.json")["values"][5:])
rev_values, rev_ts = getval(jsonr("miners-revenue.json")["values"][:-5])


""" part 1 task 1 """

plotsetup("Market capitalization", ylab="USD")

plt.plot(mc_ts, mc_values, color="black")

plt.savefig("part1_task1.png", dpi=600)
plt.cla()


""" part 1 task 2 """

plotsetup("Market capitalization (smoothed)", ylab="USD")

plt.plot(mc_ts, smooth(mc_values), color="black")
plt.plot(mc_ts, mc_values, color="black", alpha=0.2)

plt.savefig("part1_task2.png", dpi=600)
plt.cla()


""" part 2 task 1 """

plotsetup("Miner revenues", ylab="USD")

plt.plot(rev_ts, smooth(rev_values, n=7), color="black")

plt.savefig("part2_task1.png", dpi=600)
plt.cla()


""" part 2 task 2 """

fig, ax, ax2 = plotsetup("Revenues and difficulty",ylab="USD", ylab2="Difficulty")

ax.plot(rev_ts, smooth(rev_values, n=7), color="orange", label="Revenues")
ax2.plot(diff_ts, norm(smooth(diff_values, n=7)), color="teal", label="Difficulty")

plt.savefig("part2_task2.png", dpi=600)
ax.cla()
ax2.cla()
plt.cla()


""" part 2 task 3 """

plotsetup("Reward / difficulty")

# list with the ratios normalized
ratio_values = norm([rev_values[i] / diff_values[i] for i in range(len(diff_values))])
plt.plot(diff_ts, ratio_values, color="black", alpha=0.2)
plt.plot(diff_ts, smooth(ratio_values, n=7), color="black")

plt.savefig("part2_task3.png", dpi=600)


""" part 2 task 4 """

plt.title("10% best return periods")

# gets how many are 10% of all days
elem_required = int(0.1*len(ratio_values))
# sorts the list
highest_values = sorted(ratio_values)[-elem_required:]
# new list with best-return indexes to find the timestamps
highest_idx = []

# cycles the list to find the timestamps of the higher return days
for i in range(len(ratio_values)):
    if ratio_values[i] in highest_values:
        highest_idx.append(i)
        plt.axvline(x=diff_ts[i], color="orange", alpha=0.2)

plt.savefig("part2_task4.png", dpi=600)

from matplotlib import pyplot as plt
import json

with open("market-cap.json") as f:
    values = json.load(f)["values"]

plt.plot([x["y"] for x in values])  


from visibility import Visibility, read_data
from matplotlib import pyplot as plt
from astropy.time import Time
import matplotlib.dates as mdates

landolt = read_data()

v = Visibility()
stars = v.check("2022-11-10", "2022-11-15")

for star, visibility in stars:
    star_data = landolt[landolt["Star"] == star]
    plt.cla()
    c = list(star_data['coords'])[0]
    plt.title(f"{star}, {c.ra.hour} - {c.dec.degree}")
    dates = Time(visibility["jd"], format="jd").datetime
    # print(dates)
    # print(visibility["jd"].min(), visibility["jd"].max())
    plt.plot(dates, visibility["Alt"])
    myFmt = mdates.DateFormatter('%d-%H')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.axhline(y=20, color='r', linestyle='-')
    plt.show()


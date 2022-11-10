from .utils import read_data

import numpy as np
import pandas as pd
from astropy.time import Time, TimeDelta
from astropy.coordinates import EarthLocation, AltAz, Angle
from astropy import units
from astropy.timeseries import TimeSeries
from astroplan import Observer
from matplotlib import pyplot as plt


class Visibility:
    def __init__(self):
        self.ata50 = EarthLocation(39.904607 * units.deg, 41.244430 * units.deg, 1890 * units.m)

    def calculate(self, date, obj):
        date = Time(date) + TimeDelta(0.5)
        one_day = TimeSeries(time_start=date, time_delta=3600 * units.s, n_samples=24)
        frame = AltAz(obstime=one_day.time, location=self.ata50)
        obj_alt_az = obj.transform_to(frame)
        obj_alt = obj_alt_az.alt.degree.tolist()
        return pd.DataFrame(
            {
                "time": one_day.time,
                "alt": obj_alt
            }
        )

    def check(self, start, end):
        start = Time(start)
        end = Time(end)

        if end < start:
            end, start = start, end

        stars = read_data()
        stars = stars[stars["Vmag"] < 14]
        days = (end - start).jd
        check_days = TimeSeries(time_start=start, time_delta=1 * units.day, n_samples=days)
        data = []
        for each in check_days:
            line = []
            for each_star in stars.to_numpy():
                the_date = each["time"].datetime.date()
                print(each_star[0], str(the_date))
                obs = Observer(self.ata50)

                tw_mo = obs.twilight_morning_astronomical(Time(str(the_date)), which="next")
                tw_ev = obs.twilight_evening_astronomical(Time(str(the_date)), which="next")
                visibility_chart = self.calculate(str(the_date), each_star[1])
                jds = np.array([i.jd for i in visibility_chart["time"].to_numpy()])
                time_mask = (jds < tw_mo.jd + 1) & (jds > tw_ev.jd)
                visibility_mask = (visibility_chart["alt"] > 20).to_numpy()
                mask = np.logical_and(time_mask, visibility_mask)
                visibility_chart = visibility_chart[mask]
                if len(visibility_chart) > 2:
                    # ra = each_star[1].ra.hms
                    # dec = each_star[1].dec.dms
                    # RA = f"'{str(int(ra.h)).zfill(2)}:{str(int(ra.m)).zfill(2)}:{round(ra.s, 2)}"
                    # DEC = f"'{str(int(dec.d)).zfill(2)}:{str(int(dec.m)).zfill(2)}:{round(dec.s, 2)}"
                    RA = str(Angle(f"{each_star[1].ra.hour} hour"))
                    DEC = str(Angle(f"{each_star[1].dec.degree} degree"))
                    h, t = RA.split("h")
                    m, s = t.split("m")
                    s = s.replace("s", "")

                    d, dt = DEC.split("d")
                    K = "-" if d.startswith("-") else ""
                    DDD = K + str(abs(int(d))).zfill(2)
                    dm, ds = dt.split("m")
                    ds = ds.replace("s", "")
                    RAA = f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}"
                    DECC = f"{DDD}:{str(dm).zfill(2)}:{str(ds).zfill(2)}"
                    line.append([
                        each_star[0], RAA, DECC, each_star[2], each_star[3], each_star[6], each_star[7],
                        visibility_chart["time"].min().datetime.time(), visibility_chart["time"].max().datetime.time()
                    ])
            if len(line) > 0:
                data.append([str(each["time"].datetime.date()), pd.DataFrame(line,
                                                                             columns=["source", "ra", "dec", "Vmag",
                                                                                      "B-V", "Vmerr", "B-Verr", "start",
                                                                                      "end"])])
        return data

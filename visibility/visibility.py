import pandas as pd

from .utils import read_data

import pickle
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.timeseries import TimeSeries
from astropy import units


class Visibility:
    def __init__(self):
        self.ata50 = EarthLocation(
            39.904607 * units.deg, 41.244430 * units.deg, 1850 * units.m
        )

    def calculate(self, start, end, multiplier):
        start = Time(start)
        end = Time(end)
        hours = ((end - start).sec / 3600) / multiplier
        df = (end - start).sec / hours
        tm = TimeSeries(time_start=start, time_delta=df * units.s, n_samples=hours).time
        data = read_data()
        frame = AltAz(obstime=tm, location=self.ata50)
        to_save = []
        for star, coord in zip(data["Star"].tolist(), data["coords"].tolist()):
            print(star)
            alt_az = SkyCoord(coord).transform_to(frame)
            df = pd.DataFrame(
                {
                    "jd": tm.jd,
                    "Alt": alt_az.alt.degree
                }
            )
            to_save.append([star, df])

        with open("data.pkl", "wb") as f2w:
            pickle.dump(to_save, f2w)

    def check(self, start, end=None):
        start_jd = Time(start).jd
        if end is None:
            end_jd = start_jd + 1
        else:
            end_jd = Time(end).jd

        if start_jd > end_jd:
            start_jd, end_jd = end_jd, start_jd

        with open("data.pkl", "rb") as f2w:
            to_return = []
            data = pickle.load(f2w)
            # stars = read_data()
            for star, visibility in data:
                #
                mask = (visibility["jd"] >= start_jd) & (visibility["jd"] <= end_jd)
                wanted_range = visibility[mask]
                if(len(wanted_range[wanted_range["Alt"]>20]) > 6):
                    to_return.append([star, wanted_range])

            return to_return

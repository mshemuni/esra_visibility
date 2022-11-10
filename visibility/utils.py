import pandas as pd
from astropy.coordinates import SkyCoord
import numpy as np
import requests
from bs4 import BeautifulSoup


def read_data():
    return pd.read_pickle("landolt.pkl")


def download_data():
    data = requests.get("https://www.eso.org/sci/observing/tools/standards/Landolt.html")
    if data.status_code == 200:
        html = data.text
        soup = BeautifulSoup(html)
        trs = soup.findAll('tr')
        data = []
        for tr in trs:
            tds = tr.findAll('td')
            if len(tds) == 18:
                if tds[0].text != "Star" and tds[0].text != " ":
                    # print(SkyCoord(ra=tds[2].text, dec=tds[3].text, unit=["hour", "degree"]))
                    data.append(
                        [
                            tds[0].text, SkyCoord(ra=tds[2].text, dec=tds[3].text, unit=["hour", "degree"]),
                            tds[4].text, tds[5].text, tds[10].text,
                            tds[11].text, tds[12].text, tds[13].text
                        ]
                    )
        df = pd.DataFrame(
            np.array(data),
            columns=["Star", "coords", "Vmag", "B-V", "n", "m", "Vmerr", "B-Verr"]
        )
        df["Vmag"] = df["Vmag"].astype(float)
        df["B-V"] = df["B-V"].astype(float)
        df["n"] = df["n"].astype(int)
        df["m"] = df["m"].astype(int)
        df["Vmerr"] = df["Vmerr"].astype(float)
        df["B-Verr"] = df["B-Verr"].astype(float)

        df.to_pickle("landolt.pkl")

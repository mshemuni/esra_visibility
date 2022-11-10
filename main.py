import pandas as pd
from visibility import Visibility
from pandas import ExcelWriter


stars = pd.read_pickle("landolt.pkl")
# print(stars.loc[0]["coords"])
v = Visibility()

# print(v.calculate("2022-11-10", stars.loc[0]["coords"]))
# print(v.check("2022-11-10", "2022-11-11"))

with ExcelWriter(f"gozlenebilirlik.xls") as writer:
    for date, df in v.check("2022-11-01", "2023-01-01"):
        df.to_excel(writer, f'{date}')
        #
    #     for star, df in name_df:

# with ExcelWriter("gozlenebilirlik.xls") as writer:
#     for date, star, df in v.check("2022-11-10", "2022-11-12"):
#         df.to_excel(writer, f'{date}_{star}')
#
#


# from astropy.coordinates import Angle
# a = Angle("01 05 22 hour")
# print(a.hms.h)
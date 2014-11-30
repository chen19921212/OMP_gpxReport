
import pyproj
"""
Converting Degrees, Minutes, Seconds formatted coordinate strings to decimal.
Formula:
DEC = (DEG + (MIN * 1/60) + (SEC * 1/60 * 1/60))
Assumes S/W are negative.
"""

import re

def dms2dec(dms_str):
    dms_str = re.sub(r'\s', '', dms_str)
    if re.match('[swSW]', dms_str):
        sign = -1
    else:
        sign = 1

    degree          = 0
    minute          = 0
    second          = 0
    frac_seconds    = 0

    splittedVals = re.split('\D+', dms_str)

    if len(splittedVals) > 0:
        try:
            degree          = float(splittedVals[0])
        except:
            degree = 0
    if len(splittedVals) > 1:
        try:
            minute          = float(splittedVals[1])
        except:
            minute = 0
    if len(splittedVals) > 2:
        try:
            second          = float(splittedVals[2])
        except:
            second = 0
    if len(splittedVals) > 3:
        try:
            frac_seconds_len = len(frac_seconds)

            frac_seconds = float(frac_seconds)
            for i in xrange(frac_seconds_len):
                frac_seconds = frac_seconds / 10.0
        except:
            frac_seconds = 0

    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600 + float(frac_seconds) / 36000)

utfstr = "ボールト"

print(dms2dec(str("22°43'35\"N")))
print(dms2dec(str("49°04'29\"N")))
import re

import csv
from builtins import print

class geoNamesAdapterCommon():
    def __init__(self):
        pass

# class CustomDictOne(dict):
#    def __init__(self,*arg,**kw):
#       super(CustomDictOne, self).__init__(*arg, **kw)

class geoNamesAdapter(geoNamesAdapterCommon, list):
    def __init__(self, *arg,**kw):
        geoNamesAdapterCommon.__init__(self)
        super(geoNamesAdapter, self).__init__(*arg, **kw)

    def addGeoName(self, name, latitude, longitude):
        self.append({"name" : name, "latitude" : latitude, "longitude" : longitude})

    def dms2dec(self, dms_str):
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

class geoNamesAdapterFile(geoNamesAdapter):
    dataFile = None
    fileName = None

    def __init__(self, filename = None):
        geoNamesAdapter.__init__(self)

        if(filename != None):
            self.fileName = filename
            try:
                self.dataFile = open(self.fileName, newline='')
            except Exception as ex:
                raise Exception(ex)

class geoNamesAdapterCsvFile(geoNamesAdapterFile):
    reader = None

    def __init__(self, filename = None, delimiterSecuence = ""):
        geoNamesAdapterFile.__init__(self, filename)

        if(self.dataFile != None):
            try:
                self.reader = csv.reader(self.dataFile, delimiter=delimiterSecuence)
            except Exception as ex:
                raise Exception(ex)

class geoNamesAdapterCsvFile_geoNames(geoNamesAdapterCsvFile):
    def __init__(self, filename = None):
        geoNamesAdapterCsvFile.__init__(self, filename, delimiterSecuence = "\t")

        for row in self.reader:
            print(row)
            self.addGeoName(name=row[1], longitude=float(row[5]), latitude=float(row[4]))

class geoNamesAdapterCsvFile_geoPortal(geoNamesAdapterCsvFile):
    def __init__(self, filename = None):
        geoNamesAdapterCsvFile.__init__(self, filename, delimiterSecuence = ",")
        for row in self.reader:
#"identyfikator PRNG","nazwa główna","rodzaj obiektu","klasa obiektu","obiekt nadrzędny",dopełniacz,przymiotnik,uwagi,"źródło informacji","element rozróżniający","element rodzajowy","wymowa IPA","wymowa polska","szerokość geograficzna","długość geograficzna","współrzędne prostokątne Y","współrzędne prostokątne X","data modyfikacji","rodzaj reprezentacji","system zewnetrzny","identyfikator zewnętrzny","skala mapy","status nazwy","nazwa dodatkowa","kod języka nazwy dodatkowej","język nazwy dodatkowej","latynizacja nazwy dodatkowej","nazwa historyczna","nazwa oboczna","uwagi nazw dodatkowych","uwagi nazw historycznych","uwagi nazw obocznych","obcy egzonim","pismo egzonimu","język egzonimu","latynizacja egzonimu","zagraniczny endonim","pismo endonimu","język endonimu","latynizacja endonimu",państwo,województwo,powiat,gmina,"identyfikator jednostki podziału terytorialnego kraju","data wprowadzenia","data zniesienia lub usunięcia"
#                   0             1                2               3                  4           5           6     7                  8                       9                   10         11               12                       13                     14
#             print(row)
#             for i,field in enumerate(row):
#                 print("{0}: {1}". format(i, field))
#
            print("name: {0} longitude: {1} latitude: {2}".format(row[1], row[13], row[14]))
            self.addGeoName(name=row[1], longitude= self.dms2dec(row[13]), latitude=self.dms2dec(row[14]))

if __name__ == "__main__":
    _geoNamesAdapterCsvFile_geoNames = geoNamesAdapterCsvFile_geoNames("./PL.txt")
    _geoNamesAdapterCsvFile_geoPortal = geoNamesAdapterCsvFile_geoPortal("./obiekty_fizjograficzne.csv")


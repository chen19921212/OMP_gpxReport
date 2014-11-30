import csv

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

    def addGeoName(self):
        pass

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

    def __init__(self, filename = None):
        geoNamesAdapterFile.__init__(self, filename)

        if(self.dataFile != None):
            try:
                self.reader = csv.reader(self.dataFile, delimiter='\t')
            except Exception as ex:
                raise Exception(ex)

class geoNamesAdapterCsvFile_geoNames(geoNamesAdapterCsvFile):
    def __init__(self, filename = None):
        geoNamesAdapterCsvFile.__init__(self, filename)
        pass

    def process(self):
        for row in self.reader:

            geoObject = {}
            geoObject["geonameid"]              = int(row[0])
            geoObject["name"]                   = row[1]
            geoObject["asciiname"]              = row[2]
            geoObject["alternatenames"]         = row[3]
            geoObject["latitude"]               = float(row[4])
            geoObject["longitude"]              = float(row[5])
            geoObject["feature class"]          = row[6]
            geoObject["feature code"]           = row[7]
            geoObject["country code"]           = row[8]
            geoObject["cc2"]                    = row[9]
            geoObject["admin1 code"]            = row[10]
            geoObject["admin2 code"]            = row[11]
            geoObject["admin3 code"]            = row[12]
            geoObject["admin4 code"]            = row[13]
            geoObject["population"]             = row[14]
            geoObject["elevation"]              = row[15]
            geoObject["dem"]                    = row[16]
            geoObject["timezone"]               = row[17]
            geoObject["modification date"]      = row[18]

            print("idx: {0} lon:{1} lat:{2} name:{3}".format(geoObject["geonameid"], geoObject["longitude"], geoObject["latitude"], geoObject["name"]))

class geoNamesAdapterCsvFile_geoPortal(geoNamesAdapterCsvFile):
    def __init__(self, filename = None):
        geoNamesAdapterCsvFile.__init__(self, filename)
        pass

    def process(self):
        for row in self.reader:
#"identyfikator PRNG","nazwa główna","rodzaj obiektu","klasa obiektu","obiekt nadrzędny",dopełniacz,przymiotnik,uwagi,"źródło informacji","element rozróżniający","element rodzajowy","wymowa IPA","wymowa polska","szerokość geograficzna","długość geograficzna","współrzędne prostokątne Y","współrzędne prostokątne X","data modyfikacji","rodzaj reprezentacji","system zewnetrzny","identyfikator zewnętrzny","skala mapy","status nazwy","nazwa dodatkowa","kod języka nazwy dodatkowej","język nazwy dodatkowej","latynizacja nazwy dodatkowej","nazwa historyczna","nazwa oboczna","uwagi nazw dodatkowych","uwagi nazw historycznych","uwagi nazw obocznych","obcy egzonim","pismo egzonimu","język egzonimu","latynizacja egzonimu","zagraniczny endonim","pismo endonimu","język endonimu","latynizacja endonimu",państwo,województwo,powiat,gmina,"identyfikator jednostki podziału terytorialnego kraju","data wprowadzenia","data zniesienia lub usunięcia"

#                   0
            print(row)

if __name__ == "__main__":

    print("start")
    gNAdapterCsvFile = geoNamesAdapterCsvFile()

    _geoNamesAdapterCsvFile_geoNames = geoNamesAdapterCsvFile_geoNames("./PL.txt")
    _geoNamesAdapterCsvFile_geoNames.process()

    _geoNamesAdapterCsvFile_geoPortal = geoNamesAdapterCsvFile_geoPortal("./obiekty_fizjograficzne.csv")
    _geoNamesAdapterCsvFile_geoPortal .process()

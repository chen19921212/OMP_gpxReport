from string import Template

class geoBackEndCommon(dict):
    def __init__(self, *arg, **kw):
        super(geoBackEndCommon, self).__init__(*arg, **kw)
        pass

class geoBackEnd(geoBackEndCommon):
    defaultKeys = ("Title", "StartPoint", "EndPoint", "StartDate", "EndDate", "GeoPoints", "Stat", "GpxFile")
#    defaultKeys = None

    def __init__(self, *arg, **kw):
        geoBackEndCommon.__init__(self, *arg, **kw)
        for key in self.defaultKeys:
            if not key in self:
                self[key] = None

class geoBackEndStrTempl(geoBackEnd):
    strTemplate  = None

    def __init__(self, templFname, *arg, **kw):
        geoBackEnd.__init__(self, *arg, **kw)

        fIn = open(templFname, 'r')
        self.strTemplate = Template(fIn.read())

class geoBackEndStrTemplToMd(geoBackEndStrTempl):
    strTemplate  = None

    def __init__(self, templFileName, outputFileName, *arg, **kw):
        geoBackEndStrTempl.__init__(self, templFileName, *arg, **kw)

        output = self.strTemplate.substitute(self)
        print(output)
        fOut = open(outputFileName, 'w')
        fOut.write(output)
        fOut.close()

if __name__ == "__main__":
    # geoBackEnd = geoBackEnd(Title = "Bieszczady", FigProfile = "Res/fig1.png", FigMap = "Res/fig2.png", Fig3d = "Res/fig3.png", GpxFile = "Res/bieszczady.gpx")
    # geoBackEndStrTempl(templFname='gpxReport.tpl', Title = "Bieszczady", FigProfile = "Res/fig1.png", FigMap = "Res/fig2.png", Fig3d = "Res/fig3.png", GpxFile = "Res/bieszczady.gpx")

    geoBackEndStrTemplToMd(templFileName='gpxReport.tpl', outputFileName='/home/ziemek/Projects/pooleTestProj/input/gpxReport.md', Title = "Bieszczady", FigProfile = "Res/fig1.png", FigMap = "Res/fig2.png", Fig3d = "Res/fig3.png", GpxFile = "Res/bieszczady.gpx")

    # fIn = open('gpxReport.tpl', 'r')
    # template = Template(fIn.read())
    # output = template.substitute(geoBackEnd)
    # print(output)
    # fOut = open('/home/ziemek/Projects/pooleTestProj/input/gpxReport.md', 'w')
    # fOut.write(output)
    # fOut.close()

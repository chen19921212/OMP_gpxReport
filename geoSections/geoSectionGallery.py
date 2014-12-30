from geoCommon.geoConfig import GeoConfig

import os
from PIL import Image
from string import Template

class geoSectionGalleryCommon():
    outputPath = GeoConfig.geoReport["outputPath"]
    outputResSubPath = GeoConfig.geoReport["outputResSubPath"]

    def __init__(self):
        pass


class geoNamesCommon(list):
    def __init__(self, *arg, **kw):
        super(geoNamesCommon, self).__init__(*arg, **kw)
        pass


class geoSectionGallery(geoSectionGalleryCommon, list):
    extensions = {".jpg", ".png", ".gif", ".JPG", ".PNG", ".GIF", ".Jpg", ".Png", ".Gif"}
    thumbSize = (120, 120)

    def __init__(self, picturesRepository=None, *arg, **kw):
        geoSectionGalleryCommon.__init__(self)
        super(geoSectionGallery, self).__init__(*arg, **kw)

        if (picturesRepository is not None):
            for root, dirs, files in os.walk(picturesRepository, topdown=False):
                print(files)
                for inImgFile in files:
                    if (any(inImgFile.endswith(ext) for ext in self.extensions) == True):
                        thumbOutFile = os.path.splitext(inImgFile)[0] + ".thumbnail"
                        if thumbOutFile != inImgFile:
                            try:
                                imCopyPath = os.path.join(GeoConfig.geoReport["outputPath"],
                                                              GeoConfig.geoReport["outputResSubPath"])
                                imThumbPath = os.path.join(GeoConfig.geoReport["outputPath"],
                                                               GeoConfig.geoReport["outputResSubPath"])

                                try:
                                    os.makedirs(imCopyPath)
                                except OSError:
                                    pass
                                try:
                                    os.makedirs(imThumbPath)
                                except OSError:
                                    pass

                                imCopyNamePath = os.path.join(GeoConfig.geoReport["outputPath"],
                                                              GeoConfig.geoReport["outputResSubPath"], inImgFile)
                                imThumbNamePath = os.path.join(GeoConfig.geoReport["outputPath"],
                                                               GeoConfig.geoReport["outputResSubPath"], thumbOutFile)

                                im = Image.open(os.path.join(picturesRepository, inImgFile))

                                copyOfImage = im.copy()
                                print(imCopyNamePath)
                                im.save(imCopyNamePath, "JPEG")

                                im.thumbnail(self.thumbSize, Image.ANTIALIAS)
                                print(imThumbNamePath)
                                im.save(imThumbNamePath, "JPEG")

                                picThumb = {"ThumbPathName":os.path.join(GeoConfig.geoReport["outputResSubPath"], thumbOutFile), "PicPathName": os.path.join(GeoConfig.geoReport["outputResSubPath"], inImgFile)}
                                self.append(picThumb)
                            except IOError as e:
                                print("cannot create thumbnail or copy for {0}".format(inImgFile))
                                print("Error: {0}".format(e))


    def __str__(self):
        outStr = ""

        singlePictureTemplate_fileIn = open("geoSectionGallery_PicLine.tpl", 'r')
        singlePictureTemplate = Template(singlePictureTemplate_fileIn.read())
        for picThumb in self:
            print(picThumb)
            outStr += singlePictureTemplate.substitute(picThumb)

        tablePictureTemplate_fileIn = open("geoSectionGallery_PicTable.tpl", 'r')
        tablePictureTemplate = Template(tablePictureTemplate_fileIn.read())
        outStr = tablePictureTemplate.substitute({"PicGalleryTable": outStr})

        return outStr

if __name__ == "__main__":
    geoSectionGallery = geoSectionGallery(picturesRepository="./Pic")
    print(geoSectionGallery)

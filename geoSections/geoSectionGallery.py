import os


class geoSectionGalleryCommon():
    def __init__(self):
        pass


class geoSectionGallery(geoSectionGalleryCommon):
    extensions = {".jpg", ".png", ".gif", ".JPG", ".PNG", ".GIF", ".Jpg", ".Png", ".Gif"}

    def __init__(self, picturesRepository=None):
        geoSectionGalleryCommon.__init__(self)

        if (picturesRepository is not None):
            for root, dirs, files in os.walk(picturesRepository, topdown=False):
                # print({file: any(file.endswith(ext) for ext in self.extensions) for file in files})
                print(files)
                for file in files:
                    if (any(file.endswith(ext) for ext in self.extensions) == True):
                        print({file: any(file.endswith(ext) for ext in self.extensions)})

                        #     print(os.path.join(root, file))
                        # for name in dirs:
                        #     print(os.path.join(root, file))

    def __str__(self):
        return ">>------------------------>"


if __name__ == "__main__":
    geoSectionGallery = geoSectionGallery(picturesRepository="./Pic")
    print(geoSectionGallery)

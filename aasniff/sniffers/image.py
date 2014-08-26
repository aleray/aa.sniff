from .. import sniffer, AASniffer


@sniffer("triples")
class ImageSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/image"

    def test(self):
        return self.model.query('''
            ASK {
                { ?subject dct:format ?ct .}
                UNION
                { ?subject hdr:content-type ?ct .}
                FILTER (REGEX(?ct, "^image/")).
            }''', initNs={
                "dct": "http://purl.org/dc/terms/",
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

    def sniff(self):
        print("sniffed an image")
        triples = []
        # Do semething useful with the image, like reading the EXIF metadata
        #import PIL
        #from PIL import ExifTags
        #from PIL import Image
        #img = Image.open('/path/to/the/image.jpg')
        #exif = {
            #PIL.ExifTags.TAGS[k]: v
            #for k, v in img._getexif().items()
            #if k in PIL.ExifTags.TAGS
        #}
        return triples

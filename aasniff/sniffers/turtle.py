from .. import sniffer, AASniffer


@sniffer("turtle")
class TurtleSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/turtle"

    def test(self):
        return self.model.query('''
            ASK {
                { ?subject dct:format "text/turtle" .}
                UNION
                { ?subject hdr:content-type ?object .}
                FILTER (REGEX(?object, "^text/turtle")).
            }''', initNs={
                "dct": "http://purl.org/dc/terms/",
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

    def sniff(self):
        print("sniffed a turtle file")
        return self.request.text

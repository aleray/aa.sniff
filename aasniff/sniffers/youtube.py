from .. import sniffer, AASniffer


@sniffer("triples")
class YoutubeSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/youtube"

    def test(self):
        return self.model.query('''
            ASK {
                { ?subject dct:format "text/html" .}
                UNION
                { ?subject hdr:content-type ?object .}
                FILTER (REGEX(?object, "^text/html")).
                FILTER (REGEX(str(?subject), "^http://www.youtube")).
            }''', initNs={
                "dct": "http://purl.org/dc/terms/",
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

    def sniff(self):
        print("sniffed an youtube page")
        triples = []
        # Do something useful here
        return triples

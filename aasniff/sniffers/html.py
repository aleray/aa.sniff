from .. import sniffer, AASniffer


@sniffer("rdfa")
class HtmlSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/html"

    def test(self):
        return self.model.query('''
            ASK {
                { ?subject dct:format "text/html" .}
                UNION
                { ?subject hdr:content-type ?object .}
                FILTER (REGEX(?object, "^text/html")).
            }''', initNs={
                "dct": "http://purl.org/dc/terms/",
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

    def sniff(self):
        print("sniffed an html page")
        return self.request.text

from .. import sniffer, AASniffer


@sniffer("xml")
class FeedSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/feed"

    def test(self):
        return self.model.query('''
            ASK {
                { ?subject dct:format ?object .}
                UNION
                { ?subject hdr:content-type ?object .}
                FILTER (?object = "application/rss+xml"  ||
                        ?object = "application/atom+xml" ||
                        ?object = "application/xml").
            }''', initNs={
                "dct": "http://purl.org/dc/terms/",
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

    def sniff(self):
        print("sniffed an rss or atom feed")
        return self.request.text

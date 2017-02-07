from .. import sniffer, AASniffer


@sniffer("xml")
class RDFSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/rdf"

    def test(self):
        # TODO: combine those two tests in one
        test1 = self.model.query("""
            ASK {
                { ?subject hdr:content-type ?ct .}
                FILTER (STRSTARTS(?ct, "application/rdf+xml")).
            }""", initNs={
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

        test2 = self.model.query('''
            ASK {
                { ?subject dct:format ?object .}
                UNION
                { ?subject hdr:content-type ?object .}
                FILTER (?object = "application/rss+xml"  ||
                        ?object = "application/atom+xml" ||
                        ?object = "application/xml"      ||
                        ?object = "text/xml").
            }''', initNs={
                "dct": "http://purl.org/dc/terms/",
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

        return (test1 or test2)

    def sniff(self):
        print("sniffed an rdf description (RDF, Atom, RSS, etc.)")
        return self.request.text

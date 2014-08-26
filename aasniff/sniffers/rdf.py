from .. import sniffer, AASniffer


@sniffer("xml")
class RDFSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/rdf"

    def test(self):
        # FIXME: change "^application/rdf.xml" to "^application/rdf+xml"
        # (it throws an error when trying to escape the plus sign)
        return self.model.query('''
            ASK {
                { ?subject hdr:content-type ?object .}
                FILTER (REGEX(?object, "^application/rdf.xml")).
            }''', initNs={
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

    def sniff(self):
        print("sniffed an rdf description")
        return self.request.text

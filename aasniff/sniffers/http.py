import magic
import requests
from rdflib import Namespace, URIRef, Literal, Graph
from .. import sniffer, AASniffer
import logging


@sniffer("triples")
class HttpSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/http"

    def test(self):
        return True

    def sniff(self):
        logging.info("sniffed an http resource")

        # Detects the mime type from content as an alternative to content-type
        # We make a new request to avoid consuming self.request response body
        # FIXME: there should be a way to avoid doing a second request.
        #        See <http://stackoverflow.com/questions/13197854/>
        request = requests.get(self.request.url, stream=True)
        mime = magic.from_buffer(next(request.iter_content(1024)), mime=True)

        DCT = Namespace('http://purl.org/dc/terms/')
        HDR = Namespace('http://www.w3.org/2011/http-headers#')
        subject = URIRef(self.request.url)

        triples = [(subject, DCT['format'], Literal(mime))]

        for key, value in list(self.request.headers.items()):
            triples.append((subject, HDR[key.lower()], Literal(value)))

        return triples

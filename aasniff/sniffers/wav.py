import wave
import requests
from .. import sniffer, AASniffer

try: import simplejson as json
except ImportError: import json

try: from io import StringIO
except: from io import StringIO

from rdflib import Namespace, URIRef, Literal


@sniffer("triples")
class WavSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/wav"

    def test(self):
        return self.model.query('''
            ASK {
                { ?subject dct:format "audio/x-wav" .}
                UNION
                { ?subject hdr:content-type "audio/x-wav" .}
            }''', initNs={
                "dct": "http://purl.org/dc/terms/",
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

    def sniff(self):
        print("sniffed an wav file")
        request = requests.get(self.request.url, stream=True)
        head = next(request.iter_content(1024))
        output = StringIO(head)
        f = wave.open(output, 'r')
        duration = (1.0 * f.getnframes ()) / f.getframerate ()

        subject = URIRef(self.request.url)
        AA = Namespace("http://activearchives.org/terms/")
        triples = [(subject, AA['duration'], Literal(duration))]
        return triples

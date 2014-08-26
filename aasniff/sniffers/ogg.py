import subprocess
from .. import sniffer, AASniffer

try: import simplejson as json
except ImportError: import json

from rdflib import Namespace, URIRef, Literal


@sniffer("triples")
class OggSniffer(AASniffer):
    ctx = "http://unique.url/for/my/sniffer/ogg"

    def test(self):
        return self.model.query('''
            ASK {
                { ?subject dct:format ?ct .}
                UNION
                { ?subject hdr:content-type ?ct .}
                FILTER (?ct = "application/ogg" ||
                        ?ct = "audio/ogg"       ||
                        ?ct = "video/ogg").
            }''', initNs={
                "dct": "http://purl.org/dc/terms/",
                "hdr": "http://www.w3.org/2011/http-headers#"
            }
        ).askAnswer

    def sniff(self):
        print("sniffed an ogg file")
        cmd = ['ffprobe', '-show_format', '-print_format', 'json', '-loglevel', 'quiet', self.request.url]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err =  p.communicate()

        subject = URIRef(self.request.url)
        AA = Namespace("http://activearchives.org/terms/")
        infos = json.loads(out)

        triples = [
            (subject, AA['duration'], Literal(infos['duration'])),
            (subject, AA['bit_rate'], Literal(infos['bit_rate'])),
        ]

        return triples


# This file is part of Active Archives.
# Copyright 2006-2014 the Active Archives contributors (see AUTHORS)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Also add information on how to contact you by electronic and paper mail.


from rdflib.store import NO_STORE, VALID_STORE
from rdflib.plugins.memory import IOMemory
import html5lib
import os
import rdflib
import requests
import importlib
from . import conf


registry = {}


def tidy(method):
    """
    Tidies the ouput of the given Sniffer sniff method.
    """
    def decorator(self):
        string = method(self)

        if not string:
            return string

        if self.syntax == "rdfa":
            parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("dom"))
            dom = parser.parse(string)

            ## FIXME: remove this? we moved to rdflib
            # Redland crashes if no xmlns attribute is declared.
            # see: http://bugs.librdf.org/mantis/view.php?id=521
            # Lets fix it in the meanwhile...
            elt = dom.getElementsByTagName("html")[0]
            if not elt.hasAttribute("xmlns"):
                elt.setAttribute("xmlns", "http://www.w3.org/1999/xhtml")

            string = dom.toxml()

        return string
    return decorator


def sniffer(syntax):
    """
    Registers the decorated classes to the list of available sniffers.

    Takes a syntax name to be used to parse the classes index method return value.
    """
    def decorator(cls):
        cls.syntax = syntax
        cls.sniff = tidy(cls.sniff)
        registry[cls.__name__] = cls
        return cls
    return decorator


class AASniffer(object):
    def __init__(self, request=None, model=None):
        self.request = request
        self.model = model

    def test(self):
        return True


class AAApp(object):
    """
    >>> app = AAApp()
    >>> app.index('https://openlibrary.org/authors/OL200810A.rdf')
    """
    def __init__(self, conf=conf):
        self.conf = conf
        self.ident = rdflib.URIRef("rdflib_test")

        engine = conf.STORE.get('ENGINE').lower()

        if engine in ('sqlite', 'pgsql', 'mysql'):
            print("using SQLAlchemy")
            store = rdflib.plugin.get("SQLAlchemy", rdflib.store.Store)(identifier=self.ident)

            if engine == 'sqlite':
                uri = rdflib.Literal('{ENGINE}:///{NAME}'.format(**conf.STORE))
            else:
                uri = rdflib.Literal('{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**conf.STORE))
        elif engine == "sleepycat":
            print("using Sleepycat")
            store = rdflib.plugin.get("Sleepycat", rdflib.store.Store)(identifier=self.ident)
            uri = rdflib.Literal(conf.STORE.get('NAME'))
        else:
            print('invalid engine')

        # Open previously created store, or create it if it doesn't exist yet
        self.graph = rdflib.ConjunctiveGraph(store)

        rt = self.graph.open(uri, create=False)

        if rt != VALID_STORE:
            # There is no underlying infrastructure, create it
            self.graph.open(uri, create=True)
        else:
            assert rt == VALID_STORE, 'The underlying store is corrupt'

    def index(self, url):
        """
        Inspects the resource and store the information found in the RDF store.
        """
        store = IOMemory()
        graph = rdflib.graph.ConjunctiveGraph(store=store)
        request = requests.get(url, stream=True)

        # Indexes the content with the appropriate agents (sniffers)
        for sniffer in self.conf.SNIFFERS:
            sniffer = registry[sniffer](request=request, model=graph)
            result = sniffer.sniff() if sniffer.test() else None

            # If the sniffer produced some metadata...
            if result:
                if sniffer.syntax == 'triples':
                    # The sniffer generated statements; record the statements and where they come from
                    g = rdflib.graph.Graph(store=store, identifier=rdflib.URIRef(sniffer.ctx))
                    for statement in result:
                        g.add(statement)
                else:
                    # The sniffer returned a parsable string, such as XML+RDF, HTML+RDFa...
                    #g.parse(data=result, source=url, format=sniffer.syntax)
                    # Fixme: find a way to specify the context
                    g.parse(data=result, format=sniffer.syntax)

        # FIXME: does not work as expected
        #for ctx in graph.contexts():
            ## Removes exisiting statements
            #gg = rdflib.graph.Graph(store=self.graph.store, identifier=ctx.identifier)
            #self.graph.remove_context(gg)

        for quad in graph.quads():
            # Adds the new statements
            self.graph.add(quad)

        #print(self.graph.serialize(format='nquads'))


from sniffers.http import HttpSniffer
from sniffers.feed import FeedSniffer
from sniffers.html import HtmlSniffer
from sniffers.image import ImageSniffer
from sniffers.ogg import OggSniffer
from sniffers.rdf import RDFSniffer
from sniffers.wav import WavSniffer
from sniffers.youtube import YoutubeSniffer

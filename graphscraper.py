from urllib import request
from html import parser
from urllib.parse import urlparse, urljoin
import networkx
import re

class HyperlinkScraper(parser.HTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        parser.HTMLParser.__init__(self)
        self.titleEncountered = False
        self.hrefsStripped = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' \
                and ('href', 'javascript:print()') not in attrs\
                and ('target', '_blank') not in attrs \
                and ('style', 'font-size:8px;') not in attrs:
            for attr in attrs:
                if attr[0] == 'href':
                    self.hrefsStripped.append(attr[1])

    def handle_data(self, data):
        pass


class GraphScrapper:
    def __init__(self):
        self.graph = networkx.Graph()

    def createGraphFor(self, hostName, beginingPath = '', depth = 0):
        initialUri = urljoin(hostName, beginingPath)
        self.graph.add_node(initialUri)

        if re.search('.pdf|.txt|.jpg|.png|.bmp|.svg|.doc|.zip|.ppsx', initialUri) is not None:
            return None

        try:
            requestWeather = request.urlopen(initialUri)
            data = requestWeather.read()
        except:
            return None

        try:
            hyperlinkScrapper = HyperlinkScraper()
            hyperlinkScrapper.feed(data.decode('utf-8'))
        except:
            return None

        for href in hyperlinkScrapper.hrefsStripped:
            parseResult = urlparse(href)
            uriSub = ''
            if not parseResult.netloc:
                uriSub = urljoin(initialUri, href)
            elif parseResult.netloc and len(parseResult.netloc) > 1 and parseResult.netloc == hostName:
                uriSub = href
            else:
                continue

            if self.graph.has_node(uriSub):
                self.graph.add_edge(initialUri, uriSub)
            if not self.graph.has_edge(initialUri, uriSub) and depth < 5:
                self.createGraphFor(initialUri, uriSub, depth + 1)

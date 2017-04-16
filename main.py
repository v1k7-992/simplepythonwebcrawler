import graphscraper
import sys

serverUri = sys.argv[1]

data = graphscraper.GraphScrapper()
data.createGraphFor(serverUri)

outputFile = open('output.txt', 'w')

for node in data.graph.nodes():
    print(node)
    outputFile.write(node + '\n')

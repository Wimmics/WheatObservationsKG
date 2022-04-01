import pandas as pd
import pprint
import csv
from rdflib import Graph, URIRef, Literal, BNode
from SPARQLWrapper import SPARQLWrapper, JSON

PREFIXE = '''
PREFIX bibo:   <http://purl.org/ontology/bibo/> \nPREFIX fabio: <http://purl.org/spar/fabio/> \nPREFIX dc: <http://purl.org/dc/terms/> \nPREFIX schema: <http://schema.org/> '''

endpoint = 'https://sparql-micro-services.org/service/pubmed/getArticleByPMId_sd/'

to_date = {
    "Jan" : "01",
    "Feb" : "02",
    "Mar" : "03",
    "Apr" : "04",
    "May" : "05",
    "Jun" : "06",
    "Jul" : "07",
    "Aug" : "08",
    "Sep" : "09",
    "Oct" : "10",
    "Nov" : "11",
    "Dec" : "12"
}

def to_doc_id(file, ensemble):
    df = pd.read_csv(file)
    for line in df["doc_id"]:
        ensemble.add(line)

def convert_date(s):
    print(s)
    temp = s.split(" ")
    if len(temp) == 3:
        year = temp[1].strip("\"")
        return f"{year}"
    elif len(temp) == 4:
        year = temp[1].strip("\"")
        month =to_date[temp[2].strip("\"")]
        return f'{year}-{month}'
    else:
        year = temp[1].strip("\"")
        day = temp[3].strip("\"")
        return f"{year}-{to_date[temp[2]]}-{day}"

if __name__ == '__main__':

    folders_to_scan = input("Veuillez renseigner la racine où se trouve les CSV:\n")
    ensemble = set()
    # On charge un ensemble qui contient les doc_id des articles
    # L'ensemble évite des redondances qu'il peut y avoir
    for i in range(9):
        doc_scan = f"{folders_to_scan}{i}\\documents.csv"
        print(doc_scan)
        to_doc_id(doc_scan, ensemble)
    print(len(ensemble))
    with open("article_complete.ttl",'a', encoding="utf-8") as f:

        for element in ensemble:
            query_pubMed = f"{PREFIXE} CONSTRUCT WHERE {{?article bibo:pmid \"{element}\"; ?p ?o.}}"
            sujet = f"https://pubmed.ncbi.nlm.nih.gov/{element}"

            # print(query_pubMed)
            sparql = SPARQLWrapper(endpoint)
            sparql.setQuery(query_pubMed)
            sparql.setReturnFormat("turtle")
            results = sparql.query().convert().decode('utf-8')
            p = results.split("\n")
            res = []
            for x in p:
                if x == "":
                    continue
                if x[0] != "@":
                    if not res:
                        p = x.split(" ")[1]
                        o = " ".join(x.split(" ")[2:])
                        res.append(f"\n\n<https://pubmed.ncbi.nlm.nih.gov/{element}> {p} {o}")
                        continue
                    elif "dc:issued" in x:
                        res.append(f"dc:issued \"{convert_date(x)}\"^^xsd:date;")
                    else:
                        res.append(x)
            f.write("\n".join(res))
            f.write("\n")



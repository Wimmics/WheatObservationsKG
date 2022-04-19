import pandas as pd
import time
from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError, EndPointNotFound, QueryBadFormed

PREFIXE = '''
PREFIX bibo:   <http://purl.org/ontology/bibo/> \nPREFIX fabio: <http://purl.org/spar/fabio/> \nPREFIX dc: <http://purl.org/dc/terms/> \nPREFIX schema: <http://schema.org/> '''

PREFIXE_FOR_RDF = '''@prefix bibo:   <http://purl.org/ontology/bibo/> .
@prefix fabio: <http://purl.org/spar/fabio/> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix schema: <http://schema.org/> .\n\n'''

endpoint = 'https://sparql-micro-services.org/service/pubmed/getArticleByPMId_sd/'


def to_doc_id(file, ensemble):
    df = pd.read_csv(file)
    for line in df["doc_id"]:
        ensemble.add(line)


def convert_date(s,i):
    print(f"{i} - {s}")
    temp = s.split(" ")
    year = temp[1].strip("\"")
    return f"{year}"


def sparql_endpoint_call(element):
    print(f"{element} : n°", end="")
    query_pubmed = f"{PREFIXE} CONSTRUCT WHERE {{?article bibo:pmid \"{element}\"; ?p ?o.}}"

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query_pubmed)
    sparql.setReturnFormat("turtle")
    results = sparql.query().convert().decode('utf-8')
    return results.split("\n")


if __name__ == '__main__':
    n = 8

    folders_to_scan = input("Veuillez renseigner la racine où se trouve les CSV:\n")
    for j in range(0, 9):
        ensemble = set()
        # On charge un ensemble qui contient les doc_id des articles
        # L'ensemble évite des redondances qu'il peut y avoir
        doc_scan = f"{folders_to_scan}{j}\\documents.csv"
        print(f"{doc_scan} : ", end="")
        to_doc_id(doc_scan, ensemble)
        print(len(ensemble))
        with open(f"article_complete_{j}.ttl", 'w', encoding="utf-8") as f:
            print("Starting query")
            f.write(PREFIXE_FOR_RDF)
            i = 0
            for element in ensemble:
                i += 1
                try:
                    p = sparql_endpoint_call(element)
                except EndPointInternalError as epi:
                    print("Request failed - 500 Internal Server Error")
                    with open("article_failed.txt", "a", encoding="utf-8") as err:
                        err.write(f"-{element} : Error 500\n\n")
                    continue
                except EndPointNotFound as epnf:
                    print("Request failed - 404 Not found")
                    with open("article_failed.txt", "a", encoding="utf-8") as err:
                        err.write(f"-{element} : Error 404\n\n")
                    continue
                except QueryBadFormed as eqbf:
                    print("Request Failed - 400 Bad Query formed")
                    with open("article_failed.txt", "a", encoding="utf-8") as err:
                        err.write(f"-{element} : Error 400\n\n")
                    continue


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
                            res.append(f"dc:issued \"{convert_date(x,i)}\"^^xsd:gYear;")
                        else:
                            res.append(x)
                if not res:
                    print("Empty response article")
                    with open("article_failed.txt", "a", encoding="utf-8") as err:
                        err.write(f"-{element} - Empty article\n\n")

                f.write("\n".join(res))
                f.write("\n")



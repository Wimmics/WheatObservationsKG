# Wheat Observations KG

The **Wheat Observations KG** is a Knowledge Graph that exploits the Semantic Web technologies to represent and publish the phenotypic observations made on wheat crops.

This repository provides the observations (CSV files), as well as the scripts necessary to translate the CSV files into an RDF knowledge graph (see folder [observations](observations)).

The RDF representation relies on two main vocabularies:
- the **CO_321 Wheat Crop Ontology**, of which we produce a version in OWL and SKOS (see folder [co321](co321)),
- the [Plant Phenotype Experiment Ontology](https://agroportal.lirmm.fr/ontologies/PPEO) (PPEO).


## Generation pipeline

The following slides (in French) provide details about how to generate the RDF data from the csv files representing the Observations.

https://docs.google.com/presentation/d/1tghnfjY5snZ91daxx40uco3YTfqHV3bL_62Gxcr-Zv8


## Environment
- Python 3.7 or above
- Java 11 or above
- Pandas 1.4.3
- Numpy 1.23.1
- MongoDB 1.32.5
- Morph-xR2RML

All scripts were developped on Windows 10.


## License

The code, scripts and mapping rules used to produce the knowledge graph are licensed under the terms of the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

The RDF data files produced by the code are made available under the terms of the [Etalab 2.0](https://spdx.org/licenses/etalab-2.0.html) license.

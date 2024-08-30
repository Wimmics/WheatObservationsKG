# Wheat Observations KG

## Context


The [Genetic and Genomic Information System (GnpIS)](https://urgi.versailles.inrae.fr/gnpis/) 
handles different types of data in the scope of genetics and genomics for plants including forest trees.

Soft wheat phenotype observations data are integrated in GnpIS including the result of observation campaigns carried out on micro-parcels located in France between 1999 and 2015.
The representation relies on the [Plant Phenotype Experiment Ontology](https://agroportal.lirmm.fr/ontologies/PPEO) (PPEO) and the [CO_321 Wheat Crop Ontology](co321).

Each observation is part of a study carried out by an institution on a crop site using certain biological material. The biological material is a seed with an accession number which is an approved identifier of a wheat species/variety.
Each observation precisely and formally documents the location of the micro-parcel, the measurement method, the phenotype measurement scale, the plant development stage and the organ being observed.

# What's in this repository?

This repository provides the set of tools and data used to generate the **Wheat Observations KG**, an RDF Knowledge Graph that represents the phenotypic observations extracted from GnpIS.
This repository consists of:
- the **raw observation files** in CSV format (see folder [observations/csv](observations/csv))
- a **dump of the Wheat Observations KG in the RDF Turtle syntax** (see folder [observations/dataset](observations/dataset))
- the mapping rules used to translate the CSV files into an RDF knowledge graph (see folder [observations/xr2rml_mapping_rules](observations/xr2rml_mapping_rules))
- the **CO_321 Wheat Crop Ontology** of which we produce a version in OWL and SKOS (see folder [co321](co321))



## Generation pipeline

The following slides (in French) provide details about how to generate the RDF data from the csv files representing the observations:
https://docs.google.com/presentation/d/1tghnfjY5snZ91daxx40uco3YTfqHV3bL_62Gxcr-Zv8

Furthermore, folder [co321](co321) provides the material to generate the CO_321 Wheat Crop Ontology in OWL and SKOS.


## Environment
- Python 3.7 or above
- Java 11 or above
- Pandas 1.4.3
- Numpy 1.23.1
- MongoDB 1.32.5
- Morph-xR2RML

All scripts were developed on Windows 10.


## License

The code, scripts and mapping rules used to produce the knowledge graph are licensed under the terms of the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

The RDF data files produced by the code are made available under the terms of the [Etalab 2.0](https://spdx.org/licenses/etalab-2.0.html) license.

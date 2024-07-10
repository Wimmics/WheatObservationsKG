# Lifting CO_321 to OWL/SKOS

This folder provides:
- the **CO_321 Wheat Crop Ontology** as a CSV file: `CO_321-Wheat Crop Ontology.csv`
- the scripts necessary to translate it into an RDF knowledge graph using OWL and SKOS,
- the result RDF files in folder [dataset](dataset).


## Generation pipeline

- Preprocessing: script `tranform_co_csv.py` transforms file `CO_321-Wheat Crop Ontology.csv` into multiple CSV files stored in folrder [output](output).
- Load files `output/*.csv` as separate collections in a MongoDB instance. Collection names follow the Camel Case naming convention.
- The final translation to RDF is carried out using [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml/), an implementation of the [xR2RML mapping language](http://i3s.unice.fr/~fmichel/xr2rml_specification.html) for MongoDB databases. 
The mapping file is provided in directory [xr2rml_mapping_rules](xr2rml_mapping_rules).
- The result RDF files are stored in folder [dataset](dataset) together with metadata.

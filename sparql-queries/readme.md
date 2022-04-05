

# Exemple de requête SPARQL

[TOC]

```turtle
select distinct ?docu where {
?x a oa:Annotation;
oa:hasTarget ?y;
oa:hasBody ?e .
?y oa:hasSource ?d .
?e skos:prefLabel ?a .
?d frbr:partOf/frbr:partOf ?docu .
filter (?a = "Lr34") .
}
```



## 0. Préfixes utilisés

```turtle
prefix rr:      <http://www.w3.org/ns/r2rml#> .
prefix schema:  <http://schema.org/> .
prefix bioT:    <http://purl.org/biotop/biotop.owl#> .
prefix owl:     <http://www.w3.org/2002/07/owl#> .
prefix issap:   <http://ns.inria.fr/issa/property/> .
prefix d2kab:   <http://ns.inria.fr/d2kab/> .
prefix dce:     <http://purl.org/dc/elements/1.1/> .
prefix fabio:   <http://purl.org/spar/fabio/> .
prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
prefix frbr:    <http://purl.org/vocab/frbr/core#> .
prefix ncbi:    <http://identifiers.org/taxonomy/> .
prefix rml:     <http://semweb.mmlab.be/ns/rml#> .
prefix oa:      <http://www.w3.org/ns/oa#> .
prefix dct:     <http://purl.org/dc/terms/> .
prefix xrr:     <http://i3s.unice.fr/xr2rml#> .
prefix bibo:    <http://purl.org/ontology/bibo/> .
prefix prov:    <http://www.w3.org/ns/prov#> .
prefix obo:     <http://purl.obolibrary.org/obo/> .
prefix foaf:    <http://xmlns.com/foaf/0.1/> .
```



## 1. Quels documents mentionnent le gène {x} ?

* __Variable__: gène, exemple: *“Lr34”*, *“Pm21”*, *“Sr31”* => **?a**

* __Sortie__: Document => **?d**

* __Intention__: Bibliographie sur un gène donné.

* __Requête__:

  ```turtle
  select distinct ?docu where {
    ?x a oa:Annotation; 
     oa:hasTarget ?y;
     oa:hasBody ?e .
    ?y oa:hasSource ?d .
    ?e skos:prefLabel ?a .
    ?d frbr:partOf+ ?docu .
    ?docu a fabio:ResearchPaper .
    filter (?a =   "Lr34") .
  }
  ```

* __Résultat__:

| Row  | ?d                                                       |
| ---- | -------------------------------------------------------- |
| 1    | <http://ns.inria.fr/d2kab/article/28005310               |
| 2    | <http://ns.inria.fr/d2kab/article/18074114>              |
| 3    | <http://ns.inria.fr/d2kab/article/31506776>              |
| 4    | <http://ns.inria.fr/d2kab/article/16896711>              |
| 5    | <http://ns.inria.fr/d2kab/article/21265893>              |
| 6    | <http://ns.inria.fr/d2kab/article/32281004#articletitle> |

## 2. Quels gènes sont mentionnés à proximité de *{phenotype}*? +source

* __Variable:__ *{phenotype}*, 

  * exemples: *“resistance to Powdery Mildew”*, *“crop yield”*, *“drought tolerance”*, *“protein content of seed”*.

* __Sortie:__ (gène, document)

* __Remarques:__ 

  * *“X à proximité de Y”* peut signifier deux choses:
    * X* et *Y* sont dans le même document, ou
    * *X* et *Y* sont dans le même document et distants de moins de N caractères dans la même partie de document.
  * “Source” == document

* __Intention:__ Rechercher les gènes impliqués dans le contrôle d’un phénotype donné.

* __Requête__: Même document

  ```turtle
  select distinct ?label  ?docu where {
    ?x1 a oa:Annotation; 
     oa:hasTarget ?y1;
     oa:hasBody ?e1 .
    ?y1 oa:hasSource ?d1 .
    ?e1 skos:prefLabel ?a ;
        a d2kab:Phenotype.
    ?x2 a oa:Annotation ;
           oa:hasTarget ?y2 ;
           oa:hasBody ?e2 .
    ?y2 oa:hasSource ?d2 .
    ?e2 a d2kab:Gene ;
           skos:prefLabel ?label.
    ?d1 frbr:partOf+ ?docu .
    ?d2 frbr:partOf+ ?docu .
    ?docu  a fabio:ResearchPaper .
    filter (?a =   "crop yield") .
  }
  ```

  

* __Résultat__:

  | Gene  | Document                                    |
  | ----- | ------------------------------------------- |
  | Gb7   | <http://ns.inria.fr/d2kab/article/28624908  |
  | H32   | <http://ns.inria.fr/d2kab/article/24737716  |
  | W7984 | <http://ns.inria.fr/d2kab/article/24186257> |
  | Kna1  | <http://ns.inria.fr/d2kab/article/29545269> |

  

  

## 3. Quels marqueurs sont mentionnés à proximité d’un gène, qui est lui-même mentionné à proximité de *{phenotype}*? +source

* **Variable**: *{phenotype}*, exemples: *“resistance to Powdery Mildew”*, *“crop yield”*, *“drought tolerance”*, *“protein content of seed”*.

* **Sortie**: (marqueur, gène, document, document)

* **Remarque**: La proximité marqueur-gène peut ne pas être dans le même document que la proximité gène-phénotype. (Ce qui explique deux documents en sortie).

* **Intention**: Recherche des marqueurs qui pourraient servir à sélectionner un phénotype donné.

* __Requête__:

  ```turtle
  select distinct ?gene ?marker  ?doc1 ?doc2 where {
    ?x1 a oa:Annotation; 
     oa:hasTarget ?y1;
     oa:hasBody ?e1 .
    ?y1 oa:hasSource ?d1 .
    ?e1 skos:prefLabel ?a ;
        a d2kab:Phenotype .
  
    ?x2 a oa:Annotation ;
           oa:hasTarget ?y2 ;
           oa:hasBody ?e2 .
    ?y2 oa:hasSource ?d2 .
    ?e2 a d2kab:Gene ;
           skos:prefLabel ?gene.
  
    ?x3 a oa:Annotation ;
           oa:hasTarget ?y3 ;
           oa:hasBody ?e3 .
     ?y3 oa:hasSource ?d3 .
     ?e3 a d2kab:Marker ;
            skos:prefLabel ?marker .
     
    ?x4 a oa:Annotation ;
           oa:hasTarget ?y4 ;
           oa:hasBody ?e2 .
    ?y4 oa:hasSource ?d4 .
  
    ?d1 frbr:partOf+ ?doc1 .
    ?d2 frbr:partOf+ ?doc1 .
    ?d3 frbr:partOf+ ?doc2 .
    ?d4 frbr:partOf+ ?doc2 .
    ?doc1  a fabio:ResearchPaper .
    ?doc2  a fabio:ResearchPaper .
    filter (?a =   "crop yield") .
  }
  ```

  

* __Résultat__:

  | ?gene | ?marker | ?doc1                                       | ?doc2                                       |
  | ----- | ------- | ------------------------------------------- | ------------------------------------------- |
  | W7984 | Xgwm664 | <http://ns.inria.fr/d2kab/article/28624908> | <http://ns.inria.fr/d2kab/article/28955354> |
  | W7984 | Xgwm645 | <http://ns.inria.fr/d2kab/article/28624908> | <http://ns.inria.fr/d2kab/article/28955354> |
  | Rht   | WMC617  | <http://ns.inria.fr/d2kab/article/29545269> | <http://ns.inria.fr/d2kab/article/19132076> |
  
  

### 3-1. (Nécessite la complétion de result_article avec l'API)

Comme **[3]** mais dont l’année de publication du document qui mentionne le marqueur est ultérieure à 2010.

* **Intention**: Les articles trop vieux utilisaient des techniques de marquage génétique qui sont devenues obsolètes.

* __Requête__:

  ```turtle
  select distinct ?gene ?marker  ?doc1 ?doc2 where {
    ?x1 a oa:Annotation; 
     oa:hasTarget ?y1;
     oa:hasBody ?e1 .
    ?y1 oa:hasSource ?d1 .
    ?e1 skos:prefLabel ?a .
  
    ?x2 a oa:Annotation ;
           oa:hasTarget ?y2 ;
           oa:hasBody ?e2 .
    ?y2 oa:hasSource ?d1 .
    ?e2 a d2kab:Gene ;
           skos:prefLabel ?gene.
  
    ?x3 a oa:Annotation ;
           oa:hasTarget ?y3 ;
           oa:hasBody ?e3 .
     ?y3 oa:hasSource ?d2 .
     ?e3 a d2kab:Marker ;
            skos:prefLabel ?marker .
     
    ?x4 a oa:Annotation ;
           oa:hasTarget ?y4 ;
           oa:hasBody ?e2 .
    ?y4 oa:hasSource ?d2 .
  
    ?d1 frbr:partOf+ ?doc1 .
    ?d2 frbr:partOf+ ?doc1 .
    ?d3 frbr:partOf+ ?doc2 .
    ?d4 frbr:partOf+ ?doc2 .
    ?doc2 dct:issued ?date.
    ?doc1  a fabio:ResearchPaper .
    ?doc2  a fabio:ResearchPaper .
    filter (?a =   "crop yield") .
    filter (year(?date) > 2010) .
  }
  ```

  

* __Résultat__:

  ```turtl
  "NON testé"
  ```

  

## 4. Quelles variétés présentent un <phenotype> donné? +source

* **Variable: **{phenotype}, exemples: *“resistance to Powdery Mildew”*, *“crop yield”*, *“drought tolerance”*, *“protein content of seed”*.

* **Sortie**: (variété, document)

* **Remarque**: Il s’agit de la relation *<variety_has_phenotype>*.

* **Intention**: Recherche des variétés d’intérêt car présentant un phénotype donné.

* __Requête__:

  ```turtle
  select distinct ?var  ?doc where {
    ?rel1 d2kab:hasVariety ?ano1 ;
             d2kab:hasPhenotype ?ano2 .
    
    ?ano1 a oa:Annotation ;
               oa:hasTarget ?t1 ;
               oa:hasBody ?e1 .
    ?t1 oa:hasSource ?d1 .
  
    ?e1 a d2kab:Variety ;
           skos:prefLabel ?var.
  
    ?ano2 a oa:Annotation ;
               oa:hasTarget ?t2 ;
               oa:hasBody ?e2 .
    ?t2 oa:hasSource ?d2 .
  
    ?e2 skos:prefLabel ?a ;
        a d2kab:Phenotype .
  
    ?d1 frbr:partOf+ ?doc .
    ?d2 frbr:partOf+ ?doc . # Pas nécessaire car l'annotation est dans le même doc
    ?doc  a fabio:ResearchPaper .
    filter (?a = "crop yield") .
  }
  ```

  

* __Résultat__:

  | Variété | Document                                    |
  | ------- | ------------------------------------------- |
  | Scout   | <http://ns.inria.fr/d2kab/article/32652543> |
  | Gazul   | <http://ns.inria.fr/d2kab/article/29093532> |
  | Scout   | <http://ns.inria.fr/d2kab/article/32652543> |
  
  

### 4-1. Quelles variétés présentent un <phenotype> donné et un <taxon> donné?

Comme **[4]** mais seulement dans les documents qui mentionnent aussi le blé d’été (Taxon: *Triticum aestivum*).

* **Intention**: Intéressé par les variétés de blé.

* __Requête__:

  ```SPARQL
  select ?var  ?doc where {
    ?rel1 d2kab:hasVariety ?ano1 ;
             d2kab:hasPhenotype ?ano2 .
    
    ?ano1 a oa:Annotation ;
               oa:hasTarget ?t1 ;
               oa:hasBody ?e1 .
    ?t1 oa:hasSource ?d1 .
  
    ?e1 a d2kab:Variety ;
           skos:prefLabel ?var.
  
    ?ano2 a oa:Annotation ;
               oa:hasTarget ?t2 ;
               oa:hasBody ?e2 .
    ?t2 oa:hasSource ?d2 .
  
    ?e2 skos:prefLabel ?a ;
        a d2kab:Phenotype .
  
    ?ano3 a oa:Annotation ;
                  oa:hasTarget ?t3 ;
                  oa:hasBody ?e3 .
    ?t3 oa:hasSource ?d3 .
  
    ?e3 skos:prefLabel ?label .
  
    ?d1 frbr:partOf+ ?doc .
    ?d2 frbr:partOf+ ?doc .
    ?d3 frbr:partOf+ ?doc .
    ?doc a fabio:ResearchPaper .
    filter (?a = "crop yield") .
    filter (contains(?label, "Triticum aestivum")) .
  }
  ```

  

* __Résultat__:

  | Scout | <http://ns.inria.fr/d2kab/article/32652543> |
  | ----- | ------------------------------------------- |
  | Gazul | <http://ns.inria.fr/d2kab/article/29093532> |

  

### 4-2. Quelles variétés présentent un <phenotype> donné et un <taxon> donné à l'exclusion de tout autre taxon?

Comme **[4]** mais seulement dans les documents dont le seul taxon mentionné est le blé d’été (*Triticum aestivum*).

**(requête minus filter pour éliminer les documents qui on plus de taxon)**

**res => (Les documents qui mentionne le taxon X - les documents qui mentionne aussi les Taxon Y's)**

* **Intention**: Intéressé **que** par les variétés de blé.

* __Requête__:

  ```turtle
  select distinct ?var  ?doc where {
    ?rel1 d2kab:hasVariety ?ano1 ;
          d2kab:hasPhenotype ?ano2 .
    
    ?ano1 a oa:Annotation ;
            oa:hasTarget ?t1 ;
            oa:hasBody ?e1 .
    ?t1 oa:hasSource ?d1 .
  
    ?e1 a d2kab:Variety ;
           skos:prefLabel ?var.
  
    ?ano2 a oa:Annotation ;
               oa:hasTarget ?t2 ;
               oa:hasBody ?e2 .
    ?t2 oa:hasSource ?d2 .
  
    ?e2 skos:prefLabel ?a .
  
    ?ano3 a oa:Annotation ;
                  oa:hasTarget ?t3 ;
                  oa:hasBody ?e3 .
    ?t3 oa:hasSource ?d3 .
  
    ?e3 skos:prefLabel ?label .
  
    ?d1 frbr:partOf+ ?doc .
    ?d2 frbr:partOf+ ?doc .
    ?d3 frbr:partOf+ ?doc .
    ?doc a fabio:ResearchPaper .
    MINUS {
  	?anoM a oa:Annotation ;
               	oa:hasTarget ?tar ;
               	oa:hasBody ?body .
    	?tar oa:hasSource ?d4 .
  	
  	?body a d2kab:Taxon;
  	skos:prefLabel ?s .
      ?d4 frbr:partOf+ ?doc .
  	filter (?s != "Triticum aestivum")
    }
    filter (?a = "crop yield") .
    filter (contains(?label, "Triticum aestivum")) .
  }
  ```

  

* __Résultat__:

  ```turtl
  
  ```

  

### 4-3. Quelles variétés présentent un <phenotype> donné et un <taxon> donné à l'exclusion de tout autre taxon?

Comme **[4]** mais seulement dans les documents dont le seul taxon de plante (*Magnoliopsida*) mentionné est le blé d’été (*Triticum aestivum*).

* **Intention**: Intéressé **que** par les variétés de blé, tout en n’excluant pas les documents qui mentionnent des taxons champignons.

* __Requête__:

  ```turtle
  select distinct ?var  ?doc where {
    ?rel1 d2kab:hasVariety ?ano1 ;
          d2kab:hasPhenotype ?ano2 .
    
    ?ano1 a oa:Annotation ;
            oa:hasTarget ?t1 ;
            oa:hasBody ?e1 .
    ?t1 oa:hasSource ?d1 .
  
    ?e1 a d2kab:Variety ;
           skos:prefLabel ?var.
  
    ?ano2 a oa:Annotation ;
               oa:hasTarget ?t2 ;
               oa:hasBody ?e2 .
    ?t2 oa:hasSource ?d2 .
  
    ?e2 skos:prefLabel ?a .
  
    ?ano3 a oa:Annotation ;
                  oa:hasTarget ?t3 ;
                  oa:hasBody ?e3 .
    ?t3 oa:hasSource ?d3 .
  
    ?e3 skos:prefLabel ?label .
  
    ?d1 frbr:partOf+ ?doc .
    ?d2 frbr:partOf+ ?doc .
    ?d3 frbr:partOf+ ?doc .
    ?doc a fabio:ResearchPaper.
    MINUS {
  	?anoM a oa:Annotation ;
               	oa:hasTarget ?tar ;
               	oa:hasBody ?body .
    	?tar oa:hasSource ?doc .
  	
  	
      { 
        ?body a d2kab:Taxon;
  	        skos:prefLabel ?s .
        ?e3 skos:narrower+ ?body .
      }
      union
      {  
        
        ?body a d2kab:Taxon;
  	        skos:prefLabel ?s .
      }
  	filter (?s = "Magnoliopsida")
    }
    filter (?a = "crop yield") .
    filter (contains(?label, "Triticum aestivum")) .
  }
  ```

  

* __Résultat__:

  ```turtl
  
  ```

  

### 4-4

Comme **[4]** mais en prenant en compte les sous-concepts de *{phenotype}*.

* **Sortie**: (gène, phénotype, document)
  
  * <u>Exemple</u>: *“pathogen resistance”*
  
* **Intention**: Recherche des variétés d’intérêt car présentant un phénotype général donné.

* Question:

* __Requête__:

  ```SPARQL
  SELECT distinct  ?doc ?gene ?variety  
  WHERE {
  ?rel1 d2kab:hasVariety ?aVariety ;
      d2kab:hasPhenotype ?aPhenotype.
   
  ?aVariety a oa:Annotation ;
              oa:hasTarget ?t1 ;
              oa:hasBody ?Variety .
  ?t1 oa:hasSource ?d1 .
  ?Variety a d2kab:Variety ;
          skos:prefLabel ?variety.
  ?aPhenotype a oa:Annotation ;
              oa:hasTarget ?t2 ;
              oa:hasBody ?Phenotype .
  ?t2 oa:hasSource ?d2 .
  ?e2 skos:prefLabel "pathogen resistance" ;
      skos:narrower* ?Phenotype .
  ?aTaxon a oa:Annotation ;
          oa:hasTarget ?t ;
          oa:hasBody ?Taxon.
  ?t oa:hasSource ?d .
  ?Taxon a d2kab:Taxon ;
          skos:prefLabel "Triticum aestivum".
  ?aGene a oa:Annotation ;
          oa:hasTarget ?t3;
          oa:hasBody ?Gene.
  ?t3 oa:hasSource ?d3 .
  ?Gene a d2kab:Gene ;
          skos:prefLabel ?gene.
  ?d1 frbr:partOf+ ?doc .
  ?d2 frbr:partOf+ ?doc .
  ?d3 frbr:partOf+ ?doc .
  ?d frbr:partOf+ ?doc .
  ?doc  a fabio:ResearchPaper .
  }
  
  ```
  
  
  
* __Résultat__:

  ```turtl
  
  ```




<u>Demande: Nom variable plus explicite!!!</u>


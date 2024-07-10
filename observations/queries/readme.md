- Quelles sont les variables observées dont le trait est une maladie par année et par lieu, pour les accessions “Charger”, “Apache” et “Tremie”?

Le résultat attendu est l’ensemble des variables d’observation qui ont pour trait observé une maladie répertoriée dans l’ontologie CO_321 pour les graines "Charger", "Apache" et "Tremie". L’intention de cette requête est de relever l’impact du trait de maladie sur le blé suivant les conditions de pousse.

```SPARQL
SELECT DISTINCT ?study ?date ?trait ?name ?label WHERE {
	?study a ppeo:study; ppeo:hasEndDateTime ?date.
	?obs a sosa:Observation; 
             ppeo:hasObservedSubject ?observationUnit;
            sosa:hasFeatureOfInterest ?trait; 
             sosa:observedProperty ?variable.
        ?trait a CO_321:BioticStressTrait; skos:prefLabel ?name.
	?variable a CO_321:Variable; skos:prefLabel ?label.
	?observationUnit a ppeo:observation_unit; 
                         ppeo:hasBiologicalMaterial ?biologicalMaterial; 
                         ppeo:partOf ?study.
        ?biologicalMaterial a ppeo:biological_material; 
                            ppeo:hasAccessionName ?accession.
FILTER(?accession in ("CHARGER", "APACHE", "TREMIE")). 
}
```

| Date      | Trait          | Nom du trait                      | Nom de la variable |
| --------- | -------------- | --------------------------------- | ------------------ |
| 2006-07-3 | CO_321/0000919 | Septoria tritici blotch incidence | ST-SCORE_score     |
| 2008-07-3 | CO_321/0000937 | Powdery mildew incidence          | PM-SCORE_score     |
| 2008-07-3 | CO_321/0000687 | Leaf rust notes                   | rb                 |
| 2008-07-3 | CO_321/0000907 | Stripe rust notes                 | YR-SCORE\_score    |



- Quelles sont les études pour lesquelles on observe des mesures pour les variables “frost” et “lodging”?

```SPARQL
SELECT DISTINCT ?study ?variableName
WHERE {
	?study a ppeo:study; ppeo:hasEndDateTime ?date.

	?observationUnit a ppeo:observation_unit;          
                         ppeo:hasBiologicalMaterial ?biologicalMaterial; 
                         ppeo:partOf ?study.

        ?biologicalMaterial a ppeo:biological_material;
                            ppeo:hasAccessionName ?accession.

	?observation a sosa:Observation; 
                    sosa:observedProperty ?variable;  ppeo:hasObservedSubject ?observationUnit.

	?variable a CO_321:Variable; skos:altLabel ?variableName.

        FILTER(regex(str(?variableName), "Frost")  || regex(str(?variableName), "lodging"))

}
```



- Quelles sont les accessions qui sont testées plus de 5 années consécutives dans l’ensemble du dataset?

```SPARQL
SELECT DISTINCT ?accession  WHERE{ 
  ?bioMat ppeo:hasAccessionName ?accession.

  ?s1 a ppeo:study; ppeo:hasEndDateTime ?d1.
  ?s2 a ppeo:study; ppeo:hasEndDateTime ?d2.
  ?s3 a ppeo:study; ppeo:hasEndDateTime ?d3.
  ?s4 a ppeo:study; ppeo:hasEndDateTime ?d4.
  ?s5 a ppeo:study; ppeo:hasEndDateTime ?d5.

  ?obsUnit1 a ppeo:observation_unit; 
	ppeo:partOf ?s1; 
	ppeo:hasBiologicalMaterial ?bioMat.
  ?obsUnit2 a ppeo:observation_unit; 
	ppeo:partOf ?s2; 
	ppeo:hasBiologicalMaterial ?bioMat.
  ?obsUnit3 a ppeo:observation_unit; 
	ppeo:partOf ?s3; 
	ppeo:hasBiologicalMaterial ?bioMat.
  ?obsUnit4 a ppeo:observation_unit; 
	ppeo:partOf ?s4; 
	ppeo:hasBiologicalMaterial ?bioMat.
  ?obsUnit5 a ppeo:observation_unit; 
	ppeo:partOf ?s5; 
	ppeo:hasBiologicalMaterial ?bioMat.
  
    filter(year(?d1) - year(?d2) = 1)
    filter(year(?d2) - year(?d3) = 1)
    filter(year(?d3) - year(?d4) = 1)
    filter(year(?d4) - year(?d5) = 1)
} 
```



- Quelles sont les accessions qui font l’objet d’un changement d’investigation d’une study à l’autre (eg. de INRA Wheat Network not BRC accession (B and C series) à INRA Small Grain Cereals Network)

```SPARQL
SELECT ?accession WHERE {
  ?study1 a ppeo:study; ppeo:partOf ?investigation1.
  ?investigation1 a ppeo:investigation; ppeo:hasName ?network1.
  ?investigation2 a ppeo:investigation; ppeo:hasName ?network2.
  ?study2 a ppeo:study; ppeo:partOf ?investigation2.
  ?obsUnit1 a ppeo:observation_unit; ppeo:hasBiologicalMaterial ?bioMat; ppeo:partOf ?study1.
  ?obsUnit2 a ppeo:observation_unit; ppeo:hasBiologicalMaterial ?bioMat; ppeo:partOf ?study2.
  ?bioMat a ppeo:biological_material; ppeo:hasAccessionName ?accession.
  filter(?network1 = "INRA Small Grain Cereals Network")
  filter(?network2 = "INRA Wheat Network not BRC accession (B and C series)")
}
```


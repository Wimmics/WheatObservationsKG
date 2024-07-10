import os
import glob
import pandas as pd
import re
import numpy as np
import hashlib

NAMESPACE = "http://www.cropontology.org/rdf/CO_321/"
variable_label = ["id", "name", "context", "stage", "xref", "date", "trait", "method", "scale"]
entity_synonyme_label = ["id", "synonym"]
trait_label = ["id", "name", "class", "description", "entity", "attribute", "xref"]
method_label = ["id", "name", "class", "description", "formula", "reference"]
scale_label = ["id", "name", "class", "decimal", "upper", "lower"]
concept_label = ["id", "value", "description"]



def make_variable(dataframe):
    list_data = list()
    for row in dataframe.index:
        data = list()

        data.append(dataframe["Variable ID"][row].split(":")[1])
        data.append(dataframe["Variable name"][row])
        data.append(dataframe["Context of use"][row])
        data.append(dataframe["Growth stage"][row])
        data.append(dataframe["Variable Xref"][row])
        data.append(dataframe["Date"][row])
        data.append(dataframe["Trait ID"][row].split(":")[1])
        data.append(dataframe["Method ID"][row].split(":")[1])
        data.append(dataframe["Scale ID"][row].split(":")[1])

        list_data.append(data)
    return list_data

def make_variable_synonyme(dataframe):
    list_data = list()
    for row in dataframe.index:
        if pd.isnull(dataframe["Variable synonyms"][row]) :
            continue
        else:
            for synonyme in dataframe["Variable synonyms"][row].split(","):
                data = list()

                data.append(dataframe["Variable ID"][row].split(":")[1])
                data.append(synonyme.strip())

                list_data.append(data)

    return list_data


def make_trait(dataframe):
    list_data = list()
    #["id", "name", "class", "description", "entity", "attribute", "xref"]
    for row in dataframe.index:
        data = list()

        data.append(dataframe["Trait ID"][row].split(":")[1])
        data.append(dataframe["Trait name"][row])
        data.append(f"{dataframe['Trait class'][row].title().replace(' ','')}Trait")
        data.append(dataframe["Trait description"][row])
        data.append(dataframe["Entity"][row])
        data.append(dataframe["Attribute"][row])
        data.append(dataframe["Trait Xref"][row])

        list_data.append(data)
    return list_data

def make_trait_synonyme(dataframe):
    list_data = list()

    for row in dataframe.index:
        if pd.notnull(dataframe["Trait synonyms"][row]):
            for synonyme in dataframe["Trait synonyms"][row].split(","):
                data = list()
                data.append(dataframe["Trait ID"][row].split(":")[1])
                data.append(synonyme)
                list_data.append(data)
        if pd.notnull(dataframe["Main trait abbreviation"][row]):
            data = list()
            data.append(dataframe["Trait ID"][row].split(":")[1])
            data.append(dataframe["Main trait abbreviation"][row])
            list_data.append(data)
        if pd.notnull(dataframe["Alternative trait abbreviations"][row]):
            for synonyme in dataframe["Alternative trait abbreviations"][row].split(","):
                data = list()
                data.append(dataframe["Trait ID"][row].split(":")[1])
                data.append(synonyme)
                list_data.append(data)
    return list_data


def make_method(dataframe):
    #["id", "name", "class", "description", "formula", "reference"]
    list_data = list()
    for row in dataframe.index:
        data = list()

        data.append(dataframe["Method ID"][row].split(":")[1])
        data.append(dataframe["Method name"][row])
        data.append(f"{dataframe['Method class'][row]}Method")
        data.append(dataframe["Method description"][row])
        data.append(dataframe["Formula"][row])
        data.append(dataframe["Method reference"][row])

        list_data.append(data)
    return list_data


def make_scale(dataframe):
    #["id", "name", "class", "decimal", "upper", "lower"]
    list_data = list()
    for row in dataframe.index:
        data = list()

        data.append(dataframe["Scale ID"][row].split(":")[1])
        data.append(dataframe["Scale name"][row])
        data.append(f'{dataframe["Scale class"][row]}Scale')
        data.append(dataframe["Decimal places"][row])
        data.append(dataframe["Lower limit"][row])
        data.append(dataframe["Upper limit"][row])

        list_data.append(data)
    return list_data


def make_concept_scale(dataframe):
    list_data = list()
    #["id", "value", "description"]

    for row in dataframe.index:

        if dataframe["Scale class"][row] in ["Ordinal", "Nominal"]:
            ordinal_value = co_dataframe.iloc[:, 37:]
            for column in ordinal_value.columns:
                data = list()
                if pd.isnull(dataframe[column][row]):
                    continue
                data.append(dataframe["Scale ID"][row].split(":")[1])
                try:
                    number, description = dataframe[column][row].replace(":", "=").split("=", 1)
                except:
                    print(dataframe[column][row], "Error")

                data.append(number.strip())
                if description == "":
                    data.append("No Description")
                else:
                    data.append(description.strip())
                list_data.append(data)
    return list_data


if __name__ == '__main__':

    co_dataframe = pd.read_csv("CO_321-Wheat Crop Ontology.csv", sep=";")
    variable_data = make_variable(co_dataframe)
    variable_synonyme_data = make_variable_synonyme(co_dataframe)

    trait_data = make_trait(co_dataframe)
    trait_synonyme_data = make_trait_synonyme(co_dataframe)

    method_data = make_method(co_dataframe)

    scale_data = make_scale(co_dataframe)
    ordinal_data = make_concept_scale(co_dataframe)

    pd.DataFrame(variable_data, columns=variable_label).to_csv("output/variable.csv", index=False, encoding="UTF-8")
    pd.DataFrame(variable_synonyme_data, columns=entity_synonyme_label).to_csv("variable_synonyme.csv", index=False, encoding="UTF-8")
    pd.DataFrame(trait_data, columns=trait_label).to_csv("trait.csv", index=False, encoding="UTF-8")
    pd.DataFrame(trait_synonyme_data, columns=entity_synonyme_label).to_csv("trait_synonyme.csv", index=False, encoding="UTF-8")
    pd.DataFrame(method_data, columns=method_label).to_csv("method.csv", index=False, encoding="UTF-8")
    pd.DataFrame(scale_data, columns=scale_label).fillna(0).to_csv("scale.csv", index=False, encoding="UTF-8")
    pd.DataFrame(ordinal_data, columns=concept_label).to_csv("scale_value.csv", index=False, encoding="UTF-8")
    #print(variable_data)
    #print(variable_synonyme_data)
    #print(trait_data)
    #print(scale_data)
    #print(ordinal_data)
    #print(trait_synonyme_data)
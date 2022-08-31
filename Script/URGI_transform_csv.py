import os
import glob
import pandas as pd
import numpy as np
import hashlib
import json
import time

NAMESPACE = "http://www.urgi.versailles.inrae.fr/"
FRANCE_URI = "http://wikidata/org/entity/Q142"
URI = {
    "study": f"{NAMESPACE}study/",
    "biological": f"{NAMESPACE}biological_material/",
    "observation": f"observation/",
    "observation_unit": f"{NAMESPACE}observation_unit/",
    "observation_level": f"{NAMESPACE}observation_level/",
    "factor_value": f"{NAMESPACE}factor_value/",
    "factor": f"{NAMESPACE}factor/"
}

variable_not_found = set()


studies_label = ["study_id", "study_name", "start_date", "end_date", "description"]
biological_label = ["biological_id", "genus", "species", "subspecies", "accession_number", "accession_name", "material_source_id", "material_source_doi"]
observation_unit_label = ["id", "study", "biological", "observation_level", "observation_level_number", "factor_mode", "factor_value"]
observation_label = ["observation_unit", "observation_id", "variable", "trait","method", "scale", "value"]

factor_label = ["uri_factor", "uri_factor_value", "factor", "factor_value", "factor_name", "description"]
person_label = ["type", "name", "email", "institution"]
gps_label = ["study", "site", "latitude", "longitude", "altitude"]


def extract_variable_dict(dataframe):
    variable_co = dict()
    trait_co = dict()
    method_co = dict()
    scale_co = dict()
    dataframe.fillna("", inplace=True)

    for row in dataframe.index:
        name = dataframe["Variable name"][row]
        variable_co[name] = dataframe["Variable ID"][row]
        trait_co[dataframe["Variable ID"][row]] = dataframe["Trait ID"][row]
        method_co[dataframe["Variable ID"][row]] = dataframe["Method ID"][row]
        scale_co[dataframe["Variable ID"][row]] = dataframe["Scale ID"][row]
        synonyms = dataframe["Variable synonyms"][row]
        if synonyms == "":
            continue
        for elt in dataframe["Variable synonyms"][row].split(","):
            variable_co[elt.strip()] = dataframe["Variable ID"][row].strip()

    print(variable_co)

    return variable_co, trait_co, method_co, scale_co

def extract_factor(json_array):
    dict_value = eval(json_array)[0]
    return dict_value["factor"], dict_value["modality"]

def extract_observation(json_array):
    dict_value = eval(json_array)
    return dict_value

def co_321_uri_maker(uri):
    return f"http://www.cropontology.org/rdf/CO_321/{uri.split(':')[1]}"


def encoding_resolve(string):
    return string.replace("Ã©", "é")

def uri_hash_maker(to_hash):
    """
    Create an URI with the namespace and the associated id as hash
    :param to_hash:string
    :param ns:string
    :return string:
    """
    enc = hashlib.sha1()
    enc.update(to_hash.encode('utf-8'))
    #
    return f"{enc.hexdigest()}"
    #return f"{ns}{enc.hexdigest().upper()}"


def study_maker(dataframe):
    """
    NOTE: THIS IS THE STUDY!!
    Create data for trial CSV
    The columns label are ["study_id", "study_name", "start_date", "end_date", "description"]
    :param dataframe:DataFrame
    :return: data:List
    """
    list_data = list()
    for row_elt in dataframe.index:

        data = list()

        data.append(uri_hash_maker(dataframe["study_unique_id"][row_elt]))
        data.append(dataframe["study_title"][row_elt])
        data.append(dataframe["start_date_of_study"][row_elt])
        data.append(dataframe["end_date_of_study"][row_elt])
        data.append(dataframe["description_of_growth_facilty"][row_elt])

        list_data.append(data)

    return list_data


def biological_maker(dataframe):
    """
    Create data for biological material CSV
    The column labels are ["biological_id", "genus", "species", "subspecies", "accession_number", "accession_name", "material_source_id", "material_source_doi"]
    :param dataframe:DataFrale
    :return: data:List
    """
    list_data = list()

    for row_elt in dataframe.index:
        data = list()

        data.append(dataframe["biological_material_id"][row_elt])
        data.append(dataframe["genus"][row_elt])
        data.append(dataframe["species"][row_elt])
        data.append(dataframe["subsp"][row_elt])
        data.append(dataframe["accession_number"][row_elt])
        data.append(dataframe["accession_name"][row_elt])
        data.append(dataframe["material_source_id"][row_elt])
        data.append(dataframe["material_source_doi"][row_elt])

        list_data.append(data)

    return list_data


def observation_unit_maker(dataframe):
    """
    Create data for observation unit CSV
    The column labels are ["id", "study", "biological", "observation_level", "observation_level_number","factor_mode", "factor_value"]
    :param dataframe:
    :return:
    """
    list_data = list()
    
    for row_elt in dataframe.index:
        data = list()

        data.append(dataframe["observationunitdbid"][row_elt])
        data.append(uri_hash_maker(dataframe["studydbid"][row_elt]))
        data.append(dataframe["germplasmname"][row_elt])
        data.append(dataframe["observationlevel"][row_elt])

        if pd.isnull(dataframe["replicate"][row_elt]):
            data.append(0)
        else:
            data.append(dataframe["replicate"][row_elt])

        if dataframe["experimental_factors"][row_elt] == "[]":
            data.append("itk")
            data.append("non traité")
        else:
            factor_mode, factor_value = extract_factor(dataframe["experimental_factors"][row_elt])
            data.append(factor_mode)
            data.append(factor_value)

        list_data.append(data)

    return list_data


def factor_maker(dataframe):
    """

    :param dataframe:
    :return:
    """
    list_data = list()
    
    for row_elt in dataframe.index:
        data = list()

        data.append(uri_hash_maker(dataframe["Factor"][row_elt], URI["factor"]))
        data.append(uri_hash_maker(dataframe["ModeCode"][row_elt], URI["factor_value"]))
        data.append(dataframe["Factor"][row_elt])
        data.append(dataframe["ModeCode"][row_elt])
        data.append(dataframe["ModeName"][row_elt])
        data.append(dataframe["ModeDescription"][row_elt])

        list_data.append(data)

    return list_data
        

def observation_maker(dataframe):
    """
    Create data for observation CSV
    The column labels are
    One row per (variable, value)
    The column labels are ["observation_unit", "observation_id", "variable", "trait","method", "scale", "value"]
    :param dataframe:
    :return:
    """
    list_data = list()

    for row_elt in dataframe.index:
            observations = extract_observation(dataframe["observations"][row_elt])

            for obs in observations:
                data = list()

                obs_variable = obs["observationVariableDbId"]
                data.append(dataframe["observationunitdbid"][row_elt])
                data.append(obs["observationDbId"])
                data.append(co_321_uri_maker(obs_variable))
                data.append(co_321_uri_maker(co_321_trait[obs_variable]))
                data.append(co_321_uri_maker(co_321_method[obs_variable]))
                data.append(co_321_uri_maker(co_321_scale[obs_variable]))
                data.append(obs["value"])
                list_data.append(data)

    return list_data


def gps_maker(dataframe):
    """
    ["study", "site", "latitude", "longitude", "altitude"]
    :param dataframe:
    :return:
    """
    list_data = list()

    for row_elt in dataframe.index:
        data = list()
        data.append(uri_hash_maker(dataframe["study_title"][row_elt]))
        data.append(dataframe["experimental_site_name"][row_elt])
        data.append(dataframe["geographic_location_lattitude"][row_elt])
        data.append(dataframe["geographic_location_longitude"][row_elt])
        if pd.isnull(dataframe["geographic_location_altitude"][row_elt]):
            data.append(0.0)
        else:
            data.append(dataframe["geographic_location_altitude"][row_elt])
        list_data.append(data)

    return list_data


def person_maker(dataframe):
    """

    :param dataframe:
    :return:
    """
    list_data = list()

    for row_elt in dataframe.index:
        data = list()

        data.append(dataframe["Type"][row_elt])
        data.append(f'{dataframe["LastName"][row_elt]} {dataframe["FirstName"][row_elt]}')
        data.append(dataframe["Email"][row_elt])
        data.append(dataframe["Institution"][row_elt])

        list_data.append(data)

    return list_data


if __name__ == '__main__':
    alpha = time.time()
    current_directory = os.getcwd()
    co_321_df = pd.read_csv("CO_321-Wheat Crop Ontology.csv", sep=";")
    co_321_variable, co_321_trait, co_321_method, co_321_scale = extract_variable_dict(co_321_df)

    print(current_directory + "\\wheat_complete")
    os.chdir(f"{current_directory}\\wheat_complete")
    file_csv = [x for x in glob.glob("study_*") if "_clean" not in x]
    print(file_csv)

    studies_df = pd.read_csv("studies.csv").iloc[:, 1:]
    investigation_df = pd.read_csv("investigation.csv").iloc[:, 1:]
    biological_df = pd.read_csv("biological_material.csv").iloc[:, 1:]

    gps_out = pd.DataFrame(gps_maker(studies_df), columns=gps_label)
    studies_out = pd.DataFrame(study_maker(studies_df), columns=studies_label)
    biological_out = pd.DataFrame(biological_maker(biological_df), columns=biological_label)

    observation_unit_data = list()
    observation_data = list()
    factor_data = list()
    person_data = list()

    for file in file_csv:
        df = pd.read_csv(file).iloc[:, 1:]
        observation_unit_data.extend(observation_unit_maker(df))
        observation_data.extend(observation_maker(df))

    os.chdir(f"{current_directory}")
observation_unit_df = pd.DataFrame(observation_unit_data, columns=observation_unit_label)
observation_df = pd.DataFrame(observation_data, columns=observation_label)

studies_out.to_csv("studies.csv", index=False, encoding="utf-8")
gps_out.to_csv("gps.csv", index=False, encoding="utf-8")
biological_out.to_csv("biological.csv", index=False, encoding="utf-8")
observation_unit_df.to_csv("observation_unit.csv", index=False, encoding="utf-8")
observation_df.to_csv("observations.csv", index=False, encoding="utf-8")

beta = time.time()
print(beta - alpha)



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

FACTOR = {
    "treated" : "t",
    "untreated, no fungicide" : "nt",
    "low inputs" : "fi"
}


# Variable of failed process
variable_not_found = set()
itk_fail_list = list()

# Label of the column
studies_label = ["study_id", "study_name", "start_date", "end_date", "description", "investigation"]
biological_label = ["biological_id", "genus", "species", "subspecies", "accession_number", "accession_name", "material_source_id", "material_source_doi"]
observation_unit_label = ["id", "study", "biological", "observation_level", "observation_level_number", "factor_mode", "factor_value"]
observation_label = ["observation_unit", "observation_id", "variable", "trait","method", "scale", "value"]
factor_label = ["uri_factor", "uri_factor_value", "factor", "factor_value", "factor_name", "description"]
person_label = ["type", "name", "email", "institution"]
gps_label = ["study", "site", "latitude", "longitude", "altitude"]


def extract_variable_dict(dataframe1, dataframe2):
    # todo: Generalize to every ontology that follows this pattern
    variable_co = dict()
    trait_co = dict()
    method_co = dict()
    scale_co = dict()
    dataframe1.fillna("", inplace=True)
    dataframe2.fillna("", inplace=True)

    # CO 321 CSV extraction
    for row in dataframe1.index:
        name = dataframe1["Variable name"][row]
        variable_co[name] = dataframe1["Variable ID"][row]
        trait_co[dataframe1["Variable ID"][row]] = dataframe1["Trait ID"][row]
        method_co[dataframe1["Variable ID"][row]] = dataframe1["Method ID"][row]
        scale_co[dataframe1["Variable ID"][row]] = dataframe1["Scale ID"][row]
        synonyms = dataframe1["Variable synonyms"][row]
        if synonyms == "":
            continue
        for elt in dataframe1["Variable synonyms"][row].split(","):
            variable_co[elt.strip()] = dataframe1["Variable ID"][row].strip()

    # WIPO CSV extraction
    for row in dataframe2.index:
        name = dataframe2["Variable name"][row]
        variable_co[name] = dataframe2["Variable ID"][row]
        trait_co[dataframe2["Variable ID"][row]] = dataframe2["Trait ID"][row]
        method_co[dataframe2["Variable ID"][row]] = dataframe2["Method ID"][row]
        scale_co[dataframe2["Variable ID"][row]] = dataframe2["Scale ID"][row]
        synonyms = dataframe2["Variable synonyms"][row]
        if synonyms == "":
            continue
        for elt in dataframe1["Variable synonyms"][row].split(","):
            variable_co[elt.strip()] = dataframe2["Variable ID"][row].strip()

    return variable_co, trait_co, method_co, scale_co

def extract_factor(json_array):
    """
    Extract factor from a json_array
    Old CSV from URGI
    :param json_array:
    :return:
    """
    dict_value = eval(json_array)[0]
    return dict_value["factor"], dict_value["modality"]

def extract_observation(json_array):
    """
    Extract Observations from a JSON_array
    Old CSV from URGI
    :param json_array:
    :return:
    """
    dict_value = eval(json_array)
    return dict_value

def co_321_uri_maker(uri):
    """
    Retranscript URI for Crop Ontology 321 and UO
    :param uri:
    :return:
    """
    # todo: Add WIPO support
    if 'UO' in uri:
        return f"http://purl.obolibrary.org/obo/{uri.replace(':','_')}"
    return f"http://www.cropontology.org/rdf/CO_321/{uri.split(':')[1]}"


def encoding_resolve(string):
    """
    Replace miss-translated char from CSV
    :param string:
    :return:
    """
    return string.replace("Ã©", "é")

def uri_hash_maker(to_hash):
    """
    Create an URI with the namespace and the associated id as hash
    SHA1 is used for hash the string
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
    Create data for trial CSV
    The columns label are ["study_id", "study_name", "start_date", "end_date", "description", "investigation"]
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
        data.append("INRA Small Grain Cereals Network".replace(" ","_"))

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

    # CO_321 CSV extraction
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
        try:
            factor_value = FACTOR[dataframe["itk"][row_elt]]
            data.append("itk")
            data.append(factor_value)
        except KeyError:
            itk_fail_list.append(file)
            data.append("itk")
            data.append("nt")
            return list()

        list_data.append(data)

    return list_data


def factor_maker(dataframe):
    """
    Create factor Data
    The column labels are ["uri_factor", "uri_factor_value", "factor", "factor_value", "factor_name", "description"]
    :param dataframe:
    :return:
    """
    list_data = list()
    
    for row_elt in dataframe.index:
        data = list()
        
        list_data.append(data)

    return list_data
        

def observation_maker(dataframe, file):
    """
    Create data for observation CSV
    The column labels are
    One row per (variable, value)
    The column labels are ["observation_unit", "observation_id", "variable", "trait", "method", "scale", "value"]
    :param dataframe:
    :return:
    """
    list_data = list()
    obs_var_extract = [x for x in list(dataframe.columns) if ("(" in x) and (".date" not in x)]

    for row_elt in dataframe.index:

        for obs in obs_var_extract:
            if pd.isnull(dataframe[obs][row_elt]):
                continue
            data = list()
            obs_variable = obs[obs.index("(")+1:obs.index(")")]

            data.append(dataframe["observationunitdbid"][row_elt])
            data.append(uri_hash_maker(f'{dataframe["observationunitdbid"][row_elt]}_{obs_variable}'))
            data.append(co_321_uri_maker(obs_variable))
            data.append(co_321_uri_maker(dict_trait[obs_variable]))
            data.append(co_321_uri_maker(dict_method[obs_variable]))
            data.append(co_321_uri_maker(dict_scale[obs_variable]))
            data.append(dataframe[obs][row_elt])

            list_data.append(data)

    return list_data


def gps_maker(dataframe):
    """
    Create GPS location
    The column labels are ["study", "site", "latitude", "longitude", "altitude"]
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


def investigation_maker(dataframe):
    """
    Create investigation data
    The column labels are ["id", "name", "doi"]
    :param dataframe:
    :return:
    """
    list_data = list()

    for row in dataframe.index:
        data = list()
        data.append(dataframe["investigation_title"][row].replace(" ","_"))
        data.append(dataframe["investigation_title"][row])
        data.append(dataframe["investigation_unique_id"][row])
        list_data.append(data)

    return list_data


def person_maker(dataframe):
    """
    Create person data
    The column labels are
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
    # Set timer to benchmark the generation
    alpha = time.time()
    # Find the current repository
    current_directory = os.getcwd()

    # Retrieve Crops ontology dataframe
    co_321_df = pd.read_csv("CO_321-Wheat Crop Ontology.csv", sep=";")
    wipo_df = pd.read_csv("WIPO-Wheat Inra Phenotype Ontology.csv", sep=";")
    dict_variable, dict_trait, dict_method, dict_scale = extract_variable_dict(co_321_df, wipo_df)

    print(current_directory + "\\output\\INRA_Small_Grain_Cereals_Network")
    folder = input()
    #os.chdir(f"{current_directory}\\output\\INRA_Small_Grain_Cereals_Network")
    os.chdir(folder)
    # Retrieve each individual study file
    file_csv = [x for x in glob.glob("study_*")]

    studies_df = pd.read_csv("studies.csv").iloc[:, 1:]
    investigation_df = pd.read_csv("investigation.csv").iloc[:, 1:]
    biological_df = pd.read_csv("biological_material.csv").iloc[:, 1:]
    investigation_df = pd.read_csv("investigation.csv").iloc[:, 1:]

    gps_out = pd.DataFrame(gps_maker(studies_df), columns=gps_label)
    studies_out = pd.DataFrame(study_maker(studies_df), columns=studies_label)
    biological_out = pd.DataFrame(biological_maker(biological_df), columns=biological_label)
    investigation_out = pd.DataFrame(investigation_maker(investigation_df), columns=["id", "name", "pui"])

    observation_unit_data = list()
    observation_data = list()
    factor_data = list()
    person_data = list()

    for file in file_csv:
        df = pd.read_csv(file)
        observation_unit_data.extend(observation_unit_maker(df))
        observation_data.extend(observation_maker(df, file))

    os.chdir(f"{current_directory}")
    observation_unit_df = pd.DataFrame(observation_unit_data, columns=observation_unit_label)
    observation_df = pd.DataFrame(observation_data, columns=observation_label)

    # Generate CSV file for mongoDB collection
    studies_out.to_csv("studies.csv", index=False, encoding="utf-8")
    gps_out.to_csv("gps.csv", index=False, encoding="utf-8")
    biological_out.to_csv("biological.csv", index=False, encoding="utf-8")
    observation_unit_df.to_csv("observation_unit.csv", index=False, encoding="utf-8")
    observation_df.to_csv("observations.csv", index=False, encoding="utf-8")
    investigation_out.to_csv("investigation.csv", index=False, encoding="utf-8")

    beta = time.time()
    print(itk_fail_list)
    print(beta - alpha)



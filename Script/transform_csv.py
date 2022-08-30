import os
import glob
import pandas as pd
import numpy as np
import hashlib

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


trial_label = ["URI", "TrialName", "TrialCode", "BeginningDate", "EndingDate", "TrialCampaign", "Institution"]
biological_label = ["URI", "Taxon", "Species", "AccessionNumber", "AccessionName", "LotName"]
observation_unit_label = ["URI", "BiologicalMaterial", "itk", "trial", "trial_name", "lot_value", "itk_value", "observation_level"]
observation_label = ["URI", "observation_unit", "variable", "value", "trait", "method", "scale"]
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


def co_321_uri_maker(uri):
    return f"http://www.cropontology.org/rdf/CO_321/{uri.split(':')[1]}"


def encoding_resolve(string):
    return string.replace("Ã©", "é")

def uri_hash_maker(to_hash, ns):
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
    The columns label are ["URI", "TrialName", "TrialCode", "BeginningDate", "EndingDate", "TrialCampaign", "Institution"]
    :param dataframe:DataFrame
    :return: data:List
    """
    global trial_name
    data = list()
    trial_name = dataframe["Trial"]["TrialName"].values[0]
    data.append(uri_hash_maker(dataframe["Trial"]["TrialName"].values[0], URI["study"]))
    #data.append(f"{URI['trial']}{trial_name}")
    data.append(dataframe["Trial"]["TrialName"].values[0].strip())
    data.append(dataframe["Trial"]["TrialCode"].values[0].strip())
    data.append(dataframe["Trial"]["BeginningDate"].values[0].strip())
    data.append(dataframe["Trial"]["EndingDate"].values[0].strip())
    data.append(dataframe["Trial"]["TrialSet"].values[0].strip())
    data.append(dataframe["Contact"]["Institution"].values[0].strip())
    return data


def biological_maker(dataframe):
    """
    Create data for biological material CSV
    The column labels are ["URI", "Taxon", "Species", "AccessionNumber", "AccessionName", "LotName"]
    :param dataframe:DataFrale
    :return: data:List
    """
    list_data = list()
    #dataframe.drop(['HoldingInstitution', 'CollectionName', 'CollectionType', 'PanelName', 'PanelSize'], axis=1, inplace=True)

    for row_elt in dataframe.index:
        data = list()

        number, name, lot = dataframe['AccessionNumber'][row_elt],\
                            dataframe['AccessionName'][row_elt],\
                            dataframe['LotName'][row_elt]
        data.append(uri_hash_maker(f"{lot}", URI["biological"]))
        data.append(" ".join(dataframe["TaxonScientificName"][row_elt].split(" ")[0:2]))
        data.append(dataframe["TaxonScientificName"][row_elt].split(" ")[2])
        data.append(number)
        data.append(name)
        data.append(lot)

        list_data.append(data)

    return list_data


def observation_unit_maker(dataframe):
    """
    Create data for observation unit CSV
    The column labels are ["URI", "BiologicalMaterial", "itk"]
    :param dataframe:
    :return:
    """
    list_data = list()
    
    for row_elt in dataframe.index:
        data = list()
        lot = dataframe['LotName'][row_elt]
        rep = np.int64(0)

        if 'itk' in dataframe.columns:
            itk = dataframe['itk'][row_elt]
        else:
            itk = "no-itk"
        if 'Rep' in dataframe.columns:
            rep = dataframe['Rep'][row_elt]

        data.append(uri_hash_maker(f"{trial_name}{lot}{itk}{rep}", URI["observation_unit"]))
        data.append(uri_hash_maker(f"{lot}", URI["biological"]))
        data.append(uri_hash_maker(f"{itk}", URI["factor_value"]))
        data.append(uri_hash_maker(f"{trial_name}", URI["study"]))
        data.append(trial_name)
        data.append(lot)
        data.append(itk)
        data.append(f"{rep}")

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
        

def observation_maker(dataframe, var_df):
    """
    Create data for observation CSV
    The column labels are
    One row per (variable, value)
    :param dataframe:
    :return:
    """

    var_transform = dataframe.iloc[:, dataframe.columns.get_loc("Y(m)")+1:]
    var_transform = var_transform[var_transform.columns.drop(list(var_transform.filter(regex='date')))]
    list_data = list()
    for row_elt in dataframe.index:

        lot = dataframe["LotName"][row_elt]
        rep = "0"
        if 'itk' in dataframe.columns:
            itk = dataframe["itk"][row_elt]
        else:
            itk = "no-itk"
        if "Rep" in dataframe.columns:
            rep = dataframe["Rep"][row_elt]
        for col in var_transform.columns:
            data = list()
            variable_shortname = col.strip().split("_")[0]
            search_variable = var_df[var_df["VariableShortName"] == variable_shortname]["VariableID"]
            if search_variable.empty:
                if variable_shortname in co_321_variables.keys():
                    val = co_321_variables[variable_shortname]
                    variable = val
                    traits = co_321_trait[val]
                    methods = co_321_method[val]
                    scale = co_321_scale[val]
                else:
                    variable_not_found.add(variable_shortname)
                    continue
            else:
                val = search_variable.values[0]
                variable = val
                traits = co_321_trait[val]
                methods = co_321_method[val]
                scale = co_321_scale[val]

            if pd.isnull(dataframe[col][row_elt]):
                continue
            data.append(uri_hash_maker(f"{trial_name}{lot}{itk}{rep}{variable}", URI["observation"]))
            data.append(uri_hash_maker(f"{trial_name}{lot}{itk}{rep}", URI["observation_unit"]))
            data.append(co_321_uri_maker(variable))
            data.append(dataframe[col][row_elt])
            data.append(co_321_uri_maker(traits))
            data.append(co_321_uri_maker(methods))
            data.append(co_321_uri_maker(scale))

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
        data.append(uri_hash_maker(dataframe["study_title"][row_elt], ""))
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
    cc = True
    current_directory = os.getcwd()
    co_321_df = pd.read_csv("CO_321-Wheat Crop Ontology.csv", sep=";")
    co_321_variables, co_321_trait, co_321_method, co_321_scale = extract_variable_dict(co_321_df)

    print(current_directory + "\\wheat_complete")
    os.chdir(f"{current_directory}\\wheat_complete")
    file_csv = [x for x in glob.glob("study_*") if "_clean" not in x]
    print(file_csv)

    studies_df = pd.read_csv("studies.csv").iloc[:, 1:]
    investigation_df = pd.read_csv("investigation.csv").iloc[:, 1:]

    gps_data = gps_maker(studies_df)
    print(gps_data)

    trial_data = list()
    biological_data = list()
    observation_unit_data = list()
    observation_data = list()
    factor_data = list()
    person_data = list()

    for file in file_csv:
        df = pd.read_csv(file).iloc[:, 1:]

        trial_data.append(study_maker(df))
        biological_data.extend(biological_maker(df["PlantMaterial"]))
        observation_unit_data.extend(observation_unit_maker(df["Data"]))
        observation_data.extend(observation_maker(df["Data"], df["Variable"]))
        factor_data.extend(factor_maker(df["Treatment"]))
        person_data.extend(person_maker(df["Contact"]))

    os.chdir(f"{current_directory}")

    study_df = pd.DataFrame(trial_data, columns=trial_label)
    biological_df = pd.DataFrame(biological_data, columns=biological_label)
    observation_unit_df = pd.DataFrame(observation_unit_data, columns=observation_unit_label)
    observation_df = pd.DataFrame(observation_data, columns=observation_label)
    factor_df = pd.DataFrame(factor_data, columns=factor_label)
    person_df = pd.DataFrame(person_data, columns=person_label)
    gps_df = pd.DataFrame(gps_data, columns=gps_label)

    study_df.to_csv("trials.csv", index=False, encoding="utf-8")
    biological_df.to_csv("biological.csv", index=False, encoding="utf-8")
    observation_unit_df.to_csv("observation_unit.csv", index=False, encoding="utf-8")
    observation_df.to_csv("observation.csv", index=False, encoding="utf-8")
    factor_df.to_csv("factor.csv", index=False, encoding="utf-8")
    person_df.to_csv("person.csv", index=False, encoding="utf-8")
    gps_df.to_csv("gps.csv", index=False, encoding="utf-8")

    #print(trial_data)
    #print(biological_data)
    #print(observation_unit_data)
    #print(observation_data)
    #print(factor_data)
    print(person_data)
    print(f"Variable not found => {variable_not_found}")


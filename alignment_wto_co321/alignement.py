import pandas as pd
import numpy as np

def make_align(dataframe):
    list_data = list()

    for row in dataframe.index:
        if dataframe["Mappings"][row] == "0" or pd.isnull(dataframe["CO_321_ID:trait_ID"][row]):
            continue
        data = list()
        data.append(dataframe["WTO_ID:class_ID"][row].split("/")[-1])
        data.append(dataframe["CO_321_ID:trait_ID"][row].split(":")[-1])
        data.append(dataframe["Mappings"][row])
        list_data.append(data)
    return list_data


if __name__ == '__main__':



    alignement_df = pd.read_csv("Alignement_WTO_CO321.xlsx - Final Table.csv")
    align_data = make_align(alignement_df)
    pd.DataFrame(align_data, columns=["wto","co", "match"]).to_csv("alignement.csv", index=False, encoding="UTF-8")
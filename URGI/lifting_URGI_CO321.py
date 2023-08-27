import pandas as pd
import numpy as np

error = []
"""
The main goal of this script is to transform the original CSV from URGI observation campaign to a consitant CSV.
The problem with the actual CSV is that each row is a campaign with variables that can be empty. It's hard to lift
data with morphXR2RML with such CSV and can't be uploaded in a mongoDB.

To overcome that difficulty, each row will be a variable from an observation site.
| siteX | CampaignDate | CO_321Variable |

The side effect to such approach is the number of rows in the new CSV increase exponentially.
For example, a CSV with 50k rows will be trasform in a CSV with n*k rows (n = old number of line, k = number of variable colomn)
"""


def check_shape(shape1, shape2, dtf1, dtf2):
    p, s = "", ""
    if shape1[0] == 1:
        s = dtf1["Variable ID"].values[0]
    if shape2[0] == 1:
        p = dtf2["Variable ID"].values[0]

    if s == "":
        return p
    if p == "":
        return s
    else:
        if p == s:
            return s
        print(s,p)
        error.append((p, s))
        return s


if __name__ == '__main__':

    df_urgi = pd.read_csv("Ephesis_export-1525366082352498702.csv", sep=";")
    df_co321 = pd.read_csv("CO_321-Wheat_Crop_Ontology.csv", sep=";")
    df_co321["Variable synonyms"] = df_co321["Variable synonyms"].replace(np.nan, " ")

    df_urgi = df_urgi[df_urgi.columns.drop(list(df_urgi.filter(regex='Date')))]
    variables = df_urgi.iloc[:, 10:22]
    print(variables.shape)
    pd.set_option('display.max_row', None)
    label = []
    for col in variables.columns:
        pref, suff = col.split(":")
        print(pref, suff.strip())
        temp = df_co321[df_co321['Variable synonyms'].str.contains(f'{suff.strip()}')]
        temp2 = df_co321[df_co321['Variable synonyms'].str.contains(f'{pref.strip()}')]
        label.append(check_shape(temp.shape, temp2.shape, temp, temp2))
    print(label)
    print(error)

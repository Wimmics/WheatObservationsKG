import pandas as pld
import csv

# Les préfixes des références à modifier
references = {
    "ncbi": "http://purl.obolibrary.org/obo/",
    "ID": "http://opendata.inrae.fr/wto/v3.0/thesaurus/WTO_",
    "pretend-marker": "http://ns.inria.fr/d2kab/marker/",
    "pretend-gene": "http://ns.inria.fr/d2kab/gene/",
    "pretend-variety": "http://ns.inria.fr/d2kab/variety/"
}

#No pref and alt label found
no_equivalent_name = {
    "level of polyphenol oxidase activity": "polyphenol content",
    "tiller number per plant": "number of ear-bearing tillers at anthesis",
    "heritable trait": "trait" #Aucune equivalence clair
}

#alt label used for alignment
conflict_name = {
    "pre-harvest sprouting": "pre-harvest sprouting tolerance",
    "protein content of seed": "grain protein content",
    "leaf number": "final leaf number",
    "phophorus limitation": "response to phophorus limitation",
    "nitrogen limitation": "nitrogen deficiency",
    "hard textured wheat": "hard grain texture"
}

def find_uri_by_label(dtf,label):
    if label in conflict_name.keys():
        r = dtf[dtf["Preferred Label"] == conflict_name[label]]
    elif label in no_equivalent_name.keys():
        r = dtf[dtf["Preferred Label"] == no_equivalent_name[label]]
    else:
        r = dtf[dtf["Preferred Label"] == label]

    print(f"{label} -> {r.iloc[0,0].split('_')[-1]}")
    return r.iloc[0,0].split("_")[-1]

def synop_to_df(filepath, df_wto):

    df = pld.read_csv(filepath)

    values = []
    for x in df["reference"]:
        prefix, suffix = x.split(":")
        if prefix == "ID":
            temp = df[df["reference"] == x]
            print(temp.iloc[0,8])
            suffix = find_uri_by_label(df_wto, temp.iloc[0,8])
        values.append(f'"{references[prefix]}{suffix}"')

    df['reference'] = values
    return df


# Visualisation du CSV
def csv_print_line(filepath):
    with open(filepath, "r") as csv_file:
        for line in csv_file:
            print(line)


if __name__ == "__main__":
    
    wto_csv = pld.read_csv("WHEATPHENOTYPE.csv")
    folders_to_scan = input()
    for i in range(0,9):
        temp_scan_1 = folders_to_scan + str(i) + "\\entities.csv"
        print(temp_scan_1)
        new_doc_1 = "_clean.".join(temp_scan_1.split('\\')[-1].split("."))
        df = synop_to_df(temp_scan_1, wto_csv)
        df.to_csv(
            folders_to_scan + str(i) + "\\" + new_doc_1,
            sep=",",
            index=False,
            line_terminator='\n',
            quoting=csv.QUOTE_NONE,
            escapechar='\\'
        )

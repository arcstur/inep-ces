import os
import pandas as pd
from download_data import guarantee_all_data

QT_COLUMNS = ["QT_CONC", "QT_CONC_FEM", "QT_CONC_MASC"]
FILTER_COLUMNS = [
    "SG_UF",
    "NO_CURSO",
]
NO_CURSO = os.environ.get("NO_CURSO", "Arquitetura E Urbanismo")
SG_UF = os.environ.get("SG_UF", "RS")


def main():
    guarantee_all_data()

    filename = os.environ.get("CSV_FILENAME", "dados/2021.csv")
    df = get_dataframe(filename)

    for year in df["NU_ANO_CENSO"].unique():
        df_year = df.loc[df["NU_ANO_CENSO"] == year]
        agg_dict = {column: "first" for column in FILTER_COLUMNS} | {
            column: "sum" for column in QT_COLUMNS
        }
        results = df_year.groupby("NU_ANO_CENSO").agg(agg_dict)
        print(results)


def get_dataframe(filename, usecols=None):
    usecols = ["NU_ANO_CENSO"] + FILTER_COLUMNS + QT_COLUMNS
    df = pd.read_csv(
        filename,
        delimiter=";",
        encoding="ISO-8859-1",
        # otherwise it complains about columns having mixed types
        low_memory=False,
        usecols=usecols,
    )
    df = df.loc[df["SG_UF"] == SG_UF]
    df = df.loc[df["NO_CURSO"] == NO_CURSO]
    return df


if __name__ == "__main__":
    main()

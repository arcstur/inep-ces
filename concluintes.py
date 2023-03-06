import os
import logging
import pandas as pd
from download_data import guarantee_all_data, DataYear, ALL_YEARS

QT_COLUMNS = ["QT_CONC", "QT_CONC_FEM", "QT_CONC_MASC"]
FILTER_COLUMNS = [
    "SG_UF",
    "NO_CURSO",
]
NO_CURSO = os.environ.get("NO_CURSO", "ARQUITETURA E URBANISMO")
SG_UF = os.environ.get("SG_UF", "RS")


def main():
    set_log_level()
    guarantee_all_data()

    dataframes = []
    for year in ALL_YEARS:
        logging.info(f"[{year}] Analysing data")
        df = get_dataframe(DataYear(year).path())
        dataframes.append(df)

    df = pd.concat(dataframes)

    logging.debug("Calculating results")
    agg_dict = {column: "first" for column in FILTER_COLUMNS} | {
        column: "sum" for column in QT_COLUMNS
    }
    results = df.groupby("NU_ANO_CENSO").agg(agg_dict)
    print(results)


def get_dataframe(filename, usecols=None):
    usecols = ["NU_ANO_CENSO"] + FILTER_COLUMNS + QT_COLUMNS

    logging.debug(f"Open dataframe at {filename}")
    df = pd.read_csv(
        filename,
        delimiter=";",
        encoding="ISO-8859-1",
        # otherwise it complains about columns having mixed types
        low_memory=False,
        usecols=usecols,
    )

    logging.debug(f"Filter dataframe at {filename} by SG_UF and NO_CURSO")
    df = df.loc[df["SG_UF"] == SG_UF]
    df["NO_CURSO"] = df["NO_CURSO"].str.upper()
    df = df.loc[df["NO_CURSO"] == NO_CURSO]

    return df


def set_log_level():
    logging.basicConfig(level=os.environ.get("PYTHON_LOG", "WARNING"))


if __name__ == "__main__":
    main()

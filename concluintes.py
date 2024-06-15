import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from download_data import guarantee_all_data, DataYear, ALL_YEARS

SEX_COLUMNS = [
    "QT_CONC_FEM",
    "QT_CONC_MASC",
]
AGE_COLUMNS = [
    "QT_CONC_0_17",
    "QT_CONC_18_24",
    "QT_CONC_25_29",
    "QT_CONC_30_34",
    "QT_CONC_35_39",
    "QT_CONC_40_49",
    "QT_CONC_50_59",
    "QT_CONC_60_MAIS",
]
COLOR_COLUMNS = [
    "QT_CONC_BRANCA",
    "QT_CONC_PRETA",
    "QT_CONC_PARDA",
    "QT_CONC_AMARELA",
    "QT_CONC_INDIGENA",
    "QT_CONC_CORND",
]

QT_COLUMNS = (
    [
        "QT_CONC",
    ]
    + SEX_COLUMNS
    + AGE_COLUMNS
    + COLOR_COLUMNS
)

FILTER_COLUMNS = [
    "SG_UF",
    "NO_CURSO",
]
NO_CURSO = os.environ.get("NO_CURSO", "ARQUITETURA E URBANISMO").upper()
SG_UF = os.environ.get("SG_UF", "BR").upper()
PLOT_ACTION = os.environ.get("PLOT_ACTION", "EXPORT").upper()


def main():
    set_log_level()
    guarantee_all_data()

    dataframes = []
    for year in ALL_YEARS:
        logging.info(f"[{year}] Opening")
        path = DataYear(year).path()
        df = get_dataframe(path)
        dataframes.append(df)

    df = pd.concat(dataframes)
    print(df)
    df.to_csv(f"output/{NO_CURSO}.{SG_UF}.csv", sep=";", index=False)
    df.to_excel(f"output/inep-ces-arquitetura-{SG_UF}-desagregado.xlsx", index=False)

    # logging.debug("Calculating results")
    # agg_dict = {column: "first" for column in FILTER_COLUMNS} | {
    #     column: "sum" for column in QT_COLUMNS
    # }
    # results = df.groupby("NU_ANO_CENSO").agg(agg_dict)
    # print(results[FILTER_COLUMNS + ["QT_CONC"]])

    # logging.info("Saving results")
    # os.makedirs("output/", exist_ok=True)
    # results.to_csv(f"output/{NO_CURSO}.{SG_UF}.csv", sep=";")

    # make_plots(results)


def make_plots(results):
    logging.info("Creating graphs")
    for i, columns in enumerate(
        [
            ["QT_CONC"],
            SEX_COLUMNS,
            AGE_COLUMNS,
            COLOR_COLUMNS,
        ]
    ):
        results[FILTER_COLUMNS + columns].plot()
        match PLOT_ACTION:
            case "SHOW":
                plt.show()
            case "EXPORT":
                plt.savefig(f"output/{NO_CURSO}.{SG_UF}.{i}.pdf")


def get_dataframe(filename, usecols=None):
    # usecols = ["NU_ANO_CENSO"] + FILTER_COLUMNS + QT_COLUMNS

    logging.debug(f"Open dataframe at {filename}")
    df = pd.read_csv(
        filename,
        delimiter=";",
        encoding="ISO-8859-1",
        # otherwise it complains about columns having mixed types
        low_memory=False,
    )

    if SG_UF != "BR":
        df = df.loc[df["SG_UF"] == SG_UF]
    df["NO_CURSO"] = df["NO_CURSO"].str.upper()
    df = df.loc[df["NO_CURSO"] == NO_CURSO]

    return df


def set_log_level():
    logging.basicConfig(level=os.environ.get("PYTHON_LOG", "INFO").upper())


if __name__ == "__main__":
    main()

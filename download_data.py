import os
import requests
import logging
import io
import zipfile
import hashlib

ALL_YEARS = range(2009, 2021 + 1)

# These are the MD5 hashes of the csv data files.
MD5_PER_YEAR = {
    2009: "677421fb8ad9442370175cbadae05b77",
    2010: "8ea106ef7dc41a27a43b9f246cfd3ffd",
    2011: "f626dd6d17e8f31f78ddf90f680ace48",
    2012: "f896c4a4e2b10adcf846d91486ab0ce8",
    2013: "2bbfbe1a9afe1fe5d0d7384901ae3b7e",
    2014: "bf70eb93a2a5cce0e0a48295c4834c20",
    2015: "b5bd1b6b10b4f66f359deed4ac48cb80",
    2016: "a9475f5f6815a5befb8bc91b8e2c7b1c",
    2017: "af97168b2d83b0e4b6c1572e619c183b",
    2018: "b852881daa9328e4ff3f3a2c6115ba51",
    2019: "f80ea1eddafae4780728e6fb26aa549f",
    2020: "a84c1efeedd8bcec4848ec8217b92b98",
    2021: "05d78ff911cea316cd65f08b0e93e83d",
}


class DataYear:
    def __init__(self, year):
        if year > 2021 or year < 1995:
            raise ValueError
        self.year = year

    def __str__(self):
        return f"[{self.year} data]"

    def path(self):
        return f"input/{self.year}.csv"

    def data_exists(self):
        if os.path.exists(self.path()):
            correct = MD5_PER_YEAR[self.year]
            current = hashlib.md5(open(self.path(), "rb").read()).hexdigest()
            has_correct_hash = correct == current
            if not has_correct_hash:
                logging.debug(f"{self} file exists but has incorrect hash.")
            return has_correct_hash
        else:
            logging.debug(f"{self} file does not exist")
            return False

    def guarantee_data(self):
        if not self.data_exists():
            print(f"{self} downloading file...")
            self.download_data()
        else:
            logging.info(f"{self} file already exists, using it.")

    def download_data(self):
        # TODO: make it work without `verify=False`
        response = requests.get(self.url(), verify=False)
        zip_file = io.BytesIO(response.content)
        os.makedirs(os.path.dirname(self.path()), exist_ok=True)

        with zipfile.ZipFile(zip_file, mode="r") as zip:
            path = (
                zip.namelist()[0]
                + f"dados/MICRODADOS_CADASTRO_CURSOS_{self.year}.CSV"
            )
            with zip.open(path, mode="r") as csv_file:
                with open(self.path(), "wb") as f:
                    f.write(csv_file.read())

        logging.debug(f"{self} file successfully downloaded, checking hash...")
        assert self.data_exists()

    def url(self):
        base = "https://download.inep.gov.br/microdados/"
        filename = f"microdados_censo_da_educacao_superior_{self.year}.zip"
        return base + filename


def guarantee_all_data():
    for year in ALL_YEARS:
        DataYear(year).guarantee_data()

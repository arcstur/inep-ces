import os
import requests
import io
import zipfile
import hashlib

# These are the MD5 hashes of the csv data files.
MD5_PER_YEAR = {
    2021: "05d78ff911cea316cd65f08b0e93e83d",
}


class DataYear:
    def __init__(self, year):
        if year > 2021 or year < 1995:
            raise ValueError
        self.year = year

    def path(self):
        return f"dados/{self.year}.csv"

    def data_exists(self):
        if os.path.exists(self.path()):
            correct = MD5_PER_YEAR[self.year]
            current = hashlib.md5(open(self.path(), "rb").read()).hexdigest()
            return correct == current
        return False

    def guarantee_data(self):
        if not self.data_exists():
            self.download_data()

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

    def url(self):
        base = "https://download.inep.gov.br/microdados/"
        filename = f"microdados_censo_da_educacao_superior_{self.year}.zip"
        return base + filename


def guarantee_all_data():
    for year in [2021]:
        DataYear(year).guarantee_data()

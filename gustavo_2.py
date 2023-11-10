from datetime import datetime, timedelta
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests

class ColetorEProcessadorDados:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.session = requests.Session()

    def buscar_datas(self):
        response = self.session.get(self.url, headers=self.headers)
        sopa = soup(response.content, "html.parser")
        datas = sopa.find("select", {"name": "ctl00$cphMain$ddlIssue"})
        datas = datas.find_all("option")
        return [data.text for data in datas]

    def recolher_e_processar_dados(self, data):
        Script_Manager = "ctl00$cphMain$UpdatePanel1|ctl00$cphMain$ddlIssue"
        User_Name = ""
        Password = ""
        Main_Email = ""

        parametros = {
            "ctl00$cphMain$ScriptManager1": Script_Manager,
            "ctl00$UserName": User_Name,
            "ctl00$Password": Password,
            "ctl00$cphMain$txtEmail": Main_Email,
            "__EVENTTARGET": "ctl00$cphMain$ddlIssue",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": "",
            "__VIEWSTATEGENERATOR": "",
            "__ASYNCPOST": "true",
            "ctl00$cphMain$ddlIssue": data
        }

        response = self.session.post(self.url, headers=self.headers, data=parametros)
        sopa = soup(response.content, "html.parser")
        table = sopa.find("table", {"class": "DataGrid"})
        df = pd.read_html(table.prettify())[0]
        df.columns = df.loc[0]
        df = df.loc[1:, ["Resin", "Bid"]]
        df["Data"] = data
        df = df.rename(columns={"Resin": "indicador", "Bid": "Valor"})
        
        # Tratamento adicional dos dados, se necessário
        # ...

        return df

    def coletar_e_processar_todos_os_dados(self):
        datas = self.buscar_datas()
        df_lista = []

        for data in datas:
            df_data = self.recolher_e_processar_dados(data)
            df_lista.append(df_data)

        df_concatenado = pd.concat(df_lista)
        df_concatenado.reset_index(drop=True, inplace=True)

        # Tratamento final dos dados, se necessário
        # ...

        return df_concatenado

    def baixar_excel(self, df, nome_arquivo="dados_excel.xlsx", nome_planilha="dados_excel"):
        df.to_excel(nome_arquivo, sheet_name=nome_planilha, index=False)


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4240.193 Safari/537.36"
    }
    url = "https://www.theplasticsexchange.com/Research/WeeklyReview.aspx"

    coletor_processador = ColetorEProcessadorDados(url, headers)
    df_final = coletor_processador.coletar_e_processar_todos_os_dados()
    coletor_processador.baixar_excel(df_final)


if __name__ == "__main__":
    main()
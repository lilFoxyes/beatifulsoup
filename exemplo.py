import pandas as pd
import requests
import openpyxl
from bs4 import BeautifulSoup as soup


def receber_os_dados():
 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4240.193 Safari/537.36"
    }

    url = "https://www.theplasticsexchange.com/Research/WeeklyReview.aspx"
    response = requests.get(url, headers=headers)

   
    if response.status_code != 200:
        print("Error")
        return None

  
    sopa = soup(response.content, "html.parser")

   
    table = sopa.find("table", {"class": "DataGrid"})


    df = pd.read_html(str(table))[0]

    
    df.columns = df.loc[0]

   
    df = df.drop(0, axis=0)

   
    df = df.loc[:, ["Resin", "Bid"]]

    
    df["Data"] = pd.to_datetime("2023-11-03")

   
    df = df.rename(columns={"Resin": "indicador", "Bid": "Valor"})

    return df


def dados_excel():
 
    wb = openpyxl.load_workbook("INTL_TPE.xlsx")

    sheet = wb.active

    
    df_excel = pd.read_excel(sheet.sheetpath, header=3, usecols=["ID", "indicador"])

    return df_excel


def merge():

    df_web = receber_os_dados()


    df_excel = dados_excel()


    df_merged = df_web.merge(df_excel, on="indicador", how="left")

    df = df_merged[["ID", "Data", "Valor"]]

    return df


def df_tratado():

    df["Valor"] = df["Valor"].str.replace("$", "")


    df["Valor"] = df["Valor"].astype(float)

    return df

def salvar_em_excel(df, dados_excel):
    
    dados_excel = pd.ExcelWriter(dados_excel)

   
    df.to_excel(dados_excel, sheet_name="Dados_Excel")

    
    dados_excel.save()


def main():
   
    df = merge()

   
    df = df_tratado()

    salvar_em_excel

    

if __name__ == "__main__":
    main()

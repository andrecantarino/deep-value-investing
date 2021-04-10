#!/usr/bin/env python3

import re
import csv
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict
from decimal import Decimal
from datetime import date

def scrap_page(*args, **kwargs):
    url = 'http://www.fundamentus.com.br/resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min': '',
            'pl_max': '',
            'pvp_min': '',
            'pvp_max' : '',
            'psr_min': '',
            'psr_max': '',
            'divy_min': '',
            'divy_max': '',
            'pativos_min': '',
            'pativos_max': '',
            'pcapgiro_min': '',
            'pcapgiro_max': '',
            'pebit_min': '',
            'pebit_max': '',
            'fgrah_min': '',
            'fgrah_max': '',
            'firma_ebit_min': '',
            'firma_ebit_max': '',
            'margemebit_min': '',
            'margemebit_max': '',
            'margemliq_min': '',
            'margemliq_max': '',
            'liqcorr_min': '',
            'liqcorr_max': '',
            'roic_min': '',
            'roic_max': '',
            'roe_min': '',
            'roe_max': '',
            'liq_min': '',
            'liq_max': '',
            'patrim_min': '',
            'patrim_max': '',
            'divbruta_min': '',
            'divbruta_max': '',
            'tx_cresc_rec_min': '',
            'tx_cresc_rec_max': '',
            'setor': '',
            'negociada': 'ON',
            'ordem': '1',
            'x': '28',
            'y': '16'}

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    content = re.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update({rows.getchildren()[0][0].getchildren()[0].text: {'Cotacao': todecimal(rows.getchildren()[1].text),
                                                                        'P/L': todecimal(rows.getchildren()[2].text),
                                                                        'P/VP': todecimal(rows.getchildren()[3].text),
                                                                        'PSR': todecimal(rows.getchildren()[4].text),
                                                                        'DY': todecimal(rows.getchildren()[5].text),
                                                                        'P/Ativo': todecimal(rows.getchildren()[6].text),
                                                                        'P/Cap.Giro': todecimal(rows.getchildren()[7].text),
                                                                        'P/EBIT': todecimal(rows.getchildren()[8].text),
                                                                        'P/ACL': todecimal(rows.getchildren()[9].text),
                                                                        'EV/EBIT': todecimal(rows.getchildren()[10].text),
                                                                        'EV/EBITDA': todecimal(rows.getchildren()[11].text),
                                                                        'Mrg.Ebit': todecimal(rows.getchildren()[12].text),
                                                                        'Mrg.Liq.': todecimal(rows.getchildren()[13].text),
                                                                        'Liq.Corr.': todecimal(rows.getchildren()[14].text),
                                                                        'ROIC': todecimal(rows.getchildren()[15].text),
                                                                        'ROE': todecimal(rows.getchildren()[16].text),
                                                                        'Liq.2meses': todecimal(rows.getchildren()[17].text),
                                                                        'Pat.Liq': todecimal(rows.getchildren()[18].text),
                                                                        'Div.Brut/Pat.': todecimal(rows.getchildren()[19].text),
                                                                        'Cresc.5anos': todecimal(rows.getchildren()[20].text)
                                                                        }})
    
    return result
    
def deep_value_investing():
    shares = scrap_page()
    ebit_positivo = {}
    for key, value in shares.items():
        if value.get("P/EBIT") > 0:
            ebit_positivo[key] = value

    alta_liquidez = {}
    for key, value in ebit_positivo.items():
        if value.get("Liq.2meses") > 100_000_000.0:
            alta_liquidez[key] = value

    # fonte: https://forbes.com.br/forbes-money/2021/03/vale-a-pena-investir-em-empresas-em-recuperacao-judicial-especialistas-respondem
    recuperacao_judicial = ["TEKA4", "TCNO4", "RPMG3", "LUPA3","OIBR4","MWET4","MMXM3","INEP4","VIVR3","FRTA3","IGBR3","SLED3","FHER3","HOOT4"]

    sem_recuperacao_judicial = {}
    for key, value in alta_liquidez.items():
        if key not in recuperacao_judicial:
            sem_recuperacao_judicial[key] = value

    output = OrderedDict(sorted(sem_recuperacao_judicial.items(), key=lambda t: t[1].get("P/L"), reverse=True))

    return output

def todecimal(string):
  string = string.replace('.', '')
  string = string.replace(',', '.')

  if (string.endswith('%')):
    string = string[:-1]
    return Decimal(string) / 100
  else:
    return Decimal(string)

def format_name():
    today = date.today().strftime("%d-%m-%Y")
    return f"deep_value_investing_{today}.csv"
    

def to_csv(result):
    with open(format_name(), mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Posição','acao', 'P/L', 'cotacao', 'P/VP', 'PSR','DY', 'P/Ativo','P/Cap.Giro','P/EBIT','P/ACL','EV/EBIT','EV/EBITDA','Mrg.Ebit','Mrg.Liq.','Liq.Corr.','ROIC','ROE','Liq.2meses','Pat.Liq','Div.Brut/Pat.','Cresc.5anos'])

        index = 1
        for key, value in result.items():
            writer.writerow([
                index,
                key,
                value['P/L'],
                value['Cotacao'],
                value['P/VP'],
                value['PSR'],
                value['DY'],
                value['P/Ativo'],
                value['P/Cap.Giro'],
                value['P/EBIT'],
                value['P/ACL'],
                value['EV/EBIT'],
                value['EV/EBITDA'],
                value['Mrg.Ebit'],
                value['Mrg.Liq.'],
                value['Liq.Corr.'],
                value['ROIC'],
                value['ROE'],
                value['Liq.2meses'],
                value['Pat.Liq'],
                value['Div.Brut/Pat.'],
                value['Cresc.5anos']
                ])
            index = index + 1

if __name__ == '__main__':
    from waitingbar import WaitingBar
    
    progress_bar = WaitingBar('[*] Downloading...')

    result = deep_value_investing()

    progress_bar.stop()

    to_csv(result)

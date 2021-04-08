#!/usr/bin/env python3

from flask import Flask, jsonify
from fundamentus import get_data
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)

# First update
lista, dia = dict(get_data()), datetime.strftime(datetime.today(), '%d')
lista = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in lista.items()}

@app.route("/")
def json_api():
    return jsonify(lista)

def get_data():
    global lista, dia
    
    # Then only update once a day
    if dia == datetime.strftime(datetime.today(), '%d'):
        return lista
    else:
        lista, dia = dict(get_data()), datetime.strftime(datetime.today(), '%d')
        lista = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in lista.items()}
        return lista

@app.route("/deep")
def deep_api():
    shares = get_data()
    ebit_positivo = {}
    for key, value in shares.items():
        if value.get("P/EBIT") > 0:
            ebit_positivo[key] = value

    alta_liquidez = {}
    for key, value in ebit_positivo.items():
        if value.get("Liq.2meses") > 100_000_000.0:
            alta_liquidez[key] = value

    # TODO: remover bancos e seguradoras

    # fonte: https://forbes.com.br/forbes-money/2021/03/vale-a-pena-investir-em-empresas-em-recuperacao-judicial-especialistas-respondem
    recuperacao_judicial = ["TEKA4", "TCNO4", "RPMG3", "LUPA3","OIBR4","MWET4","MMXM3","INEP4","VIVR3","FRTA3","IGBR3","SLED3","FHER3","HOOT4"]

    sem_recuperacao_judicial = {}
    for key, value in alta_liquidez.items():
        if key not in recuperacao_judicial:
            sem_recuperacao_judicial[key] = value

    output = OrderedDict(sorted(sem_recuperacao_judicial.items(), key=lambda t: t[1].get("P/L")))

    for key, value in output.items():
        print(key, value.get("P/L"), value.get("Cotacao"))

    return jsonify(output)

app.run(debug=True)

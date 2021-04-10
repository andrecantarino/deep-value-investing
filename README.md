# deep value investing

Esse software calcula o deep value investing das ações da bolsa brasileira gerando um arquivo `.csv` com o resultado.
Ele é baseada no repositório [phoemur/fundamentus](https://github.com/phoemur/fundamentus) que fez web scraping da [fundamentus](http://www.fundamentus.com.br) para obter esses dados.

## Etapas

0. [X] Efetuar web scrapingg na página da fundamentus para obter ações da bolsa brasileira
1. [X] Excluir empresas com EBIT negativo
2. [X] Excluir empresas com liquidez diária muito baixa
3. [X] Excluir bancos e seguradoras
4. [X] Excluir empresas em recuperação judicial
5. [X] Criar ranking por Earning Yield
6. [X] Gerar csv a partir dos dados processados

## Requerimentos
Python >= 3

## Instalação
Nenhuma instalação é necessária e todo pacote se encontra na biblioteca padrão.

## Utilização
`python3 dvi.py`
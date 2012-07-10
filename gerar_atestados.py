#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright 2012 Andrés M. R. Martano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------


import os
import shutil
import subprocess
from os.path import join


# Declarações globais
PASTA_GERADOR = join("/home","programador","Gerador")
MODELO_PRINCIPAL = join(PASTA_GERADOR,"modelo.tex")
ASSINATURA = join(PASTA_GERADOR,"assinatura.jpg")
DESENHO = join(PASTA_GERADOR,"desenho.png")
SIMBOLO = join(PASTA_GERADOR,"simbolo.png")
PASTA_TEMPORARIA = "/tmp"
PASTA_ATUAL = os.getcwd()


# Gera os atestados baseado em dados na pasta_local
def gerar(pasta_local):
    arq = open(MODELO_PRINCIPAL)
    total = arq.read()
    arq.close()
    arq = open(join(pasta_local,"modelo"))
    especifico = arq.read().splitlines()
    arq.close()

    if len(especifico) < 3:
        print("MODELO TEM CONTEUDO DE MENOS. VC COLOCOU TITULO E TEXTO PRINCIPAL?")

    # Prepara modelo especifico para essa vez
    titulo = especifico[0]
    texto = especifico[2]
    total = total.replace("[TITULO]", titulo)
    total = total.replace("[TEXTO]", texto)
    total = total.replace("[NOME]", '\uline{{\small\\bfseries{{\\nome}}}}')
    arq = open(join(PASTA_TEMPORARIA,"mod.tex"), "w")
    arq.write(total)
    arq.close()

    # Copia imagens e nomes para a mesma pasta
    shutil.copy(ASSINATURA, PASTA_TEMPORARIA)
    shutil.copy(DESENHO, PASTA_TEMPORARIA)
    shutil.copy(SIMBOLO, PASTA_TEMPORARIA)
    shutil.copy(join(pasta_local,"nomes"), PASTA_TEMPORARIA)

    nomes = open(join(pasta_local,"nomes")).read().splitlines()
    nomes.pop(0)

    # Prepara diretorio dos atestados
    c = "rm -r %s" % join(pasta_local,"atestados")
    os.system(c)
    c = "mkdir -p %s" % join(pasta_local,"atestados")
    os.system(c)

    # Gera um arquivo com todos os atestados
    os.chdir(PASTA_TEMPORARIA)
    subprocess.call(["pdflatex", "mod.tex"])

    # Separa atestados
    c = 'pdfseparate mod.pdf "%s"' % join(PASTA_ATUAL,pasta_local,"atestados","%d.pdf")
    os.system(c)
    os.chdir(join(PASTA_ATUAL,pasta_local,"atestados"))

    # Renomeia atestados
    i = 1
    for nome in nomes:
        comando = 'mv %s.pdf "%s.pdf"' % (str(i), nome)
        os.system(comando)
        i += 1
    os.chdir(PASTA_ATUAL)


# Verifica se a pasta atual tem dados para gerar atestados ou se deve entrar nas
# pastas
if os.path.exists("modelo"):
    gerar("")
else:
    pastas = os.listdir(".")
    for pasta in pastas:
        if os.path.isdir(pasta):
            gerar(pasta)

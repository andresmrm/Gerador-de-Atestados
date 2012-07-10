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
import sys
from os.path import join


PASTA_RECURSOS = join("/home","programador","Gerador","recursos")
ARQ_TEXTO = join(PASTA_RECURSOS,"email_texto")
ARQ_TITULO = join(PASTA_RECURSOS,"email_titulo")
ENVIAR = False
VERBOSE = False

def procurar_arqs(diretorios):
    nomes = []
    for diretorio in diretorios:
        for root, dirs, arqs in os.walk(diretorio):
            for arq in arqs:
                if arq[-4:] == ".pdf":
                    nomes.append(join(root,arq))
    return nomes

# Carrega dados do BD
bd = {}
arq = open(join(PASTA_RECURSOS,"bd"),"r")
antigos = arq.read()
antigos = antigos.decode("utf-8")
arq.close()
for linha in antigos.splitlines():
    campos = linha.split(",")
    nome = campos[0]
    email = campos[1]
    bd[nome] = email

# Caso tenha recebido nomes pelo terminal, envia apenas para eles
nomes = []
diretorios = []
for arg in sys.argv[1:]:
    if arg[0] == '-':
        if arg == "-e":
            ENVIAR = True
        elif arg == "-v":
            VERBOSE = True
    elif os.path.isdir(arg):
        diretorios.append(arg)
    elif arg[-4:] == ".pdf":
        nomes.append(arg)
nomes = nomes+procurar_arqs(diretorios)
if len(nomes) == 0:
    nomes = procurar_arqs(".")
nomes.sort()

# Prepara titulo
titulo = open(ARQ_TITULO).read().splitlines()[0]

# Envia emails com atestados, para aquelas pessoas que foram encontradas no BD
i = 0
for nome in nomes:
    nome = nome.decode("utf-8")
    nome_arq = nome
    nome = nome.rpartition("/")[2]
    nome = nome.rpartition(".")[0]
    nome = nome.replace("Profa. Dra. ","")
    nome = nome.replace("Prof. Dr. ","")
    email = bd.get(nome)
    if email != None:
        print nome,email
        email = email.partition("#")[0]
        comando = 'mutt -s "%s" -a "%s" -- %s < %s' % (titulo, nome_arq, email, ARQ_TEXTO)
        comando = comando.encode("utf-8")
        if VERBOSE:
            print comando
        if ENVIAR:
            print "ENVIANDO..."
            os.system(comando)
            print "ENVIADO!"
        else:
            i += 1
    else:
        i += 1
        print(nome,"------------------------------------")

print("NUM DE ATESTADOS NAO ENVIADOS: %s" % str(i))

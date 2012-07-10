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
from os.path import join


# Abre arquivo com emails exportados do google
arq = open(join("recursos","google.csv"))
novos = arq.read()
novos = novos.decode("utf-16le")
arq.close()

# Le emails que ja estao no BD
bd = {}
caminho_bd = join("recursos","bd")
if os.path.isfile(caminho_bd):
    arq = open(caminho_bd)
    antigos = arq.read()
    antigos = antigos.decode("utf-8")
    arq.close()

    for linha in antigos.splitlines():
        campos = linha.split(",")
        nome = campos[0].strip()
        email = campos[1].strip()
        var = bd.get(email)
        if var == None:
            bd[email] = nome
        else:
            print("EMAIL %s REPETIDO! DESCARTANDO: %s DEIXANDO: %s" % (email,nome,var))

# Adiciona emails que estao no arquivo exportado do google mas nao no BD
for linha in novos.splitlines()[1:]:
    linha = linha.strip()
    campos = linha.split(",")
    nome = campos[0].strip()
    emails = []
    for c in campos:
        if c.find("@") != -1:
            if c not in emails:
                emails.append(c.strip())
    if len(nome) > 1 and len(emails) > 0:
        if bd.get(emails[0]) == None:
            bd[emails[0]] = nome.title()
            print("Adicionando: %s - %s" %(nome,emails[0]))

# Ordena tudo
ordenada = []
for email in bd:
    nome = bd[email]
    linha = "%s,%s\n" % (nome, email)
    linha = linha.encode("utf-8")
    ordenada.append(linha)
ordenada.sort()

# Reescreve BD
arq = open(caminho_bd,"w")
for linha in ordenada:
    arq.write(linha)
arq.close()

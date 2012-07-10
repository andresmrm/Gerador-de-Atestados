Gerador-de-Atestados
====================

Um gerador de atestados utilizando Latex e Python.


Como gerar atestados:
----------

1. Instale Latex e seus extras
2. Edite *gerador_atestados.py* para que as variáveis globais apontem para os arquivos certos
3. Coloca as imagens citadas nas variáveis globais nos locais certos
4. Renomeie os *modelo_de...* para seus nomes corretos e os coloque nas pastas certas
5. Rode *gerador_atestados.py*


Como envia-los por email:
----------

1. Instale e configure o Mutt
2. Gere os certificados como explicado anteriormente
3. Faça o arquivo de BD, ou altere um gerado com o *atualizar_emails.py* e um arquivo exportado do Gmail
4. Rode *enviar_atestados.py*

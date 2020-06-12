from datetime import datetime
import ast
from locale import setlocale, LC_ALL
import os
from django.conf import settings
from django.http import HttpResponse
import time

"""
Lib destinada a gerar macros para o Terminal HOD

Tipos de Operação (op):

"inclusao_dep": Inclusão de dependentes pelo CDIADEPEND
"movfin": Movimentação Financeira pelo FPATMOVFIN
"adautoriza": Liberação de rubricas pelo ADAUTORIZA
"atua_uorg": Atualização de UORGs pelo CDALFUNC
"permanencia_dep": Permanência de dependentes pelo CDIADEPEND
"exclusao_dep": Exclusão de dependentes pelo CDIADEPEND
"altera_fard": Atualização de índice fardamento pelo CDIEINDFAR
"inclusao_servidores": Inclusão de Servidores pelo CDINREGIST e demais telas

"""

setlocale(LC_ALL, '')

OPCOES = {
    "inclusao_dep": "Inclusão de dependentes pelo CDIADEPEND",
    "movfin": "Movimentação Financeira pelo FPATMOVFIN",
    "atua_uorg": "Atualização de UORGs pelo CDALFUNC",
    "adautoriza": "Liberação de rubricas pelo ADAUTORIZA",
    "permanencia_dep": "Permanência de dependentes pelo CDIADEPEND",
    "exclusao_dep": "Exclusão de dependentes pelo CDIADEPEND",
    "altera_fard": "Atualização de índice fardamento pelo CDIEINDFAR",
    "inclusao_servidores": "Inclusão de Servidores pelo CDINREGIST",
}

def baixar_macro(op, query):

    def exitscreen(count):
        # if count == ((list(act(0).keys())[-1] * len(query)) + 2): #TODO: CALCULO ESTA ERRADO. EM ARQUIVOS GRANDES PARA ANTES
        #     return "true"
        # else:
        return "false"

    def entryscreen(count):
        if count == 0:
            return "true"
        else:
            return "false"

    def nextscreen(count): #TODO: erro do exitscreen reflete aqui. nesta tela o nextscreen fica vazio
        # if count == ((list(act(0).keys())[-1] * len(query)) + 2):
        #     return ""
        # else:
        return str("        <nextscreen name=\"Tela" + str((count + 1)) + "\" />\n")

    def actions(tela, linha_incl):
        screens = ""
        for x in range(len(act(linha_incl)[tela])):
            if (act(linha_incl)[tela][x]) is None:
                continue
            else:
                screens += act(linha_incl)[tela][x] + str("\n")
        return screens

    def descriptions(tela):
        screens = ""  # Formula nao esta funcionando para o ultimo item de cada lista
        for x in range(len(description[op][tela])):
            if (description[op][tela][x]) is None:
                continue
            else:
                screens += description[op][tela][x] + str("\n")
            return screens

    def description_field(numfields, numinputfields):
        if (numfields < 0 or numfields == ""):
            x1 = ""
        else:
            x1 = "            <numfields number=\"" + str(numfields) + "\" optional=\"false\" invertmatch=\"false\" />"
        if (numinputfields < 0 or numinputfields == ""):
            x2 = ""
        else:
            x2 = "            <numinputfields number=\"" + str(
                numinputfields) + "\" optional=\"false\" invertmatch=\"false\" />"
        return [x1, x2]

    def var_field(op):
        if usevars[op][0] != "true":
            return ""
        else:
            full_param = "<vars>\n"
            for item in usevars[op][1:]:
                full_param += str(item) + "\n"
            full_param += "</vars>\n"
            return full_param

    if op == "adautoriza":
        val = {}
        query = query.order_by('cod').values('cod', 'matricula')
        querycod = query.distinct('cod').values('cod')
        count=0
        for i in range(len(querycod)):
            queryspaces = int(len(query.filter(cod=querycod[i]['cod']).values('matricula')))
            for p in range((queryspaces//12)+(1 if queryspaces % 12 != 0 else 0)):
                val[count] = {str(querycod[i]['cod']):query.filter(cod=querycod[i]['cod']).values('matricula')[12*p:12*(p+1)]}
                count += 1
        query = val

    usevars = {
        "inclusao_dep": ["false"],
        # "movfin": ["true", " <create name=\"$operacao$\" type=\"string\"/>"],
        "movfin": ["false"],
        "adautoriza": ["false"],
    }

    description = {
        "inclusao_dep": {
            0: [""],
            1: description_field(70, 4),  # Ultimo campo nao aparece
            2: [""],
            3: [""],
            4: description_field(129, 24),
            5: description_field(150, 14),
            6: description_field(149, 1),
            7: description_field(156, 0),
            8: description_field(70, 4),  # Ultimo campo nao aparece
        },
        "movfin": {
            0: [""],
            1: description_field(70, 4),  # TODO: Ultimo campo nao aparece
            2: description_field(84, 6),
            3: [""],
            4: [""],
            5: [""],
            6: [""],
            7: description_field(84, 6),
            8: description_field(70, 4),  # Ultimo campo nao aparece
        },
        "adautoriza": {
            0: [""],
            1: description_field(47, 1),  # TODO: Ultimo campo nao aparece
            2: description_field(91, 10),
            3: description_field(91, 9),
            4: description_field(125, 12),
            5: description_field(122, 1),
            6: description_field(125, 0),
            7: description_field(47, 1),
        },
    }

    def act(linha_incl):

        def input(param, *adparam):
            full_param = str(param)
            for item in adparam:
                full_param += str(item)
            return (
                        "        <input value=\"" + full_param + "\" row=\"0\" col=\"0\" movecursor=\"true\" xlatehostkeys=\"true\" encrypted=\"false\" />")

        def mouseclick(row, column):
            return ("        <mouseclick row=\"" + str(row) + "\" col=\"" + str(column) + "\" />")

        def iffield(expression, **iftrueiffalse):
            """
            :param expression: Expressão condicional conforme exigido pelo sistema, que irá dentro
            da chave "<if condition= ...>" . Ex: "(($condition1$ !='')&&($condition2$)||($condition3$ < 100))"

            :param iftrueiffalse: key arguments "iftrue" e "iffalse" para definir o que executar se a condição for
            verdadeira e se for falsa, sempre expressa entre colchetes. Ex:

            iffield("5>3",iftrue=[input("1577661","[enter]"), mouseclick(5,20),input("[enter]")],
                          iffalse=[input("[enter]"*5)])

            :return: retorna expressão if para a macro. Ex:

            <if condition="5>3>
               <input value="1577661[enter]" row="0" col="0" movecursor="true" xlatehostkeys="true" encrypted="false"/>
               <mouseclick row="5" col="20" />
               <input value="[enter]" row="0" col="0" movecursor="true" xlatehostkeys="true" encrypted="false" />
            </if>
            <else>
               <input value="[enter][enter][enter][enter][enter]" row="0" col="0" movecursor="true" xlatehostkeys=
               "true" encrypted="false" />
            </else>
            """

            full_param = (
                    "        <if condition=\"" + str(expression) + ">\n"
            )
            iftrue = iftrueiffalse.get("iftrue")
            iffalse = iftrueiffalse.get("iffalse")
            for item in iftrue:
                full_param += str(item) + "\n"
            full_param += "\n        </if>\n"
            if iffalse != None:
                full_param += "      <else>\n"
                for item in iffalse:
                    full_param += str(item) + "\n"
                full_param += "      </else>\n"
            return full_param  # TODO: Verificar se expressao deu certo e se conversao de tuplas em listas funcionou
        str_query = lambda x: '' if x is None else str(x)
        action={}
        if op=="inclusao_dep":
            def beneficios_str(linha_incl):
                ben = ast.literal_eval(query[linha_incl].beneficios)
                ben = [n.strip() for n in ben]
                beneficios_str = ""
                for x in range(len(ben)):
                    if ben[x] == "10":
                        continue
                    else:
                        beneficios_str += str(ben[x]).zfill(2) + str(
                            query[linha_incl].data_protocolo_req.strftime(("%d%b%Y")))
                return beneficios_str

            if query[linha_incl].certidao_tipo:
                certidao = "X[tab]"
            else:
                certidao = "[tab]X"

            action = {
                        0: [mouseclick(22, 15), input("&gt;CDIADEPEND[enter]")],
                        1: [input(query[linha_incl].matricula_titular, "[enter]")],
                        2: [input("[enter]" * 5)],
                        3: [input(query[linha_incl].nacionalidade.cod, query[linha_incl].cpf, "[enter]")],
                        4: [input("[deleteword][tab]" * 28), mouseclick(9, 40),
                            input(query[linha_incl].sexo.cod, str(query[linha_incl].grau.cod).zfill(3),
                            str(query[linha_incl].condicao.cod).zfill(2), query[linha_incl].nome_mae), 
                            mouseclick(15, 16), input(certidao),
                            mouseclick(16, 22), input(str_query(query[linha_incl].certidao_nome_cartorio)),
                            mouseclick(17, 19), input(str_query(query[linha_incl].certidao_antiga_uf)),
                            mouseclick(17, 38),input(str_query(query[linha_incl].certidao_antiga_numero)),
                            mouseclick(17, 56),input(str_query(query[linha_incl].certidao_antiga_folha)),
                            mouseclick(17, 70),input(str_query(query[linha_incl].certidao_antiga_livro)),
                            mouseclick(19, 19),input(str_query(query[linha_incl].certidao_nova_numero)),
                            input("[enter]")],
                        5: [input("[deleteword][tab]" * 28, beneficios_str(linha_incl), "[enter]")],
                        6: [input("S[enter]")],
                        7: [input("[enter]")],
                        8: [input("[pf12]")],
                    }
        if op=="movfin":

            if query[linha_incl]['valor']!= None :
                if query[linha_incl]['ass_calc']!= None and int(query[linha_incl]['ass_calc']) != 38:
                    query[linha_incl]['valor']=str(query[linha_incl]['valor']).replace(".",",")
                else:
                    query[linha_incl]['valor']=str(query[linha_incl]['valor']).replace(".","")

            action = {
                    0: [mouseclick(22,15),input("&gt;FPATMOVFIN[enter]")],
                    1: [input(query[linha_incl]['matricula_titular'],"[enter]")],
                    2: [input(query[linha_incl]['r_d'],query[linha_incl]['rubrica'],query[linha_incl]['seq'],
                        query[linha_incl]['op'],
                              ("[enter]" if query[linha_incl]['op']=="E" else "[down]X[enter]"))],
                    3: [input("[enter]")] if query[linha_incl]['op']=="E" else (
                        [input(query[linha_incl]['prazo'],query[linha_incl]['valor']),mouseclick(14, 27),
                        input(query[linha_incl]['ass_calc'],"[enter]","[enter]")] if int(query[linha_incl]['ass_calc'])!=38 else
                        [mouseclick(14, 27),input(query[linha_incl]['ass_calc']),mouseclick(18, 27),
                        input(query[linha_incl]['valor'],"[enter]","[enter]")]),
                    4: [input("[enter]")] if query[linha_incl]['op']=="E" else
                        [input(query[linha_incl]['doc_legal'],"[tab]"),mouseclick(13,14),
                         input((query[linha_incl]['justificativa'])[0:45]),mouseclick(14,14),
                         input((query[linha_incl]['justificativa'])[45:90]),mouseclick(15,14),
                         input((query[linha_incl]['justificativa'])[90:135]),mouseclick(16,14),
                         input((query[linha_incl]['justificativa'])[135:180]),input("[enter]")],
                    5: [input("C[enter]")],
                    6: [input("[enter]")],
                    7: [input("[pf12]")],
                    8: [input("[pf12]")],
                }
        if op=="adautoriza":
             seq1=['82265',]
             q = list(query[list(query.keys())[linha_incl]].keys())[0]
             def querymat(q):
                 p = ''
                 for i in range(len(query[list(query.keys())[linha_incl]][q])):
                    p += query[list(query.keys())[linha_incl]][q][i]['matricula']
                 return p
             action = {
                    0: [mouseclick(22,15),input("&gt;ADAUTORIZA[enter]")],
                    1: [input("3[enter]")],
                    2: [input(q,"X","[down][delete]"*8,"[enter]")] if q in seq1 else [input(q,"[enter]")],
                    3: [input("[enter]")],
                    4: [input(querymat(q),"[enter]")],#TODO: Nao esta lendo a 0, que possui
                    5: [input("C[enter]")],
                    6: [input("[enter]")],
                    7: [input("[pf3]")],
                }

        return action

    count = 0

    header = (
            "<HAScript name=\"" + op + " - " + str(
        datetime.now()) + "\" description=\"\" timeout=\"60000\" pausetime=\"300\" promptall=\"true\" blockinput="
                          "\"false\" author=\"\" creationdate=\"03/10/2019 15:58:18\" supressclearevents="
                          "\"false\" usevars=\"" + usevars[op][0] + "\" ignorepauseforenhancedtn=\"true\""
                          " delayifnotenhancedtn=\"0\" ignorepausetimeforenhancedtn=\"true\">\n"
         + var_field(op) #TODO: Ver se funcionou
    )

    body = ""
    start_time = time.time()
    for linha_incl in range(len(query)):

        for tela in act(0):
            screen = (
                # Condicionais em entry e exitscreen dependendo se forem a tela de entrada ou saida
                    "<screen name=\"Tela" + str(count) + "\" entryscreen=\"" + entryscreen(
                count) + "\" exitscreen=\"" + exitscreen(count) +
                    "\" transient=\"false\">\n"
                    "    <description >\n"
                    "        <oia status=\"NOTINHIBITED\" optional=\"false\" invertmatch=\"false\" />\n" +
                    str(descriptions(tela)) +
                    "    </description>\n"
                    "    <actions>\n" +
                    str(actions(tela, linha_incl)) +
                    "    </actions>\n"
                    "    <nextscreens timeout=\"0\" >\n" +
                    str(nextscreen(count)) +
                    "    </nextscreens>\n"
                    "</screen>\n\n"
            )
            count += 1
            body += screen
    print('Tempo para execução MACROS: ' + str(time.time() - start_time))
    footer = (
        "</HAScript>"
    )
    macro = header + body + footer
    # print (macro)
    fname = op + "_" + str(datetime.now().strftime("%d%b%Y_%Hh%Mm%Ss%fms")) + ".mac"
    file_path = os.path.join(settings.MEDIA_ROOT, r'main/macros' + '/' + fname)
    with open(file_path, "w") as f:
        # chunk=400
        # for i in range(0,len(macro),chunk):
        #     f.write(macro[i:chunk])
        f.write(macro)
    response = HttpResponse(open(file_path, "r").read())
    response['Content-Disposition'] = 'attachment; filename=' + fname
    response['Content-Type'] = 'application/octet-stream'
    return response

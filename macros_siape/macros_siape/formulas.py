import calendar
import unicodedata
import re
from datetime import datetime


def limpastr(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    if palavra != None:
        nfkd = unicodedata.normalize('NFKD', palavra)
    else:
        nfkd = ''
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)


def days360(start_date, end_date, method_eu=False):
    start_day = start_date.day
    start_month = start_date.month
    start_year = start_date.year
    end_day = end_date.day
    end_month = end_date.month
    end_year = end_date.year

    if (
            start_day == 31 or
            (
                    method_eu is False and
                    start_month == 2 and (
                            start_day == 29 or (
                            start_day == 28 and
                            calendar.isleap(start_year) is False
                    )
                    )
            )
    ):
        start_day = 30

    if end_day == 31:
        if method_eu is False and start_day != 30:
            end_day = 1

            if end_month == 12:
                end_year += 1
                end_month = 1
            else:
                end_month += 1
        else:
            end_day = 30

    return (
            end_day + end_month * 30 + end_year * 360 -
            start_day - start_month * 30 - start_year * 360
    )


ADAUTORIZA = {
    1: [82256, 6],
    2: [82869, 6],
    3: [82265, 1],
    4: [82128, 6],
    5: [82133, 6],
    6: [82385, 6],
}
def gerarMOVFIN(self,form,**kwargs):
    def dado(info):
        try:
            return form.cleaned_data[info]
        except AttributeError:
            return form(info)

    def lanca(r_d, cod, seq, op, **kwargs):
        mesano_folha = datetime.strptime(str(dado('mes_pgto')),'%b%Y')

        #TODO: Caso a folha vire e o lancamento do mes nao entrar nele, fazer com que recalcule e entre na proxima
        if kwargs.get("sistema"):
            sistema = kwargs.get("sistema")
        else:
            sistema = DatasSistema.objects.get(sistema=1)

        if op != "E":
            prazo = kwargs.get("prazo")
            valor = kwargs.get("valor")
            if kwargs.get("ass_calc"):
                ass_calc = kwargs.get("ass_calc")
            else:
                ass_calc = 21
            doc_legal = "LEI 10486/02"
            OPTIONS_op = {'1': "INCLUSAO DE DEPENDENTE", '2': "PERMANENCIA DE DEPENDENTE",
                          '3': "EXCLUSAO DE DEPENDENTE", '9': "GSV"}
            if ([cod,seq] in ADAUTORIZA.values()) and r_d == "R":
                autorizada = False
            else:
                autorizada = True
            justificativa = (OPTIONS_op[str(dado('op'))] + str((" A CONTAR DE " +
                             dado('data_protocolo_req').strftime(("%d%b%Y"))) if
                             dado('data_protocolo_req') else "") + " - SEI " + dado('sei') +
                             " - LANCADO POR " + dado('lancado_por') + " EM " +
                             str(datetime.now().strftime("%d%b%Y às %H:%M:%S")))
            serv.arquivomovfin_set.create(r_d=r_d, cod=Rubrica.objects.get(cod=cod), op=op, seq=seq, tipo=False,
                                          prazo=prazo,
                                          valor=valor, ass_calc=ass_calc, doc_legal=doc_legal,
                                          justificativa=limpastr(justificativa), autorizada=autorizada, sistema=sistema,
                                          mesano_folha=mesano_folha)#TODO: Ver se retirar limpastr de justificativa trará problemas no lancamento
        else:
            serv.arquivomovfin_set.create(r_d=r_d, cod=Rubrica.objects.get(cod=cod), seq=seq, op=op, sistema=sistema,
                                          mesano_folha=mesano_folha)

    if kwargs.get("matricula_titular"):
        serv = Servidor.objects.get(matricula=kwargs.get("matricula_titular"))
    else:
        serv = Servidor.objects.get(matricula=dado('matricula_titular'))
    if dado('data_protocolo_req'):
        mes_retr = str(dado('data_protocolo_req').strftime(("%b%Y")))
    # Lanca Aux Moradia
    if dado('aux_mor') != None and int(dado('aux_mor')) != 0:
        lanca("R", 82135, 1, "E")
        lanca("R", 82135, 1, "I", prazo="000", valor=dado('aux_mor'))
    # Lanca Aux Moradia Retroativo
    if dado('aux_mor_retr') != None and int(dado('aux_mor_retr')) != 0:
        if dado('aux_mor_retr') < 0:
            lanca("D", 82135, 1, "I", prazo="", ass_calc=38, valor=abs(dado('aux_mor_retr')))
        else:
            lanca("R", 82135, 6, "I", prazo=mes_retr, valor=dado('aux_mor_retr'))

    # Lanca Fundo de Saude
    if dado('fsa') != None:
        if ((str(dado('op')) == '1' and int(dado('fsa')) != 0 and dado('fsa') !=
             Remuneracao.objects.get(cod_cargo=serv.cod_cargo).fsa) or
                str(dado('op')) == '3'):
            lanca("D", 98036, 1, "E")
        if int(dado('fsa')) != 0:
            lanca("D", 98036, 1, "I", prazo="000", valor=dado('fsa'))
    # Lanca Aux Pre Esc Retroativo
    if dado('aux_pre_retr') != None and int(dado('aux_pre_retr')) != 0:
        if dado('aux_pre_retr') > 0:
            lanca("R", 82869, 6, "I", prazo=mes_retr, valor=dado('aux_pre_retr'))
        else:
            lanca("D", 82869, 1, "I", prazo="", ass_calc=38, valor=abs(dado('aux_pre_retr')))
    # Lanca Cota Pre Esc Retroativa
    if dado('cota_pre_retr') != None and int(dado('cota_pre_retr')) != 0:
        if dado('cota_pre_retr') < 0:
            lanca("D", 73528, 6, "I", prazo=mes_retr, valor=abs(dado('cota_pre_retr')))
        else:
            lanca("R", 73528, 1, "I", prazo="001", valor=dado('cota_pre_retr'))
    # Lanca Aux Natalidade
    if dado('aux_nat') != None and int(dado('aux_nat')) != 0:
        lanca("R", 82265, 1, "I", prazo="001", valor=dado('aux_nat'))
    if int(dado('op')) == 9 and kwargs.get("valor"):
        #TODO: Somar GSVs já existentes dentro do mês
        lanca("R", 82307, 1, "I", prazo="001", valor=kwargs.get("valor"))

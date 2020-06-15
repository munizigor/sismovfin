from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
import re
from macros_siape.macros import baixar_macro
import time
import os
from django.conf import settings



def index(request):
	return render(request, 'main/main_page.html')
def download_sample(request):
	response = HttpResponse(open(os.path.join(settings.MEDIA_ROOT, r'main/modelo_arquivo.csv'), 'rb'), content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename= modelo.csv'
	return response
def submit_movfin(request):
	start_time = time.time()
	message = None
	if request.method == 'GET':
		message = ('Por favor, tente novamente.')
	elif request.method == 'POST':
		csv_file = request.FILES['csv_file']
		file_data = csv_file.read().decode("utf-8", "ignore")
		file_data = file_data.split("\n")
		movfin_list = []
		# Verificando se a primeira linha eh cabecalho
		init = 0
		if not(file_data[0].split(";")[0].isnumeric()):
			init = 1
		for idx, line in enumerate(file_data[init:]):
			movfin = {}
			fields = line.split(";")
			if not fields[0]:
				continue
			message_length = ('Erro na linha ' + str(idx+1) + '. Se forem lançamentos de INCLUSÃO ou ALTERAÇÃO, Verifique ' +
							  'se ela possui, respectivamente, todas as seguintes colunas: \'MATRICULA\', \'REND/DESC\',' +
							  ' \'RUBRICA\', \'SEQUENCIA\', \'OPERAÇÃO\', \'PRAZO/MÊS REF.\', \'VALOR\', \'ASSUNTO DE CALCULO\', ' +
							  '\'DOC LEGAL\' e \'JUSTIFICATIVA\'. Caso se trate de EXCLUSÃO, verifique se ela possui, na sequência,' +
							  ' as colunas \'MATRICULA\', \'REND/DESC\', \'RUBRICA\', \'SEQUENCIA\' e \'OPERAÇÃO\'  ')

			try:
				movfin['op'] = str(re.sub('[^a-zA-Z]|[\x22]', '', fields[4][0]).strip()).upper()
			except IndexError:
				message = message_length
				break
			if not(len(fields) == 10) and not(len(fields) >= 5 and movfin['op']=='E'):
				message = message_length
				break
			else:
				movfin['matricula_titular'] = str(re.sub('[^0-9]', '', fields[0]).strip()).zfill(7)
				movfin['r_d'] = str(re.sub('[^a-zA-Z]|[\x22]', '', fields[1][0]).strip()).upper()
				movfin['rubrica'] = str(re.sub('[^0-9]', '', fields[2]).strip()).zfill(5)
				movfin['seq'] = str(re.sub('[^0-9]', '', fields[3]).strip()).zfill(0)
				if movfin['op']!='E':
					movfin['prazo'] = str(re.sub('[^0-9]', '', fields[5]).strip()).zfill(3) if int(float(movfin['seq'])) in range (1,6) else str(fields[5].strip()).upper()
					try:
						movfin['valor'] = '{:.2f}'.format(float(fields[6].replace(',','.').strip()))  # TODO: Nao dividir por 100 se valores ja estiverem formatados
					except ValueError:
						message = ('Erro na linha ' + str(idx+1) + '. Certifique que o CSV foi salvo SEM FORMATAR CAMPOS ENTRE ASPAS COMO TEXTO')
						break
					movfin['ass_calc'] = '{00}'.format(str(re.sub('[^0-9]', '', fields[7]).strip()))
					movfin['doc_legal'] = str(fields[8][:30].strip()).upper()
					movfin['justificativa'] = str(fields[9][:200].strip()).upper() + ' - LANCADO EM ' + str(datetime.now().strftime("%d%b%Y às %H:%M:%S"))
				else:
					movfin['prazo'] = None
					movfin['valor'] = None
					movfin['ass_calc'] = None
					movfin['doc_legal'] = None
					movfin['justificativa'] = None
				movfin_list.append(movfin)
	if message:
		messages.error(request, message, extra_tags='safe')
		return index(request)
	else:
		print('Tempo para execução VIEWS: ' + str(time.time() - start_time))
		return baixar_macro('movfin',movfin_list)

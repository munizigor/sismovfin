		//                      //
		//DECLARAÇÃO DE FUNÇÕES//
        //                      //

	    //Marcar todas as caixas de seleção

    function CheckUncheckAll(){
        var  selectAllCheckbox=document.getElementById("checkUncheckAll");
        if(selectAllCheckbox.checked==true){
            var checkboxes =  document.getElementsByName("rowSelectCheckBox");
            for(var i=0, n=checkboxes.length;i<n;i++) {
                checkboxes[i].checked = true;
            }
        } else {
            var checkboxes =  document.getElementsByName("rowSelectCheckBox");
            for(var i=0, n=checkboxes.length;i<n;i++) {
                checkboxes[i].checked = false;
            }
        }
    }

    function RefreshReload() {
    	history.back();
    	location.reload();
    }


		//Validar CPF
	function TestaCPF(strCPF) {
        var Soma;
        var Resto;
        Soma = 0;
        strCPF = document.getElementById("cpf").value.replace(/[.-]/g,'')
      if (strCPF == "00000000000") return false;

      for (i=1; i<=9; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i);
      Resto = (Soma * 10) % 11;

        if ((Resto == 10) || (Resto == 11))  Resto = 0;
        if (Resto != parseInt(strCPF.substring(9, 10)) ) return false;

      Soma = 0;
        for (i = 1; i <= 10; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
        Resto = (Soma * 10) % 11;

        if ((Resto == 10) || (Resto == 11))  Resto = 0;
        if (Resto != parseInt(strCPF.substring(10, 11) ) ) return false;
        return true;
    }



        //Auxilio Moradia

    function AltAuxMor () {
//                if (parseInt(document.getElementsByName('op')[0].value)==1) {
                    if (parseInt(document.getElementsByName('op')[0].value)==1 &&
                        document.getElementById('id_beneficios_4').checked &&
                        document.getElementById('itMorMaj').value =='2') {
                        document.getElementById('valAuxMorRetr').value = ((Number(auxmor)-Number(auxmorsd))*(datadiff/30)).toFixed(2);
                        document.getElementById('valAuxMor').value = Number(auxmor).toFixed(2);
                    }
//                }
//                if (parseInt(document.getElementsByName('op')[0].value)==3) {
                    else if (parseInt(document.getElementsByName('op')[0].value)==3 &&
                        (document.getElementById('id_beneficios_4').checked ||
                         document.getElementById('itMorMaj').value =='1')) {
                        document.getElementById('valAuxMorRetr').value = ((Number(auxmorsd)-Number(auxmor))*(datadiff/30)).toFixed(2);
                        document.getElementById('valAuxMor').value = Number(auxmorsd).toFixed(2);
                    }
//                }
                else {
                    document.getElementById('valAuxMor').value = '';
                    document.getElementById('valAuxMorRetr').value = '';
                }
        }

    function AltFSA () {
                if (document.getElementById('id_beneficios_2').checked && parseInt(document.getElementsByName('op')[0].value)==1) {
                    document.getElementById('valFSA').value = Number(fsa*(parseInt(document.getElementById('itQtDepSau').value)+1)).toFixed(2);
                }
                else if (parseInt(document.getElementsByName('op')[0].value)==3 &&
                    ((parseInt(document.getElementById("id_causa_exclusao").value) !=  99 ||
                    document.getElementById('id_beneficios_2').checked) &&
                    parseInt(document.getElementById('itQtDepSau').value)>0)) {
                    document.getElementById('valFSA').value = Number(fsa*(parseInt(document.getElementById('itQtDepSau').value)-1)).toFixed(2);
                    }
                else {
                    document.getElementById('valFSA').value = '';
                }
        }

    function AltNat () {
                if (document.getElementById('id_beneficios_3').checked) {
                    if (document.getElementById('itQtGemSel').value == '0'){
                        document.getElementById('valNat').value = Number(auxnat).toFixed(2);
                    }
                    else {
                        document.getElementById('valNat').value = Number(auxnat*(1+(0.5*(1+parseInt(document.getElementById('itQtGemSel').value))))).toFixed(2);
                    }
                }
                else {
                    document.getElementById('valNat').value = '';
                }
        }

    function AltPreEsc () {
            if (parseInt(document.getElementsByName('op')[0].value)==1 &&
                document.getElementById('id_beneficios_0').checked) {
                document.getElementById('valPreEscRetr').value = (Number(auxpre)*mesdiff).toFixed(2);
                document.getElementById('valCotaPreEscRetr').value = (Number(-cotapre)*mesdiff).toFixed(2);
            }
            else if (parseInt(document.getElementsByName('op')[0].value)==3 &&
                document.getElementById('id_beneficios_0').checked) {
                document.getElementById('valPreEscRetr').value = (Number(-auxpre)*mesdiff).toFixed(2);
                document.getElementById('valCotaPreEscRetr').value = (Number(cotapre)*mesdiff).toFixed(2);
            }
            else {
                document.getElementById('valPreEscRetr').value = '';
                document.getElementById('valCotaPreEscRetr').value = '';
            }
        }
    //Verificar validade de data e calcular diferencas remuneratorias

    var datadiff;
    var mesdiff;
    function AtualizaDatas() {
        if (document.getElementById('data_protocolo_req').value!='') {
            var datein = document.getElementById('data_protocolo_req').value;
            $.get("/dep/dias360/", {INICIO: datein} , function(response){
                datadiff=response[0];
                mesdiff=response[1];
                if (response == "Data invalida") { //Alerta válido para Pre Esc e Moradia Retroativos
                alert("Digite uma data de requerimento válida");
                document.getElementById("data_protocolo_req").style.color = "red";
                datadiff=0;
                mesdiff=0;
                }
                else {
                document.getElementById("data_protocolo_req").style.color = "#495057";
                            $.get("/dep/dias360/", {INICIO: datein} , function(response){
                datadiff=response[0];
                mesdiff=response[1];});
                }
            AltPreEsc();
            AltAuxMor();
            }
    );
    }

    }

    if (document.getElementById('data_protocolo_req')!=null) {
        document.getElementById('data_protocolo_req').addEventListener('change', function () {AtualizaDatas()});
	}

    //Puxar CPF do db
    function ConsultaCPF(strCPF) {
        strCPF = document.getElementById("cpf").value.replace(/[.-]/g,'');
        var HttpCPF = new XMLHttpRequest();
        HttpCPF.open("GET", '/dep/consultacpf/?CPF='+strCPF);
        HttpCPF.send();
        HttpCPF.onreadystatechange = (e) => {
                if (parseInt(HttpCPF.responseText) != 0) {
                    return true; //TODO: Return nao esta funcionando
                }
                else {
                    return false;

                }
        }
    }

        //                              //
		//FIM DE DECLARACAO DAS FUNCOES//
        //                              //


        //                                           //
		//INICIO DE DECLARACAO DE PARAMETROS DE INICIO//
        //                                          //


        //Formatar data
		//$("#itDataIncl").val($.datepicker.formatDate('dd/mm/yy', new Date()));

		$(".data").datepicker({
		    changeMonth: true,
            changeYear: true,
            dateFormat: 'dd/mm/yy',
            dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
            dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
            dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
            monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
            monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
            nextText: 'Próximo',
            prevText: 'Anterior',
            onSelect: function () {AtualizaDatas()},
        });

        //Item dos Irmãos gemeos, Natalidade, Moradia e Pre Esc priori escondido e igual a 0 quando Inclusao
        if (parseInt(document.getElementsByName('op')[0].value)==1) {
		document.getElementById("itQtGemSel").value = 0;
		document.getElementById("itQtGem").style.display = "none";
        document.getElementById('id_beneficios_0').checked = false;
        document.getElementById('listid_beneficios_0').style.display = "none";
        document.getElementById('id_beneficios_3').checked = false;
        document.getElementById('listid_beneficios_3').style.display = "none";
        document.getElementById('id_beneficios_4').checked = false;
        document.getElementById('listid_beneficios_4').style.display = "none";

        //Deixar beneficios pre selecionados
        document.getElementById("id_beneficios_1").checked=true; //Deducao IR
        document.getElementById("id_beneficios_2").checked=true; //Saude
        document.getElementById("id_beneficios_4").checked=true; //Auxilio Moradia


        //Fazer desaparecer Beneficio Aux Moradia se servidor já tiver o beneficio
		document.getElementById('itMorMaj').onchange = function() {
            if (document.getElementById('itMorMaj').value != '2') {
                document.getElementById('id_beneficios_4').checked = false;
                document.getElementById('listid_beneficios_4').style.display = "none";
            } else {
                document.getElementById('listid_beneficios_4').style.display = "initial";
                document.getElementById('id_beneficios_4').checked = true;
            }
        }

		//Fazer desaparecer escolha de Quantidade de Gemeos, Natalidade e Pre Escolar se o dependente não for filho
		document.getElementById("id_grau").onchange = function() {
            if (parseInt(document.getElementById("id_grau").value) !=  8 &&
                parseInt(document.getElementById("id_grau").value) !=  6) {
                document.getElementById("itQtGem").style.display = "none";
                document.getElementById("itQtGemSel").value = 0;
                document.getElementById('id_beneficios_3').checked = false;
                document.getElementById('listid_beneficios_3').style.display = "none";
                document.getElementById('id_beneficios_0').checked = false;
                document.getElementById('listid_beneficios_0').style.display = "none";
            } else {
                document.getElementById("itQtGem").style.display = "initial";
                document.getElementById('listid_beneficios_3').style.display = "initial";
                document.getElementById('listid_beneficios_0').style.display = "initial";
            }
        }
    }

    //Tabela Beneficios escondida e igual a 0 quando Exclusao
    if (parseInt(document.getElementsByName('op')[0].value) == 3) {
        document.getElementsByClassName('beneficios')[0].style.display = "none";
//        document.getElementById("AuxFun").style.display = "none";//TODO Nao funcionando esconder o Aux Fun
        document.getElementById('id_beneficios_0').checked = false;
        document.getElementById('id_beneficios_1').checked = false;
        document.getElementById('id_beneficios_2').checked = false;
        document.getElementById('id_beneficios_3').checked = false;
        document.getElementById('id_beneficios_4').checked = false;
        //Fazer reaparecer beneficios se remocao parcial de dependencia
		document.getElementById("id_causa_exclusao").addEventListener('change', function () {
            if (parseInt(document.getElementById("id_causa_exclusao").value) ==  2) {
//                document.getElementById("AuxFun").style.display = "initial";
                document.getElementsByClassName('beneficios')[0].style.display = "none";
            }
		    else if (parseInt(document.getElementById("id_causa_exclusao").value) ==  99) {
                document.getElementsByClassName('beneficios')[0].style.display = "initial";
//                document.getElementById("AuxFun").style.display = "none";
                document.getElementById("MorMaj").style.display = "none";
                document.getElementById("itMorMaj").value = 2;
                document.getElementById("itQtDepSau").value = 0;
                document.getElementById("valFSA").value = "";
            }
            else {
                document.getElementsByClassName('beneficios')[0].style.display = "none";
                document.getElementById("MorMaj").style.display = "initial";
//                document.getElementById("AuxFun").style.display = "none";
                document.getElementById("itMorMaj").value = 2;
            }
		}
    );
    }
    // Puxar mes pagamento atual
    if (document.getElementById("itMesPagto")!=null) {
        var HttpPgto = new XMLHttpRequest();
        var mespgto;
        HttpPgto.open("GET", '/dep/mesfolha/');
        HttpPgto.responseType="text";
        HttpPgto.send();

        HttpPgto.onreadystatechange = (e) => {
              mespgto = JSON.parse(HttpPgto.responseText);
              document.getElementById("itMesPagto").value = mespgto[1].toUpperCase();
              diapgto = new Date(mespgto[0]).toUTCString();
         }
     }

 /*       function getVal(url) {
        var xmlhttp = new XMLHttpRequest();


        xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var myArr = JSON.parse(this.responseText);
            }
        };

        xmlhttp.open("GET", url, true);
        xmlhttp.send();
        }
*/
        //TODO: Fazer desaparecer outros ids beneficios conforme tabela Grau_Cond_Benef

		//TODO: Alterar de jQuery para Vue.js ou JS puro
	//mascaras das id's
		$("#sei").mask("00000-00000000/0000-00");
		$("#cpf").mask("000.000.000-00");
		$("#data_protocolo_req").mask("00/00/0000");
		$("#certidao_nova_numero").mask("000000   00   00   0000   0   00000   000   0000000   00");
		$("#certidao_nome_cartorio").mask("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS");

	//limpar dados de certidao quando alternar tab's

    if (parseInt(document.getElementsByName('op')[0].value)==1) {
		document.getElementById("antigo-tab").onclick = function () {
			document.getElementById('certidao_nova_numero').value ='';
		};
		document.getElementById("novo-tab").onclick = function () {
			document.getElementById('certidao_antiga_folha').value ='';
			document.getElementById('certidao_antiga_livro').value ='';
			document.getElementById('certidao_antiga_numero').value ='';
			document.getElementById('certidao_antiga_ano').value ='';
		};
		}


        //                                           //
		//FIM DE DECLARACAO DE PARAMETROS DE INICIO//
        //                                          //


    //Validar CPF
    document.getElementById("cpf").addEventListener('blur', function () {
        cpf = document.getElementById("cpf").value.replace(/[.-]/g,'')
        if (cpf!="") {
            if (ConsultaCPF()) {
                alert("CPF já lançado como dependente");
                document.getElementById("cpf").style.color = "red";
                setTimeout(function () {document.getElementById("cpf").focus();},1);
            }
            if (!TestaCPF()) {
                alert("CPF Inválido. Digite o número correto");
                document.getElementById("cpf").style.color = "red";
                setTimeout(function () {document.getElementById("cpf").focus();},1);
            }
            else {
            document.getElementById("cpf").style.color = "#495057";
            }
        }
     }
     );

    //Verificar se CPF já consta na base
    /*document.getElementById("cpf").addEventListener('blur', function () {
        cpf = document.getElementById("cpf").value.replace(/[.-]/g,'')
        //TODO: incluir condição se cpf for diferente de vazio
        if (!TestaCPF(cpf)) {
            alert("CPF Inválido. Digite o número correto");
            document.getElementById("cpf").style.color = "red";
           //setTimeout(function () {document.getElementById("cpf").focus();},1);
        }
        else {
        document.getElementById("cpf").style.color = "#495057";
        }
     }
     );*/


	//TODO: buscar nome dependente pelo CPF no sistema TCU
//	$("#cpf").on('change', function() {
//       if ($("#cpf").val().match(/\d/g).length==11) {
//            $.ajax({
//                dataType: "json",
//               url:"https://siga.apps.tcu.gov.br/siga/cpf/" + $("#cpf").val().match(/\d/g).join(""),
//                data:"",
//                success: function(response){
//                            var obj = JSON.parse(response);
//                            $("#nome").val(obj.value);
//                         }
//           });
//	    }
//	})

	//buscar matriculas
		$(function() {
			$("#matricula_titular").autocomplete({
			source: "search/",
			select: function (event, ui) { //item selected
			AutoCompleteSelectHandler(event, ui)
			},
			minLength: 4,
			});
		});

			function AutoCompleteSelectHandler(event, ui) {
				var selectedObj = ui.item;
			}
    //Inicio da funcao para puxar dados do requerimento
    function DadosReq() {
        num_req=document.getElementById('num_req');
        if (num_req.value.length >= 8){
        $.ajax({
            url:'/dep/consultareq/',
            data: {
                'num_req': num_req.value
            },
            dataType: 'json',
            success: function (response) {
                console.log(response);
                $("#matricula_titular").val(response["Matrícula SIAPE"]);
                $("#matricula_titular").blur();
                $("#cpf").val(response["CPF do DEPENDENTE"]);
                $("#id_sexo").val(response["Sexo do DEPENDENTE"].charAt(0));
               //todo: $("#id_nacionalidade").val(response["Nacionalidade do DEPENDENTE"]);
               $("#nome_mae").val(response["Nome da Mãe do DEPENDENTE"]);
               $("#certidao_nova_numero").val(response["Matrícula da certidão de Nascimento/Casamento"]);
               $("#id_certidao_nome_cartorio").val(response["Nome do Cartório"]);
               $("#sei").val(response["Sei"]);
            }
        });

//        var HttpReq = new XMLHttpRequest();
//
//        HttpReq.open("GET", '/dep/consultareq/?num_req='+num_req.value);
//        HttpReq.send();
//        HttpReq.onreadystatechange = (e) => {
//                if (parseInt(HttpReq.responseText) != 0) {
//                    return true; //TODO: Return nao esta funcionando
//                }
//                else {
//                    return false;
//
//                }
//        }
        }
    }

	//Função geral para atualizar dados financeiros e matricula quando for selecionada alterada

	    var auxmor=0;
	    var auxmorsd=0;
	    var fsa = 0;
	    var auxnat=0;
	    var auxpre=0;
	    var cotapre=0;

		$("#matricula_titular").on('blur', function (e) {
			var matr = document.getElementById('matricula_titular').value;

			document.getElementById("nome_tit").value='';
			document.getElementById("sit_func").value='';
            document.getElementById("cod_cargo").value='';
            //Executado apenas se nao for permanencia - op=1
            if (parseInt(document.getElementsByName('op')[0].value)!=2) {
                document.getElementById("valAuxMor").value='';
                document.getElementById("valFSA").value='';
                document.getElementById("valAuxMorRetr").value='';
                document.getElementById("valPreEscRetr").value='';
                document.getElementById("valNat").value='';
			}
			if (matr.length>=6) {
				$.get("/dep/atualizaNome/", {GET_ID : matr} , function(response){
//				if (this.status != 200) {
//				alert(this.status + "Matrícula Inválida. Digite o número correto");
//			    }
//                else {}
					$("#nome_tit").val(response[0]);
					$("#sit_func").val(response[1]);
					$("#cod_cargo").val(response[2]);
                    if (parseInt(document.getElementsByName('op')[0].value)!=2) { //Executado apenas se for Inclusao - op=1
                        auxmor=response[3];
                        auxmorsd=response[4];
                        fsa = response[5];
                        auxnat = response[6];
                        auxpre = response[7];
                        cotapre = response[8];
                        AltAuxMor ();
                        AltFSA ();
                        AltNat ();
                        AltPreEsc ();
			        }
				});
			}
		})

        //Alterar valores na folha de pagamentos

        //Puxa dados do requerimento
        document.getElementById('num_req').addEventListener('blur', function () {DadosReq()});

        //Altera Aux MOradia a medida em que se alteram os parametros

        var classMoradia = document.getElementsByClassName('moradia');
        for (var i = 0; i < classMoradia.length; i++) {
            classMoradia[i].addEventListener('change', function () {AltAuxMor ()})  ;
        }

       //Altera FSA a medida em que se alteram os parametros
        var classFSA = document.getElementsByClassName('fsa');
        for (var i = 0; i < classFSA.length; i++) {
            classFSA[i].addEventListener('change', function () {AltFSA ()})  ;
        }

       //Altera Natalidade
        var classNat = document.getElementsByClassName('natalidade');
        for (var i = 0; i < classNat.length; i++) {
            classNat[i].addEventListener('change', function () {AltNat ()})  ;
        }

       //Altera PreEsc e Mor
        var classPreEsc = document.getElementsByClassName('preescolar');
        for (var i = 0; i < classPreEsc.length; i++) {
            classPreEsc[i].addEventListener('change', function () {AltPreEsc ()})  ;
        }

        //TODO: filtrar COndicao de acordo com grau de dependência

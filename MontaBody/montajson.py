
'''
Função criada para utilizá-la no LOGIX com serviço rest rodando.
Monta o body correto para realizar o POST dos dados exatamente como o programa de inclusão de clientes da API
Logix espera.

llopes

'''

def MontaBody(array):
    empresa       = array[0]
    cUser         = array[1]
    codcli        = array[2]
    nome          = array[3]
    nome_reduzido = array[4]
    cnpj_cpf      = array[5]
    telefone      = array[6]
    tplogradouro  = array[7]
    rua           = array[8]
    numero        = array[9]
    complemento   = array[10]
    cep           = array[11]
    bairro        = array[12]
    cod_ibge      = array[13]

    cStringJson = {
        "lr_principal":{
            "empresa":empresa,
            "usuario":cUser
        },
        "lr_mestre":{
            "codigo":codcli,
            "nome":nome,
            "nome_reduzido":nome_reduzido,
            "situacao":"A",
            "tipo_cliente":"03",
            "classe":"A",
            "cliente_terceiro":"N"
        },
        "lr_info_fiscal":{
            "cnpj_cpf":cnpj_cpf,
            "inscricao_estadual":"ISENTO",
            "micro_empresa":"N",
            "zona_franca":"N",
            "cprb":"N",
            "inovar_auto":"N"
        },
        "lr_contato":{
            "caixa_postal":"",
            "telex":"",
            "ddi":"",
            "ddd":"",
            "telefone":telefone,
            "fax":""
      },
        "lr_endereco":{
            "tipo_logradouro":tplogradouro,
            "logradouro":rua,
            "numero_identificacao":numero,
            "complemento":complemento,
            "cep":cep,
            "bairro":bairro,
            "cidade_ibge":cod_ibge
      },
        "lr_localidade":{
            "rota":"0",
            "praca":"0",
            "local":"0",
            "mercado":"99",
            "continente":"99",
            "regiao":"99"
      },
        "lr_canal_venda":{
            "nivel_1":9000,
            "nivel_2":9999,
            "nivel_3":0,
            "nivel_4":0,
            "nivel_5":0,
            "nivel_6":0,
            "nivel_7":0,
            "carteira":"01"
      }
   }

    return print(cStringJson)


MontaBody()
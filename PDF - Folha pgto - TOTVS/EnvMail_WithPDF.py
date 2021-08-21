# Conexao banco e API-RESTFUL
import os
import sys
import mysql.connector
from flask import Flask, jsonify, request
import json
# Envio de E-mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import email.mime.application
#Montando PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

'''
Este código realiza um select na tabela SRV (pagamentos) do sistema PROTHEUS, na database informada pela 
requisição. Retornando um Json com todas informações, além de criar um PDF da folha de pagamento e enviar por e-mail
com anexo do PDF criado

llopes

'''

app = Flask(__name__)
app.debug = True

canvas = canvas.Canvas("folha.pdf", pagesize=letter)

def GeneratePDF(canvas,liquido,periodo,liqtot,liqdesc):

    canvas.setLineWidth(.3)
    canvas.setFont('Courier', 10)

    # EIXO X , Y ---> Espaço entre linhas está 15 (eixo y)

    ################################linhas envoltre - Cabeçalho#################################

    canvas.line(15,780,15,715) #desenha uma linha x , y , x , y
    canvas.line(590,780,590,715) #desenha uma linha x , y , x , y
    canvas.line(15,780,590,780) #desenha uma linha x , y , x , y


    ################################cabeçalho principal#########################################

    canvas.drawString(30,760,'INDUSTRIA COLCHÕES CASTOR LTDA')
    canvas.setFont('Courier-Bold', 10)
    canvas.drawString(400,760,'Folha de Pagamento de Salário')
    
    canvas.setFont('Courier', 10)
    canvas.drawString(30,745,'Av. Armando Silva, 310 Ourinhos SP')
    canvas.drawString(400,745,"Mês referencia: " + periodo)

    canvas.drawString(30,730, "09.451.214/0001-01")

    canvas.line(15,715,590,715) #desenha uma linha x , y , x , y

    ###############################Line - Funcionario##########################################

    canvas.drawString(30,700,'Código')
    canvas.drawString(150,700,'Nome do funcionario')
    canvas.drawString(340,700,'Dt Admissao')
    canvas.drawString(500,700,'Função')

    ############################### linhas codefunci ##########################################

    canvas.line(15,715,15,400) #desenha uma linha x , y , x , y
    canvas.line(590,715,590,330) #desenha uma linha x , y , x , y
    canvas.line(15,670,590,670) #desenha uma linha x , y , x , y

    ############################### INFO FUNCI ################################################

    canvas.drawString(30,685,'XXXXXX') #CODIGO
    canvas.drawString(130,685,'LUCAS MATHEUS CORREA LOPES') #NOME
    canvas.drawString(340,685,'03/11/2020') # DT ADMISSAO
    canvas.drawString(475,685,'ANALISTA PROTHEUS') # FUNCAO

    canvas.line(15,656,590,656) #desenha uma linha x , y , x , y

    ############################### cabeçalho verbas ##########################################

    canvas.drawString(30,660,'Código') #CODIGO
    canvas.line(85,670,85,400) #desenha uma linha x , y , x , y
    canvas.drawString(130,660,'Descr') #CODIGO
    canvas.line(220,670,220,400) #desenha uma linha x , y , x , y
    canvas.drawString(260,660,'Referencia') #CODIGO
    canvas.line(360,670,360,360) #desenha uma linha x , y , x , y
    canvas.drawString(393,660,'Vencimentos') #CODIGO
    canvas.line(494,670,494,330) #desenha uma linha x , y , x , y
    canvas.drawString(510,660,'Descontos') #CODIGO

    ############################## Totalizadores ##############################################

    canvas.line(15,400,590,400) #desenha uma linha x , y , x , y
    canvas.drawString(393,390,'Tot Venctos') #CODIGO
    canvas.drawString(393,370,'R$ XXXXXXX.XX' )#+ str(liqtot)) #CODIGO
    canvas.drawString(510,390,'Tot Desc') #CODIGO
    canvas.drawString(510,370,'R$ XXXXXX.XX' )#+str(liqdesc)) #CODIGO
    canvas.line(360,385,590,385) #desenha uma linha x , y , x , y
    canvas.line(360,360,590,360) #desenha uma linha x , y , x , y

    # valor líquido
    canvas.line(360,360,360,330) #desenha uma linha x , y , x , y
    canvas.drawString(393,340,'TOTAL LIQ =>') #CODIGO
#    canvas.drawString(510,340,'R$ ' + liquido)  #CODIGO
    canvas.drawString(510,340,'R$ XXXXXX.XX')  #CODIGO
    canvas.line(360,330,590,330) #desenha uma linha x , y , x , y

    ################################## itens verbas ##########################################

    # Salvar PDF
    canvas.save()

    print('PDF GERADO')


def envmail(mensagemid):

    # tem que ser habilitado acesso menos seguro em app de terceiros no gmail google

    #The mail addresses and password
    sender_address = 'youremail@gmail.com'
    sender_pass = 'yourpass'
    receiver_address = 'youremail@gmail.com'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Folha de pagamento'   #The subject line

    # Anexando o PDF

    pdfname='folha.pdf' #D:\PythonProjects
    fp=open(pdfname,'rb')
    anexo = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
    fp.close()
    anexo.add_header('Content-Disposition','attachment',filename=pdfname)

    #anexo
    message.attach(anexo)
    #mensagem
    message.attach(MIMEText(mensagemid, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Email enviado!')
    print()

#CONEXAO BANCO MYSQ-LOCAL - TOTVS
def conexao():

    config = {
    'host':'localhost',
    'port':'3306',
    'user':'userofsql',
    'password':'yourpass',
    'database':'totvs'
    }

    conn = mysql.connector.connect(**config)
    return conn


#FIRST ROUTE
@app.route('/')
def index():
    return "Servidor REST no ar!"

def queryfol(matricula,per):

    conex = conexao()
    cursor = conex.cursor()

    tratastr = matricula.isalnum() #somente aceita letras e números

    #nao aceita aspas simples
    if tratastr:
        final_mat = matricula
    else:
        final_mat = matricula.replace('\'',"")

    sql = "SELECT" \
        " ROUND(SUM(CASE WHEN RD_PD = '812' THEN RD_VALOR END), 2) liq_fol,  " \
        " ROUND(SUM(CASE WHEN RD_PD = '808' THEN RD_VALOR END), 2) liq_adi,  " \
        " ROUND(SUM(CASE WHEN RD_PD = '463' THEN RD_VALOR END), 2) liq_fer,  " \
        " ROUND(SUM(CASE WHEN RD_PD = '482' THEN RD_VALOR END), 2) desc_ref, " \
        " ROUND(SUM(CASE WHEN RD_PD = '401' THEN RD_VALOR END), 2) desc_inss, " \
        " ROUND(SUM(CASE WHEN RD_PD = '402' THEN RD_VALOR END), 2) desc_inss_ferias, " \
        " ROUND(SUM(CASE WHEN RD_PD = '410' THEN RD_VALOR END), 2) desc_irrf, " \
        " RD_MES, " \
        " SUBSTR(RD_PERIODO,1,4) ANO" \
        "   FROM SRD100 R " \
        "WHERE RD_MAT= "+final_mat+" "\
        "AND D_E_L_E_T_=' ' " \
        "AND RD_TIPO1='V' " \
        "AND RD_PERIODO = '" +per+ "\'" \
        " GROUP BY RD_MES, SUBSTR(RD_PERIODO,1,4) "
    
    cursor.execute(sql)         # executando query
    results = cursor.fetchall() # fetchall retorna todos os dados
    cursor.close()              # encerrando cursor
    conex.close()               # encerrando conexao

    return results

@app.route('/rendimentos/<string:matricula>', methods=['GET'])
def jsonreturn(matricula):
    per = request.args.get('periodo', default = 1, type = str)
    print()

    query = queryfol(matricula,per)

    if len(query) == 1:

        mes_query = query[0][7]
        
        if mes_query == '01':
            strmes = 'JANEIRO'
        elif mes_query == '02':
            strmes = 'FEVEREIRO'
        elif mes_query == '03':
            strmes = 'MARCO'
        elif mes_query == '04':
            strmes = 'ABRIL'
        elif mes_query == '05':
            strmes = 'MAIO'
        elif mes_query == '06':
            strmes = 'JUNHO'
        elif mes_query == '07':
            strmes = 'JULHO'
        elif mes_query == '08':
            strmes = 'AGOSTO'
        elif mes_query == '09':
            strmes = 'SETEMBRO'
        elif mes_query == '10':
            strmes = 'OUTUBRO'
        elif mes_query == '11':
            strmes = 'NOVEMBRO'
        else:
            strmes = 'DEZEMBRO'

        funci = 'LUCAS MATHEUS CORREA LOPES'

        mensagemid  = 'Funci: ' + funci + '\n' 
#        mensagemid += 'Liquido folha: ' + str(query[0][0]) + '\n' 
#        mensagemid += 'Liquido Adi: ' + str(query[0][1]) + '\n'
#        mensagemid += 'Desconto INSS ' + str(query[0][4]) + '\n'
        mensagemid += 'Periodo: ' + strmes + '/' + query[0][8]
        
        # Montar array apendando novos dados e passar na chamada da funcao
        periodo = strmes+'/'+query[0][8]
        liqtot = query[0][0] + query[0][1]
        liqdesc = query[0][4] + query[0][3]

        GeneratePDF(canvas, str(query[0][0]), periodo, liqtot, liqdesc)
        envmail(mensagemid)

        return jsonify({
        'Status':'Ok',
        'SMensagem':'Dados recebidos',
        'AFunci_Nome':'LUCAS MATHEUS CORREA LOPES',
        'Liquido_FOL':'9999.99',#query[0][0], 
        'Liquido_ADI':'9999.99',#query[0][1],
        'Liquido_FER':'1234.99',#query[0][2],
        'Desconto_REFEIT':'25.99',#query[0][3],
        'Desconto_INSS':'888.99',#query[0][4],
        'Desconto_INSS_FERIAS':'444',#query[0][5],
        'Desconto_IRRF':'333',#query[0][6],
        'Per_MES':strmes, 
        'Per_ANO':query[0][8]}) #caso tenha resultado na query, retorna
    
    else:                   #se não, mostra mensagem de erro
        return jsonify({
        'Status':'Erro',
        'Mensagem':'Periodo nao encontrado'})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000')   # ip geral


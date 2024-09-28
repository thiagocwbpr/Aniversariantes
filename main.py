
from flask import Flask, render_template
import mysql.connector
import webbrowser
from datetime import datetime

app = Flask(__name__)

# Configurações do banco de dados
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'LivelyConnect'
DB_USER = 'root'
DB_PASSWORD = 'dbvendas123'

# Função para buscar aniversariantes do dia e do mês
def buscar_aniversariantes():
    # Data de hoje
    hoje = datetime.now().date()

    # String de conexão com o banco de dados
    conn = mysql.connector.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    # Consulta para buscar aniversariantes do dia
    cursor.execute("""
                  SELECT 
                  FUNCIONARIO_ID
                , NOME, SOBRENOME
                , DATE_FORMAT(DATA_DE_NASCIMENTO, '%d-%m') AS ANIVERSARIO
                , NOME_DA_FUNCAO
                , NOME_DO_SETOR
                , NOME_DA_SUBORDINACAO

                          FROM tb_funcionarios
                          WHERE MONTH(DATA_DE_NASCIMENTO) = MONTH(CURDATE()) 
                          AND DAY(DATA_DE_NASCIMENTO) = DAY(CURDATE());
    """)
    aniversariantes_do_dia = cursor.fetchall()

    # Consulta para buscar aniversariantes do mês

    cursor.execute("""
                  SELECT 
                  FUNCIONARIO_ID
                , NOME
                , SOBRENOME
                , DATE_FORMAT(DATA_DE_NASCIMENTO, '%d-%m') AS ANIVERSARIO
                , NOME_DA_FUNCAO
                , NOME_DO_SETOR
                , NOME_DA_SUBORDINACAO

                          FROM tb_funcionarios
                          WHERE MONTH(DATA_DE_NASCIMENTO) = MONTH(CURDATE())
                          ORDER BY DATE_FORMAT(DATA_DE_NASCIMENTO, '%d-%m') DESC;
    """)
    aniversariantes_do_mes = cursor.fetchall()

    # Fechamento de conexão com o banco de dados

    cursor.close()
    conn.close()

    return aniversariantes_do_dia, aniversariantes_do_mes

# Rota para exibir os aniversariantes

@app.route('/')
def exibir_aniversariantes():
    aniversariantes_do_dia, aniversariantes_do_mes = buscar_aniversariantes()
    return render_template('aniversariantes.html', aniversariantes_do_dia=aniversariantes_do_dia, aniversariantes_do_mes=aniversariantes_do_mes)

if __name__ == '__main__':
    app.run(debug=True)
    webbrowser.open_new('http://127.0.0.1:5000/')

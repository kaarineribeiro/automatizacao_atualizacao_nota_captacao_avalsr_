import pandas as pd
import pyodbc
from dotenv import dotenv_values
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()
config = dotenv_values(pathlib.Path.joinpath(file_path, '.env'))
ano_referencia = '2024'



db_data = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=' + config['DB_SERVER_IP'] + ';'
    'Database=' + config['DB_NAME'] + ';'
    'UID=' + config['DB_USERNAME'] + ';'
    'PWD=' + config['DB_USER_PWD'] + ';'
)



def get_db_conn() :
    return pyodbc.connect(db_data)


def exec_query(consulta, replace, replace_with):

    with open(pathlib.Path.joinpath(file_path, consulta), 'r') as file:
        query_content = file.read()
    
    query_content = query_content.replace(replace, replace_with)

    conn = get_db_conn()
    df = pd.read_sql(query_content, conn).reset_index(drop=True)
    conn.close()
    return df



def update_nota(consulta, socio, nova_nota):

    with open(pathlib.Path.joinpath(file_path, consulta), 'r') as file:
        query_content = file.read()
    
    query_content = query_content.replace('$colaborador', socio)
    query_content = query_content.replace('$ano_referencia', ano_referencia)
    query_content = query_content.replace('$nivel', nova_nota)

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(query_content)
    cursor.commit()
    cursor.close()


def replace_nota():

    avaliacoes = exec_query('consulta_avaliacoes.sql','','')
    captacoes = exec_query('consulta_captacoes.sql', '$ano_referencia', ano_referencia)

    for socio in avaliacoes['No_Socio']:
        
        valor_captacao = float(captacoes.loc[captacoes['No_Socio'] == socio, 'Vl_ValorTotalCaptadoAno'].iloc[0])
        replace_socio =  "'" + socio + "'"
        nova_nota = '0.0'

        if 0.0 < valor_captacao <= 300000.0: 
            nova_nota = str(0.3)
        elif 300000.00 < valor_captacao <= 1000000.00:
            nova_nota = str(0.6)
        elif valor_captacao > 1000000.00:
            nova_nota = str(1.0)

        update_nota('update_nota_captacao.sql', replace_socio, nova_nota)

        print(socio)
        print(nova_nota)


def main():
    replace_nota()

if __name__=="__main__":
    main()



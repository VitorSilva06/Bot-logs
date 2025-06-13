import pandas as pd
from db.db import db_name, sql, cursor
from time import sleep


def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    """Carrega e trata os dados do CSV."""
    df = pd.read_csv(caminho_csv)

    # Renomear colunas
    df.rename(columns={
        'UDI': 'ID',
        'Product ID': 'ID_Produto',
        'Type': 'Tipo',
        'Air temperature [K]': 'Temp_Ar_K',
        'Process temperature [K]': 'Temp_Processo_K',
        'Rotational speed [rpm]': 'Velocidade_Rotacao_rpm',
        'Torque [Nm]': 'Torque_Nm',
        'Tool wear [min]': 'Desgaste_Ferramenta_min',
        'Target': 'Falha',
        'Failure Type': 'Tipo_Falha'
    }, inplace=True)

    # Conversão de tipos
    df = df.astype({
        'ID': 'int',
        'ID_Produto': 'str',
        'Tipo': 'str',
        'Temp_Ar_K': 'float',
        'Temp_Processo_K': 'float',
        'Velocidade_Rotacao_rpm': 'int',
        'Torque_Nm': 'float',
        'Desgaste_Ferramenta_min': 'int',
        'Falha': 'int',
        'Tipo_Falha': 'str'
    })

    # Remover coluna ID (se não for necessária)
    df.drop('ID', axis=1, inplace=True)
    
    return df


def verificar_nulos(df: pd.DataFrame):
    """Imprime se existem valores nulos no DataFrame."""
    linhas_nulas = df[df.isnull().any(axis=1)]
    if not linhas_nulas.empty:
        print("⚠️ Linhas com valores nulos detectadas:")
        print(linhas_nulas)
    else:
        print("✔️ Nenhum valor nulo encontrado.")


def salvar_no_banco(df: pd.DataFrame, nome_tabela: str):
    """Salva o DataFrame no banco de dados."""
    print("📥 Inserindo os dados no banco...")
    conn = sql.connect(db_name)
    df.to_sql(nome_tabela, conn, if_exists='append', index=False)
    conn.close()
    sleep(2)
    print(" Dados carregados com sucesso!")


def main():
    df = carregar_dados('predictive_maintenance.csv')
    verificar_nulos(df)
    salvar_no_banco(df, 'manutencao')


if __name__ == '__main__':
    main()

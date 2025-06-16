import pandas as pd
from db.db import db_name, sql
from time import sleep
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Gerar imagem sem interface gráfica. Corrige o erro de quando for montar os graficos
from matplotlib import pyplot as plt
from fpdf import FPDF
import os
import smtplib
from email.message import EmailMessage


def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    """Carrega e trata os dados do CSV."""
    df = pd.read_csv(caminho_csv)

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

    df = df.astype({
        'ID': 'int',
        'ID_Produto': 'str',
        'Tipo': 'str',
        'Temp_Ar_K': 'float',
        'Temp_Processo_K': 'float',
        'Velocidade_Rotacao_rpm': 'float',
        'Torque_Nm': 'float',
        'Desgaste_Ferramenta_min': 'float',
        'Falha': 'float',
        'Tipo_Falha': 'str'
    })

    df.drop('ID', axis=1, inplace=True)
    return df


def verificar_nulos(nome_tabela: str):
    """Consulta e exibe registros no banco que possuem valores nulos."""
    conn = sql.connect(db_name)
    data_atual = datetime.now()

    query = f"""
    SELECT *
    FROM {nome_tabela}
    WHERE 
        ID_Produto IS NULL OR ID_Produto = '' OR
        Tipo IS NULL OR Tipo = '' OR
        Temp_Ar_K IS NULL OR
        Temp_Processo_K IS NULL OR
        Velocidade_Rotacao_rpm IS NULL OR
        Torque_Nm IS NULL OR
        Desgaste_Ferramenta_min IS NULL OR
        Falha IS NULL OR
        Tipo_Falha IS NULL OR Tipo_Falha = ''
        AND date(Data_Insercao) = '{data_atual.strftime('%Y-%m-%d')}';
    """

    df_nulos = pd.read_sql_query(query, conn)
    conn.close()

    if not df_nulos.empty:
        print("Registros no banco com campos nulos:")
    else:
        print("Nenhum valor nulo encontrado no banco.")

    return df_nulos


def salvar_no_banco(df: pd.DataFrame, nome_tabela: str):
    """Salva o DataFrame no banco de dados."""
    print("Inserindo os dados no banco...")
    conn = sql.connect(db_name)
    df.to_sql(nome_tabela, conn, if_exists='append', index=False)
    conn.close()
    sleep(2)
    print("Dados carregados com sucesso!")


def query_falhas(nome_tabela: str):
    """Consulta no banco os registros de falhas do dia."""
    data_atual = datetime.now()
    conn = sql.connect(db_name)
    query = f"""
    SELECT *
    FROM {nome_tabela}
    WHERE Falha = 1
    AND date(Data_Insercao) = '{data_atual.strftime('%Y-%m-%d')}'
    ORDER BY Data_Insercao DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def gerar_relatorio(tabela: str, nome_pdf='relatorio.pdf'):
    dados = query_falhas(tabela)

    # Gráfico 1: Quantidade de Falhas
    contagem = dados['Tipo_Falha'].value_counts()
    eixo_x = contagem.index
    eixo_y = contagem.values

    plt.figure(figsize=(10, 5))
    plt.bar(eixo_x, eixo_y, color='skyblue')
    plt.xlabel('Tipo de Falha')
    plt.ylabel('Quantidade')
    plt.title('Quantidade de Falhas por Tipo')
    img1 = 'grafico_falhas.png'
    plt.tight_layout()
    plt.savefig(img1)
    plt.close()

    # Tabela: Top 10 produtos com mais falhas
    top10_tabela = dados['ID_Produto'].value_counts().head(10).reset_index()
    top10_tabela.columns = ['ID_Produto', 'Total_Falhas']

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('tight')
    ax.axis('off')
    tabela = ax.table(cellText=top10_tabela.values,
                      colLabels=top10_tabela.columns,
                      cellLoc='center',
                      loc='center')
    tabela.scale(1.2, 1.5)
    plt.title('Top 10 Produtos com Mais Falhas', pad=20)
    plt.tight_layout()
    img2 = 'tabela_top10.png'
    plt.savefig(img2)
    plt.close()

    # Tabela: Estatísticas Descritivas 
    stats = dados[['Temp_Ar_K', 'Temp_Processo_K', 'Velocidade_Rotacao_rpm',
                   'Torque_Nm', 'Desgaste_Ferramenta_min']].describe()
    stats = stats.T[['mean', 'min', 'max']].round(2)

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')
    table = ax.table(
        cellText=stats.values,
        rowLabels=stats.index,
        colLabels=stats.columns,
        cellLoc='center',
        rowLoc='center',
        loc='center',
        colColours=['#4F81BD'] * 3,
        rowColours=['#DCE6F1'] * len(stats)
    )
    plt.title('Estatísticas Descritivas', fontsize=16)
    plt.tight_layout()
    img3 = 'tabela_stats.png'
    plt.savefig(img3)
    plt.close()

    # --- Criar PDF ---
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, 'Relatório Resumido de Falhas', ln=True, align='C')
    pdf.ln(10)
    pdf.image(img1, x=10, w=pdf.w - 20)

    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, 'Top 10 Produtos com Mais Falhas', ln=True, align='C')
    pdf.ln(10)
    pdf.image(img2, x=20, w=pdf.w - 40)

    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, 'Estatísticas Descritivas', ln=True, align='C')
    pdf.ln(10)
    pdf.image(img3, x=10, w=pdf.w - 20)

    pdf.output(nome_pdf)
    print(f"PDF salvo como {nome_pdf}")

    os.remove(img1)
    os.remove(img2)
    os.remove(img3)

    nulos = verificar_nulos('manutencao')
    corpo = f'Segue o relatório gerado.\n\u26A0 Valores nulos encontrados:\n{nulos if not nulos.empty else "Nenhum"}'

    enviar_email(
        destinatario=os.getenv('DESTINATARIO_ENV'),
        assunto='Relatório de Falhas',
        corpo=corpo,
        pdf=nome_pdf,
        remetente=os.getenv('REMETENTE_ENV'),
        senha=os.getenv('SENHA_ENV')
    )
    print('Email enviado com sucesso.')


def enviar_email(destinatario, assunto, corpo, pdf, remetente, senha):
    try:
        mensagem = EmailMessage()
        mensagem['Subject'] = assunto
        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        mensagem.set_content(corpo)

        with open(pdf, 'rb') as f:
            mensagem.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(pdf))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(mensagem)

    except Exception as e:
        print("Erro ao enviar o e-mail:", e)




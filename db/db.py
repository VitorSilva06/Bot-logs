import sqlite3 as sql

# Definir nome do banco de dados
db_name = "maintenance_db.db"

# Criar conexão com o banco de dados
conn = sql.connect(db_name)
cursor = conn.cursor()

# Criar tabela de manutenção
cursor.execute("""
CREATE TABLE IF NOT EXISTS manutencao (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Produto TEXT,
    Tipo TEXT,
    Temp_Ar_K REAL,
    Temp_Processo_K REAL,
    Velocidade_Rotacao_rpm INTEGER,
    Torque_Nm REAL,
    Desgaste_Ferramenta_min INTEGER,
    Falha INTEGER,
    Tipo_Falha TEXT
)
""")
conn.commit()

# Fechar conexão
conn.close()
print("✔️ Banco de dados e tabela criados com sucesso!")

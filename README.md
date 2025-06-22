# ⚙️ ScanFlux – Monitoramento e Análise de Manutenção Preditiva

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Build](https://img.shields.io/badge/status-em%20desenvolvimento-orange)

> Interface desktop interativa para análise de falhas industriais com relatórios automatizados em PDF e envio por email.

---

## 🖼️ Interface

| Seleção de Arquivo | Análise de Dados | Relatório Gerado |
|--------------------|------------------|------------------|

---

## 📦 Funcionalidades

✅ Carrega arquivos `.csv` com dados de sensores industriais  
✅ Armazena as informações em banco SQLite  
✅ Gera gráficos, tabelas e estatísticas no PDF  
✅ Envia relatório automaticamente por email  
✅ Interface construída com PyQt5 e Qt Designer  
✅ Pronto para empacotamento com PyInstaller

---

## 📁 Estrutura do Projeto

ScanFlux/
├── db/
│ └── db.py # Criação da tabela SQLite
├── main.py # Lógica de processamento e relatório
├── view.py # Interface gráfica PyQt5
├── interface.ui # Layout criado no Qt Designer
├── .env # Configuração do envio de email (não incluso no repositório)
├── requirements.txt # Dependências do projeto
└── README.md # Documentação

yaml
Copiar código

---

## 🚀 Como Executar

### 1️⃣ Instale as dependências

```bash
pip install -r requirements.txt
Ou:

bash
Copiar código
pip install pyqt5 pandas matplotlib fpdf python-dotenv
2️⃣ Configure o .env
Crie um arquivo .env com:

env
Copiar código
REMETENTE_ENV=seu_email@gmail.com
SENHA_ENV=sua_senha_de_app
DESTINATARIO_ENV=email_destino@gmail.com
⚠️ Use uma senha de app do Gmail para segurança.


📊 Relatório Gerado
O relatório em PDF contém:

📈 Gráfico de barras por tipo de falha

🧾 Tabela com os 10 produtos com mais falhas

📉 Estatísticas descritivas dos sensores

✉️ Envio automático para o email definido

🧠 Tecnologias Usadas
Python 3.8+

PyQt5 – Interface gráfica

SQLite3 – Banco de dados local

Pandas – Processamento de dados

Matplotlib – Geração de gráficos

FPDF – Relatórios em PDF

dotenv + smtplib – Envio seguro de emails

📌 Observações
Funciona em Windows

Use ambiente virtual (venv) para evitar conflitos

Após empacotar, o app pode ser usado sem Python instalado

📃 Licença
Este projeto está licenciado sob os termos da MIT License. Veja o arquivo LICENSE para mais detalhes.

🤝 Contribuições
Contribuições são muito bem-vindas!
Sinta-se à vontade para abrir uma Issue ou enviar um Pull Request.

📬 Contato
Desenvolvido por Vitor Silva
📧 vitordasilva0605@gmail.com

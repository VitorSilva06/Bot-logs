from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
import sys, os
import pandas as pd
import shutil
from datetime import datetime
from main import carregar_dados, salvar_no_banco, gerar_relatorio, query_falhas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)

        self.btn_selecionar.clicked.connect(self.selecionar_arquivo)
        self.btn_analisar.clicked.connect(self.analisar_dados)
        self.btn_imprimir.clicked.connect(self.imprimir_relatorio)

        self.df = None
        self.caminho_arquivo = None

    def selecionar_arquivo(self):
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecione o arquivo CSV", "", "CSV Files (*.csv)")
        if arquivo:
            nome_arquivo = os.path.basename(arquivo)
            destino = os.path.join(os.getcwd(), nome_arquivo)

            try:
                if os.path.abspath(arquivo) == os.path.abspath(destino):
                    temp = destino + ".tmp"
                    shutil.copyfile(arquivo, temp)
                    shutil.copyfile(temp, destino)
                    os.remove(temp)
                else:
                    shutil.copyfile(arquivo, destino)

                print(f"Arquivo copiado para: {destino}")
                self.caminho_arquivo = destino
                self.arquivo_input.setText(nome_arquivo)

            except Exception as e:
                print(f"Erro ao copiar o arquivo: {e}")
                QMessageBox.critical(self, "Erro", f"Erro ao copiar o arquivo:\n{e}")

    def analisar_dados(self):
        if not self.caminho_arquivo:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo CSV primeiro.")
            return

        try:
            self.df = carregar_dados(self.caminho_arquivo)
            salvar_no_banco(self.df, 'manutencao')

            dados_falhas = query_falhas('manutencao')
            resumo = dados_falhas['Tipo_Falha'].value_counts().reset_index()
            resumo.columns = ['Tipo Falha', 'Quantidade']

            self.tabela_resumo.setRowCount(len(resumo))
            self.tabela_resumo.setColumnCount(len(resumo.columns))
            self.tabela_resumo.setHorizontalHeaderLabels(resumo.columns.tolist())

            for i, row in resumo.iterrows():
                for j, val in enumerate(row):
                    self.tabela_resumo.setItem(i, j, QTableWidgetItem(str(val)))

            QMessageBox.information(self, "Sucesso", "Dados analisados e resumo exibido.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao analisar os dados:\n{e}")

    def imprimir_relatorio(self):
        if self.df is None:
            QMessageBox.warning(self, "Aviso", "Você precisa carregar e analisar os dados antes de gerar o relatório.")
            return

        try:
            gerar_relatorio('manutencao', nome_pdf='relatorio.pdf')
            QMessageBox.information(self, "Relatório", "Relatório gerado e enviado com sucesso.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar relatório:\n{e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec_())

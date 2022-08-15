"""
Testes do sistema de backup
"""
import os.path
import backup


def testa_data():
    """
    Função que testa qual arquivo foi modificado por último
    """
    aux = backup.data_modificacao(os.getcwd() + r'\HD', os.getcwd() + r'\Pendrive')
    assert aux == 'Pendrive'
    # assert aux == 'HD'
    # assert aux == 'igual'



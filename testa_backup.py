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


def testa_tabela_decisao():
    """Função que testa se a tabela de decisão foi criada de forma correta,
    como uma tupla estática, ou seja o valor sempre é o mesmo em todos os casos"""
    assert isinstance(backup.tabela_decisao(), tuple)



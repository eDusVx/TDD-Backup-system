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


def testa_executar_tabela():
    """
    Função que testa se a execução da tabela de decisão está correta
    """
    decision_table = backup.tabela_decisao()
    assert backup.executar_tabela(decision_table) == 'Pen-drive para HD'
    # assert backup.executar_tabela(decision_table) == 'HD para Pen-Drive'
    # assert backup.executar_tabela(decision_table) == 'Erro'
    # assert backup.executar_tabela(decision_table) == 'Faz nada'
    # assert backup.executar_tabela(decision_table) == 'Impossível'


def testa_backup():
    """
    Função que testa se foi feita a ação necessária.
    """
    assert backup.backup(backup.acao) == 'Os dados do pendrive ' \
                                         'foram copiados para o HD com sucesso!'
    # assert backup.backup(backup.acao) == 'Backup para Pendrive concluido com sucesso!'
    # assert backup.backup(backup.acao) == 'Erro'
    # assert backup.backup(backup.acao) == 'Impossível'


testa_data()
testa_tabela_decisao()
testa_executar_tabela()
testa_backup()

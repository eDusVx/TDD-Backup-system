"""
Sistema de backup usando tabela de decisão
"""
import os.path
import shutil
import datetime
from ast import literal_eval
from typing import Tuple, List, Dict, Any


def data_modificacao(diretorio1: str, diretorio2: str) -> str:
    """
    Função que compara a data de modificação dos arquivos
    """
    aux = 'branco'
    m_time1 = os.path.getmtime(diretorio1)
    m_time2 = os.path.getmtime(diretorio2)
    dt_m1 = datetime.datetime.fromtimestamp(m_time1)
    dt_m2 = datetime.datetime.fromtimestamp(m_time2)
    if dt_m1 > dt_m2:
        aux = 'HD'
    if dt_m2 > dt_m1:
        aux = 'Pendrive'
    if dt_m1 == dt_m2:
        aux = 'igual'
    assert isinstance(aux, str)
    return aux


def tabela_decisao() -> Tuple[List[str], Dict[str, List[Any]]]:
    """
    Função que cria a tabela de decisão
    """
    conditions = ['Tem Backup.parm',
                  'Faz backup',
                  'ArqX ∈ HD',
                  'ArqX ∈ Pen-drive',
                  'Data PenD < HD',
                  'Data PenD == HD',
                  'Data PenD > HD']
    action2rules = []
    action = ['HD para Pen-Drive; [(1,1,1,0,0,0,0),(1,1,1,1,1,0,0),'
              '(1,1,1,0,0,0,1),(1,1,1,0,0,1,0),(1,1,1,0,0,1,1),'
              '(1,1,1,0,1,0,0),(1,1,1,0,1,0,1),(1,1,1,0,1,1,0),'
              '(1,1,1,0,1,1,1)]',
              'Pen-drive para HD; [(1,0,1,1,0,0,1),(1,0,0,1,0,0,0),(1,0,0,1,0,0,1),(1,0,0,1,0,1,0),'
              '(1,0,0,1,0,1,1),(1,0,0,1,1,0,0),(1,0,0,1,1,0,1),(1,0,0,1,1,1,0),(1,0,0,1,1,1,1)]',
              'Faz nada; [(1,1,1,1,0,1,0),(1,0,1,1,0,1,0),(1,1,0,1,0,0,0),(1,1,0,1,0,0,1),'
              '(1,1,0,1,0,1,0),(1,1,0,1,0,1,1),(1,1,0,1,1,0,0),(1,1,0,1,1,0,1),(1,1,0,1,1,1,0),'
              '(1,1,0,1,1,1,1)]',
              'Erro; [(1,1,1,1,0,0,1),(1,0,1,0,0,0,0),(1,0,1,1,1,0,0),'
              '(1,1,0,0,0,0,0),(1,0,0,0,0,0,0),(1,0,1,0,0,0,1),(1,0,1,0,0,1,0),(1,0,1,0,0,1,1),'
              '(1,0,1,0,1,0,0),(1,0,1,0,1,0,1),(1,0,1,0,1,1,0),(1,0,1,0,1,1,1),(1,1,0,0,0,0,1),'
              '(1,1,0,0,0,1,0),(1,1,0,0,0,1,1),(1,1,0,0,1,0,0),(1,1,0,0,1,0,1),(1,1,0,0,1,1,0),'
              '(1,1,0,0,1,1,1),(1,0,0,0,0,0,1),(1,0,0,0,0,1,0),(1,0,0,0,0,1,1),(1,0,0,0,1,0,0),'
              '(1,0,0,0,1,0,1),(1,0,0,0,1,1,0),(1,0,0,0,1,1,1)]',
              'Impossivel; [(0,0,0,0,0,0,0)]']
    for i in range(0, 4):
        name, _, rules = [x.strip() for x in action[i].partition(';')]
        rules = literal_eval(rules)
        assert all(len(rule) == len(conditions) for rule in rules), \
            'string para igualar tamanho'
        action2rules.append((name, rules))
    rule2actions = dict((y, []) for y in set(sum((x[1] for x in action2rules), [])))  # type: Any
    for action, rules in action2rules:
        for j in rules:
            rule2actions[j].append(action)
    return conditions, rule2actions



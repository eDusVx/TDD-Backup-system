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


def executar_tabela(decision_table: Any) -> Any:
    """
    função que executa a tabela de decisão
    """
    erro = 3
    rule = [0, 0, 0, 0, 0, 0, 0]
    contador = 0
    contador2 = 0
    conditions, rule2actions = decision_table
    aux = conditions
    aux = aux + [1]
    if erro == 2:
        return aux
    try:
        with open('Backup.parm.txt', 'r', encoding="utf-8") as backup_parm:
            backup_parm = backup_parm.read().split()
            rule[0] = 1
    except FileNotFoundError:
        return 'Impossível'
    print('deseja fazer backup y/n?')
    auxiliar = input()
    if auxiliar == 'y':
        rule[1] = 1
    for i in enumerate(backup_parm):
        i = i[0]
        if os.path.isfile(os.getcwd() + fr'\HD\{backup_parm[i]}'):
            contador += 1
        if os.path.isfile(os.getcwd() + fr'\Pendrive\{backup_parm[i]}'):
            contador2 += 1
    if contador == len(backup_parm):
        rule[2] = 1
    if contador2 == len(backup_parm):
        rule[3] = 1
    if data_modificacao(os.getcwd() + r'\HD', os.getcwd() + r'\Pendrive') == 'HD':
        rule[4] = 1
    if data_modificacao(os.getcwd() + r'\HD', os.getcwd() + r'\Pendrive') == 'igual':
        rule[5] = 1
    if data_modificacao(os.getcwd() + r'\HD', os.getcwd() + r'\Pendrive') == 'Pendrive':
        rule[6] = 1
    assert len(rule) == 7  # Tamanho da lista de decisões tem de ser 7
    rule = tuple(rule)
    return rule2actions.get(rule)[0]


def backup(funcao: str) -> Any:
    """
    função que executa a acção necessária
    """
    hard_disk = 'HD'
    pendrive = 'Pendrive'
    if funcao == 'HD para Pen-Drive':
        files = os.listdir(hard_disk)
        assert files
        for fname in files:
            shutil.copy2(os.path.join(hard_disk, fname), pendrive)
        return 'Backup para Pendrive concluido com sucesso!'
    if funcao == 'Pen-drive para HD':
        files = os.listdir(pendrive)
        assert files
        for fname in files:
            shutil.copy2(os.path.join(pendrive, fname), hard_disk)
        return 'Os dados do pendrive foram copiados para o HD com sucesso!'
    if funcao == 'Impossível':
        return 'Impossível'
    if funcao == 'Erro':
        return 'Erro'
    return None


dt = tabela_decisao()
acao = executar_tabela(dt)
print(backup(acao))

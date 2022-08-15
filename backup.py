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




#!/usr/bin/env python3
import re

def task_name(frase):
    # resultado = re.search(r'^\w+\b\s+\w+\b', frase)
    # if resultado:
        # return resultado.group() + '...'
    if len(frase)>15:
        return frase[:15]+' ...'
    return frase

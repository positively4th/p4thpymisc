from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from .misc import items


def select(msg, labelValueMap={}, default=None, countLimit=1):

    _default = None
    if default:
        for label, value in items(labelValueMap):
            if default == value:
                _default = label
                break

    multiSelect = countLimit is None or countLimit > 1

    choices = [Choice(value, name=label)
               for label, value in labelValueMap.items()]
    res = inquirer.select(
        message=msg,
        choices=choices,
        default=_default,
        multiselect=multiSelect
    ).execute()
    return res

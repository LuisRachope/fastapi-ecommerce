@staticmethod
def update_columns_obj(obj: object, **kwargs: object) -> object:
    """Atualiza os atributos de um objeto com base nos valores fornecidos nos kwargs"""
    for key, value in kwargs.items():
        if value is not None:
            setattr(obj, key, value)
    return obj

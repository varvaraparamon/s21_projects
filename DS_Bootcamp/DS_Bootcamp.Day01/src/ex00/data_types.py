def data_types():
    int_ = 1
    str_ = "str"
    float_ = 1.2
    bool_ = True
    list_ = [1, 2, 3]
    dict_ = {"1": "2"}
    tuple_ = (1, 2, 3)
    set_ = {1, 2, 3}

    types_list = [
        type(int_).__name__,
        type(str_).__name__,
        type(float_).__name__,
        type(bool_).__name__,
        type(list_).__name__,
        type(dict_).__name__,
        type(tuple_).__name__,
        type(set_).__name__
    ]
    
    types_str = ', '.join(types_list)
    print(f"[{types_str}]")

if __name__ == '__main__':
    data_types()
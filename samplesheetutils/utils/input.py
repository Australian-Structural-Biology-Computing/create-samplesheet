def sanitize_input(input_str, disallowed_chars = [',', ' ', '<', '>', '.', "'", '"', ';', ':'], replcement='_'):
    for i in disallowed_chars:
        input_str = input_str.replace(i, '_')
    return input_str


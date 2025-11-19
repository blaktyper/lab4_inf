def read_uint32(file):

    bytes_data = file.read(4)
    if len(bytes_data) != 4:
        raise ValueError("Unexpected end of file")
    return int.from_bytes(bytes_data, byteorder='little')

def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        data = {}
        num_lessons = read_uint32(file)
        lessons = {}
        for _ in range(num_lessons):
            lesson_name_len = read_uint32(file)
            lesson_name = file.read(lesson_name_len).decode('utf-8')
            num_fields = read_uint32(file)
            lesson_data = {}

            for _ in range(num_fields):
                key_len = read_uint32(file)
                key = file.read(key_len).decode('utf-8')
                value_len = read_uint32(file)
                value = file.read(value_len).decode('utf-8')
                lesson_data[key] = value

            lessons[lesson_name] = lesson_data

        num_academic_config_fields = read_uint32(file)
        academic_config = {}
        for _ in range(num_academic_config_fields):
            key_len = read_uint32(file)
            key = file.read(key_len).decode('utf-8')
            value_len = read_uint32(file)
            value = file.read(value_len).decode('utf-8')
            academic_config[key] = value

        num_locals_fields = read_uint32(file)
        locals_data = {}
        for _ in range(num_locals_fields):
            key_len = read_uint32(file)
            key = file.read(key_len).decode('utf-8')
            value_len = read_uint32(file)
            value = file.read(value_len).decode('utf-8')
            locals_data[key] = value

        data['lessons'] = lessons
        data['academic_config'] = academic_config
        data['locals'] = locals_data
        return data

def convert_to_toml(data):
    toml_str = ''

    for lesson_name, lesson_data in data['lessons'].items():
        toml_str += f'[{lesson_name}]\n'
        for key, value in lesson_data.items():
            if value.startswith('[') and value.endswith(']'):
                toml_str += f'{key} = {value}\n'
            else:
                toml_str += f'{key} = "{value}"\n'
        toml_str += '\n'

    toml_str += '[academic_config]\n'
    for key, value in data['academic_config'].items():
        toml_str += f'{key} = "{value}"\n'
    toml_str += '\n'

    toml_str += '[locals]\n'
    for key, value in data['locals'].items():
        if value.startswith('[') and value.endswith(']'):
            toml_str += f'{key} = {value}\n'
        else:
            toml_str += f'{key} = "{value}"\n'
    toml_str += '\n'
    return toml_str


def save_to_toml(toml_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(toml_data)

if __name__ == "__main__":
    input_binary_file = 'inf_data.bin'
    output_toml_file = 'output_config.toml'
    parsed_data = read_binary_file(input_binary_file)
    toml_data = convert_to_toml(parsed_data)
    save_to_toml(toml_data, output_toml_file)
    print(f"Конвертация завершена. Данные сохранены в {output_toml_file}")
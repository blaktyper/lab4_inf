import struct
import toml
def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        data = {}

        num_lessons = struct.unpack('I', file.read(4))[0]
        lessons = {}
        for i in range(num_lessons):
            lesson_name_len = struct.unpack('I', file.read(4))[0]
            lesson_name = file.read(lesson_name_len).decode('utf-8')
            num_fields = struct.unpack('I', file.read(4))[0]
            lesson_data = {}

            for _ in range(num_fields):
                key_len = struct.unpack('I', file.read(4))[0]
                key = file.read(key_len).decode('utf-8')
                value_len = struct.unpack('I', file.read(4))[0]
                value = file.read(value_len).decode('utf-8')
                lesson_data[key] = value

            lessons[f'informatics_lab_{i + 1}'] = lesson_data

        num_academic_config_fields = struct.unpack('I', file.read(4))[0]
        academic_config = {}
        for _ in range(num_academic_config_fields):
            key_len = struct.unpack('I', file.read(4))[0]
            key = file.read(key_len).decode('utf-8')
            value_len = struct.unpack('I', file.read(4))[0]
            value = file.read(value_len).decode('utf-8')
            academic_config[key] = value

        num_locals_fields = struct.unpack('I', file.read(4))[0]
        locals_data = {}
        for _ in range(num_locals_fields):
            key_len = struct.unpack('I', file.read(4))[0]
            key = file.read(key_len).decode('utf-8')
            value_len = struct.unpack('I', file.read(4))[0]
            value = file.read(value_len).decode('utf-8')
            locals_data[key] = value

        data['lessons'] = lessons
        data['academic_config'] = academic_config
        data['locals'] = locals_data
        return data

def convert_to_toml(data):
    toml_data = {
        'academic_config': data['academic_config'],
        'locals': data['locals'],
    }

    for lesson_name, lesson_data in data['lessons'].items():
        toml_data[lesson_name] = lesson_data

    return toml.dumps(toml_data)

def save_to_toml(toml_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(toml_data)

if __name__ == "__main__":
    input_binary_file = 'inf_data.bin'
    output_toml_file = 'output_config_2.toml'
    parsed_data = read_binary_file(input_binary_file)
    toml_data = convert_to_toml(parsed_data)
    save_to_toml(toml_data, output_toml_file)
    print(f"Конвертация завершена. Данные сохранены в {output_toml_file}")

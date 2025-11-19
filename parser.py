import struct


def parse_hcl_file(file_path):
    data = {"lessons": {}, "academic_config": {}, "locals": {}}
    current_block = None
    current_key = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith('}'):
                if line.startswith('}'):
                    current_block = None
                continue

            if line.startswith('lesson'):
                current_key = line.split()[1].strip('"')
                current_block = 'lesson'
                data['lessons'][current_key] = {}
            elif line.startswith('academic_config'):
                current_block = 'academic_config'
            elif line.startswith('locals'):
                current_block = 'locals'
            elif '=' in line:
                key, value = line.split('=', 1)
                key, value = key.strip(), value.strip().strip('"')
                if current_block == 'lesson' and current_key:
                    data['lessons'][current_key][key] = value
                elif current_block:
                    data[current_block][key] = value

    return data


def write_string(file, s):

    bytes_data = s.encode('utf-8')
    file.write(struct.pack('I', len(bytes_data)))
    file.write(bytes_data)


def convert_to_binary(data, output_file):
    with open(output_file, 'wb') as file:

        file.write(struct.pack('I', len(data["lessons"])))
        for lesson_name, lesson_data in data["lessons"].items():
            write_string(file, lesson_name)
            file.write(struct.pack('I', len(lesson_data)))
            for key, value in lesson_data.items():
                write_string(file, key)
                write_string(file, value)


        for section in ["academic_config", "locals"]:
            file.write(struct.pack('I', len(data[section])))
            for key, value in data[section].items():
                write_string(file, key)
                write_string(file, value)


if __name__ == "__main__":
    parsed_data = parse_hcl_file('inf.hcl')
    convert_to_binary(parsed_data, 'inf_data.bin')
    print("Файл inf.hcl успешно конвертирован в бинарный объект inf_data.bin")
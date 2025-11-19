import struct
import xml.etree.ElementTree as ET

def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        data_dict = {}
        index = 0
        num_lessons = struct.unpack_from('I', data, index)[0]
        index += 4
        lessons = {}
        for _ in range(num_lessons):
            lesson_name_len = struct.unpack_from('I', data, index)[0]
            index += 4
            lesson_name = data[index:index + lesson_name_len].decode('utf-8')
            index += lesson_name_len
            num_fields = struct.unpack_from('I', data, index)[0]  # Читаем количество полей
            index += 4
            lesson_data = {}
            for _ in range(num_fields):
                key_len = struct.unpack_from('I', data, index)[0]
                index += 4
                key = data[index:index + key_len].decode('utf-8')
                index += key_len

                value_len = struct.unpack_from('I', data, index)[0]
                index += 4
                value = data[index:index + value_len].decode('utf-8')
                index += value_len
                lesson_data[key] = value
            lessons[lesson_name] = lesson_data

        num_academic_config_fields = struct.unpack_from('I', data, index)[0]
        index += 4
        academic_config = {}
        for _ in range(num_academic_config_fields):
            key_len = struct.unpack_from('I', data, index)[0]
            index += 4
            key = data[index:index + key_len].decode('utf-8')
            index += key_len

            value_len = struct.unpack_from('I', data, index)[0]
            index += 4
            value = data[index:index + value_len].decode('utf-8')
            index += value_len
            academic_config[key] = value

        num_locals_fields = struct.unpack_from('I', data, index)[0]
        index += 4
        locals_data = {}
        for _ in range(num_locals_fields):
            key_len = struct.unpack_from('I', data, index)[0]
            index += 4
            key = data[index:index + key_len].decode('utf-8')
            index += key_len

            value_len = struct.unpack_from('I', data, index)[0]
            index += 4
            value = data[index:index + value_len].decode('utf-8')
            index += value_len
            locals_data[key] = value

        data_dict['lessons'] = lessons
        data_dict['academic_config'] = academic_config
        data_dict['locals'] = locals_data
        return data_dict

def convert_to_xml(data):
    root = ET.Element('root')

    lessons_elem = ET.SubElement(root, 'lessons')
    for lesson_name, lesson_data in data['lessons'].items():
        lesson_elem = ET.SubElement(lessons_elem, lesson_name)
        for key, value in lesson_data.items():
            field_elem = ET.SubElement(lesson_elem, key)
            field_elem.text = value

    academic_config_elem = ET.SubElement(root, 'academic_config')
    for key, value in data['academic_config'].items():
        field_elem = ET.SubElement(academic_config_elem, key)
        field_elem.text = value

    locals_elem = ET.SubElement(root, 'locals')
    for key, value in data['locals'].items():
        field_elem = ET.SubElement(locals_elem, key)
        field_elem.text = value

    tree = ET.ElementTree(root)

    import xml.dom.minidom
    xml_str = ET.tostring(root, 'utf-8')
    dom = xml.dom.minidom.parseString(xml_str)
    formatted_xml = dom.toprettyxml(indent="  ")
    return formatted_xml

def save_to_xml(xml_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(xml_data)

if __name__ == "__main__":
    input_binary_file = 'inf_data.bin'
    output_xml_file = 'output_config.xml'
    parsed_data = read_binary_file(input_binary_file)
    xml_data = convert_to_xml(parsed_data)
    save_to_xml(xml_data, output_xml_file)
    print(f"Конвертация завершена. Данные сохранены в {output_xml_file}")

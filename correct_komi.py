import os
import pickle


def get_new_files(directory, processed_files):
    new_files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith('.sgf') and filename not in processed_files:
            new_files.append(filepath)
    return new_files


def batch_replace_in_files(directory, old_text, new_text, processed_files):
    new_files = get_new_files(directory, processed_files)
    if new_files:
        for filepath in new_files:
            with open(filepath, 'r') as file:
                file_content = file.read()

            # 替换文本内容
            updated_content = file_content.replace(old_text, new_text)

            # 写入更新后的内容
            with open(filepath, 'w') as file:
                file.write(updated_content)

            processed_files.add(os.path.basename(filepath))
            print(f"文件 '{os.path.basename(filepath)}' 更新完成")

    # 存储已处理的文件列表到本地
    with open('processed_files.pkl', 'wb') as file:
        pickle.dump(processed_files, file)


if __name__ == '__main__':
    directory_path = '/Users/yqli/Downloads/Go-SGF/'  # 将其替换为包含要修改文件的目录路径
    old_text_to_replace = 'KM[375]'
    new_text_to_replace = 'KM[7.5]'
    if os.path.exists('processed_files.pkl'):
        with open('processed_files.pkl', 'rb') as file:
            processed_files = pickle.load(file)
    else:
        processed_files = set()
    batch_replace_in_files(directory_path, old_text_to_replace, new_text_to_replace, processed_files)

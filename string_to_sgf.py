def index_to_sgf_position(index):
    x = index // 19
    y = index % 19
    return chr(97 + x) + chr(97 + y)


def go_string_to_sgf_final_state(go_string):
    black_positions = []
    white_positions = []
    for index, value in enumerate(go_string):
        pos = index_to_sgf_position(index)
        if value == '1':
            black_positions.append(pos)
        elif value == '2':
            white_positions.append(pos)

    # FF[4] - SGF format version 4, GM[1] - Game type (1 for Go), SZ[19] - Size of the board
    sgf_content = "(;GM[1]FF[4]SZ[19]KM[7.5]"

    if black_positions:
        sgf_content += "AB"
        for pos in black_positions:
            sgf_content += f"[{pos}]"
    if white_positions:
        sgf_content += "AW"
        for pos in white_positions:
            sgf_content += f"[{pos}]"
    sgf_content += ")"
    return sgf_content


if __name__ == '__main__':
    go_string = "1000000000000000000100000000000000000022000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    sgf_file_content = go_string_to_sgf_final_state(go_string)
    with open('test.sgf', 'w') as f:
        f.write(sgf_file_content)
        print(sgf_file_content)

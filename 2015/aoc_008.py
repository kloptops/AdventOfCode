def decode_string(text):
    i = 1
    output = ''
    while i < len(text)-1:
        c = text[i]
        if c == '\\':
            i += 1
            c = text[i]
            if c == 'x':
                output += chr(int(text[i+1:i+3], 16))
                i += 3
                continue

        output += c
        i += 1
     
    return output

def encode_string(text):
    output = '"'
    for c in text:
        if c in '\\"':
            output += '\\'
        output += c
    output += '"'
    return output

def simulate(data):
    # code here
    output_a = 0
    output_b = 0
    for line in data:
        text = decode_string(line)
        block = encode_string(line)
        print(line, block)
        output_a += (len(line) - len(text))
        output_b += (len(block) - len(line))

    return output_a, output_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_008.txt')
    results = simulate(data)
    print(results[0], 1371)
    print(results[1], 2117)


if __name__ == '__main__':
    main()

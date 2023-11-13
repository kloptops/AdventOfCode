def incrementer(text):
    text = list(map(lambda x: ord(x) - 97, text))
    
    while True:
        i = len(text)-1
        text[i] += 1
        while i > 0:
            if text[i] > 25:
                text[i] -= 26
                text[i-1] += 1
                i -= 1
            else:
                break
        
        yield ''.join(map(lambda x: chr(x + 97), text))

def check_a(text):
    if 'i' in text:
        return False
    if 'o' in text:
        return False
    if 'l' in text:
        return False

    for i in range(len(text) - 3):
        if (
                ord(text[i]) == ord(text[i+1])-1 and
                ord(text[i]) == ord(text[i+2])-2):
            break
    else:
        return False
    
    count = 0
    for i in range(26):
        if chr(97 + i)+chr(97 + i) in text:
            count += 1
    
    if count >= 2:
        return True
    else:
        return False
      

def simulate(data):
    # code here
    for password_a in incrementer(data):
        if check_a(password_a):
            break
    
    for password_b in incrementer(password_a):
        if check_a(password_b):
            break

    return password_a, password_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = 'vzbxkghb'
    results = simulate(data)
    print(results[0], 'vzbxxyzz')
    print(results[1], 'vzcaabcc')


if __name__ == '__main__':
    main()

def happy_key(person_a, person_b):
    if person_a > person_b:
        return person_b, person_a
    return person_a, person_b


def happy_next(happy_index, person_a, people, last_person):
    happy_best = None
    if len(people) == 1:
        temp = happy_index[happy_key(person_a, people[0])]
        temp += happy_index[happy_key(people[0], last_person)]
        return temp

    for person_b in people:
        next_people = people[::]
        next_people.remove(person_b)

        happy = happy_index[happy_key(person_a, person_b)]
        new_happy = happy_next(happy_index, person_b, next_people, last_person)

        if happy_best is None or happy_best < (happy + new_happy):
            happy_best = happy + new_happy

    return happy_best

def simulate(data):
    happy_index = {}
    people = set()

    for line in data:
        'Alice would gain 54 happiness units by sitting next to Bob.'
        person_a, _, shift, amount, *_, person_b = line[:-1].split(' ')
        if shift == 'lose':
            amount = -int(amount)
        else:
            amount = int(amount)
        
        people.add(person_a)

        print(person_a, amount, person_b)

        happy_index.setdefault(happy_key(person_a, person_b), 0)
        happy_index[happy_key(person_a, person_b)] += amount
    
    people = list(people)

    happy_best_a = None
    for person_a in people:
        next_people = people[::]
        next_people.remove(person_a)
        
        happy = happy_next(happy_index, person_a, next_people, person_a)
        if happy_best_a is None or happy_best_a < happy:
            happy_best_a = happy
    
    for person in people:
        happy_index[happy_key('Myself', person)] = 0
    people.append('Myself')

    happy_best_b = None
    for person_a in people:
        next_people = people[::]
        next_people.remove(person_a)
        
        happy = happy_next(happy_index, person_a, next_people, person_a)
        if happy_best_b is None or happy_best_b < happy:
            happy_best_b = happy

    return happy_best_a, happy_best_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_013.txt')
    results = simulate(data)
    print(results[0], 709)
    print(results[1], )

if __name__ == '__main__':
    main()

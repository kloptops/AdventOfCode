WAIT, ORE, CLAY, OBSIDIAN, GEODE = range(-1, 4)
CHOICE_TXT = ['ORE', 'CLAY', 'OBSi', 'GEOD', 'WAIT']
def new_state(minutes):
    return (
        minutes,
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [],
        None)


def copy_state(minutes, resources, robots, factory, choice):
    return (
        minutes,
        resources[:],
        robots[:],
        factory[:],
        choice)

def check_recipe(resources, recipe):
    makable = 1<<32

    for need, have in zip(recipe, resources):
        if have < need:
            return False

        if need > 0:
            makable = min(makable, have // need)

    if makable > 3:
        # skip it if we can make more than 2
        return False

    return True


def craft_recipe(resources, recipe):
    for i in range(len(recipe)):
        resources[i] -= recipe[i]


def res_score(time_left, resources, robots):
    temp = (100 * (resources[GEODE] + (robots[GEODE] * time_left))) + resources[OBSIDIAN]
    
    return temp


def run_blueprint(idx, mode, blueprint, total_minutes):

    minutes = 0
    stack = [new_state(minutes)]
    best_score = None
    best_factory = None

    split = 0
    best_skipper = [0] * (total_minutes + 1)
    best_skips = 0

    while len(stack) > 0:
        split += 1

        #prune_choices(stack, total_minutes)
        minutes, resources, robots, factory, choice = stack.pop(-1)

        if (split % 100_000) == 0:
            print(f'>>( {idx}{mode} )>> {split} - {minutes}/{total_minutes}: Res: {resources}, Rob: {robots}, Steps {len(factory)}, Cho: {CHOICE_TXT[choice]}, Stack {len(stack)}, BS: {best_skips}')
            pass

        score = res_score(total_minutes - minutes, resources, robots)
        if minutes > 1 and score < max(best_skipper[:minutes]):
            best_skips += 1
            continue

        elif score > best_skipper[minutes]:
            best_skipper[minutes] = score

        while minutes < total_minutes:
            if choice is not None:
                if choice >= ORE:
                    craft_recipe(resources, blueprint[choice])

                factory.append(choice)

            minutes += 1
            #print(f'== Minute {minutes} ==')
            if len(factory) > 1 and factory[-2] is not None:
                if factory[-2] >= ORE:
                    robots[factory[-2]] += 1

            for i, units in enumerate(robots):
                resources[i] += units

            choices = []
            choices.append(WAIT)

            for i, robot_recipe in enumerate(blueprint):
                if check_recipe(resources, robot_recipe):
                    choices.append(i)

            if GEODE in choices:
                choices = [GEODE]

            elif OBSIDIAN in choices:
                choices = [WAIT, OBSIDIAN]

            elif (total_minutes - minutes) <= 4:
                if ORE in choices:
                    choices.remove(ORE)
                if CLAY in choices:
                    choices.remove(CLAY)

            choice = choices.pop(-1)
            for sub_choice in choices[::-1]:
                stack.append(copy_state(
                    minutes,
                    resources,
                    robots,
                    factory,
                    sub_choice))

            score = res_score(total_minutes - minutes, resources, robots)
            if score > best_skipper[minutes]:
                best_skipper[minutes] = score


        if best_score is None or resources[GEODE] > best_score:

            best_score = resources[GEODE]
            best_factory = factory

            factory_text = ', '.join((
                CHOICE_TXT[choice]
                for choice in best_factory))
            
            #print()
            #print('new score', split, best_score, factory_text)
            #print()


    factory_text = ', '.join((
        CHOICE_TXT[choice]
        for choice in best_factory))

    print(split, best_score, factory_text)
    return best_score


def load_blueprints(data):
    blueprints = []
    for line in data:
        o, c, o1, o2, g1, g2  = list(map(int, (
            x
            for x in line.split(':')[1].split(' ')
            if x.isdigit())))

        blueprint = (
            ( o,  0,  0, 0),
            ( c,  0,  0, 0),
            (o1, o2,  0, 0),
            (g1,  0, g2, 0),
            )
        blueprints.append(blueprint)
        
        #print(blueprint)

    return blueprints


def simulate(data):
    # code here
    blueprints = load_blueprints(data)
    total_a = 0
    total_b = 1

    for i, blueprint in enumerate(blueprints, 1):
        if i <= 3:
            result_b = run_blueprint(i, 'b', blueprint, 32)
        else:
            result_b = 1

        result_a = run_blueprint(i, 'a', blueprint, 24)

        print(f'{i}: {result_a} {result_b}')
        total_a += i * result_a
        total_b *= result_b

    return total_a, total_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_019.txt')
    results = simulate(data)
    print(results[0], 1521)
    print(results[1], 16926)


if __name__ == '__main__':
    main()

"""

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

"""


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data

def simulate(data, translate, rps_game):
    add_score = {
        'R': 1,
        'P': 2,
        'S': 3,
        'LOSE': 0,
        'DRAW': 3,
        'WIN': 6,
        }

    total_score = 0

    for line in data:
        a, b = line.split(' ')
        a = translate[a]
        b = translate[b]
        result = rps_game[(a, b)]
    
        score = add_score[b] + add_score[result]
        total_score += score
    
    return total_score

def main():
    translate_a = {
        'A': 'R',
        'X': 'R',
        'B': 'P',
        'Y': 'P',
        'C': 'S',
        'Z': 'S',
        }
    
    rps_game_a = {
        ('R', 'R'): 'DRAW',
        ('R', 'P'): 'WIN',
        ('R', 'S'): 'LOSE',
        ('P', 'R'): 'LOSE',
        ('P', 'P'): 'DRAW',
        ('P', 'S'): 'WIN',
        ('S', 'R'): 'WIN',
        ('S', 'P'): 'LOSE',
        ('S', 'S'): 'DRAW',
        }
    
    translate_b = {
        'A': 'R',
        'X': 'LOSE',
        'B': 'P',
        'Y': 'DRAW',
        'C': 'S',
        'Z': 'WIN',
        }
    
    rps_game_b = {
        ('R', 'DRAW'): 'R',
        ('R', 'WIN'): 'P',
        ('R', 'LOSE'): 'S',
        ('P', 'DRAW'): 'P',
        ('P', 'WIN'): 'S',
        ('P', 'LOSE'): 'R',
        ('S', 'DRAW'): 'S',
        ('S', 'WIN'): 'R',
        ('S', 'LOSE'): 'P',
        }

    data = get_data('data/input_002.txt')
    print(simulate(data, translate_a, rps_game_a), 14264)
    print(simulate(data, translate_b, rps_game_b), 12382)

if __name__ == '__main__':
    main()

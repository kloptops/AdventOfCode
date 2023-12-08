"""
--- Day 7: Camel Cards ---

Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?

--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""

CARDS_R = '23456789TJQKA'
CARDS_J = 'J23456789TQKA'
CARDS = 'AKQJT98765432'

HIGH_CARD, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND, FULL_HOUSE, FOUR_OF_A_KIND, FIVE_OF_A_KIND = range(7)
HAND_TYPE = {
    (5, ): FIVE_OF_A_KIND,
    (4, 1): FOUR_OF_A_KIND,
    (3, 2): FULL_HOUSE,
    (3, 1, 1): THREE_OF_A_KIND,
    (2, 2, 1): TWO_PAIR,
    (2, 1, 1, 1): ONE_PAIR,
    (1, 1, 1, 1, 1): HIGH_CARD,
    }

print(HAND_TYPE)

import functools
from util import *


def hand_compare(a, b, order=None):
    if order is None:
        order = CARDS_R

    hand_a = a[0]
    hand_b = b[0]

    cmp = hand_a['type'] - hand_b['type']

    if cmp != 0:
        return cmp

    for card_a, card_b in zip(hand_a['hand'], hand_b['hand']):
        cmp = order.index(card_a) - order.index(card_b)
        if cmp != 0:
            return cmp

    return 0

def hand_compare2(a, b):
    return hand_compare(a, b, order=CARDS_J)

def hand_info(hand):
    sort_hand = sorted(hand, key=lambda card: CARDS.index(card))

    info = {
        'hand': ''.join(hand),
        'set': ''.join(set(sort_hand)),
        'numbers': {
            card: hand.count(card)
            for card in set(hand)
            },
        'values': None,
        'type': None,
        }

    info['values'] = tuple(sorted(info['numbers'].values(), reverse=True))
    info['type'] = HAND_TYPE[ info['values'] ]
    # print(f"{hand}: {info}")

    return info


def trial_hands(hand):
    AVAILABLE_CARDS = list(
        sorted(
            list(
                set(
                    hand.replace('J', '')
                    )
                ),
            key=lambda card: CARDS_R.index(card)))

    for card in AVAILABLE_CARDS:
        yield hand.replace('J', card)


def best_hand_info(hand):
    base_hand_info = hand_info(hand)

    if 'J' not in hand:
        return base_hand_info

    if hand == 'JJJJJ':
        return base_hand_info

    best_hand_info = base_hand_info.copy()
    for trial_hand in trial_hands(hand):
        new_hand_info = hand_info(trial_hand)
        if hand_compare([best_hand_info], [new_hand_info]) < 0:
            best_hand_info = new_hand_info

    print(f"{hand} -> {best_hand_info['hand']}")
    del best_hand_info['hand']
    base_hand_info.update(**best_hand_info)

    return base_hand_info


def load_hands(data):
    output1, output2 = [], []
    for line in data:
        hand, value = line.strip().split()
        info1 = hand_info(hand)
        output1.append([info1, int(value)])

        info2 = best_hand_info(hand)
        output2.append([info2, int(value)])

    return output1, output2


def process(data1, data2):
    total_a = 0
    total_b = 0

    ## Do something here.
    for i, hand_data in enumerate(sorted(data1, key=functools.cmp_to_key(hand_compare)), 1):
        # print(f"{hand_data[0]['hand']} -> {i} * {hand_data[1]}")
        total_a += i * hand_data[1]

    for i, hand_data in enumerate(sorted(data2, key=functools.cmp_to_key(hand_compare2)), 1):
        # print(f"{hand_data[0]['hand']} -> {i} * {hand_data[1]}")
        total_b += i * hand_data[1]

    return total_a, total_b


def main():
    data1, data2 = load_hands(load_data('input_007.txt'))

    results = process(data1, data2)

    print(results[0], '==', 248179786)
    print(results[1], '==', None)


if __name__ == '__main__':
    main()

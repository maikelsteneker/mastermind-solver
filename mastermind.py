#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description='Solve a mastermind game.', epilog='If no options are provided, the original rules are used.')
parser.add_argument('colour_names', metavar='colour-names', type=str, nargs='*',
                    help='names for the colours of the pegs (defaults to numbers)')
parser.add_argument('-c', '--colours', type=int, default=6,
                    help='the number of different colours')
parser.add_argument('-p', '--pegs', type=int, default=4,
                    help='the number of pegs')
parser.add_argument('-u', '--unique', dest='unique', action='store_true',
                    help='Allow non-unique solutions.')
parser.add_argument('-n', '--numbers', dest='numbers', action='store_true',
                    help='Use numbers instead of colours')
args = parser.parse_args()

n_colours = args.colours
n_pegs = args.pegs
unique = args.unique
colour_names = ['Colour %d' % (i+1) for i in range(n_colours)]
if all((args.colour_names==[], n_colours == 6, args.pegs == 4, not unique, not args.numbers)):
    # default rules
    colour_names = ['red', 'yellow', 'green', 'blue', 'white', 'black']
for i in range(len(args.colour_names)):
    colour_names[i] = args.colour_names[i]
if args.numbers:
    colour_names = ['%d' % (i+1) for i in range(n_colours)]

pretty_guess = lambda guess: ' '.join(colour_names[i] for i in guess)

def generate_all_solutions(n_colours=n_colours, n_pegs=n_pegs, unique=unique, forbidden=[]):
    """Generates all possible solutions for a given number of colours and pegs."""
    if n_pegs > 0:
        for head in range(n_colours):
            if not unique or head not in forbidden:
                new_forbidden = forbidden+[head] if unique else forbidden
                tails = generate_all_solutions(n_colours=n_colours, n_pegs=n_pegs-1, forbidden=new_forbidden)
                for tail in tails:
                    yield [head] + tail
    else:
        yield []

def generate_solutions(solutions_generator=generate_all_solutions, hints=[]):
    for solution in solutions_generator():
        if not any(conflict(solution, hint) for hint in hints):
            yield solution

def judge(solution, guess):
    """Judge the guess based on the correct solution. Returns a tuple
    containing the number of elements in the right location and the
    number of elements that are correct, but in the wrong location
    (in that order).
    
    >>> judge([1,2,3,4],[1,2,4,5])
    (2, 1)
    >>> judge([1,2,3,4],[1,2,3,4])
    (4, 0)
    """
    assert len(solution) == len(guess)
    correct_location, correct_colour = set(), set()
    for i in range(len(solution)):
        if solution[i] == guess[i]:
            correct_location.add(i)
    for i in range(len(solution)):
        for g in guess:
            if solution[i] == g:
                correct_colour.add(i)
                break
    return len(correct_location), len(correct_colour - correct_location)

# shape of a hint: (guess, (correct_location, correct_colour))

def conflict(solution, hint):
    """Decides whether there's a conflict between a solution and a hint.
    
    >>> conflict([1,2,3,4], ([1,2,4,5], (2, 1)))
    False
    >>> conflict([1,2,3,4], ([1,2,4,5], (2, 0)))
    True
    """
    guess, judgement = hint
    return judge(solution, guess) != judgement

if __name__=='__main__':
    import doctest
    doctest.testmod()
    
    done = False
    hints = []
    next_guess = list(range(n_pegs)) if unique else [0, 0, 1, 1]
    try:
        while not done:
            print('Next guess: {0}'.format(pretty_guess(next_guess)))
            try:
                hints.append((next_guess,
                    (int(input('Number of pegs on the correct location: ')),
                     int(input('Number of correct pegs in the wrong location: ')))))
            except ValueError:
                print('Please provide a valid number.')
            generator = generate_solutions(hints=hints)
            next_guess = next(generator)
            try:
                next(generator)
            except StopIteration:
                done = True
        solution = next_guess
        print('Solution: {0}'.format(pretty_guess(solution)))
    except StopIteration:
        print('No solution that satisfies the provided hints!')
    except EOFError:
        print()
        print('Input ended before solution could be found!')

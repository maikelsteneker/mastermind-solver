#!/usr/bin/env python3
n_colours = 9
n_pegs = 4
unique = True

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
    next_guess = list(range(n_pegs))
    while not done:
        print('Next guess: {0}'.format(next_guess))
        hints.append((next_guess,
            (int(input('Number of pegs on the correct location: ')),
             int(input('Number of correct pegs in the wrong location: ')))))
        generator = generate_solutions(hints=hints)
        next_guess = next(generator)
        try:
            next(generator)
        except StopIteration:
            done = True
    solution = next_guess
    print('Solution: {0}'.format(solution))

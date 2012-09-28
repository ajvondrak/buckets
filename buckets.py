"""UCI Puzzle - Buckets

You're out hiking with friends and everyone's getting hungry. You have a packet
of soup mix, and its recipe requires exactly 4 quarts of water. Unfortunately,
you forgot your 4-quart cooking pot at home. All you have is a 5-quart pot and
a 3-quart pot. There is a stream nearby, so you have an unlimited source of
water. How will you use the 5-quart pot and the 3-quart pot to measure exactly
4 quarts of water?
"""

### Basic Operations ###

# For now, we'll represent the state of our pots by the tuple
#     (three_qt, five_qt)
# where three_qt is the number of quarts of water contained in the 3-quart pot
# and five_qt is the number of quarts of water contained in the 5-quart pot.
# This isn't really general, but it *is* simple.

def pour(source_contents, source_capacity, target_contents, target_capacity):
    """Transfer as much water from source to target as possible."""
    how_much_we_have = source_contents
    how_much_will_fit = target_capacity - target_contents
    amount_poured = min(how_much_we_have, how_much_will_fit)
    return (source_contents - amount_poured, target_contents + amount_poured)

def pour_three_qt_into_five_qt((three_qt, five_qt)):
    return pour(three_qt, 3, five_qt, 5)

def pour_five_qt_into_three_qt((three_qt, five_qt)):
    five_qt, three_qt = pour(five_qt, 5, three_qt, 3)
    return (three_qt, five_qt)

def fill_three_qt((three_qt, five_qt)):
    return (3, five_qt)

def fill_five_qt((three_qt, five_qt)):
    return (three_qt, 5)

def empty_three_qt((three_qt, five_qt)):
    return (0, five_qt)

def empty_five_qt((three_qt, five_qt)):
    return (three_qt, 0)

def possible_moves(buckets):
    yield pour_three_qt_into_five_qt(buckets), \
            "Pour all you can from the 3-quart pot to the 5-quart pot."
    yield pour_five_qt_into_three_qt(buckets), \
            "Pour all you can from the 5-quart pot to the 3-quart pot."
    yield fill_three_qt(buckets), \
            "Fill the 3-quart pot."
    yield fill_five_qt(buckets), \
            "Fill the 5-quart pot."
    yield empty_three_qt(buckets), \
            "Empty the 3-quart pot into the stream."
    yield empty_five_qt(buckets), \
            "Empty the 5-quart pot into the stream."

### Breadth-first search ###

def amounts((three_qt, five_qt)):
    return ("%d quarts of water in the 3-quart pot" % three_qt,
            "%d quarts of water in the 5-quart pot" % five_qt)

def reconstruct_path(parent, source, target):
    from textwrap import fill
    states = []
    actions = []
    state = target
    while state != source:
        states.append(state)
        state, action = parent[state]
        actions.append(action)
    states.reverse()
    actions.reverse()
    for step, (action, state) in enumerate(zip(actions, states)):
        print fill("%1d. %s" % (step + 1, action), 80)
        print fill("This leaves %s and %s." % amounts(state), 80,
                    initial_indent=" " * 3, subsequent_indent=" " * 3)
        print

def search(source, target):
    from collections import deque
    parent = {}
    visited = set([source])
    worklist = deque([source])
    while worklist:
        state = worklist.popleft()
        if state == target:
            reconstruct_path(parent, source, target)
            return
        for next_state, action in possible_moves(state):
            if next_state not in visited:
                visited.add(next_state)
                worklist.append(next_state)
                parent[next_state] = (state, action)

### Answer the puzzle. ###

if __name__ == '__main__':
    print __doc__
    print "ANSWER:\n"
    search((0, 0), (0, 4))
    # BFS guarantees shortest path (if one exists)
    print "This answer is guaranteed to use the least number of steps."

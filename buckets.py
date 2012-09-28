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
    yield pour_three_qt_into_five_qt(buckets)
    yield pour_five_qt_into_three_qt(buckets)
    yield fill_three_qt(buckets)
    yield fill_five_qt(buckets)
    yield empty_three_qt(buckets)
    yield empty_five_qt(buckets)

### Breadth-first search

def reconstruct_path(parent, source, target):
    path = []
    state = target
    while state != source:
        path.append(state)
        state = parent[state]
    path.append(source)
    return list(reversed(path))

def search(source, target):
    from collections import deque
    parent = {}
    visited = set([source])
    worklist = deque([source])
    while worklist:
        state = worklist.popleft()
        if state == target:
            return reconstruct_path(parent, source, target)
        for next_state in possible_moves(state):
            if next_state not in visited:
                visited.add(next_state)
                worklist.append(next_state)
                parent[next_state] = state

if __name__ == '__main__':
    print search((0, 0), (0, 4))

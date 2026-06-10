from z3 import *

def test_simplification():
    width = Int('width')
    length = Int('length')
    s = Solver()
    s.add(30 == 2 * (length + width))
    s.add(length == 2 * width)
    assert s.check() == sat
    model = s.model()
    assert str(model[width]) == '5'
    print("Simplification test PASSED")

def test_complication():
    width = Int('width')
    length = Int('length')
    perimeter = Int('perimeter')
    d = Int('d')
    e = Int('e')
    s = Solver()
    s.add(perimeter == 30)
    s.add(length == 2 * width)
    s.add(perimeter == 2 * (length + width))
    s.add(d + e == 30)
    s.add(d - e == 4)
    s.add(perimeter == d + e)
    assert s.check() == sat
    model = s.model()
    assert str(model[width]) == '5'
    print("Complication test PASSED")

test_simplification()
test_complication()

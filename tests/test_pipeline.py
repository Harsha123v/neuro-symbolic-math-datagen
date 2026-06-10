from z3 import *

def test_formalization():
    width = Int('width')
    length = Int('length')
    perimeter = Int('perimeter')
    s = Solver()
    s.add(perimeter == 30)
    s.add(length == 2 * width)
    s.add(perimeter == 2 * (length + width))
    assert s.check() == sat
    model = s.model()
    assert str(model[width]) == '5'
    assert str(model[length]) == '10'
    print("Formalization test PASSED")

test_formalization()

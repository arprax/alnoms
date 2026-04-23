import ast
from alnoms.core.autogen import AutoGen


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def parse_func(src: str):
    """Parse a function source string into an AST node."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return node
    return None


# ---------------------------------------------------------
# Classification Tests
# ---------------------------------------------------------
def test_classify_nested_loops():
    src = """
def f(arr):
    for x in arr:
        for y in arr:
            pass
"""
    func = parse_func(src)
    assert AutoGen._classify(func) == "nested_loops"


def test_classify_hash_heavy():
    src = """
def f():
    d = {1: 2}
    return d
"""
    func = parse_func(src)
    assert AutoGen._classify(func) == "hash_heavy"


def test_classify_sorting():
    src = """
def f(a):
    a.sort()
"""
    func = parse_func(src)
    assert AutoGen._classify(func) == "sorting"


def test_classify_sequential():
    src = """
def f(a):
    for x in a:
        pass
"""
    func = parse_func(src)
    assert AutoGen._classify(func) == "sequential"


def test_classify_generic():
    src = """
def f(a):
    return a + 1
"""
    func = parse_func(src)
    assert AutoGen._classify(func) == "generic"


# ---------------------------------------------------------
# Input Model Tests
# ---------------------------------------------------------
def test_sequential_string():
    s = AutoGen._sequential_string(5)
    assert s == "abcde"


def test_random_string_deterministic():
    s1 = AutoGen._random_string(10)
    s2 = AutoGen._random_string(10)
    assert s1 == s2  # deterministic


def test_random_list_length():
    lst = AutoGen._random_list(7)
    assert len(lst) == 7


def test_hash_collision_array():
    arr = AutoGen._hash_collision_array(20)
    # Should contain repeated values due to collisions
    assert len(set(arr)) < 20


# ---------------------------------------------------------
# Generation Dispatch Tests
# ---------------------------------------------------------
def test_generate_nested_loops():
    out = AutoGen.generate("nested_loops", 5)
    assert isinstance(out, tuple)
    assert out[0] == [0, 1, 2, 3, 4]


def test_generate_hash_heavy():
    out = AutoGen.generate("hash_heavy", 10)
    assert isinstance(out, tuple)
    assert isinstance(out[0], list)


def test_generate_sorting():
    out = AutoGen.generate("sorting", 8)
    assert isinstance(out[0], list)


def test_generate_sequential():
    out = AutoGen.generate("sequential", 5)
    assert out[0] == "abcde"


def test_generate_generic():
    out = AutoGen.generate("generic", 5)
    assert isinstance(out[0], str)


# ---------------------------------------------------------
# Public Entrypoint Tests
# ---------------------------------------------------------
def test_infer_and_generate_end_to_end():
    src = """
def f(arr):
    for x in arr:
        for y in arr:
            pass
"""
    func = parse_func(src)
    out = AutoGen.infer_and_generate(func, 4)
    assert out == ([0, 1, 2, 3],)

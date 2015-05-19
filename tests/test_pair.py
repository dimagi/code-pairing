from pair import CodePairs


def test_basic():
    cp = CodePairs(config_path='tests/basic.yml')
    pairs = cp._generate_pairs()

    assert len(pairs) == 2


def test_uneven_groups():
    cp = CodePairs(config_path='tests/uneven.yml')
    pairs = cp._generate_pairs()

    assert len(pairs) == 3

def test_uneven_groups2():
    cp = CodePairs(config_path='tests/uneven2.yml')
    pairs = cp._generate_pairs()

    assert len(pairs) == 2
    assert any(map(lambda p: len(p) == 3, pairs))

def test_odd_number():
    cp = CodePairs(config_path='tests/odd.yml')
    pairs = cp._generate_pairs()

    assert len(pairs) == 3
    assert any(map(lambda p: len(p) == 3, pairs))


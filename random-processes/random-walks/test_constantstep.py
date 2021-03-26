from constantstep import Constant_Step, random
import pytest
random.seed(5) # Random seed used to create reproducibility of results and generate numbers to write the below tests. 

@pytest.fixture
def walk():
    N = 10
    ss = 2
    iterations = 5
    return Constant_Step(N, ss , iterations)

def test_constant_step_init(walk):
    assert walk.N == 10
    assert walk.ss == 2
    assert walk.iterations == 5
    assert len(walk.x) == walk.N
    assert len(walk.y) == walk.N
    assert len(walk.z) == walk.N
    assert len(walk.distances) == 10

def test_gen_random_walk(walk):
    assert walk.gen_random_walk('1D') == -2
    assert walk.gen_random_walk('2D') == (-4, -2)
    assert walk.gen_random_walk('3D') == (-6, -4, 4)

def test_calc_displacements(walk):
    assert walk.calc_displacements('1D') == (0.4, 6.985699678629192)
    assert walk.calc_displacements('2D') == (3.6, 6.511528238439882)
    assert walk.calc_displacements('3D') == (-5.2, 5.440588203494177)
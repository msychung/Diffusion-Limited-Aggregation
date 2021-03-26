from variablestep import Variable_Step
import random
import pytest
random.seed(5)   # Random seed used to create reproducibility of results and generate numbers to write the below tests. 

@pytest.fixture
def walk():
    T = 100
    N = 5
    M = 3
    iterations = 10
    return Variable_Step(T, N, M, iterations)

def test_variable_step_init(walk):
    assert walk.T == 100
    assert walk.N == 5
    assert walk.M == 3
    assert walk.iterations == 10
    assert round(walk.dt) == 5
    assert len(walk.t) == 5

def test_brownian_1D_loop(walk):
    assert len(walk.brownian_1D_loop()['x']) == 5

def test_brownian_1D_vec(walk):
    assert len(walk.brownian_1D_vec()['Time']) == 5

def test_brownian_2D_loop(walk):
    assert len(walk.brownian_2D_loop()['x']) == 5

def test_brownian_2D_vec(walk):
    assert len(walk.brownian_2D_vec()['Time']) == 5

def test_brownian_3D_vec(walk):
    assert len(walk.brownian_3D_vec()['Time']) == 5

def test_calc_displacements(walk):
    assert round(walk.calc_displacements('1D'), 1) == 2.4
    assert round(walk.calc_displacements('2D'), 1) == 2.1
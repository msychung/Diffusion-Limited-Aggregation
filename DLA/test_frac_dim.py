import pytest
from frac_dim import Fractal_Dimension

@pytest.fixture
def fractal():
    n = 100
    seed_shape = 'dot'
    spawn_shape = 'square'
    padSize = 50
    return Fractal_Dimension(n, seed_shape, spawn_shape, padSize)

def test_fractal_dimension_init(fractal):
    assert len(fractal.clusters) == 89

def test_cluster_mass(fractal):
    assert len(fractal.cluster_mass()[0]) == 89
    assert len(fractal.cluster_mass()[1]) == 89

def test_cluster_radius(fractal):
    assert len(fractal.cluster_radius()[0]) == 89
    assert len(fractal.cluster_radius()[1]) == 89
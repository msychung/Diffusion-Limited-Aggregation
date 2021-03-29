from dla_prototype import Particle, Application
import pytest

@pytest.fixture
def particle():
    x, y = 5, 10
    return Particle(x, y)

@pytest.fixture
def application():
    n = 100
    seed_shape = 'line'
    spawn_shape = 'square'
    padSize = 70
    crystal_size_limit = 100
    return Application(n, seed_shape, spawn_shape, padSize, crystal_size_limit)

def test_particle_init(particle):
    assert particle.x == 5
    assert particle.y == 10

def test_particle_update(particle):
    particle.update(1, 2)
    assert particle.x == 1
    assert particle.y == 2

def test_application_init(application):
    assert application.size == (800, 600)
    assert application.width == 800
    assert application.height == 600
    assert application.crystalColor == 0xDCDCDC
    assert application.n == 100
    assert application.seed_shape == 'line'
    assert application.spawn_shape == 'square'
    assert application.start_x == 400
    assert application.start_y == 300
    assert application.padSize == 70
    assert application.sqdomainMin_x == 330
    assert application.sqdomainMax_x == 470
    assert application.sqdomainMin_y == 230
    assert application.sqdomainMax_y == 370
    assert application.radius == 70
    assert application.crystal_size_limit == 100
    assert len(application.all_particles) == 100
    assert application.crystal_position == []
    assert application.min_x == 400
    assert application.max_x == 400
    assert application.min_y == 300
    assert application.max_y == 300

def test_applicaiton_square_spawn(application):
    assert isinstance(application.square_spawn()[0], int)
    assert isinstance(application.square_spawn()[1], int)

def test_applicaiton_circle_spawn(application):
    assert isinstance(application.circle_spawn()[0], int)
    assert isinstance(application.circle_spawn()[1], int)

def test_gen_seed(application):
    with pytest.raises(Exception):
        application.gen_seed('test')

@pytest.mark.parametrize('new_x, new_y, expected_x, expected_y', [
    (230, 120, 470, 370),
    (300, 50, 470, 370),
    (420, 160, 420, 370),
    (270, 300, 470, 300)
])

def test_wrap_around_square(application, particle, new_x, new_y, expected_x, expected_y):
    assert application.wrap_around(particle, new_x, new_y) == (expected_x, expected_y) # Needs to be extended to circle shape too...

def test_wrap_around_circle(application, particle):
    application.spawn_shape = 'circle'
    assert application.wrap_around(particle, 100, 150) == (-5, -10)
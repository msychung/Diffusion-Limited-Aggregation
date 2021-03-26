from dla_prototype import Particle, Application
import pytest

@pytest.fixture
def particle_square():
    spawn_shape = 'square'
    sqdomainMin_x = 30 
    sqdomainMax_x = 100
    sqdomainMin_y = 40
    sqdomainMax_y = 110
    start_x = 400
    start_y = 300
    radius = 50
    return Particle(spawn_shape, sqdomainMin_x, sqdomainMax_x, sqdomainMin_y, sqdomainMax_y, start_x, start_y, radius)

@pytest.fixture
def particle_circle():
    spawn_shape = 'circle'
    sqdomainMin_x = 30 
    sqdomainMax_x = 100
    sqdomainMin_y = 40
    sqdomainMax_y = 110
    start_x = 400
    start_y = 300
    radius = 50
    return Particle(spawn_shape, sqdomainMin_x, sqdomainMax_x, sqdomainMin_y, sqdomainMax_y, start_x, start_y, radius)


def test_particle_init(particle_square, particle_circle):
    assert particle_square.spawn_shape == particle_square.square_spawn
    assert particle_circle.spawn_shape == particle_circle.circle_spawn

    with pytest.raises(Exception):
        Particle('hexagon', 1, 1, 1, 1, 1, 1, 1)

def test_particle_square_spawn():
    pass

def test_particle_circle_spawn():
    pass



@pytest.fixture
def application():
    n = 100
    seed_shape = 'line'
    spawn_shape = 'circle'
    domain_shape = 'circle'
    padSize = 70
    radius = 50
    crystal_size_limit = 100
    return Application(n, seed_shape, spawn_shape, domain_shape, padSize, radius, crystal_size_limit)


def test_application_init(application):
    assert application.displaySurface == None
    assert application.size == (640, 360)
    assert application.width == 640
    assert application.height == 360
    assert application.pixelArray == None
    assert application.crystalColor == 0xDCDCDC
    assert application.n == 100
    assert application.seed_shape == 'line'
    assert application.spawn_shape == 'circle'
    assert application.domain_shape == 'circle'
    assert application.start_x == 320
    assert application.start_y == 180
    assert application.updateFlag == False
    assert application.padSize == 70
    assert application.sqdomainMin_x == 250
    assert application.sqdomainMax_x == 390
    assert application.sqdomainMin_y == 110
    assert application.sqdomainMax_y == 250
    assert application.radius == 50
    assert application.crystal_size_limit == 100
    assert len(application.all_particles) == 100
    assert application.crystal_position == []
    assert application.min_x == 320
    assert application.max_x == 320
    assert application.min_y == 180
    assert application.max_y == 180

    

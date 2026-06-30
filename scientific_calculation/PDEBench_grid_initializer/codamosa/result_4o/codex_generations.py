

# Generated at 2026-05-13 10:57:51.501403
# Unit test for function gaussian_initial_condition
def test_gaussian_initial_condition():x, y = make_uniform_grid(100, 100, length_x=1.0, length_y=1.0)

# Generated at 2026-05-13 10:58:01.332295
# Unit test for function make_uniform_grid
def test_make_uniform_grid():# Test for correct grid dimensions
    x, y = make_uniform_grid(5, 4, length_x=2.0, length_y=1.0)
    assert x.shape == (5, 4)
    assert y.shape == (5, 4)

    # Test for correct grid values
    assert np.allclose(x[:, 0], np.linspace(0.0, 2.0, 5))
    assert np.allclose(y[0, :], np.linspace(0.0, 1.0, 4))

    # Test for include_endpoint=False
    x, y = make_uniform_grid(5, 4, length_x=2.0, length_y=1.0, include_endpoint=False)
    assert np.allclose(x[:, 0], np.linspace(0.0, 2.0, 5, endpoint=False))

# Generated at 2026-05-13 10:58:05.785732
# Unit test for function gaussian_initial_condition
def test_gaussian_initial_condition():x, y = make_uniform_grid(100, 100, length_x=1.0, length_y=1.0)

# Generated at 2026-05-13 10:58:11.159529
# Unit test for function gaussian_initial_condition
def test_gaussian_initial_condition():x, y = make_uniform_grid(10, 10)

# Generated at 2026-05-13 10:58:14.496186
# Unit test for function make_uniform_grid
def test_make_uniform_grid():# Test valid grid creation
    x, y = make_uniform_grid(4, 3, length_x=2.0, length_y=1.0)
    assert x.shape == (4, 3)
    assert y.shape == (4, 3)
    assert np.allclose(x[:, 0], np.linspace(0.0, 2.0, 4))
    assert np.allclose(y[0, :], np.linspace(0.0, 1.0, 3))

    # Test with include_endpoint=False
    x, y = make_uniform_grid(4, 3, length_x=2.0, length_y=1.0, include_endpoint=False)
    assert np.allclose(x[:, 0], np.linspace(0.0, 2.0, 4, endpoint=False))

# Generated at 2026-05-13 10:58:17.276389
# Unit test for function gaussian_initial_condition
def test_gaussian_initial_condition():x, y = make_uniform_grid(10, 10)

# Generated at 2026-05-13 10:58:23.716520
# Unit test for function gaussian_initial_condition
def test_gaussian_initial_condition():x, y = make_uniform_grid(50, 50)

# Generated at 2026-05-13 10:58:46.104053
# Unit test for function make_uniform_grid

# Generated at 2026-05-13 10:58:50.952314
# Unit test for function gaussian_initial_condition
def test_gaussian_initial_condition():x, y = make_uniform_grid(10, 10)

# Generated at 2026-05-13 10:59:09.566488
# Unit test for function make_uniform_grid
def test_make_uniform_grid():# Test valid grid creation
    x, y = make_uniform_grid(4, 3, length_x=2.0, length_y=1.0)
    assert x.shape == (4, 3)
    assert y.shape == (4, 3)
    assert np.allclose(x[:, 0], np.linspace(0.0, 2.0, 4))
    assert np.allclose(y[0, :], np.linspace(0.0, 1.0, 3))

    # Test grid with include_endpoint=False
    x, y = make_uniform_grid(4, 3, length_x=2.0, length_y=1.0, include_endpoint=False)
    assert np.allclose(x[:, 0], np.linspace(0.0, 2.0, 4, endpoint=False))
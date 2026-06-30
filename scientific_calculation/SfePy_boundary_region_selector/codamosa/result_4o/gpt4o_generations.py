

# Generated at 2026-05-13 12:08:51.244730
# Unit test for function select_boundary_nodes
def test_select_boundary_nodes():points = np.array([[0.0, 1.0], [1.0, 0.0], [2.0, 2.0], [3.0, 1.0]])
assert np.array_equal(select_boundary_nodes(points, axis=0, value=0.0), np.array([True, False, False, False]))
assert np.array_equal(select_boundary_nodes(points, axis=1, value=1.0), np.array([True, False, False, True]))
assert np.array_equal(select_boundary_nodes(points, axis=0, value=2.0), np.array([False, False, True, False]))
assert np.array_equal(select_boundary_nodes(points, axis=1, value=0.0, tolerance=1e-8), np.array([False, True, False, False]))

# Generated at 2026-05-13 12:08:58.408741
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:09:03.072846
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:09:07.752971
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:09:11.031863
# Unit test for function select_boundary_nodes
def test_select_boundary_nodes():points = np.array([[0.0, 1.0], [1.0, 0.0], [2.0, 2.0], [3.0, 1.0]])
assert np.array_equal(select_boundary_nodes(points, axis=0, value=0.0), np.array([True, False, False, False]))
assert np.array_equal(select_boundary_nodes(points, axis=1, value=1.0), np.array([True, False, False, True]))
assert np.array_equal(select_boundary_nodes(points, axis=0, value=2.0), np.array([False, False, True, False]))

# Generated at 2026-05-13 12:09:16.784284
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:09:22.169245
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:09:29.955336
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:09:43.282401
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:09:48.868413
# Unit test for function select_boundary_nodes
def test_select_boundary_nodes():points = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 0.5], [1.0, 1.0], [0.0, 1.0]])
assert np.array_equal(select_boundary_nodes(points, axis=0, value=0.0), np.array([True, False, False, False, True]))
assert np.array_equal(select_boundary_nodes(points, axis=0, value=1.0), np.array([False, True, False, True, False]))
assert np.array_equal(select_boundary_nodes(points, axis=1, value=0.0), np.array([True, True, False, False, False]))
assert np.array_equal(select_boundary_nodes(points, axis=1, value=1.0), np.array([False, False, False, True, True]))

# Generated at 2026-05-13 12:10:01.511063
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:10:08.881733
# Unit test for function select_boundary_nodes

# Generated at 2026-05-13 12:10:14.753735
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:10:19.322390
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:10:23.574448
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:10:27.477952
# Unit test for function select_boundary_nodes

# Generated at 2026-05-13 12:10:31.611445
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:10:36.773443
# Unit test for function classify_boundary

# Generated at 2026-05-13 12:10:41.558697
# Unit test for function classify_boundary
def test_classify_boundary():points = [
        [0.0, 0.5],
        [1.0, 0.5],
        [0.5, 0.0],
        [0.5, 1.0],
        [0.5, 0.5]
    ]
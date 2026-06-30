

# Generated at 2026-05-16 15:30:24.224709
# Unit test for function power_method
def test_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:30:29.969877
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [1, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 1]) / np.sqrt(2)
eigenvalue, eigenvector = inverse_power_method(A)
assert np.isclose(eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:30:32.943451
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [1, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 1]) / np.sqrt(2)
eigenvalue, eigenvector = inverse_power_method(A)
assert np.isclose(eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:30:36.540004
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [1, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 1]) / np.sqrt(2)
eigenvalue, eigenvector = inverse_power_method(A)
assert np.isclose(eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:30:40.188975
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [1, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 1]) / np.sqrt(2)
eigenvalue, eigenvector = inverse_power_method(A)
assert np.isclose(eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:30:43.989346
# Unit test for function power_method
def test_power_method():A = np.array([[4, 1], [2, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 1]) / np.linalg.norm([1, 1])
eigenvalue, eigenvector = power_method(A)
assert np.isclose(eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:30:46.465292
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:30:48.477209
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:30:49.924800
# Unit test for function power_method
def test_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:30:51.406078
# Unit test for function __iterate
def test___iterate():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:31:15.153748
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [2, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 2]) / np.linalg.norm([1, 2])
computed_eigenvalue, computed_eigenvector = inverse_power_method(A)
assert np.isclose(computed_eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(computed_eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:31:17.301623
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:31:24.868638
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [2, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 1]) / np.sqrt(2)
eigenvalue, eigenvector = inverse_power_method(A)
assert np.isclose(eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:31:26.970739
# Unit test for function power_method
def test_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:31:28.946032
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:31:31.182847
# Unit test for function power_method
def test_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:31:34.543794
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [2, 3]])

# Generated at 2026-05-16 15:31:39.533793
# Unit test for function inverse_power_method
def test_inverse_power_method():A = np.array([[4, 1], [2, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 2]) / np.linalg.norm([1, 2])
computed_eigenvalue, computed_eigenvector = inverse_power_method(A)
assert np.isclose(computed_eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(computed_eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:31:48.752191
# Unit test for function power_method
def test_power_method():A = np.array([[4, 1], [2, 3]])
expected_eigenvalue = 5.0
expected_eigenvector = np.array([1, 1]) / np.linalg.norm([1, 1])
eigenvalue, eigenvector = power_method(A)
assert np.isclose(eigenvalue, expected_eigenvalue, rtol=1e-5)
assert np.allclose(np.abs(eigenvector), np.abs(expected_eigenvector), rtol=1e-5)

# Generated at 2026-05-16 15:31:51.587753
# Unit test for function power_method
def test_power_method():A = np.array([[4, 1], [2, 3]])
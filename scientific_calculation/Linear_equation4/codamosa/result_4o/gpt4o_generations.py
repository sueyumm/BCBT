

# Generated at 2026-05-16 16:04:52.841245
# Unit test for function jakobi
def test_jakobi():A = np.array([[4.0, 1.0, 2.0],
              [3.0, 5.0, 1.0],
              [1.0, 1.0, 3.0]])
b = np.array([4.0,7.0,3.0])
expected_result = np.linalg.solve(A, b)
result = jakobi(A, b, 25)
assert np.allclose(result, expected_result, rtol=1e-2)

# Generated at 2026-05-16 16:04:56.806186
# Unit test for function jakobi
def test_jakobi():A = np.array([[4.0, 1.0, 2.0],
              [3.0, 5.0, 1.0],
              [1.0, 1.0, 3.0]])
b = np.array([4.0,7.0,3.0])
expected_result = np.linalg.solve(A, b)
result = jakobi(A, b, 25)
assert np.allclose(result, expected_result, rtol=1e-2)

# Generated at 2026-05-16 16:05:00.500198
# Unit test for function jakobi
def test_jakobi():A = np.array([[4.0, 1.0, 2.0],
              [3.0, 5.0, 1.0],
              [1.0, 1.0, 3.0]])
b = np.array([4.0,7.0,3.0])
expected_result = np.linalg.solve(A, b)
result = jakobi(A, b, 25)
assert np.allclose(result, expected_result, rtol=1e-2)
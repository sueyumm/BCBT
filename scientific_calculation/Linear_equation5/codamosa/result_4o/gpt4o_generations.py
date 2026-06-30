

# Generated at 2026-05-16 16:05:15.628182
# Unit test for function back_subsitute
def test_back_subsitute():U = np.array([[2, 1], [0, 3]], dtype=float)

# Generated at 2026-05-16 16:05:22.359166
# Unit test for function back_subsitute
def test_back_subsitute():U = np.array([[2, 1], [0, 3]], dtype=float)

# Generated at 2026-05-16 16:05:26.824596
# Unit test for function back_subsitute
def test_back_subsitute():U = np.array([[2, 1], [0, 3]], dtype=float)

# Generated at 2026-05-16 16:05:34.122784
# Unit test for function back_subsitute
def test_back_subsitute():U = np.array([[2, 1, -1],
                  [0, 3, 2],
                  [0, 0, 1]], dtype=float)

# Generated at 2026-05-16 16:05:38.623347
# Unit test for function back_subsitute
def test_back_subsitute():U = np.array([[2, 1, -1],
                  [0, 3, 2],
                  [0, 0, 1]], dtype=float)

# Generated at 2026-05-16 16:05:43.461185
# Unit test for function back_subsitute
def test_back_subsitute():U = np.array([[2, 1, -1],
                  [0, 3, 2],
                  [0, 0, 1]], dtype=float)

# Generated at 2026-05-16 16:05:46.468569
# Unit test for function back_subsitute
def test_back_subsitute():U = np.array([[2, 1], [0, 3]], dtype=float)

# Generated at 2026-05-16 16:05:54.563188
# Unit test for function gauss
def test_gauss():A = np.array([[2.0, 1.0], [5.0, 7.0]])
b = np.array([11.0, 13.0])
n = 2
A_expected = np.array([[2.0, 1.0], [0.0, 2.0]])
b_expected = np.array([11.0, 3.0])
A_result, b_result = gauss(A.copy(), b.copy(), n)
assert np.allclose(A_result, A_expected)
assert np.allclose(b_result, b_expected)

# Generated at 2026-05-16 16:05:59.975172
# Unit test for function gauss
def test_gauss():A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([1.0, 2.0])
n = 2
A_expected = np.array([[2.0, 1.0], [0.0, 2.5]])
b_expected = np.array([1.0, 1.5])
A_result, b_result = gauss(A.copy(), b.copy(), n)
assert np.allclose(A_result, A_expected)
assert np.allclose(b_result, b_expected)

# Generated at 2026-05-16 16:06:03.347198
# Unit test for function back_subsitute
def test_back_subsitute():U = np.array([[2, -1, 0], [0, 1, -1], [0, 0, 3]], dtype=float)
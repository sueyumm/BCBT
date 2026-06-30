

# Generated at 2026-05-16 16:04:12.173820
# Unit test for function lu_decomposition_doolittle
def test_lu_decomposition_doolittle():A = array([[2., 1., 1.], [4., 3., 3.], [8., 7., 9.]])
b = array([4., 10., 22.])
x = lu_decomposition_doolittle(A, b)
assert allclose(dot(A, x), b)

# Generated at 2026-05-16 16:04:14.716388
# Unit test for function lu_decomposition_doolittle
def test_lu_decomposition_doolittle():A = array([[2., 1.], [4., 3.]])
b = array([1., 2.])
x = lu_decomposition_doolittle(A, b)
assert_allclose(dot(A, x), b)
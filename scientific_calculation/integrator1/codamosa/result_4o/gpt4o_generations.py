

# Generated at 2026-04-27 09:56:52.303269
# Unit test for function torus
def test_torus():assert torus(3, 0, 0) == True

# Generated at 2026-04-27 09:57:06.212470
# Unit test for function gauss_leg
def test_gauss_leg():a, b, N = 0, 1, 5

# Generated at 2026-04-27 09:57:22.580548
# Unit test for function gauss_leg
def test_gauss_leg():a, b, N = 0, 1, 5

# Generated at 2026-04-27 09:57:34.836482
# Unit test for function sphere
def test_sphere():assert sphere(0, 0, 0) == True

# Generated at 2026-04-27 09:57:43.286438
# Unit test for function gauss_leg
def test_gauss_leg():a, b, N = 0, 1, 5

# Generated at 2026-04-27 09:57:58.428638
# Unit test for function gauss_leg
def test_gauss_leg():a, b, N = 0, 1, 5

# Generated at 2026-04-27 09:58:15.186141
# Unit test for function torus
def test_torus():assert torus(3, 0, 0) == True

# Generated at 2026-04-27 09:58:28.597982
# Unit test for function monte_carlo_3d
def test_monte_carlo_3d():a = [0, 0, 0]

# Generated at 2026-04-27 09:58:35.282503
# Unit test for function torus
def test_torus():assert torus(3, 0, 0) == True

# Generated at 2026-04-27 09:58:55.536551
# Unit test for function torus
def test_torus():assert torus(3, 0, 0) == True

# Generated at 2026-05-16 17:45:44.532584
# Unit test for function trap
def test_trap():assert abs(trap(lin, 0, 1, 100) - 0.5) < 1e-4

# Generated at 2026-05-16 17:45:46.811298
# Unit test for function gauss_leg
def test_gauss_leg():x, w = gauss_leg(0, 1, 3)
result = gauss_quad(lambda t: t**2, x, w)
expected = 1/3
assert abs(result - expected) < 1e-6, f"Expected {expected}, got {result}"

# Generated at 2026-05-16 17:45:51.295961
# Unit test for function legendre

# Generated at 2026-05-16 17:45:55.544626
# Unit test for function monte_carlo_3d
def test_monte_carlo_3d():a = [0, 0, 0]

# Generated at 2026-05-16 17:45:58.455553
# Unit test for function monte_carlo_1d
def test_monte_carlo_1d():result = monte_carlo_1d(lambda x: x, 0, 1, 10000)  # 136

# Generated at 2026-05-16 17:46:03.376131
# Unit test for function torus


# Generated at 2026-05-13 09:04:09.770649
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5, 0, 1) == 0.5

# Generated at 2026-05-13 09:04:15.578396
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5) == 0.5

# Generated at 2026-05-13 09:04:49.521428
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5, 0, 1) == 0.5

# Generated at 2026-05-13 09:04:54.573805
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5) == 0.5

# Generated at 2026-05-13 09:04:59.146816
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5) == 0.5

# Generated at 2026-05-13 09:05:19.456478
# Unit test for function normalize_color_value
def test_normalize_color_value():# Test case 1: Normal case within range
    assert normalize_color_value(0.5, 0.0, 1.0) == 0.5

    # Test case 2: Value below range with clipping
    assert normalize_color_value(-0.5, 0.0, 1.0, clip=True) == 0.0

    # Test case 3: Value above range with clipping
    assert normalize_color_value(1.5, 0.0, 1.0, clip=True) == 1.0

    # Test case 4: Value below range without clipping
    assert normalize_color_value(-0.5, 0.0, 1.0, clip=False) == -0.5

    # Test case 5: Value above range without clipping

# Generated at 2026-05-13 09:05:24.142217
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5) == 0.5

# Generated at 2026-05-13 09:05:28.677010
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5, 0, 1) == 0.5

# Generated at 2026-05-13 09:05:32.915550
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5) == 0.5

# Generated at 2026-05-13 09:05:37.245540
# Unit test for function normalize_color_value
def test_normalize_color_value():assert normalize_color_value(0.5, 0, 1) == 0.5
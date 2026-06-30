

# Generated at 2026-05-13 11:55:19.529451
# Unit test for function contact_force
def test_contact_force():# Test case 1: No gap, no friction
    assert contact_force(0, 1000) == 0.0

    # Test case 2: Positive gap, no friction
    assert contact_force(1, 1000) == 0.0

    # Test case 3: Negative gap, no friction
    assert contact_force(-1, 1000) == 1000.0

    # Test case 4: Negative gap, with friction
    assert contact_force(-1, 1000, 0.5) == 1500.0

    # Test case 5: Negative gap, friction capped at 1.0
    assert contact_force(-1, 1000, 2.0) == 2000.0

    # Test case 6: Invalid negative stiffness

# Generated at 2026-05-13 11:55:24.267621
# Unit test for function contact_force
def test_contact_force():assert contact_force(1.0, 100.0) == 0.0

# Generated at 2026-05-13 11:55:29.350529
# Unit test for function contact_force
def test_contact_force():assert contact_force(1.0, 100.0) == 0.0

# Generated at 2026-05-13 11:55:33.424830
# Unit test for function contact_force
def test_contact_force():assert contact_force(1, 100) == 0.0
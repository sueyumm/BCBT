

# Generated at 2026-05-13 09:06:03.828441
# Unit test for function interval_relation
def test_interval_relation():assert interval_relation(1, 5, 6, 10) == "disjoint"

# Generated at 2026-05-13 09:06:09.273919
# Unit test for function interval_relation
def test_interval_relation():assert interval_relation(1, 5, 6, 10) == "disjoint"

# Generated at 2026-05-13 09:06:23.641071
# Unit test for function interval_relation

# Generated at 2026-05-13 09:06:29.425032
# Unit test for function interval_relation

# Generated at 2026-05-13 09:06:33.858388
# Unit test for function interval_relation

# Generated at 2026-05-13 09:06:37.565383
# Unit test for function interval_relation

# Generated at 2026-05-13 09:06:44.297765
# Unit test for function interval_relation
def test_interval_relation():assert interval_relation(1, 5, 6, 10) == "disjoint"

# Generated at 2026-05-13 09:06:49.739802
# Unit test for function interval_relation

# Generated at 2026-05-13 09:06:54.531866
# Unit test for function interval_relation

# Generated at 2026-05-13 09:06:58.662107
# Unit test for function interval_relation
def test_interval_relation():# Test for equal intervals
    assert interval_relation(1, 5, 1, 5) == "equal"
    assert interval_relation(1, 5, 1, 5, closed=False) == "equal"

    # Test for disjoint intervals
    assert interval_relation(1, 3, 4, 6) == "disjoint"
    assert interval_relation(1, 3, 3, 6, closed=False) == "disjoint"

    # Test for contains
    assert interval_relation(1, 5, 2, 4) == "contains"
    assert interval_relation(1, 5, 2, 4, closed=False) == "contains"

    # Test for inside
    assert interval_relation(2, 4, 1, 5) == "inside"
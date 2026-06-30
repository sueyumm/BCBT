

# Generated at 2026-05-13 11:55:50.448732
# Unit test for function dof_category
def test_dof_category():# Test case 1: Node and component are positive, and key is in constrained
    assert dof_category(1, 0, {(1, 0)}) == "fixed"

    # Test case 2: Node and component are positive, and key is not in constrained, component == 0
    assert dof_category(2, 0, {}) == "x-free"

    # Test case 3: Node and component are positive, and key is not in constrained, component == 1
    assert dof_category(3, 1, {}) == "y-free"

    # Test case 4: Node and component are positive, and key is not in constrained, component > 1
    assert dof_category(4, 2, {}) == "extra"

    # Test case 5: Node is negative

# Generated at 2026-05-13 11:55:53.665295
# Unit test for function dof_category
def test_dof_category():# Test case 1: Node and component are positive, and key is in constrained
    assert dof_category(1, 0, {(1, 0)}) == "fixed"
    
    # Test case 2: Node and component are positive, component is 0, and key is not in constrained
    assert dof_category(2, 0, {}) == "x-free"
    
    # Test case 3: Node and component are positive, component is 1, and key is not in constrained
    assert dof_category(3, 1, {}) == "y-free"
    
    # Test case 4: Node and component are positive, component is neither 0 nor 1, and key is not in constrained
    assert dof_category(4, 2, {}) == "extra"
    
    # Test case 5: Node is negative

# Generated at 2026-05-13 11:55:56.440235
# Unit test for function dof_category
def test_dof_category():assert dof_category(1, 0, {(1, 0)}) == "fixed"

# Generated at 2026-05-13 11:56:05.867601
# Unit test for function dof_category
def test_dof_category():assert dof_category(1, 0, {(1, 0)}) == "fixed"

# Generated at 2026-05-13 11:56:12.238002
# Unit test for function dof_category
def test_dof_category():# Test for fixed DOF
    assert dof_category(1, 0, {(1, 0)}) == "fixed"
    assert dof_category(2, 1, {(2, 1)}) == "fixed"

    # Test for x-free DOF
    assert dof_category(1, 0, {}) == "x-free"

    # Test for y-free DOF
    assert dof_category(1, 1, {}) == "y-free"

    # Test for extra DOF
    assert dof_category(1, 2, {}) == "extra"

    # Test for negative index
    try:
        dof_category(-1, 0, {})
    except ValueError as e:
        assert str(e) == "negative index"

    try:
        dof_category(1, -1, {})
    except ValueError as e:
        assert str(e) == "negative index"

# Generated at 2026-05-13 11:56:15.767579
# Unit test for function dof_category
def test_dof_category():constrained = {(1, 0), (2, 1)}

# Generated at 2026-05-13 11:56:21.821104
# Unit test for function dof_category
def test_dof_category():# Test case 1: Node and component are positive, and key is in constrained
    assert dof_category(1, 0, {(1, 0)}) == "fixed"
    
    # Test case 2: Node and component are positive, component is 0, and key is not in constrained
    assert dof_category(2, 0, {}) == "x-free"
    
    # Test case 3: Node and component are positive, component is 1, and key is not in constrained
    assert dof_category(3, 1, {}) == "y-free"
    
    # Test case 4: Node and component are positive, component is neither 0 nor 1, and key is not in constrained
    assert dof_category(4, 2, {}) == "extra"
    
    # Test case 5: Node is negative

# Generated at 2026-05-13 11:56:27.563882
# Unit test for function dof_category
def test_dof_category():constrained = {(1, 0), (2, 1)}

# Generated at 2026-05-13 11:56:33.018478
# Unit test for function dof_category
def test_dof_category():assert dof_category(1, 0, {(1, 0)}) == "fixed"

# Generated at 2026-05-13 11:56:36.678705
# Unit test for function dof_category
def test_dof_category():constrained = {(1, 0), (2, 1)}
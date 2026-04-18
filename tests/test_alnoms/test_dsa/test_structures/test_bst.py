from alnoms.dsa.structures import BinarySearchTree


def test_bst_put_get_delete():
    bst = BinarySearchTree()
    bst.put("a", 1)
    bst.put("b", 2)
    assert bst.get("a") == 1
    assert bst.contains("b")
    bst.delete("a")
    assert not bst.contains("a")
    assert sorted(bst.keys()) == ["b"]

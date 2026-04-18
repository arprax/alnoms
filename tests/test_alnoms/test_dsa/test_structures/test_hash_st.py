from alnoms.dsa.structures import SeparateChainingHashST


def test_separate_chaining_hash_basic_ops():
    st = SeparateChainingHashST(m=5)
    st.put("a", 1)
    st.put("b", 2)
    assert st.get("a") == 1
    assert st.contains("b")
    st.delete("a")
    assert not st.contains("a")
    keys = st.keys()
    assert "b" in keys

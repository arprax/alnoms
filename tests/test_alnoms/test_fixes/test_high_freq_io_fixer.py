from alnoms.fixes.high_freq_io_fixer import HighFrequencyIOFixer


def test_high_freq_io_fixer_explain():
    f = HighFrequencyIOFixer()
    msg = f.explain({})
    assert "i/o" in msg.lower() or "write" in msg.lower()


def test_high_freq_io_fixer_snippets():
    f = HighFrequencyIOFixer()
    s = f.snippet_before_after({})
    assert "buffer" in s["after"].lower()

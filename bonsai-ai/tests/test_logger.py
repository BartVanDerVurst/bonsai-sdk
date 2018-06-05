from bonsai_ai.logger import Logger


def test_included_domain(capsys, logging_config):
    log = Logger()
    log.foo('bar')
    log.baz('qux')
    out, err = capsys.readouterr()
    assert out == ''
    assert err.find('[foo] bar\n') >= 0
    assert err.find('[baz] qux\n') >= 0


def test_excluded_domain(capsys, logging_config):
    log = Logger()
    log.spam('eggs')
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


def test_enable_all(capsys, logging_config):
    log = Logger()
    log.set_enable_all(True)
    log.spam('eggs')
    out, err = capsys.readouterr()
    assert out == ''
    assert err.find("[spam] eggs\n") >= 0
    log.set_enable_all(False)

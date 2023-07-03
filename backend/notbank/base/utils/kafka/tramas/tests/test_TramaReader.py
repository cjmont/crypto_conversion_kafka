from notbank.base.utils.kafka.tramas.trama_reader import TramaReader

trama = 'hello     world  !'


def test_trama_reader_normal_read():
    trama_reader = TramaReader(trama)
    hello = trama_reader.read(5)
    assert hello == 'hello'
    world = trama_reader.read(10)
    assert world == 'world'
    exclamation = trama_reader.read(3)
    assert exclamation == '!'
    assert trama_reader.is_done()


def test_trama_reader_back_read():
    trama_reader = TramaReader(trama)
    exclamation = trama_reader.read_from_back(3)
    assert exclamation == '!'
    world = trama_reader.read_from_back(10)
    assert world == 'world'
    hello = trama_reader.read_from_back(5)
    assert hello == 'hello'
    assert trama_reader.is_done()


def test_trama_reader_read_both_sides():
    trama_reader = TramaReader(trama)
    exclamation = trama_reader.read_from_back(3)
    assert exclamation == '!'
    hello = trama_reader.read(5)
    assert hello == 'hello'
    padded_world = trama_reader.get_unread()
    assert padded_world == '     world'
    assert not trama_reader.is_done()

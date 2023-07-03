from notbank.base.utils.kafka.tramas.exceptions import TramaException
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


def test_trama_writer_correct_write():
    data = [
        ('hello', 5),
        ('world', 10),
        ('!', 3),
    ]
    trama = TramaWriter.write(data)
    assert trama == 'hello     world  !'


def test_trama_writer_wrong_data():
    data = [
        ('hello', 3),
        ('world', 10),
        ('!', 3),
    ]
    try:
        TramaWriter.write(data)
        assert False
    except TramaException:
        assert True

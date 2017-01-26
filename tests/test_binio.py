from datetime import datetime

def test_open():
    from drs4.binio import DRS4BinaryFile

    with DRS4BinaryFile('tests/test.dat') as f:
        pass


def test_file_header():
    from drs4.binio import DRS4BinaryFile

    with DRS4BinaryFile('tests/test.dat') as f:

        assert len(f.board_ids) == 1
        assert list(f.time_widths[f.board_ids[0]].keys()) == [1, ]

def test_read_first_event():

    from drs4.binio import DRS4BinaryFile

    with DRS4BinaryFile('tests/test.dat') as f:

        event = next(f)

        assert event.event_id == 1


def test_read_all():

    from drs4.binio import DRS4BinaryFile

    with DRS4BinaryFile('tests/test.dat') as f:

        events = [e for e in f]

    assert len(events) == 1000

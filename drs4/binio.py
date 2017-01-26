import numpy as np
import struct
from collections import namedtuple
from io import BufferedReader, FileIO
from datetime import datetime


Event = namedtuple(
    'Event',
    [
        'event_id',
        'timestamp',
        'range_center',
        'adc_data',
        'scalers',
        'trigger_cells',
    ]
)



class DRS4BinaryFile(BufferedReader):

    def __init__(self, filename):
        super().__init__(FileIO(filename, 'rb'))

        assert self.read(4) == b'DRS2', 'File does not seem to be a DRS4 binary file'
        assert self.read(4) == b'TIME', 'File does not contain TIME header'

        self.board_ids = []
        self.time_widths = {}
        self.channels = {}

        header = self.read(4)
        while header.startswith(b'B#'):
            board_id, = struct.unpack('H', header[2:])
            self.board_ids.append(board_id)
            self.time_widths[board_id] = {}
            self.channels[board_id] = []

            header = self.read(4)
            while header.startswith(b'C'):
                channel = int(header[1:].decode())
                self.channels[board_id].append(channel)

                self.time_widths[board_id][channel] =  self._read_timewidth_array()

                header = self.read(4)

        self.num_boards = len(self.board_ids)

        self.seek(-4, 1)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            header = self.read(4)
        except IOError:
            raise StopIteration

        if header != b'EHDR':
            raise StopIteration

        event_id, = struct.unpack('I', self.read(4))
        year, month, day, hour, minute, second, ms = struct.unpack(
            '7H', self.read(struct.calcsize('7H'))
        )
        timestamp = datetime(year, month, day, hour, minute, second, ms * 1000)
        range_center, = struct.unpack('H', self.read(2))

        scalers = {}
        trigger_cells = {}
        adc_data = {}

        for board_id, channels in self.channels.items():
            assert self.read(2) == b'B#'
            assert struct.unpack('H', self.read(2))[0] == board_id

            assert self.read(2) == b'T#'
            trigger_cells[board_id], = struct.unpack('H', self.read(2))

            scalers[board_id] = {}
            adc_data[board_id] = {}

            for channel in channels:
                assert self.read(4) == 'C{:03d}'.format(channel).encode('ascii')

                scalers[board_id][channel], = struct.unpack('I', self.read(4))
                adc_data[board_id][channel] = self._read_adc_data()

        return Event(
            event_id=event_id,
            timestamp=timestamp,
            range_center=range_center,
            adc_data=adc_data,
            scalers=scalers,
            trigger_cells=trigger_cells,
        )

    def _read_timewidth_array(self):
        return np.frombuffer(self.read(1024 * 4), 'float32')

    def _read_adc_data(self):
        return np.frombuffer(self.read(1024 * 2), 'uint16')



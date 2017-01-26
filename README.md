# pydrs4

Python package for the drs4 evaluation board


### Reading binary files of the drs4 evaluation board software

Each event contains a dictinory `adc_data`, mapping to the data like this:
board_id → channel_id → data.

to the adc data of the corresponding channel.
```python
import matplotlib.pyplot as plt
from drs4 import DRS4BinaryFile

with DRS4BinaryFile('path/to/binaryfile') as f:
    
    print(f.board_ids)
    print(f.channels)

    event = next(f)
    print(event.event_id)
    print(event.timestamp)

    plt.plot(event.adc_data[1157][1])
    plt.show()
  
```

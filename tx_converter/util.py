import dataclasses, csv
from io import FileIO
from typing import List, Optional, Type
from dataclasses import dataclass


def write_dataclass_csv(data: List[dataclass], f: FileIO, entry_type: Optional[Type[dataclass]]=None):
    if entry_type is None:
        entry_type = type(data[0])

    cols = [f.name for f in dataclasses.fields(entry_type)]
    writer = csv.DictWriter(f, fieldnames=cols)

    writer.writeheader()
    for entry in data:
        writer.writerow(dataclasses.asdict(entry))

import csv
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any


def to_csv(p: Path, my_dataclasses: Any) -> None:
    # TODO: エラー処理

    #  https://docs.python.org/ja/3.10/library/dataclasses.html#dataclasses.is_dataclass
    for obj in my_dataclasses:
        is_dataclass_instance = is_dataclass(obj) and (not isinstance(obj, type))
        if not is_dataclass_instance:
            raise ValueError('dataclassのインスタンスじゃないよ')

    with p.open(mode='w') as f:
        w = csv.writer(f)

        w.writerow(my_dataclasses[0].__dict__.keys())
        rows = [dataclass.__dict__.values() for dataclass in my_dataclasses]

        w.writerows(rows)

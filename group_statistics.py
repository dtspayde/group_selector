#!/usr/bin/env python3
# coding: utf-8

from pathlib import Path
from collections import Counter, OrderedDict
import json


def cli():
    file = Path("2019s1_phys235_history.txt")
    with file.open(mode='r') as f:
        dict_history = json.load(f)
    i = 0
    for k, v in dict_history.items():
        print(i, k, v.values())
        i += 1

    cnt = Counter()

    for x in dict_history.values():
        for y in x.values():
            cnt[y] += 1

    print(cnt)

    cnt_ordered = OrderedDict(sorted(cnt.items(), key=lambda x: x[0]))

    {print(k, v/2) for k, v in cnt_ordered.items()}

    for k, v in dict_history.items():
        for k_sub, v_sub in v.items():
            if v_sub >= 2:
                print(k, k_sub, v_sub)


if __name__ == "__main__":
    cli()

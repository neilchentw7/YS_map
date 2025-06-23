import csv

class DataFrame:
    def __init__(self, data=None, dtype=None, columns=None):
        if data is None:
            data = []
        if isinstance(data, dict):
            data = [data]
        self.data = [dict(row) for row in data]
        if columns:
            for row in self.data:
                for col in columns:
                    row.setdefault(col, None)
        self.columns = columns or (list(self.data[0].keys()) if self.data else [])

    def copy(self):
        return DataFrame([row.copy() for row in self.data], columns=self.columns.copy())

    @property
    def empty(self):
        return len(self.data) == 0

    def insert(self, loc, column, value):
        vals = list(value)
        for i, row in enumerate(self.data):
            row[column] = vals[i]
        if column not in self.columns:
            self.columns.insert(loc, column)

    @property
    def index(self):
        return list(range(len(self.data)))

    def drop(self, idx):
        self.data.pop(idx)
        return self

    def reset_index(self, drop=False):
        return self

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        if isinstance(item, str):
            return [row[item] for row in self.data]
        return self.data[item]


def DataFrame_from_rows(rows):
    return DataFrame(rows)


def concat(dfs, ignore_index=True):
    data = []
    for df in dfs:
        data.extend(df.data)
    return DataFrame(data)


def read_csv(path, dtype=None):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            if dtype:
                for col, func in dtype.items():
                    row[col] = func(row[col])
            rows.append(row)
    return DataFrame(rows)

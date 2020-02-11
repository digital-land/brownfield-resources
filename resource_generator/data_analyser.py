#!/usr/bin/env python3


class DataAnalyser():

    def __init__(self, data):
        super().__init__()
        self.data = data

    def row_count(self):
        return len(self.data)

    def sum_max_dwellings(self):
        return sum([x['maximum-net-dwellings'] for x in self.data])

    def sum_min_dwellings(self):
        return sum([x['minimum-net-dwellings'] for x in self.data])

    def total_hectares(self):
        return sum([x['hectares'] for x in self.data])

    def summary(self):
        return {
            "total": self.row_count(),
            "hectares": self.total_hectares(),
            "max_dwellings": self.sum_max_dwellings(),
            "min_dwellings": self.sum_min_dwellings()
        }

#!/usr/bin/env python3


class DataAnalyser():

    def __init__(self, data):
        super().__init__()
        self.data = data

    def count_pip(self):
        permission_types = [x["PermissionType"] for x in self.data]
        return permission_types.count("permission in principle")

    def row_count(self):
        return len(self.data)

    def sum_max_dwellings(self):
        return sum([x['NetDwellingsRangeTo'] for x in self.data])

    def sum_min_dwellings(self):
        return sum([x['NetDwellingsRangeFrom'] for x in self.data])

    def total_hectares(self):
        return sum([x['Hectares'] for x in self.data])

    def summary(self):
        return {
            "total": self.row_count(),
            "hectares": self.total_hectares(),
            "max_dwellings": self.sum_max_dwellings(),
            "min_dwellings": self.sum_min_dwellings(),
            "permission_in_principle": self.count_pip()
        }

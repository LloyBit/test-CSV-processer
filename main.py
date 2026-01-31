from typing import Union
from tabulate import tabulate
import argparse
import csv

def _convert_value(val: str) -> Union[str, int, float]:
    """Try converting string to int or float; return as-is on failure."""
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val

class CSVProcessor:
    """Handles CSV parsing, filtering, aggregation, and sorting."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.datalist = []
        self.parse_csv()
        self.func_name_dict = {"min": min, "max": max, "avg": self.avg}

    def parse_csv(self) -> None:
        """Parse CSV file into datalist with type conversion (int/float where possible)."""
        with open(self.file_path, "r", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.datalist.append([_convert_value(v) for v in row])

    def filter(self, column: str, value: Union[str, int, float], data: list = None) -> list:
        """Filter rows by column=value. Uses data if provided, else self.datalist."""
        source = data if data is not None else self.datalist
        col_idx = source[0].index(column)
        return [source[0]] + [r for r in source[1:] if r[col_idx] == value]

    def aggregate(
        self, column: str, agg_func: str, data: list = None
    ) -> list:
        """Aggregate column with min/max/avg. Uses data if provided."""
        source = data if data is not None else self.datalist
        col_idx = source[0].index(column)
        values = [r[col_idx] for r in source[1:] if isinstance(r[col_idx], (int, float))]
        if not values:
            return [[agg_func, None]]
        func = self.func_name_dict[agg_func]
        return [[agg_func, func(values)]]

    def sort(self, column: str, way: str, data: list = None) -> list:
        """Sort by column. way: 'asc'/'ask' or 'desc'."""
        source = data if data is not None else self.datalist
        reverse = way.lower() == "desc"
        col_idx = source[0].index(column)
        return [source[0]] + sorted(
            source[1:], key=lambda x: x[col_idx], reverse=reverse
        )

    def avg(self, lst: list) -> float:
        """Arithmetic mean of numeric list."""
        return sum(lst) / len(lst)

    def output(self, data: list = None) -> None:
        """Print data as table. Uses self.datalist if data is None."""
        target = data if data is not None else self.datalist
        print(tabulate(target, tablefmt="grid", numalign="right"))

class CLIProcessor:
    """Orchestrates CSV processing based on CLI arguments."""

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.file_path = args.file.name if hasattr(args.file, "name") else args.file

    def _parse_where(self) -> tuple:
        """Parse where arg (col=val) with type conversion."""
        parts = self.args.where.split("=", 1)
        return (_convert_value(parts[0]), _convert_value(parts[1]))

    def run(self) -> None:
        """Execute workflow: filter -> order -> aggregate -> output."""
        if self.args.order_by and self.args.aggregate:
            raise ValueError("Недопустимое сочетание аргументов")

        processor = CSVProcessor(self.file_path)
        result = processor.datalist

        if self.args.where:
            col, val = self._parse_where()
            result = processor.filter(col, val, data=result)

        if self.args.order_by and not self.args.aggregate:
            col, way = self.args.order_by.split("=", 1)
            result = processor.sort(col, way, data=result)

        if self.args.aggregate:
            col, agg = self.args.aggregate.split("=", 1)
            result = processor.aggregate(col, agg, data=result)

        processor.output(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filtering and aggregation")
    parser.add_argument(
        "-f", "--file", default="test_data.csv", type=argparse.FileType("r"), help="Path to csv-file"
    )
    parser.add_argument("-w", "--where", default=False, type=str, help="Filter by column")
    parser.add_argument("-a", "--aggregate", default=False, type=str, help="Parametrize aggregation")
    parser.add_argument("-o", "--order-by", default=False, type=str, help="Asc/desc ordering")
    args = parser.parse_args()

    CLIProcessor(args).run()

from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return str(result)


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError(f"Invalid numeric data: {data}")
        return str(sum(data) if isinstance(data, list) else data)

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        return (isinstance(data, list) and
                all(isinstance(d, (int, float)) for d in data))

    def format_output(self, result: str) -> str:
        values: List[float] = []
        if result.startswith('[') and result.endswith(']'):
            values = [float(num) for num in result[1:-1].split(',')]
        elif result.isdigit():
            values = [float(result)]

        if len(values) > 1:
            n = len(values)
            total = sum(values)
            avg = total / n
            return f"processed {n} numeric values, sum={total}, avg={avg}"
        else:
            return f"processed 1 numeric value, sum={result}"


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError(f"Invalid text data: {data}")
        return str(data)

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def format_output(self, result: str) -> str:
        stats: Dict[str, int] = {
            'chars': len(result),
            'words': len(result.split())
        }
        return (f"processed text: {stats['chars']} characters, "
                f"{stats['words']} words")


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError(f"Invalid log data: {data}")
        return str(data)

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def format_output(self, result: str) -> str:
        parts: Union[List[str], None] = result.split(':', 1)
        if len(parts) != 2:
            return f"[UNKNOWN] Unknown level detected: {result}"

        level, message = parts
        level = level.strip()
        message = message.strip()

        if level == 'ERROR':
            return f"[ALERT] {level} level detected: {message}"
        else:
            return f"[{level}] {level} level detected: {message}"


def stream_processor() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print("\nInitialising numeric processor...")
    numeric_data = [1, 2, 3, 4, 5]
    np = NumericProcessor()
    print(f"Processing data: {numeric_data}")
    res = np.process(numeric_data)
    if np.validate(numeric_data):
        print("Validation: numeric data verified")
    else:
        print("Validation: problems in numeric data")
    print(f"Output: {np.format_output(str(numeric_data))}")

    text_data = "Hello Nexus World"
    tp = TextProcessor()
    print("\nInitialising text processor...")
    print(f'Processing data: "{text_data}"')
    res = tp.process(text_data)
    if tp.validate(res):
        print("Validation: text data verified")
    else:
        print("Validation: problems in text data")
    print(f"Output: {tp.format_output(res)}")

    log_data = "ERROR: connection timeout"
    lp = LogProcessor()
    print("\nInitialising log processor...")
    print(f'Processing data: "{log_data}"')
    res = lp.process(log_data)
    if lp.validate(res):
        print("Validation: log entry verified")
    else:
        print("Validation: problems in log entry")
    print(f"Output: {lp.format_output(res)}")

    processor_list = [np, tp, lp]
    print("\n=== Polymorphic processing demo ===")
    print("Processing multiple data types through same interface...")
    demo_data: Optional[List]
    demo_data = [
        [1, 2, 3],
        "System ready",
        "INFO: system ready"
    ]

    # Iterazione polimorfica sugli oggetti tramite la stessa interfaccia
    for i, (processor, data) in enumerate(zip(processor_list, demo_data), 1):
        processor.process(data)
        out = processor.format_output(str(data))
        print(f"Result {i}: {out}")

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    stream_processor()

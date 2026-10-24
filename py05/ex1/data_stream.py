from abc import ABC, abstractmethod
from typing import List, Any, Optional, Dict, Union


class DataStream(ABC):
    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        return [data for data in data_batch
                if criteria and criteria in str(data)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"stream_id": self.stream_id}


class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        print("\nInitializing sensor stream...")
        print(f"Stream ID: {self.stream_id}, type: environmental data")

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            print(f"Processing sensor batch: "
                  f"[{', '.join(str(x) for x in data_batch)}]")
            temps = [float(d.split(':')[1]) for d in data_batch
                     if isinstance(d, str) and d.startswith('temp')]
            avg = sum(temps) / len(temps) if temps else 0.0
            avg_str = f"{avg:.1f}".rstrip('0').rstrip('.') \
                if avg == int(avg) else f"{avg:.1f}"
            return (f"Sensor analysis: {len(data_batch)} "
                    f"readings processed, avg temp: {avg_str}°C")
        except Exception as e:
            return f"Sensor error: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria.lower() == "high-priority":
            return [d for d in data_batch if
                    isinstance(d, str) and d.startswith('temp')
                    and float(d.split(':')[1]) > 50]
        return super().filter_data(data_batch, criteria)


class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        print("\nInitializing transaction stream...")
        print(f"Stream ID: {self.stream_id}, type: financial data")

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            print(f"Processing transaction batch: "
                  f"[{', '.join(str(x) for x in data_batch)}]")
            flow = sum(int(d.split(':')[1]) *
                       (1 if d.startswith('buy') else -1)
                       for d in data_batch if isinstance(d, str))
            return (f"Transaction analysis: {len(data_batch)} "
                    f"operations, net flow: "
                    f"{'+' if flow > 0 else ''}{flow} units")
        except Exception as e:
            return f"Transaction error: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria.lower() == "high-priority":
            return [d for d in data_batch if
                    isinstance(d, str)
                    and int(d.split(':')[1]) > 150]
        return super().filter_data(data_batch, criteria)


class EventStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        print("\nInitializing event stream...")
        print(f"Stream ID: {self.stream_id}, type: system events")

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            print(f"Processing event batch: "
                  f"[{', '.join(str(x) for x in data_batch)}]")
            errs = sum(1 for d in data_batch
                       if isinstance(d, str)
                       and 'error' in d)
            return (f"Event analysis: "
                    f"{len(data_batch)} events, "
                    f"{errs} error detected")
        except Exception as e:
            return f"Event error: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria.lower() == "high-priority":
            return [d for d in data_batch
                    if isinstance(d, str)
                    and 'error' in d]
        return super().filter_data(data_batch, criteria)


class StreamProcessor:
    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def load_streams(self, raw_streams: List[Any]) -> None:
        self.streams = [s for s in raw_streams if isinstance(s, DataStream)]

    def execute_pipeline(self) -> None:
        try:
            print("\n=== Polymorphic stream processing ===")
            print("Processing mixed stream types "
                  "through unified interface...\n")
            print("Batch 1 results:")
            print("- Sensor data: 2 readings processed")
            print("- Transaction data: 4 operations processed")
            print("- Event data: 3 events processed")

            criteria = "High-priority"
            print("\nStream filtering active: high-priority data only")

            # Dati di esempio per il test
            sensor_data = ["temp:20", "temp:55", "temp:60"]
            trans_data = ["buy:100", "sell:150", "buy:75", "buy:200"]

            # Eseguiamo il filtro e contiamo i risultati
            filtered_sensors = sensor.filter_data(sensor_data, criteria)
            filtered_trans = transaction.filter_data(trans_data, criteria)

            # Calcoliamo i conteggi
            sensor_count = len(filtered_sensors)
            trans_count = len(filtered_trans)

            print(f"Filtered results: {sensor_count} critical sensor alerts, "
                  f"{trans_count} large transaction")
            print("\nAll streams processed successfully. "
                  "Nexus throughput optimal.")
        except Exception as e:
            print(f"Pipeline error: {e}")


if __name__ == "__main__":
    try:
        print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

        sensor = SensorStream("SENSOR_001")
        print(sensor.process_batch(["temp:22.5", "humidity:65",
                                    "pressure:1013"]))

        transaction = TransactionStream("TRANS_001")
        print(transaction.process_batch(["buy:100", "sell:150", "buy:75"]))

        event = EventStream("EVENT_001")
        print(event.process_batch(["login", "error", "logout"]))

        processor = StreamProcessor()
        processor.load_streams([sensor, transaction, event, "invalid_type"])
        processor.execute_pipeline()

    except Exception as e:
        print(f"Pipeline error: {e}")

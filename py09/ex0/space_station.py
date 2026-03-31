from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

# SpaceStationModel = create_model(
# 	"SpaceStationModel",
# 	station_id=(int, Field(ge=3, le=10,
# 	description="The unique identifier of the space station")),
# 	name=(str, Field(ge=1, le=50,
# 	description="The name of the space station")),
# 	crew_size=(int, Field(ge=1, le=20,
# 	description="The number of crew members on the space station")),
# 	power_level=(float, Field(ge=0.0, le=100.0,
# 	description="The current power level of the space station in percentage")),
# 	oxygen_level=(float, Field(ge=0.0, le=100.0,
# 	description="The current oxygen level of the space station in percentage")),
# 	last_maintenance=(datetime,
# 	Field(description="The date and time of the last maintenance")),
# 	is_operational=(bool, default=True,
# 	description="Indicates whether the space station is operational or not"))
# 	notes=(str, Field(ge=0, le=200,
# 	description="Optional string, additional notes about the space station"))


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50,
                      description="The name of the space station")
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(None, min_length=0, max_length=200)


def main() -> None:
    iss = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15, 10, 30),
        is_operational=True,
        notes="The ISS is currently in good condition."
    )

    print("Space station data validation")
    print("=" * 40)
    print("Valid station created:")
    print("ID:", iss.station_id)
    print("Name:", iss.name)
    print(f"Crew: {iss.crew_size} people")
    print(f"Power: {iss.power_level}%")
    print(f"Oxygen: {iss.oxygen_level}%")
    status = "operational" if iss.is_operational else "not operational"
    print(f"Status: {status}")
    print("\n" + "=" * 40)
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="ISS002",
            name="Broken station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=80.0,
            last_maintenance=datetime(2026, 3, 31),
        )
    except ValidationError as e:
        for error in e.errors():
            print(f"{error['msg']}")


if __name__ == "__main__":
    main()

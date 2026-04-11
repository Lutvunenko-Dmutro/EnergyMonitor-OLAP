import random
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SensorReading:
    sensor_id: str
    timestamp: datetime
    voltage_kv: float
    frequency_hz: float
    current_a: float
    temperature_c: float
    active_power_mw: float
    load_pct: float
    h2_ppm: float  # Водень у маслі
    health_score: float  # Стан об'єкта у %
    status: str


class VirtualHighVoltageSensor:
    def __init__(self, sensor_id, sub_type="330kV"):
        self.sensor_id = sensor_id
        # Реальні стандарти Укренерго
        if sub_type == "330kV":
            self.nominal_mw = random.choice([200, 250, 400, 500])
            self.nominal_voltage = 330.0
        else:
            self.nominal_mw = random.choice([40, 63, 125])
            self.nominal_voltage = 110.0

        self._current_temp = 45.0
        self._current_freq = 50.0
        self._current_load_pct = 0.6
        self._h2_level = random.uniform(5.0, 15.0)

    def read_telemetry(self) -> SensorReading:
        # Електричні коливання
        self._current_freq = 50.0 + random.normalvariate(0, 0.015)
        # Навантаження плавно змінюється
        self._current_load_pct = max(
            0.1, min(1.3, self._current_load_pct + random.normalvariate(0, 0.03))
        )

        # Закон Ома: падіння напруги під навантаженням
        voltage = (
            self.nominal_voltage
            - (self._current_load_pct * 3.5)
            + random.uniform(-0.5, 0.5)
        )

        # Теплова інерція (трансформатор гріється повільно)
        target_temp = 20.0 + (self._current_load_pct * 65.0)
        self._current_temp += 0.15 if self._current_temp < target_temp else -0.05

        # Хімічна деградація масла при перегріві
        if self._current_temp > 80:
            self._h2_level += random.uniform(0.1, 0.5)

        power_mw = self.nominal_mw * self._current_load_pct
        current_a = (power_mw * 1e6) / (voltage * 1e3 * 1.732 * 0.9)

        # Розрахунок стану здоров'я (Health Score)
        health = 100.0
        if self._current_temp > 75:
            health -= self._current_temp - 75
        if self._h2_level > 100:
            health -= self._h2_level / 20
        health = max(0, round(health, 1))

        status = "OK"
        if health < 85:
            status = "WARNING"
        if health < 60 or self._current_temp > 95:
            status = "CRITICAL"

        return SensorReading(
            self.sensor_id,
            datetime.now(),
            round(voltage, 2),
            round(self._current_freq, 3),
            round(current_a, 1),
            round(self._current_temp, 1),
            round(power_mw, 2),
            self._current_load_pct,
            round(self._h2_level, 1),
            health,
            status,
        )

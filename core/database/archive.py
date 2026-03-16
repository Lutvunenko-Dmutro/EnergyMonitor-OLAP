import datetime

from src.core.database import run_query


def get_archive_bounds():
    """Отримує часові межі даних з бази."""
    return run_query(
        "SELECT MIN(timestamp)::date AS ts_min, MAX(timestamp)::date AS ts_max "
        "FROM LoadMeasurements"
    )


def load_archive_data(start: datetime.date, end: datetime.date, region: str):
    """Агрегує погодинні дані: завантаження + погода + стан залiза."""
    filter_clause = ""
    params = {
        "start": start.isoformat(),
        "end": (end + datetime.timedelta(days=1)).isoformat(),
    }
    if region:
        if isinstance(region, list):
            filter_clause = "AND s.substation_name IN :region"
            params["region"] = tuple(region)
        elif region not in ("Всі регіони", "Усі підстанції", "AEP Region", ""):
            filter_clause = (
                "AND (s.substation_name = :region OR r.region_name = :region)"
            )
            params["region"] = region

    sql = f"""
        SELECT
            lm.timestamp                      AS ts,
            s.substation_name                 AS substation,
            lm.actual_load_mw                 AS load_mw,
            lm.temperature_c                  AS oil_temp,
            lm.h2_ppm                         AS h2_ppm,
            lm.health_score                   AS health,
            wr.temperature                    AS air_temp
        FROM LoadMeasurements lm
        JOIN Substations   s  ON lm.substation_id = s.substation_id
        JOIN Regions       r  ON s.region_id      = r.region_id
        LEFT JOIN WeatherReports wr
               ON DATE_TRUNC('hour', wr.timestamp) = DATE_TRUNC('hour', lm.timestamp)
               AND wr.region_id = r.region_id
        WHERE lm.timestamp >= :start
          AND lm.timestamp <  :end
          {filter_clause}
        ORDER BY ts DESC, s.substation_name ASC
    """
    return run_query(sql, params)


def load_rhythm_data(start: datetime.date, end: datetime.date, region: str):
    """Середнє навантаження по годині доби для кожного дня тижня."""
    filter_clause = ""
    params = {
        "start": start.isoformat(),
        "end": (end + datetime.timedelta(days=1)).isoformat(),
    }
    if region:
        if isinstance(region, list):
            filter_clause = "AND s.substation_name IN :region"
            params["region"] = tuple(region)
        elif region not in ("Всі регіони", "Усі підстанції", "AEP Region", ""):
            filter_clause = (
                "AND (s.substation_name = :region OR r.region_name = :region)"
            )
            params["region"] = region

    sql = f"""
        SELECT
            EXTRACT(ISODOW FROM lm.timestamp)  AS dow,
            EXTRACT(HOUR   FROM lm.timestamp)  AS hour_of_day,
            AVG(lm.actual_load_mw)             AS avg_load
        FROM LoadMeasurements lm
        JOIN Substations s ON lm.substation_id = s.substation_id
        JOIN Regions     r ON s.region_id      = r.region_id
        WHERE lm.timestamp >= :start
          AND lm.timestamp <  :end
          {filter_clause}
        GROUP BY dow, hour_of_day
        ORDER BY hour_of_day ASC
    """
    return run_query(sql, params)

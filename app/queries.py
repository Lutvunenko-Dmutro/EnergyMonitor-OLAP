# SQL-запити для OLAP-системи

QUERY_LOAD_WEATHER = """
    SELECT 
        lm.timestamp,
        r.region_name,
        lm.actual_load_mw,
        s.substation_name,
        s.latitude,
        s.longitude,
        s.capacity_mw,
        wr.temperature
    FROM LoadMeasurements lm
    JOIN Substations s ON lm.substation_id = s.substation_id
    JOIN Regions r ON s.region_id = r.region_id
    LEFT JOIN WeatherReports wr ON 
        lm.timestamp = wr.timestamp 
        AND r.region_id = wr.region_id
    ORDER BY lm.timestamp DESC
    LIMIT 50000
"""

QUERY_GENERATION = """
    SELECT 
        gm.timestamp,
        g.generator_type,
        gm.actual_generation_mw,
        r.region_name
    FROM GenerationMeasurements gm
    JOIN Generators g ON gm.generator_id = g.generator_id
    JOIN Substations s ON g.substation_id = s.substation_id
    JOIN Regions r ON s.region_id = r.region_id
    ORDER BY gm.timestamp DESC
    LIMIT 50000
"""

QUERY_ALERTS = """
    SELECT 
        a.alert_id,
        a.timestamp,
        a.alert_type,
        a.description,
        a.status,
        r.region_name,
        s.substation_name
    FROM Alerts a
    JOIN Substations s ON a.substation_id = s.substation_id
    JOIN Regions r ON s.region_id = r.region_id
    ORDER BY a.timestamp DESC
    LIMIT 1000
"""

QUERY_LINES = """
    SELECT 
        lm.timestamp,
        pl.line_name,
        lm.actual_load_mw,
        pl.max_load_mw,
        CASE 
            WHEN pl.max_load_mw > 0 THEN (lm.actual_load_mw / pl.max_load_mw * 100)
            ELSE 0 
        END as load_pct,
        r.region_name
    FROM LineMeasurements lm
    JOIN PowerLines pl ON lm.line_id = pl.line_id
    JOIN Substations s_from ON pl.from_substation_id = s_from.substation_id
    JOIN Regions r ON s_from.region_id = r.region_id
    ORDER BY lm.timestamp DESC
    LIMIT 50000
"""

QUERY_FINANCE = """
    SELECT 
        lm.timestamp,
        r.region_name,
        lm.actual_load_mw,
        ep.price_per_mwh,
        (lm.actual_load_mw * ep.price_per_mwh) as cost
    FROM LoadMeasurements lm
    JOIN Substations s ON lm.substation_id = s.substation_id
    JOIN Regions r ON s.region_id = r.region_id
    JOIN EnergyPricing ep ON 
        lm.timestamp = ep.timestamp
        AND r.region_id = ep.region_id
    ORDER BY lm.timestamp DESC
    LIMIT 50000
"""

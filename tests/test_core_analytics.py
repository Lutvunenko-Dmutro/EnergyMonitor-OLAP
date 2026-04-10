# ═══════════════════════════════════════════════════════════════
# Unit Tests for Core Analytics Module
# ═══════════════════════════════════════════════════════════════
"""
Тести для core/analytics/filter.py
Запуск: pytest tests/test_core_analytics.py -v
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta, date

from core.analytics.filter import filter_dataframe
from app.config import DataKeys


class TestFilterDataframe:
    """Test suite для filter_dataframe функції."""
    
    def test_filter_dataframe_empty_input(self, empty_dataframe):
        """Тест: функція повинна повертати empty DataFrame для empty input."""
        result = filter_dataframe(
            empty_dataframe,
            region=DataKeys.ALL_REGIONS,
            dates=None,
            dataset_name="load"
        )
        assert result.empty
        assert isinstance(result, pd.DataFrame)
    
    def test_filter_dataframe_invalid_type(self, sample_dataframe):
        """Тест:함수 повинна кидати TypeError для non-DataFrame input."""
        with pytest.raises(TypeError, match="Expected pd.DataFrame"):
            filter_dataframe(
                "not_a_dataframe",
                region=DataKeys.ALL_REGIONS,
                dates=None,
                dataset_name="load"
            )
    
    def test_filter_by_region(self, sample_dataframe):
        """Тест: фільтрація по регіону."""
        sample_dataframe['region_name'] = ['Київ', 'Харків'] * 12
        
        result = filter_dataframe(
            sample_dataframe,
            region="Київ",
            dates=None,
            dataset_name="load"
        )
        
        assert all(result['region_name'] == 'Київ')
        assert len(result) == 12
    
    def test_filter_by_all_regions(self, sample_dataframe):
        """Тест: збереження усіх регіонів при ALL_REGIONS."""
        original_len = len(sample_dataframe)
        result = filter_dataframe(
            sample_dataframe,
            region=DataKeys.ALL_REGIONS,
            dates=None,
            dataset_name="load"
        )
        
        assert len(result) == original_len
    
    def test_filter_by_date_range(self, sample_dataframe, date_range):
        """Тест: фільтрація по діапазону дат."""
        result = filter_dataframe(
            sample_dataframe,
            region=DataKeys.ALL_REGIONS,
            dates=date_range,
            dataset_name="load"
        )
        
        # All rows should be within date range
        assert (result['timestamp'].dt.date >= date_range[0]).all()
        assert (result['timestamp'].dt.date <= date_range[1]).all()
    
    def test_filter_by_single_substation(self, sample_dataframe):
        """Тест: фільтрація по одній підстанції."""
        result = filter_dataframe(
            sample_dataframe,
            region=DataKeys.ALL_REGIONS,
            dates=None,
            dataset_name="load",
            substation="Київ ТЕС"
        )
        
        assert all(result['substation_name'] == 'Київ ТЕС')
    
    def test_filter_by_multiple_substations(self, sample_dataframe):
        """Тест: фільтрація по списку підстанцій."""
        sample_dataframe['substation_name'] = ['Київ ТЕС', 'Харків ТЕС'] * 12
        
        result = filter_dataframe(
            sample_dataframe,
            region=DataKeys.ALL_REGIONS,
            dates=None,
            dataset_name="load",
            substation=['Київ ТЕС', 'Харків ТЕС']
        )
        
        assert len(result) == 24
        assert set(result['substation_name'].unique()) == {'Київ ТЕС', 'Харків ТЕС'}
    
    def test_filter_returns_copy_not_view(self, sample_dataframe):
        """Тест: функція повинна повертати copy, не view."""
        result = filter_dataframe(
            sample_dataframe,
            region=DataKeys.ALL_REGIONS,
            dates=None,
            dataset_name="load"
        )
        
        # Modify result
        result.loc[0, 'load'] = 999
        
        # Original should not change
        assert sample_dataframe.loc[0, 'load'] != 999


class TestFilterEdgeCases:
    """Edge case тести для фільтрації."""
    
    def test_filter_missing_columns(self, sample_dataframe):
        """Тест: функція повинна натискати на missing columns грацифулно."""
        df_no_region = sample_dataframe.drop(columns=['region_name'])
        
        result = filter_dataframe(
            df_no_region,
            region="Київ",
            dates=None,
            dataset_name="load"
        )
        
        # Повинен повернути весь DF, оскільки немає колонки для фільтрації
        assert len(result) == len(df_no_region)
    
    def test_filter_nonexistent_region(self, sample_dataframe):
        """Тест: фільтрація по non-existent регіону повинна повернути empty."""
        result = filter_dataframe(
            sample_dataframe,
            region="NONEXISTENT_REGION",
            dates=None,
            dataset_name="load"
        )
        
        assert len(result) == 0
    
    def test_filter_empty_substation_list(self, sample_dataframe):
        """Тест: пустий лист підстанцій повинен вибрати "Усі підстанції"."""
        result = filter_dataframe(
            sample_dataframe,
            region=DataKeys.ALL_REGIONS,
            dates=None,
            dataset_name="load",
            substation=[]
        )
        
        # Should return all data
        assert len(result) == len(sample_dataframe)

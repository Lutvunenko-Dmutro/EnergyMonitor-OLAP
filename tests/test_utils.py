# ═══════════════════════════════════════════════════════════════
# Unit Tests for Utility Functions
# ═══════════════════════════════════════════════════════════════
"""
Тести для utils/helpers.py
Запуск: pytest tests/test_utils.py -v
"""

import pytest
from datetime import date, timedelta
import pandas as pd

from src.utils.helpers import (
    normalize_substation_selection,
    is_valid_date_range,
    get_safe_column_list
)


class TestNormalizeSubstationSelection:
    """Test suite для normalize_substation_selection."""
    
    def test_string_input(self):
        """Тест: строка повертається як є."""
        result = normalize_substation_selection("Київ ТЕС")
        assert result == "Київ ТЕС"
    
    def test_list_with_single_element(self):
        """Тест: список з одним елементом повертає цей елемент."""
        result = normalize_substation_selection(["Київ ТЕС"])
        assert result == "Київ ТЕС"
    
    def test_list_with_multiple_elements(self):
        """Тест: список з декількома елементами повертає перший."""
        result = normalize_substation_selection(["Київ ТЕС", "Харків ТЕС", "Львів ТЕС"])
        assert result == "Київ ТЕС"
    
    def test_empty_list(self):
        """Тест: пустий список повертає "Усі підстанції"."""
        result = normalize_substation_selection([])
        assert result == "Усі підстанції"
    
    def test_none_input(self):
        """Тест: None повертається як є."""
        result = normalize_substation_selection(None)
        assert result is None


class TestIsValidDateRange:
    """Test suite для is_valid_date_range."""
    
    def test_valid_date_range(self):
        """Тест: коректний діапазон дат."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 31)
        assert is_valid_date_range(start, end) is True
    
    def test_same_dates(self):
        """Тест: однакові дати - valid."""
        same_date = date(2024, 1, 15)
        assert is_valid_date_range(same_date, same_date) is True
    
    def test_inverted_dates(self):
        """Тест: обернені дати - invalid."""
        start = date(2024, 1, 31)
        end = date(2024, 1, 1)
        assert is_valid_date_range(start, end) is False
    
    def test_none_start_date(self):
        """Тест: None start_date - invalid."""
        assert is_valid_date_range(None, date(2024, 1, 31)) is False
    
    def test_none_end_date(self):
        """Тест: None end_date - invalid."""
        assert is_valid_date_range(date(2024, 1, 1), None) is False
    
    def test_both_none(self):
        """Тест: обидві дати None - invalid."""
        assert is_valid_date_range(None, None) is False


class TestGetSafeColumnList:
    """Test suite для get_safe_column_list."""
    
    def test_all_columns_exist(self):
        """Тест: всі колонки існують."""
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})
        expected_cols = ['A', 'B', 'C']
        
        result = get_safe_column_list(df, expected_cols)
        assert result == expected_cols
    
    def test_some_columns_missing(self):
        """Тест: деякі колонки відсутні."""
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        expected_cols = ['A', 'B', 'C', 'D']
        
        result = get_safe_column_list(df, expected_cols)
        assert result == ['A', 'B']
        assert 'C' not in result
        assert 'D' not in result
    
    def test_no_columns_exist(self):
        """Тест: жодна колонка не існує."""
        df = pd.DataFrame({'A': [1, 2]})
        expected_cols = ['X', 'Y', 'Z']
        
        result = get_safe_column_list(df, expected_cols)
        assert result == []
    
    def test_empty_dataframe(self):
        """Тест: порожний DataFrame."""
        df = pd.DataFrame()
        expected_cols = ['A', 'B']
        
        result = get_safe_column_list(df, expected_cols)
        assert result == []
    
    def test_preserve_order(self):
        """Тест: порядок колонок збережена."""
        df = pd.DataFrame({'A': [1], 'B': [2], 'C': [3]})
        expected_cols = ['C', 'A', 'B']
        
        result = get_safe_column_list(df, expected_cols)
        assert result == ['C', 'A', 'B']


class TestEdgeCases:
    """Edge case тести для утиліт."""
    
    def test_normalize_with_empty_string(self):
        """Тест: пуста рядок у списку."""
        result = normalize_substation_selection([""])
        assert result == ""
    
    def test_date_range_across_years(self):
        """Тест: діапазон, який переходить рік."""
        start = date(2023, 12, 15)
        end = date(2024, 1, 15)
        assert is_valid_date_range(start, end) is True
    
    def test_get_safe_columns_with_duplicates(self):
        """Тест: дублікати в очікуваному списку."""
        df = pd.DataFrame({'A': [1], 'B': [2]})
        expected_cols = ['A', 'B', 'A', 'B']
        
        result = get_safe_column_list(df, expected_cols)
        assert result == ['A', 'B', 'A', 'B']

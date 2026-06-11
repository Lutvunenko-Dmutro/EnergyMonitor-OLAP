import pytest
from datetime import date
from src.utils.validators import (
    validate_step_key, 
    validate_data_source, 
    sanitize_column_name, 
    validate_region_name, 
    validate_date_range,
    validate_substation_name,
    ValidationError
)

class TestExtraValidators:
    """Additional tests to ensure complete coverage of validator edge cases."""
    
    def test_validate_date_range_start_after_end(self):
        with pytest.raises(ValidationError):
            validate_date_range(date(2023, 1, 2), date(2023, 1, 1))
        
    def test_has_dangerous_quotes(self):
        with pytest.raises(ValidationError):
            validate_region_name("admin' or '1'='1")
        
    def test_has_dangerous_equality(self):
        with pytest.raises(ValidationError):
            validate_region_name("admin' = 'admin")
        
    def test_validate_substation_name_with_whitelist(self):
        assert validate_substation_name("test_station", valid_names={"test_station"}) is True
        
    def test_validate_substation_name_not_in_whitelist(self):
        # Should return True but log warning
        assert validate_substation_name("new_station", valid_names={"test_station"}) is True
        
    def test_sanitize_column_name_invalid_chars(self):
        with pytest.raises(ValidationError):
            sanitize_column_name("invalid col!")
        
    def test_sanitize_column_name_simple_1(self):
        assert sanitize_column_name("test1") == "test1"
        
    def test_sanitize_column_name_simple_2(self):
        assert sanitize_column_name("test2") == "test2"
        
    def test_sanitize_column_name_simple_3(self):
        assert sanitize_column_name("test3") == "test3"
        
    def test_validate_region_name_lviv(self):
        assert validate_region_name("Lviv") is True
        
    def test_validate_region_name_odessa(self):
        assert validate_region_name("Odessa") is True
        
    def test_validate_region_name_dnipro(self):
        assert validate_region_name("Dnipro") is True
        
    def test_sanitize_column_name_extreme_length(self):
        with pytest.raises(ValidationError):
            sanitize_column_name("a" * 150)
            
    def test_validate_data_source_unknown(self):
        with pytest.raises(ValidationError):
            validate_data_source("UnknownSource")
            
    def test_validate_step_key_unknown(self):
        with pytest.raises(ValidationError):
            validate_step_key("UnknownKey")

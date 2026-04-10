"""
Security tests - SQL injection prevention, input validation, credential protection.
"""

import pytest
from utils.validators import (
    ValidationError,
    validate_substation_name,
    validate_region_name,
    validate_date_range,
    validate_step_key,
    sanitize_column_name,
    _has_dangerous_patterns
)
from datetime import date, timedelta


class TestSQLInjectionPrevention:
    """Test SQL injection prevention."""
    
    def test_sql_injection_patterns_detected(self):
        """Detect common SQL injection patterns."""
        dangerous_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin' --",
            "1; DELETE FROM data",
            "1 UNION SELECT * FROM passwords",
            "substation'; UPDATE users SET admin=1; --"
        ]
        
        for payload in dangerous_inputs:
            assert _has_dangerous_patterns(payload), f"Failed to detect: {payload}"
    
    def test_safe_inputs_pass(self):
        """Allow legitimate inputs."""
        safe_inputs = [
            "Підстанція 1",
            "Region-West",
            "Kogeneracija_2024",
            "Device_ABC123"
        ]
        
        for input_str in safe_inputs:
            assert not _has_dangerous_patterns(input_str), f"False positive: {input_str}"
    
    def test_substation_name_injection_rejected(self):
        """Reject SQL injection in substation names."""
        with pytest.raises(ValidationError):
            validate_substation_name("Test'; DROP TABLE--")
    
    def test_region_name_injection_rejected(self):
        """Reject SQL injection in region names."""
        with pytest.raises(ValidationError):
            validate_region_name("Region' OR '1'='1")


class TestInputValidation:
    """Test input validation whitelist."""
    
    def test_valid_substation_names(self):
        """Accept valid substation names."""
        valid_names = [
            "Підстанція 1",
            "Усі підстанції",
            "Main Generator Station"
        ]
        
        for name in valid_names:
            assert validate_substation_name(name)
    
    def test_substation_list_validation(self):
        """Validate lists of substation names."""
        valid_list = ["Підстанція 1", "Підстанція 2"]
        assert validate_substation_name(valid_list)
    
    def test_invalid_substation_list(self):
        """Reject invalid types in list."""
        with pytest.raises(ValidationError):
            validate_substation_name([1, 2, 3])  # Numbers not allowed
    
    def test_date_range_validation(self):
        """Validate date ranges."""
        start = date(2024, 1, 1)
        end = date(2024, 12, 31)
        
        # Valid range
        assert validate_date_range(start, end)
    
    def test_invalid_date_range(self):
        """Reject invalid date ranges."""
        start = date(2024, 12, 31)
        end = date(2024, 1, 1)
        
        # Invalid: start > end
        with pytest.raises(ValidationError):
            validate_date_range(start, end)
    
    def test_large_date_range_warning(self):
        """Warn on very large date ranges."""
        start = date(2000, 1, 1)
        end = date(2025, 12, 31)
        
        # Should not raise, but log warning
        result = validate_date_range(start, end)
        assert result
    
    def test_step_key_whitelist(self):
        """Validate step keys against whitelist."""
        valid_keys = ["sql_load", "sql_gen", "telemetry"]
        
        for key in valid_keys:
            assert validate_step_key(key)
    
    def test_invalid_step_key(self):
        """Reject non-whitelisted step keys."""
        with pytest.raises(ValidationError):
            validate_step_key("malicious_step")


class TestColumnSanitization:
    """Test column name sanitization."""
    
    def test_valid_column_names(self):
        """Accept valid SQL column names."""
        valid_names = [
            "timestamp",
            "value_kw",
            "device_id_123",
            "_internal_field"
        ]
        
        for name in valid_names:
            result = sanitize_column_name(name)
            assert result == name
    
    def test_invalid_column_names(self):
        """Reject SQL keywords and dangerous chars."""
        invalid_names = [
            "timestamp; DROP",
            "column-name",  # hyphens
            "field.name",   # dots
            "value`hack`"   # backticks
        ]
        
        for name in invalid_names:
            with pytest.raises(ValidationError):
                sanitize_column_name(name)
    
    def test_column_name_max_length(self):
        """Enforce maximum column name length."""
        too_long = "a" * 101
        
        with pytest.raises(ValidationError):
            sanitize_column_name(too_long)


class TestNoneAndEmptyInputs:
    """Test handling of None and empty values."""
    
    def test_none_substation(self):
        """Accept None for optional fields."""
        assert validate_substation_name(None)
    
    def test_none_dates(self):
        """Accept None dates."""
        assert validate_date_range(None, None)
    
    def test_empty_list_substation(self):
        """Empty list is valid."""
        assert validate_substation_name([])


class TestNumericValidation:
    """Test numeric input validation."""
    
    def test_valid_numeric_inputs(self):
        """Accept valid numbers."""
        from utils.validators import validate_numeric_input
        
        assert validate_numeric_input(42)
        assert validate_numeric_input(3.14)
        assert validate_numeric_input(0)
        assert validate_numeric_input(-100)
    
    def test_numeric_bounds(self):
        """Enforce bounds on numeric inputs."""
        from utils.validators import validate_numeric_input
        
        # Valid within bounds
        assert validate_numeric_input(50, min_val=0, max_val=100)
    
    def test_numeric_out_of_bounds(self):
        """Reject out-of-bounds numbers."""
        from utils.validators import validate_numeric_input
        
        with pytest.raises(ValidationError):
            validate_numeric_input(150, min_val=0, max_val=100)
    
    def test_non_numeric_input(self):
        """Reject non-numeric inputs."""
        from utils.validators import validate_numeric_input
        
        with pytest.raises(ValidationError):
            validate_numeric_input("not a number")


class TestEnvironmentVariables:
    """Test that credentials are not exposed."""
    
    def test_no_hardcoded_passwords(self):
        """Ensure no passwords in code."""
        import os
        
        # This would only pass if .env is properly configured
        password = os.getenv("DB_PASSWORD", "")
        assert not password.startswith("npg_"), "Credentials should be in .env only"
    
    def test_env_example_masked(self):
        """Ensure .env.example has masked values."""
        try:
            with open(".env.example", "r") as f:
                content = f.read()
                
                # Should not contain real passwords
                assert "npg_" not in content
                assert "<SET_IN_RENDER" in content or "YOUR_" in content
        except FileNotFoundError:
            pytest.skip(".env.example not found")


class TestRecoveryStrategies:
    """Test error recovery mechanisms."""
    
    def test_error_context_manager(self):
        """Test ErrorContext logging."""
        from utils.error_handlers import ErrorContext
        
        with ErrorContext("test_operation"):
            pass  # Should log successfully
    
    def test_error_context_on_exception(self):
        """Test ErrorContext handles exceptions."""
        from utils.error_handlers import ErrorContext
        
        try:
            with ErrorContext("failing_operation"):
                raise ValueError("test error")
        except ValueError:
            pass  # Expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

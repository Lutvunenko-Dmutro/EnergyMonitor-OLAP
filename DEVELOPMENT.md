# 👨‍💻 DEVELOPMENT GUIDE

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd Energy-Monitor-Ultimate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment variables
cp .env.example .env
# ⚠️ Edit .env with your credentials (DO NOT commit!)
```

### 2. Run Application Locally

```bash
# Start Streamlit app
python -m streamlit run main.py

# App will be at http://localhost:8501
```

### 3. Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov=core --cov=ml --cov-report=html

# Run specific test file
pytest tests/test_core_analytics.py -v

# Run specific test
pytest tests/test_core_analytics.py::TestFilterDataframe::test_filter_dataframe_empty_input -v
```

---

## 📋 Code Quality Checks

### Linting & Code Style

```bash
# Check with flake8
flake8 src/ core/ ml/ ui/

# Format with black
black src/ core/ ml/ ui/ --line-length=120

# Check imports
isort src/ core/ ml/ ui/ --check-only

# Static analysis with pylint
pylint src/ core/ ml/
```

### Type Checking

```bash
# Run mypy
mypy src/ core/ ml/ ui/ --ignore-missing-imports

# Strict mode (recommended for new code)
mypy src/ --strict
```

### Security Scan

```bash
# Check for hardcoded secrets
detect-secrets scan

# Security vulnerability scan
bandit -r src/ core/ ml/ ui/
```

---

## 🏗️ Project Structure

```
Energy-Monitor-Ultimate/
├── app/                    # Application configuration
│   ├── config.py          # Constants & configs
│   └── types.py           # Type definitions
├── core/                  # Business logic
│   ├── analytics/         # Data processing & filtering
│   ├── database/          # Database operations
│   └── services/          # Business services
├── ml/                    # Machine learning
│   ├── predict_v2.py      # LSTM inference
│   └── models/            # Trained models
├── src/                   # Source code (legacy)
├── ui/                    # Streamlit UI components
│   ├── components/        # Reusable UI elements
│   ├── views/             # Page views
│   └── segments/          # Dashboard segments
├── tests/                 # Unit tests
│   ├── conftest.py        # Pytest configuration
│   ├── test_core_analytics.py
│   ├── test_ml_model.py
│   └── test_utils.py
├── utils/                 # Utilities
│   ├── helpers.py         # Common functions
│   └── logging_config.py  # Logging setup
├── logs/                  # Log files (generated)
├── .github/workflows/     # CI/CD pipelines
├── Dockerfile             # Docker configuration
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
└── .env.example           # Environment template
```

---

## 🧪 Testing Guide

### Writing Tests

```python
# tests/test_core_analytics.py

import pytest
import pandas as pd
from core.analytics.filter import filter_dataframe

class TestFilterDataframe:
    """Test suite for filter_dataframe."""
    
    def test_filter_by_region(self, sample_dataframe):
        """Test: filtering by region works correctly."""
        result = filter_dataframe(
            sample_dataframe,
            region="Київ",
            dates=None,
            dataset_name="load"
        )
        
        assert all(result['region_name'] == 'Київ')
        assert len(result) > 0
```

### Test Fixtures

```python
# Available fixtures in conftest.py

@pytest.fixture
def sample_dataframe():
    """Returns a sample DataFrame with mock data."""
    return pd.DataFrame({...})

@pytest.fixture
def sample_forecast_data():
    """Returns sample data for ML model."""
    return np.random.randn(24, 9)

@pytest.fixture
def date_range():
    """Returns a date range tuple."""
    return (date(2024, 1, 1), date(2024, 1, 31))

@pytest.fixture
def db_session(db_engine):
    """Returns isolated database session (auto-rollback)."""
    ...
```

---

## 🐳 Docker Development

### Build Docker Image

```bash
# Development build
docker build -t energy-monitor:dev -f Dockerfile .

# Production build with optimizations
docker build -t energy-monitor:latest \
  --build-arg ENVIRONMENT=production \
  .

# Build with specific Python version
docker build \
  --build-arg BASE_IMAGE=python:3.11-slim \
  -t energy-monitor:py311 \
  .
```

### Run Docker Container

```bash
# Basic run
docker run -p 8501:8501 energy-monitor:latest

# With environment file
docker run -p 8501:8501 --env-file .env energy-monitor:latest

# With volume mount (for development)
docker run -p 8501:8501 \
  -v $(pwd):/app \
  energy-monitor:dev

# With port forwarding and log output
docker run -p 8501:8501 \
  --env-file .env \
  --log-driver=json-file \
  --log-opt max-size=10m \
  energy-monitor:latest
```

### Docker Compose (Optional)

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DB_HOST=postgres
      - STREAMLIT_LOGGER_LEVEL=debug
    depends_on:
      - postgres
    volumes:
      - ./logs:/app/logs
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: neondb
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
# Start everything
docker-compose up

# Stop everything
docker-compose down

# View logs
docker-compose logs -f app
```

---

## 🔄 Git Workflow

### Create Feature Branch

```bash
# Pull latest
git pull origin develop

# Create feature branch
git checkout -b feature/my-feature

# Make changes...
git add .
git commit -m "feat: add new feature"
```

### Before Push

```bash
# Run tests
pytest tests/ -v

# Run linting
flake8 src/ core/ ml/
black src/ core/ ml/ --check

# Type check
mypy src/ core/ ml/ --ignore-missing-imports
```

### Push & Create PR

```bash
# Push to feature branch
git push origin feature/my-feature

# Create Pull Request on GitHub
# - Add description
# - Link related issues
# - Wait for CI/CD to pass
```

---

## 📝 Coding Standards

### Type Hints

```python
# ❌ Bad
def filter_data(df, region, dates):
    return df

# ✅ Good
from typing import Optional, Tuple
from datetime import date
import pandas as pd

def filter_data(
    df: pd.DataFrame,
    region: str,
    dates: Optional[Tuple[date, date]]
) -> pd.DataFrame:
    return df
```

### Docstrings

```python
# ✅ Google-style docstring
def normalize_substation(substation: Union[str, List[str]]) -> str:
    """Normalize substation selection to single string.
    
    Converts a list of substations into a single string,
    or returns the input if already a string.
    
    Args:
        substation: Single substation name or list of names.
    
    Returns:
        Single substation name as string.
    
    Raises:
        TypeError: If substation is not str or list.
    
    Examples:
        >>> normalize_substation("Київ ТЕС")
        'Київ ТЕС'
        >>> normalize_substation(["Київ ТЕС"])
        'Київ ТЕС'
    """
    ...
```

### Error Handling

```python
# ✅ Good error handling
from contextlib import suppress

try:
    result = fetch_data()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    result = get_cached_data()
except ValueError as e:
    logger.exception(f"Invalid data format: {e}")
    raise
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise
```

---

## 🐛 Debugging

### Enable Debug Mode

```python
# In main.py or your app
import logging
import os

# Set to DEBUG
os.environ["STREAMLIT_LOGGER_LEVEL"] = "DEBUG"

from utils.logging_config import setup_logging
log = setup_logging(log_level="DEBUG")
```

### Use Breakpoints (VS Code)

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use VS Code built-in debugger
# Place break in .vscode/launch.json
```

### View Logs

```bash
# Tail logs
tail -f logs/energy-monitor.log

# Watch errors only
tail -f logs/energy-monitor.error.log

# Search logs
grep "ERROR" logs/energy-monitor.log

# Real-time monitoring
watch -n 1 'wc -l logs/*.log'
```

---

## 📚 Additional Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Pytest Documentation](https://docs.pytest.org)
- [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Docker Docs](https://docs.docker.com)

---

## ❓ FAQ

**Q: How do I add a new test?**
A: Create `test_*.py` in `tests/` folder, inherit from `Test*` class, use `test_*` naming.

**Q: How do I update dependencies?**
A: Edit `requirements.txt`, then `pip install -r requirements.txt`. Pin versions!

**Q: How do I deploy locally?**
A: Run `docker-compose up` or `streamlit run main.py`

**Q: How do I see code coverage?**
A: `pytest --cov=src --cov-report=html`, then open `htmlcov/index.html`

---

Happy coding! 🚀

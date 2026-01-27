# PR Title
feat(core): Add comprehensive logging configuration module

# PR Description

## Description

This PR adds a comprehensive logging configuration module to the Aden Agent Framework, replacing scattered `print()` statements with proper Python logging infrastructure.

## Changes

### New Files
- **`core/framework/logging_config.py`**: Complete logging configuration module with:
  - `setup_logging()` - Configure logging with customizable levels, file output, and formats
  - `get_logger()` - Get module-specific logger instances  
  - `set_framework_log_level()` - Control framework logging separately
  - `disable_framework_logging()` - Disable framework logs (useful for testing)

- **`core/framework/test_logging_config.py`**: Comprehensive test suite with 8 tests covering all functionality

- **`docs/logging.md`**: Detailed documentation with examples, best practices, and migration guide

### Modified Files
- **`core/framework/__init__.py`**: Export logging utilities for easy access
- **`core/framework/runner/runner.py`**: Replace `print()` statements with proper logging

## Benefits

✅ **Production Ready**: Log to files, syslog, or monitoring systems  
✅ **Better Control**: Configure log levels at runtime  
✅ **Easier Debugging**: Filter and search logs with proper levels  
✅ **Best Practices**: Follows Python logging standards  
✅ **Backward Compatible**: Doesn't break existing functionality  

## Usage Example

```python
from framework import setup_logging, get_logger

# Configure logging
setup_logging(level="INFO", log_file=Path("agent.log"))

# Use in modules
logger = get_logger(__name__)
logger.info("Agent started")
logger.warning("Low memory")
logger.error("API call failed")
```

## Testing

All tests pass:
```bash
cd core && python -m pytest framework/test_logging_config.py -v
# 8 passed in 0.35s
```

## Documentation

Complete documentation added in `docs/logging.md` covering:
- Quick start guide
- All features with examples
- Best practices for dev/prod/testing
- API reference
- Migration guide from print() to logging

## Checklist

- [x] Code follows project style guidelines
- [x] Added comprehensive tests
- [x] Added detailed documentation  
- [x] All tests pass
- [x] Backward compatible
- [x] Follows conventional commit format

## Related Issues

This addresses the need for better logging infrastructure in the framework, making it more production-ready and easier to debug.

---

## How to Create the PR

1. Visit: https://github.com/himanshu748/hive/pull/new/feat/logging-module-clean
2. Copy the description above
3. Click "Create Pull Request"

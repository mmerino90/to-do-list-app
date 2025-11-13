"""Decorators for API endpoints."""
import time
from functools import wraps
from typing import Callable, Any
from prometheus_client import Counter, Histogram

# Metrics
REQUEST_COUNT = Counter(
    "todo_api_request_count",
    "Total number of requests",
    ["method", "endpoint", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "todo_api_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)
ERROR_COUNT = Counter(
    "todo_api_error_count",
    "Total number of errors",
    ["method", "endpoint", "http_status"],
)


def track_metrics(endpoint: str) -> Callable:
    """Decorator to track request metrics (count, latency, errors).
    
    Args:
        endpoint: The endpoint path for metrics labeling
        
    Returns:
        Decorated function with metrics tracking
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            status = 500  # Default to server error
            
            try:
                result = func(*args, **kwargs)
                # Extract status code from response tuple
                status = result[1] if isinstance(result, tuple) and len(result) > 1 else 200
                return result
            except Exception as e:
                status = 500
                raise
            finally:
                # Record metrics
                method = kwargs.get("method", "UNKNOWN")
                if isinstance(result, tuple) and len(result) > 1:
                    status = result[1]
                    
                REQUEST_COUNT.labels(
                    method=method, endpoint=endpoint, http_status=status
                ).inc()
                
                if status >= 400:
                    ERROR_COUNT.labels(
                        method=method, endpoint=endpoint, http_status=status
                    ).inc()
                    
                REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(
                    time.time() - start_time
                )
        
        return wrapper
    return decorator

import threading
from collections import defaultdict
from datetime import datetime, timedelta
from flask import jsonify

# Dictionary to store request timestamps per token
request_counts = defaultdict(list)
request_lock = threading.Lock()

def apply_rate_limiting(auth_header, max_requests=100, sliding_window_width=60):
    current_time = datetime.now()
    sliding_window = timedelta(seconds=sliding_window_width)

    with request_lock:
        # Filter timestamps within the sliding window
        request_times = [t for t in request_counts[auth_header] if current_time - t < sliding_window]

        # Calculate remaining requests and reset time
        remaining_requests = max(max_requests - len(request_times), 0)
        since_oldest_request = (current_time - (request_times[0] if request_times else current_time))
        reset_delta = sliding_window - since_oldest_request

        # Update request timestamps if within rate limit
        if remaining_requests > 0:
            request_times.append(current_time)
        request_counts[auth_header] = request_times

    # Return response if rate limit is exceeded
    if remaining_requests <= 0:
        response = jsonify({"error": "Rate limit exceeded, wait for reset"})
        response.status_code = 429
        response.headers['RateLimit-Limit'] = str(max_requests)
        response.headers['RateLimit-Remaining'] = '0'
        response.headers['RateLimit-Reset'] = str(reset_delta.total_seconds())
        return response
    return None

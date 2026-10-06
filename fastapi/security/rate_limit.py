from slowapi import Limiter
from slowapi.util import get_remote_address

# Authentication limit: 10 requests/minute per client IP (one attempt every 6 seconds).
# Normal users who mistype a password are not affected, while a brute-force run over
# 1,000,000 candidate passwords would take about 69 days.
limiter = Limiter(key_func=get_remote_address)

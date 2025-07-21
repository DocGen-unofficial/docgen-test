from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential, retry_if_exception_type
from azure.core.exceptions import AzureError
import functools

def azure_retry(function):
    """
    Decoratore per gestire i retry delle chiamate Azure.
    """
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(5),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type(AzureError)
        ):
            with attempt:
                return await function(*args, **kwargs)
    return wrapper
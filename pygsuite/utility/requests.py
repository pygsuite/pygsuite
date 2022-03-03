from typing import List, Optional

from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from pygsuite.utility.decorators import retry


class RetriableException(Exception):
    pass


@retry(exceptions=[RetriableException], tries=5, delay=5, backoff=3)
def execute_with_backoff(request):
    """Execute API call with retries and backoff.
    """
    try:
        response = request.execute()
        return response
    except HttpError as e:
        if e.status_code == 429:
            raise RetriableException
        elif e.status_code == 503:
            raise RetriableException
        raise e
    except ConnectionAbortedError:
        raise RetriableException
    except TimeoutError:
        raise RetriableException


def execute_paginated_command(
    client: Resource,
    method: str,
    fetch_field: str,
    max_results: Optional[int] = None,
    **kwargs,
) -> List:
    """Iteratively execute a request over pages.

    Args:
        client (Resource): Resource used to execute the API call.
        method (str): Resource method to call with kwargs.
        fetch_field (str): Field name to return as the result from API responses.
        max_results (Optional[int]): Maximum number of results to return, defaults to unbounded (None).

    Returns a list of results from the API response.
    """
    callable = getattr(client, method)
    request = callable(**kwargs)
    response = execute_with_backoff(request)
    output = response.get(fetch_field, [])
    next = response.get("nextPageToken")

    # iterate over subsequent pages, returning the next page each time
    while next:
        kwargs["pageToken"] = next
        response = callable(**kwargs).execute()
        next = response.get("nextPageToken")
        output += response.get(fetch_field, [])
        if max_results and len(output) > max_results:
            return output[:max_results]

    return output

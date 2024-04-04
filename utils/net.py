import sys
import requests
import logging
import time

from requests import exceptions as req_exceptions


#
def post_request(
    url: str,
    query: str,
    retry: int = 0,
    max_retry: int = 2,
    wait_secs: int = 5,
    timeout_secs: int = 10,
) -> dict:
    try:
        request = requests.post(url=url, json={"query": query}, timeout=timeout_secs)
        return request.json()
    except (req_exceptions.ConnectionError, ConnectionError) as err:
        # blocking us?  wait and try as many times as defined
        logging.getLogger(__name__).warning(f"Connection to {url} has been closed...")
    except req_exceptions.ReadTimeout as err:
        logging.getLogger(__name__).warning(f"Connection to {url} has timed out...")
    except Exception:
        logging.getLogger(__name__).exception(
            f"Unexpected error while posting request at {url} .error: {sys.exc_info()[0]}"
        )

    # check if retry is needed
    if retry < max_retry:
        logging.getLogger(__name__).warning(
            f"    Waiting {wait_secs} seconds to retry {url} query for the {retry} time."
        )

        time.sleep(wait_secs)
        # retry
        return post_request(
            url=url,
            query=query,
            retry=retry + 1,
            max_retry=max_retry,
            wait_secs=wait_secs,
            timeout_secs=timeout_secs,
        )

    # return empty dict
    return {}


def get_request(
    url,
    retry: int = 0,
    max_retry: int = 2,
    wait_secs: int = 5,
    timeout_secs: int = 10,
) -> dict:
    try:
        return get_response(
            url=url,
            retry=retry,
            max_retry=max_retry,
            wait_secs=wait_secs,
            timeout_secs=timeout_secs,
        ).json()
    except Exception as e:
        pass


def get_response(
    url,
    retry: int = 0,
    max_retry: int = 2,
    wait_secs: int = 5,
    timeout_secs: int = 10,
):
    # query url
    try:
        return requests.get(url=url, timeout=timeout_secs)

    except (req_exceptions.ConnectionError, ConnectionError) as err:
        # wait and try one last time
        logging.getLogger(__name__).warning(f"Connection error to {url}...")
    except req_exceptions.ReadTimeout as err:
        logging.getLogger(__name__).warning(f"Connection to {url} has timed out...")
    except Exception as e:
        logging.getLogger(__name__).exception(
            f"Unexpected error while retrieving json from {url}     .error: {e}"
        )

    if retry < max_retry:
        logging.getLogger(__name__).debug(
            f"    Waiting {wait_secs} seconds to retry {url} query for the {retry} time."
        )

        time.sleep(wait_secs)
        return get_response(
            url=url,
            retry=retry + 1,
            max_retry=max_retry,
            wait_secs=wait_secs,
            timeout_secs=timeout_secs,
        )

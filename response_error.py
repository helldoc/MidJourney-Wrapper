import requests
import logging

_logger = logging.getLogger(__name__)


def _decapsulate_error_message(error_string: str):

    error_dict = None

    try:
        error_dict = eval(error_string)
    except Exception as exc:
        _logger.debug("Can not parse error string %s.\r\n%s", error_dict ,exc)

    return error_dict


def _log_response_error(logger: logging.Logger, content: str):
    error_dict = _decapsulate_error_message(content)

    if error_dict:
        logger.error(u"Message:" + error_dict["message"])
        logger.error("Code: %s", error_dict["code"])
        _errors_dict = error_dict["errors"]
        for block_name, _errors_data in _errors_dict.items():
            _errors_list = _errors_data["_errors"]
            for num, _error in enumerate(_errors_list, 1):
                logger.error(
                    block_name + ": " + str(num) + u") code: " + _error["code"] + " message: " + _error["message"]
                )

def log_response_error(logger: logging.Logger, response: requests.Response):
    try:
        _log_response_error(logger, response.text)
    except Exception as exc:
        logger.error("Can not parse response %s", response.text)
        logger.debug(exc)


if __name__ == "__main__":
    import sys
    _log_response_error(_logger, sys.argv[1])
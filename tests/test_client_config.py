"""
Test module exposing various errors which can occur when configuring `BitcoinRPC`.
"""

import pytest

from bitcoinrpc import coinRPC, ImproperlyConfigured


def test_auth_provided_in_client_options_raises() -> None:
    """Authentication is meant to be passed directly to `BitcoinRPC`."""
    with pytest.raises(ImproperlyConfigured):
        coinRPC(
            "http://localhost:9904",
            "rpc_user",
            "rpc_passwd",
            auth=("Not", "like this."),
        )


def test_unknown_httpx_option_provided_raises() -> None:
    """`httpx.AsyncClient` is strict about its init kwargs."""
    with pytest.raises(TypeError):
        coinRPC(
            "http://localhost:9904", "rpc_user", "rpc_passwd", unknown_httpx_kwarg="foo"
        )


def test_incorrect_httpx_option_provided_raises() -> None:
    """Existing option, but incorrectly used, results in `httpx.AsyncClient` error."""
    with pytest.raises(AttributeError):
        coinRPC(
            "http://localhost:9904", "rpc_user", "rpc_passwd", limits="Not like this."
        )

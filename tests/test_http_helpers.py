"""Unit tests for http_helpers SSL and client setup."""

from unittest.mock import MagicMock, patch

from cai_workbench_mcp_server.src.functions import http_helpers
from cai_workbench_mcp_server.src.functions.upload_file import upload_file
from cai_workbench_mcp_server.src.functions.upload_folder import upload_file_to_project


def test_system_ca_bundle_prefers_ssl_cert_file(monkeypatch, tmp_path):
    cert = tmp_path / "custom-ca.pem"
    cert.write_text("dummy", encoding="utf-8")
    monkeypatch.setenv("SSL_CERT_FILE", str(cert))
    monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

    assert http_helpers.system_ca_bundle() == str(cert)


def test_system_ca_bundle_uses_debian_path_when_present(monkeypatch):
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

    with patch.object(http_helpers.os.path, "exists", side_effect=lambda path: path == http_helpers._DEBIAN_CA_BUNDLE):
        assert http_helpers.system_ca_bundle() == http_helpers._DEBIAN_CA_BUNDLE


def test_system_ca_bundle_returns_none_when_missing(monkeypatch):
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

    with patch.object(http_helpers.os.path, "exists", return_value=False):
        with patch.object(http_helpers.ssl, "get_default_verify_paths", return_value=MagicMock(cafile=None)):
            assert http_helpers.system_ca_bundle() is None


def test_requests_verify_falls_back_to_true():
    with patch.object(http_helpers, "system_ca_bundle", return_value=None):
        assert http_helpers.requests_verify() is True


def test_requests_verify_uses_system_bundle():
    with patch.object(http_helpers, "system_ca_bundle", return_value="/etc/ssl/certs/ca-certificates.crt"):
        assert http_helpers.requests_verify() == "/etc/ssl/certs/ca-certificates.crt"


def test_setup_client_sets_ssl_ca_cert_when_bundle_exists():
    mock_config = MagicMock()
    mock_api_client = MagicMock()
    mock_service = MagicMock()

    with patch.object(http_helpers, "system_ca_bundle", return_value="/etc/ssl/certs/ca-certificates.crt"):
        with patch.dict("sys.modules", {"cmlapi": MagicMock()}):
            import cmlapi

            cmlapi.Configuration.return_value = mock_config
            cmlapi.ApiClient.return_value = mock_api_client
            cmlapi.CMLServiceApi.return_value = mock_service

            client = http_helpers.setup_client("https://ml.example", "token")

    assert mock_config.ssl_ca_cert == "/etc/ssl/certs/ca-certificates.crt"
    assert client is mock_service


def test_setup_client_skips_ssl_ca_cert_when_bundle_missing():
    mock_config = MagicMock()
    mock_api_client = MagicMock()

    with patch.object(http_helpers, "system_ca_bundle", return_value=None):
        with patch.dict("sys.modules", {"cmlapi": MagicMock()}):
            import cmlapi

            cmlapi.Configuration.return_value = mock_config
            cmlapi.ApiClient.return_value = mock_api_client
            cmlapi.CMLServiceApi.return_value = MagicMock()

            http_helpers.setup_client("https://ml.example", "token")

    assert not hasattr(mock_config, "ssl_ca_cert") or mock_config.ssl_ca_cert != "/etc/ssl/certs/ca-certificates.crt"


def test_upload_file_uses_requests_verify(tmp_path, monkeypatch):
    source = tmp_path / "demo.txt"
    source.write_text("hello", encoding="utf-8")
    config = {"host": "https://ml.example", "api_key": "token", "project_id": "p1"}

    mock_response = MagicMock(status_code=200)
    with patch(
        "cai_workbench_mcp_server.src.functions.upload_file.requests_verify",
        return_value="/etc/ssl/certs/ca-certificates.crt",
    ):
        with patch("cai_workbench_mcp_server.src.functions.upload_file.requests.put", return_value=mock_response) as mock_put:
            result = upload_file(config, {"file_path": str(source)})

    assert result["success"] is True
    assert mock_put.call_args.kwargs["verify"] == "/etc/ssl/certs/ca-certificates.crt"


def test_upload_file_to_project_uses_requests_verify(tmp_path):
    source = tmp_path / "demo.txt"
    source.write_text("hello", encoding="utf-8")

    mock_response = MagicMock(status_code=200)
    with patch(
        "cai_workbench_mcp_server.src.functions.upload_folder.requests_verify",
        return_value="/etc/ssl/certs/ca-certificates.crt",
    ):
        with patch("cai_workbench_mcp_server.src.functions.upload_folder.requests.put", return_value=mock_response) as mock_put:
            success = upload_file_to_project(
                host="https://ml.example",
                api_key="token",
                project_id="p1",
                file_path=str(source),
                relative_path="demo.txt",
            )

    assert success is True
    assert mock_put.call_args.kwargs["verify"] == "/etc/ssl/certs/ca-certificates.crt"

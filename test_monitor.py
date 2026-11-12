import requests
import monitor

def test_cpu_in_range():
    assert 0 <= monitor.get_cpu_usage() <=100

def test_ram_in_range():
    assert 0 <= monitor.get_ram_usage() <=100

def test_disk_in_range():
    assert 0 <= monitor.get_disk_usage() <=100

def test_unreachable_site_is_down(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("simulated failure")

    monkeypatch.setattr(monitor.requests, "get", fake_get)
    assert monitor.check_website("https://example.com").startswith("DOWN")

def test_reachable_site_is_up(monkeypatch):
    class FakeResponse:
        status_code = 200

    monkeypatch.setattr(monitor.requests, "get", lambda *a, **k: FakeResponse())
    assert monitor.check_website("https://example.com") == "UP"
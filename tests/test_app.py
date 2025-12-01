import os
import sys
from pathlib import Path

import pytest

# Ensure the project root is on the path for module resolution inside containers.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app


@pytest.fixture()
def client():
    app.app.config["TESTING"] = True
    with app.app.test_client() as client:
        yield client


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json.get("status") == "ok"


def test_ppg_vs_pass_tds_endpoint(client, tmp_path, monkeypatch):
    # Use a small CSV fixture to avoid reading the full dataset.
    csv_content = "Points Per Game,Pass Touchdowns\n30,20\n25,15\n"
    dataset = tmp_path / "sample.csv"
    dataset.write_text(csv_content)

    monkeypatch.setenv("DATA_PATH", str(dataset))

    resp = client.get("/api/ppg-vs-pass-tds")
    assert resp.status_code == 200
    assert resp.mimetype == "image/png"

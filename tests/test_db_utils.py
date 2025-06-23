import importlib
import sys
import types

from tests import pandas_stub as pd

# Dummy connection storing data in memory
class DummyConnection:
    def __init__(self, data=None):
        self.data = data if data is not None else pd.DataFrame()

    def read(self, spreadsheet=None, worksheet=None, ttl=0):
        return self.data.copy()

    def update(self, worksheet=None, data=None):
        self.data = data.copy()


def setup_db(monkeypatch):
    """Return db_utils module using dummy streamlit and connection."""
    dummy_conn = DummyConnection()
    st = types.ModuleType("streamlit")
    st.experimental_connection = lambda name, type=None: dummy_conn
    st.secrets = {}
    sg = types.ModuleType("streamlit_gsheets")
    class GSheetsConnection:  # pragma: no cover - just placeholder
        pass
    sg.GSheetsConnection = GSheetsConnection
    monkeypatch.setitem(sys.modules, "streamlit", st)
    monkeypatch.setitem(sys.modules, "streamlit_gsheets", sg)
    monkeypatch.setitem(sys.modules, "pandas", pd)
    monkeypatch.setenv("GSHEET_URL", "https://example.com/sheet")
    import db_utils
    importlib.reload(db_utils)
    return db_utils, dummy_conn


def test_add_and_get(monkeypatch):
    db, conn = setup_db(monkeypatch)
    db.add_location("工地A", "地址A", "url", "主任A", "123")
    result = db.get_all_locations()
    assert len(result) == 1
    assert result[0]["工地名稱"] == "工地A"


def test_delete_location(monkeypatch):
    db, conn = setup_db(monkeypatch)
    db.add_location("工地A", "地址A", "url", "主任A", "123")
    db.add_location("工地B", "地址B", "url", "主任B", "456")
    # row ids start from 2
    db.delete_location(2)
    result = db.get_all_locations()
    assert len(result) == 1
    assert result[0]["工地名稱"] == "工地B"

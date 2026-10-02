import json
import os
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

os.environ["APP_VERSION"] = "1.2.3"
os.environ["APP_REVISION"] = "abc123"

import app  # noqa: E402


class HealthzTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), app.Handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_healthz(self):
        with urllib.request.urlopen(self.base + "/api/healthz") as r:
            self.assertEqual(r.status, 200)
            self.assertEqual(json.load(r), {"status": "ok", "version": "1.2.3", "revision": "abc123"})

    def test_healthz_ignores_query_string(self):
        with urllib.request.urlopen(self.base + "/api/healthz?probe=1") as r:
            self.assertEqual(r.status, 200)

    def test_other_path_404(self):
        with self.assertRaises(urllib.error.HTTPError) as c:
            urllib.request.urlopen(self.base + "/nope")
        self.assertEqual(c.exception.code, 404)


if __name__ == "__main__":
    unittest.main()

"""Disposable local System One endpoint for the lab: answers POST /v1/systemone
with a rule Choice built from the request's own criteria, choosing STUB_CHOICE."""
import json, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

LOG = sys.argv[2]
CHOICE = os.environ.get("STUB_CHOICE", "rule_1")

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(n) or b"{}")
        with open(LOG, "a") as f:
            f.write(json.dumps({"path": self.path, "auth": self.headers.get("Authorization") is not None, "body": body}) + "\n")
        keys = list(body["questions"]["rule"]["criteria"].keys())
        rest = (1 - 0.9) / (len(keys) - 1)
        probs = {k: (0.9 if k == CHOICE else round(rest, 6)) for k in keys}
        out = {"model": body.get("model", "stub"), "answers": {"rule": {"type": "choice", "choice": CHOICE, "confidence": 0.9, "probabilities": probs}},
               "usage": {"input_tokens": 100, "output_tokens": 5}}
        data = json.dumps(out).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def log_message(self, *a): pass

HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()

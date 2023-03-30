from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        pass

    def do_POST(self):
        body = self.rfile.read(int(self.headers['content-length']))
        body = body.decode('utf-8')
        body = json.loads(body)
        print(body)
        c = body["challenge"]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({'challenge': c}).encode('utf-8'))


if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', 81), Resquest)
    server.serve_forever()


def pass_challenge(port):
    server = ThreadingHTTPServer(('0.0.0.0', port), Resquest)
    server.serve_forever()

import http.server
import socketserver
import json
import urllib.parse
import importlib
import sys
import io
import traceback
import os

PORT = 8001
DIRECTORY = "docs/atlas"

class AtlasHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/run':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                module_name = data.get('module')
                function_name = data.get('function')
                args_list = data.get('args', [])
                kwargs_dict = data.get('kwargs', {})

                # Ensure src is in path so we can import from it
                src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                if src_path not in sys.path:
                    sys.path.insert(0, src_path)

                # Capture stdout
                old_stdout = sys.stdout
                redirected_output = sys.stdout = io.StringIO()

                try:
                    # Dynamically import module and get function
                    module = importlib.import_module(module_name)
                    # Reload module to get latest code changes without restarting server
                    importlib.reload(module)
                    
                    func = getattr(module, function_name)
                    
                    # Execute function
                    result = func(*args_list, **kwargs_dict)
                    
                    output = redirected_output.getvalue()
                    
                    response = {
                        "status": "success",
                        "output": output,
                        "result": repr(result)
                    }
                except Exception as e:
                    output = redirected_output.getvalue()
                    error_trace = traceback.format_exc()
                    response = {
                        "status": "error",
                        "output": output,
                        "error": str(e),
                        "traceback": error_trace
                    }
                finally:
                    # Restore stdout
                    sys.stdout = old_stdout

            except json.JSONDecodeError:
                response = {"status": "error", "error": "Invalid JSON payload"}
            except Exception as e:
                response = {"status": "error", "error": str(e), "traceback": traceback.format_exc()}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # Add CORS headers just in case
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            super().do_POST()

    # Allow CORS preflight requests
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Change working directory so that relative paths in the app still work
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

with socketserver.TCPServer(("", PORT), AtlasHandler) as httpd:
    print(f"Atlas Active Server started at http://localhost:{PORT}")
    print("Serving UI from docs/atlas/ and listening for Execution API on /run")
    httpd.serve_forever()

import subprocess
import json
from pathlib import Path
from typing import Dict
from fastapi import FastAPI
from fastapi.responses import JSONResponse

TEST_EXTRACT_FILE_PATH = str(Path(__file__).parent.parent) + "/tests/test_extract.py"
TEST_TRANSFORM_FILE_PATH = str(Path(__file__).parent.parent) + "/tests/test_transform.py"
TEST_EXTRACT_RESULT_FILE_PATH = "./fastapi/tmp/test-extract-result.json"
TEST_TRANSFORM_RESULT_FILE_PATH = "./fastapi/tmp/test-transform-result.json"

def get_response_from_pytest(test_result_file_path :str, test_file_path:str) -> Dict:
    try: 
        subprocess.run(['pytest',f'--json={test_result_file_path}',f'{test_file_path}'])
        with open(f'{test_result_file_path}', 'r') as f:
            result = json.load(f)
            if 'failed' not in result['report']['summary'] and result['report']['summary']['num_tests'] > 0:
                response = JSONResponse(content=result, status_code=200)
            else:
                response = JSONResponse(content=result, status_code=206)
    except Exception as e:
        print(f"Error::: {e}")
        response = JSONResponse(content={"error:": f"{e}"}, status_code=500)
    
    return response

app = FastAPI()

@app.get('/api/v1/test-extract')
def run_tests():
    return get_response_from_pytest(TEST_EXTRACT_RESULT_FILE_PATH, TEST_EXTRACT_FILE_PATH)

@app.get('/api/v1/test-transform')
def run_tests():
    return get_response_from_pytest(TEST_TRANSFORM_RESULT_FILE_PATH, TEST_TRANSFORM_FILE_PATH)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
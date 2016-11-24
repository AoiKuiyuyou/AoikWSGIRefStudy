# AoikWSGIRefStudy
Python **wsgiref** library study.

Tested working with:
- Python 2.7 and 3.5

Trace call using [AoikTraceCall](https://github.com/AoiKuiyuyou/AoikTraceCall):
- [WSGIRequestHandlerTraceCall.py](/src/WSGIRequestHandlerTraceCall.py)
- [WSGIRequestHandlerTraceCallLogPy2.txt](/src/WSGIRequestHandlerTraceCallLogPy2.txt?raw=True)
- [WSGIRequestHandlerTraceCallLogPy3.txt](/src/WSGIRequestHandlerTraceCallLogPy3.txt?raw=True)
- [WSGIRequestHandlerTraceCallNotesPy2.txt](/src/WSGIRequestHandlerTraceCallNotesPy2.txt?raw=True)
- [WSGIRequestHandlerTraceCallNotesPy3.txt](/src/WSGIRequestHandlerTraceCallNotesPy3.txt?raw=True)

## Table of Contents
- [Set up AoikTraceCall](#set-up-aoiktracecall)
  - [Setup via pip](#setup-via-pip)
  - [Setup via git](#setup-via-git)
- [Usage](#usage)
  - [Start server](#start-server)
  - [Send request](#send-request)

## Set up AoikTraceCall
- [Setup via pip](#setup-via-pip)
- [Setup via git](#setup-via-git)

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikTraceCall
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikTraceCall

cd AoikTraceCall

python setup.py install
```

## Usage
- [Start server](#start-server)
- [Send request](#send-request)

### Start server
Run:
```
python "AoikWSGIRefStudy/src/WSGIRequestHandlerTraceCall.py" > Log.txt 2>&1
```

### Send request
Run:
```
curl -X POST -d hello http://127.0.0.1:8000/
```

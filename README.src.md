[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
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
[:toc(beg='next', indent=-1)]

## Set up AoikTraceCall
[:tod()]

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
[:tod()]

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

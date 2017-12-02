## About
Python implementation of Mikrotik RouterOS [API](https://wiki.mikrotik.com/wiki/Manual:API) protocol.
This lib currently provides some helpers for communication with RouterOS, so it's not complete "api framework".

### Usage

Example with login process and sending commands for receiving list of interfaces
can be found [here](https://github.com/mrin/miktapi/blob/master/examples/simple_interface_print.py).

Lib helpers:

```python
from miktapi.sentence import sentence_pack, sentence_unpack, SentenceUnpacker
from miktapi.helper import SentenceParser, password_encode
    
# encode command for router, returns byte string
sentence_pack(['/interface/print', '.tag=mytag', '?name=ether1'])   

# decode response from router if you have complete one sentence in appropriate format
# returns tuple('!done', '.tag=mytag', '=disabled=true', ...)
sentence_unpack(one_sentence_bytes)

# also you can decode sentences as you read bytes
# unpacker is itarable object
# returns tuple('!done', '.tag=mytag', '=disabled=true', ...) on each iteration
unpacker = SentenceUnpacker()
while True:
    readed_bytes = sock.read(2048)
    unpacker.feed(readed_bytes)
    for sentence in unpacker:
        print(sentence)
        
# if you want to parse decoded sentence (tuple) in more readable view
# returns tuple(REPLY_WORD, TAG_WORD, dict('disabled': True, ....))
reply, tag, words = SentenceParser.parse_sentence(sentence, cast_int=True, cast_bool=True)

# to encode password for login process
# challenge=from initial login response
password_encode(password, challenge)
```
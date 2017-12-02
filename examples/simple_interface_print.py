from miktapi.sentence import sentence_pack, SentenceUnpacker
from miktapi.helper import SentenceParser, password_encode
from socket import create_connection


MIKROTIK_IP = '192.168.0.1'
MIKROTIK_API_PORT = 8728
MIKROTIK_API_USERNAME = 'admin'
MIKROTIK_API_PASSWORD = '123456'
SOCKET_TIMEOUT = 3

sock = create_connection((MIKROTIK_IP, MIKROTIK_API_PORT), SOCKET_TIMEOUT)
need_close_socket = False

# initial login
sock.sendall(sentence_pack(['/login', '.tag=login']))

sentence_unpacker = SentenceUnpacker()

while True:

    data = sock.recv(4096)

    # exit loop if connection closed by Mikrotik
    if data == b'':
        break

    sentence_unpacker.feed(data)

    for sentence in sentence_unpacker:

        print('GOT=', sentence)

        reply, tag, words = SentenceParser.parse_sentence(sentence)

        # login auth
        if tag == 'login' and reply == '!done':
            challenge = words.get('ret')
            encoded_pwd = password_encode(MIKROTIK_API_PASSWORD, challenge)
            sock.sendall(
                sentence_pack([
                    '/login',
                    '=name=%s' % MIKROTIK_API_USERNAME,
                    '=response=%s' % encoded_pwd,
                    '.tag=authorize'
                ]))

        # ask interfaces when authorized successfully
        elif tag == 'authorize' and reply == '!done':
            sock.sendall(sentence_pack(['/interface/print', '.tag=interface_print']))

        # exit from loop when interface print finished or got error
        elif tag == 'interface_print' and reply == '!done' \
                or reply in ('!fatal', '!trap'):
            need_close_socket = True
            break

    if need_close_socket:
        sock.close()
        break

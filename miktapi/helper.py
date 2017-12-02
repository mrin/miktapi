from binascii import unhexlify, hexlify
from hashlib import md5
from .exceptions import ParseException


class SentenceParser(object):
    cast_map = {'yes': True, 'true': True, 'no': False, 'false': False}

    @classmethod
    def parse_sentence(cls, sentence, cast_int=True, cast_bool=True):
        reply_word = sentence[0]
        if not reply_word.startswith('!'):
            raise ParseException('Unexpected reply word')
        if len(sentence) > 1 and sentence[1].startswith('.tag'):
            tag_word = cls.parse_word(sentence[1], cast_int=False, cast_bool=False)[1]
            words = sentence[2:]
        else:
            tag_word = None
            words = sentence[1:]
        return (reply_word, tag_word, dict(cls.parse_word(w, cast_int, cast_bool) for w in words))

    @classmethod
    def parse_word(cls, word, cast_int=True, cast_bool=True):
        if word.startswith('!'):
            return ('reply_word', word)
        else:
            parts = word.split('=')
            if len(parts) == 1:
                return ('message', parts[0])
            else:
                if parts[0] == '': del parts[0]
                len_parts = len(parts)
                if len_parts == 1:
                    return (parts[0], '')
                elif len_parts == 2:
                    return (parts[0], cls._cast(parts[1], cast_int, cast_bool))
                elif len_parts > 2:
                    return [parts[0], [cls._cast(v, cast_int, cast_bool) for v in parts[1:len_parts]]]
                else:
                    raise ParseException('Unexpected word format {}'.format(word))

    @classmethod
    def _cast(cls, v, cast_int, cast_bool):
        if cast_int:
            try:
                return int(v)
            except ValueError:
                pass
        if cast_bool:
            return cls.cast_map.get(v, v)
        return v


def password_encode(password, challenge, encoding='ASCII'):
    challenge = challenge.encode(encoding, 'strict')
    challenge = unhexlify(challenge)
    password = password.encode(encoding, 'strict')
    md = md5()
    md.update(b'\x00' + password + challenge)
    password = hexlify(md.digest())
    return '00' + password.decode(encoding, 'strict')

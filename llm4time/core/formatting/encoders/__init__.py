from .encode_numeric import encode_numeric
from .encode_textual import encode_textual

from .decoders import (
    TSType,
    DECODERS,
    decode_numeric,
    decode_textual
)


ENCODERS = {
    TSType.NUMERIC: encode_numeric,
    TSType.TEXTUAL: encode_textual
}

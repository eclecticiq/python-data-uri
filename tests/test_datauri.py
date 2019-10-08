import datauri

import pytest

SAMPLE_URL_ENCODED = 'data:,A%20brief%20note'
SAMPLE_BASE64_ENCODED = (
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA'
    'AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO'
    '9TXL0Y4OHwAAAABJRU5ErkJggg==')


def test_parse_url_encoded():
    # from https://tools.ietf.org/html/rfc2397
    parsed = datauri.parse(SAMPLE_URL_ENCODED)
    assert parsed.media_type is None
    assert parsed.data == b'A brief note'
    assert parsed.uri == SAMPLE_URL_ENCODED

    parsed = datauri.parse('data:text/plain;charset=whatever,%aa%bb%cc')
    assert parsed.media_type == 'text/plain;charset=whatever'
    assert parsed.data == b'\xaa\xbb\xcc'


def test_parse_base64():
    # from https://en.wikipedia.org/wiki/Data_URI_scheme
    parsed = datauri.parse(SAMPLE_BASE64_ENCODED)
    assert parsed.media_type == 'image/png'
    assert parsed.data.startswith(b'\x89PNG')


def test_parse_base64_with_missing_padding():
    # from https://en.wikipedia.org/wiki/Base64#Output_Padding
    parsed = datauri.parse('data:text/plain;base64,YW55IGNhcm5hbCBwbGVhcw')
    assert parsed.data == b'any carnal pleas'
    parsed = datauri.parse('data:text/plain;base64,YW55IGNhcm5hbCBwbGVhc3U')
    assert parsed.data == b'any carnal pleasu'
    parsed = datauri.parse('data:text/plain;base64,YW55IGNhcm5hbCBwbGVhc3Vy')
    assert parsed.data == b'any carnal pleasur'


def test_parse_invalid():
    invalid_inputs = [
        '',
        'foobar',
        'http://not-a-data-uri',
        'data:',
        'data:text/plain;base64,Y'
    ]
    for s in invalid_inputs:
        with pytest.raises(datauri.DataURIError) as excinfo:
            datauri.parse(s)
        assert 'data uri' in str(excinfo.value)


def test_discover():
    template = """
    blah {} blah and
    {} and some more blah
    this one is incomplete data:
    and this one is malformed data:foobar
    """
    text = template.format(SAMPLE_URL_ENCODED, SAMPLE_BASE64_ENCODED)
    g = datauri.discover(text)
    actual = list(g)
    expected = [
        datauri.parse(SAMPLE_URL_ENCODED),
        datauri.parse(SAMPLE_BASE64_ENCODED)]
    assert actual == expected


@pytest.mark.parametrize('data, charset, text', [
    ('data:text/plain;charset=UTF-8;base64,0L7Qu9C10LM=', 'UTF-8', 'олег'),
    ('data:text/plain;base64,YW55IGNhcm5hbCBwbGVhc3Vy', None, 'any carnal pleasur'),
    ('data:image/png;base64,YW55IGNhcm5hbCBwbGVhc3Vy', None, None),
])
def test_text_decoding(data, charset, text):
    parsed = datauri.parse(data)
    assert parsed.charset == charset
    assert parsed.text == text


def test_container_equality():
    a = datauri.parse(SAMPLE_URL_ENCODED)
    b = datauri.parse(SAMPLE_URL_ENCODED)
    assert a == b


def test_repr():
    a = datauri.parse(SAMPLE_URL_ENCODED)
    actual = repr(a)
    expected = "<ParsedDataURI media_type=None data=b'A brief note'>"
    assert actual == expected

    b = datauri.parse(SAMPLE_BASE64_ENCODED)
    assert repr(b).endswith("...'>")


def test_is_hashable():
    a = datauri.parse(SAMPLE_URL_ENCODED)
    b = datauri.parse(SAMPLE_URL_ENCODED)
    assert hash(a) == hash(b)

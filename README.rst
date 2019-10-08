=======
datauri
=======

``datauri`` is a small Python library implementing the ``data:`` uri
scheme defined in RFC2397_. The generic format is::

  data:[<mediatype>][;base64],<data>

.. _RFC2397: https://tools.ietf.org/html/rfc2397


Installation
============

Install ``datauri`` from PyPI using::

  pip install datauri

Note: this library is for Python 3 only.


Usage
=====

.. code-block:: python

  >>> import datauri

To parse a string containing a ``data:`` uri, use ``parse()``:

.. code-block:: python

  >>> parsed = datauri.parse('data:text/plain,A%20brief%20note')

This returns a parse result:

.. code-block:: python

  >>> parsed.media_type
  'text/plain'
  >>> parsed.data
  b'A brief note'
  >>> parsed.uri
  'data:text/plain,A%20brief%20note'

This is a simple container class with a few attributes:

* The ``media_type`` attribute is a string (``str``) or ``None`` in
  case it was absent. Any (optional) embedded text encoding
  specifications are not processed in any way; it is up to the
  application to deal with that.

* The ``data`` attribute is a byte string (``bytes``) with the decoded
  data. URL encoding and base64 is handled transparently.

* For convenience, the ``uri`` attribute contains the input uri.

Parsed URIs compare equal if their media type and data are the same.
Instances are hashable, so they can be used as dictionary keys.

Parsing failures will raise a ``DataURIError``:

.. code-block:: python

  >>> datauri.parse('invalid')
  Traceback (most recent call last):
  …
  datauri.DataURIError: invalid data uri

The ``DataURIError`` subclasses the built-in ``ValueError``,
so this will work as expected:

.. code-block:: python

  try:
      datauri.parse('invalid')
  except ValueError:
      pass

You can specify ``strict=False`` to say the library to be tolerant to whitespaces:

.. code-block:: python

  >>> parsed = datauri.parse(' data: text/plain; base64, YW55IGNhcm 5hbCBwbGVhcw ')


In addition to parsing a string, this library can also discover (and
directly parse) any ``data:`` URIs found in a larger string:

.. code-block:: python

  s = 'long string with data:text/plain,A%20brief%20note and more'
  for parsed in datauri.discover(s):
      print(s)


More information
================

- RFC2397:
  https://tools.ietf.org/html/rfc2397

- Wikipedia:
  https://en.wikipedia.org/wiki/Data_URI_scheme

- Mozilla developer documentation:
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs


Known issues
============

Currently, only parsing has been implemented.


Contributing
============

Please use Github issues to report problems or propose improvements.


Version history
===============

* 1.0.0

  Initial release.


License
=======

*(This is the OSI approved 3-clause "New BSD License".)*

Copyright © 2017, EclecticIQ

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

* Neither the name of the author nor the names of its contributors may be used
  to endorse or promote products derived from this software without specific
  prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

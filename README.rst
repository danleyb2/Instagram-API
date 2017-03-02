*Please go through the*
`contribution guidelines <https://github.com/danleyb2/Instagram-API/blob/master/.github/CONTRIBUTING.md>`_. *This is
just a translated Python implementation of this PHP* `repository <https://github.com/mgp25/Instagram-API>`_.

|logo| Instagram Python
#######################

|license|

**PHP**: |latestphp| |downloadsphp|

**PYTHON:** |latestpy| |downloadspy|

This is Instagram's private API. It has all the features the Instagram app has, including media upload.

**Read the** `wiki <https://github.com/danleyb2/Instagram-API/wiki>`_ **and previous issues before opening a new one!**
Maybe your issue is already answered.

**Wiki for the PHP code should be 90% applicable too because the code is just translated, not transformed.**

**Frequently Asked Questions:** `F.A.Q. <https://github.com/danleyb2/Instagram-API/wiki/FAQ>`_

**Do you like this project? Support it by donating to the** `PHP <https://github.com/mgp25/Instagram-API>`_ **repo.**

Installation
************

PyPI
====

.. code-block:: bash

    pip install instagram-python


.. code-block:: python

    from InstagramAPI import Instagram

    instagram = Instagram()

If you want to test code that is in the master branch, which hasn't been pushed as a release, you can use Github.

.. code-block:: bash

    pip install https://github.com/danleyb2/Instagram-API/archive/master.zip

Examples
********

All examples can be found `here <https://github.com/danleyb2/Instagram-API/tree/master/examples>`_.

Why did i do the API?
*********************

For me: *I love writing code*.

For him:

    After legal measures, Facebook, WhatsApp and Instagram blocked my accounts. In order to use Instagram
    on my phone i needed a new phone, as they banned my UDID, so that is basically why i made this API.

What is Instagram?
******************

According to `the company <https://instagram.com/about/faq/>`_:

    Instagram is a fun and quirky way to share your life with friends through a series of pictures. Snap a photo with
    your mobile phone, then choose a filter to transform the image into a memory to keep around forever. We're building
    Instagram to allow you to experience moments in your friends' lives through pictures as they happen. We imagine a
    world more connected through photos."

License
*******

MIT

Terms and conditions
********************

- You will **NOT** use this API for marketing purposes (spam, massive sending...).
- We do **NOT** give support to anyone that wants this API to send massive messages or similar.
- We reserve the right to block any user of this repository that does not meet these conditions.

Legal
*****

This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by Instagram or any of its
affiliates or subsidiaries. This is an independent and unofficial API. Use at your own risk.

Contributing
************

If you have any suggestions,contributions or improvements, (unless it should only be applied on this side) please
make them to the php `repo <https://github.com/mgp25/Instagram-API>`_ if you can so i can replicate them to this
side.


.. |latestpy| image:: http://img.shields.io/pypi/v/instagram-python.svg
.. _latestpy: https://pypi.python.org/pypi/instagram-python

.. |latestphp| image:: https://poser.pugx.org/mgp25/instagram-php/v/stable
.. _latestphp: https://packagist.org/packages/mgp25/instagram-php

.. |downloadspy| image:: http://img.shields.io/pypi/dm/instagram-python.svg
.. _downloadspy: https://pypi.python.org/pypi/instagram-python

.. |downloadsphp| image:: https://poser.pugx.org/mgp25/instagram-php/downloads
.. _downloadsphp: https://packagist.org/packages/mgp25/instagram-php

.. |license| image:: https://poser.pugx.org/mgp25/instagram-php/license
.. _license: https://packagist.org/packages/mgp25/instagram-php

.. |logo| image:: /examples/assets/instagram.png

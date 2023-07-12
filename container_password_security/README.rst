.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================
Patch Password security
=======================

This module is a patch. It's a workaround to bypass an issue caused by the Mittwald Secret generator.

It seems that the Mittwald Secret generator sometimes is not putting any special characters in the password.
Since at least one special character is required by default when installing module password security,
this module sets the default for required special character to zero.

udsi - Unlimited Drive Storage Improved
=======================================

UDSI is a UDS client that is cleaner, faster, and more efficient than any existing client.

Logic
-----

- Google-type documents don't count towards Drive storage quota
- Most clients chunk data into Documents, which is slow and more apparent
- Sheets can take 50,000 characters per cell, with virtually unlimited cells, whereas Documents can handle about 1,000,000 characters total
- Centralized storage of file data in Sheets makes access easier and faster

Basic Process
-------------

Going up:
- File data is base64 encoded, resulting in a roughly 4:3 ratio
- Encoded data is broken into arrays of 10 50k character blocks
- Chunked data is formatted and submitted as a row into the dump sheet

Coming down:
- Rows are pulled sequentially from the top
- Pulled data is merged from block array into .part file
- .part file is converted to final product according to metadata
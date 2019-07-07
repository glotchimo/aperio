# UDSI - Unlimited Drive Storage Improved

UDSI is a UDS client that is cleaner, faster, and more efficient than any existing client.

### Logic

- Google documents don't count towards Drive storage quota
- Most clients chunk data into Documents, which is slow and more apparent
- Sheets can take 50,000 characters per cell, with virtually unlimited cells, whereas Documents can handle about 1,000,000 characters total
- Centralized storage of file data in Sheets makes access easier and faster

### Process

**Going up:**
- File data is base64 encoded, resulting in a roughly 4:3 size ratio.
- Encoded data is chunked into arrays of 10 50k-character blocks.
- Chunked data is formatted and added as a row into the dump sheet.

**Coming down:**
- Rows are pulled sequentially from the top of the sheet and recombined.
- Data is put in a UDSIFile object, from which it can be exported to its original state.

## Quickstart

First, install UDSI with `pip`.

    pip install udsi

As of version 0.1.0, UDSI is completely headless, so usage is in the context of Python. Also note: all of these examples are assuming you've already instantiated an authenticated Client object.

**Uploading a file:**

    from udsi.utils import build

    file = build('path/to/file')
    r = await client.upload(file)

**Retrieving, rebuilding, and exporting a file:**

    from udsi.utils import rebuild

    response, data = await client.get('file id')
    file = rebuild(response, data)
    file.export()

## Development Plan

The first priority is building a solid core upon which we can build more cool stuff. The focus right now and for the next few iterations will be tuning and expanding the core functionality (client and utilities).

That said, the next big addition will be a CLI, and following that, a GUI.

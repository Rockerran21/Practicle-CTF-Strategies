# Learning Materials

This guide teaches the techniques needed for Operation GHOST ROUTE without
revealing its specific answers.

## 1. Correlate before you decode

One alert rarely tells the whole story. Build a small timeline using fields that
survive across data sources:

- Username
- Hostname
- Source IP
- Process ID and parent process
- URL, domain, and file hash
- Timestamp

Start with the rarest event, then pivot outward. A suspicious download becomes
more meaningful when the same host launches a script interpreter and begins an
unusual DNS pattern minutes later.

## 2. Handle timestamps consistently

Convert every timestamp to one timezone before comparing events. ISO 8601 values
ending in `Z` are UTC. Never assume file order is chronological; sort on the
parsed timestamp.

## 3. Recognize DNS tunnelling patterns

Normal DNS labels are usually readable service names. Possible tunnelling often
shows:

- Many queries to one uncommon parent domain
- Long, high-entropy labels
- Sequential counters such as `00`, `01`, `02`
- A consistent source host and short time interval
- Encodings limited to hexadecimal or Base32 character sets

Base32 commonly uses uppercase `A-Z` and digits `2-7`. Padding characters may be
removed because `=` is inconvenient inside DNS labels. Restore padding until
the encoded length is divisible by eight before decoding.

## 4. Reassemble before transforming

If labels include sequence numbers, sort numerically and concatenate the data
portion. Applying a decoder to individual chunks can fail when encoding groups
cross chunk boundaries.

Example extraction logic:

```python
chunks = {int(sequence): data for sequence, data in extracted_labels}
encoded = "".join(chunks[index] for index in sorted(chunks))
```

## 5. Repeating-key XOR

Repeating-key XOR combines each byte with a cycling key:

```python
plaintext = bytes(value ^ key[i % len(key)] for i, value in enumerate(ciphertext))
```

XOR is reversible, so the same operation encrypts and decrypts. The difficult
part is identifying the key material. Look for endpoint commands or script
parameters that describe how a key was derived from another observable, such as
a file hash.

## 6. Compression signatures

Attackers often compress data before encoding it. After undoing encryption or
obfuscation, inspect the first bytes rather than assuming the result is text.
For zlib streams, common headers include `78 01`, `78 9c`, and `78 da` in hex.
Python can decompress a zlib byte string with `zlib.decompress(data)`.

## 7. Evidence quality

Separate observation from interpretation:

- Observation: host A queried 18 subdomains in 40 seconds.
- Interpretation: the pattern is consistent with DNS exfiltration.

A strong report records both and explains why benign alternatives are less
likely.

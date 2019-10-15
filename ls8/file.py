import sys
if len(sys.argv) != 2:
    print("usage: file.py <filename>", file=sys.stderr)
    sys.exit(1)
try:
    with open(sys.argv[1]) as f:
        for line in f:
            # Process comments:
            # Ignore anything after a # symbol
            comment_split = line.split("#")
            # Convert any numbers from binary strings to integers
            num = comment_split[0]
            try:
                x = int(num, 2)
            except ValueError:
                continue
            # print in binary and decimal
            print(f"{x:08b}: {x:d}")
except FileNotFoundError:
    print(f"{sys.argv[0]}: {sys.argv[1]} not found")
    sys.exit(2)
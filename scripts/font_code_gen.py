""" This script was used to generate the character code table in ../docs/font_codes.md
"""

table_header = "| Dec | Hex |    Bin    | Name |"
col_div = "| --- | --- | --------- | ---- |"
table_rows = [table_header, col_div]

for i in range(256):
    row_entry = "| {:03d} | ${:02x} | %{:08b} |      |".format(i, i, i)
    table_rows.append(row_entry)

table = "\n".join(table_rows)

with open("font_codes.md", "w") as f:
    f.write("# Font Codes\n\n")
    f.write(table)
    f.write("\n")
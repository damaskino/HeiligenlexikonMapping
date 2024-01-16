# import gzip
# import ijson
# import sys
# import json
#
# file_path = "D:\\0-MasterData\\latest-all.json.gz"
#
# with gzip.open(file_path, "rt", encoding="utf-8") as f:
#     items = ijson.items(f, "item")
#
#     for item in items:
#         print(item)
#
#         with open("mydump.json", "w", encoding="utf-8") as new_file:
#             json.dump(item, new_file)
#         break

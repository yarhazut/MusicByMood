from pathlib import Path
import os
source_path = Path("C:\Brother");

for a in source_path.glob("**/*"):
    if a.is_dir():
        newPath= a;
        for b in newPath.glob("**/*"):
            if b.is_file():
                songName =os.path.basename(b)
                path= b;

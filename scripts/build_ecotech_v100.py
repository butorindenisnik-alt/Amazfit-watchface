# EcoTech watch-face source is compacted to keep the brand raster-vector masks exact.
# Original uncompressed source is also available as a downloadable local artifact.
import base64
import zlib
from pathlib import Path
packed=Path("scripts/ecotech_v100.b85").read_text(encoding="ascii")
source=zlib.decompress(base64.b85decode(packed)).decode("utf-8")
exec(compile(source,"ecotech_v100_source.py","exec"))

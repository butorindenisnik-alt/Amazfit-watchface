# EcoTech Balance 2 v1.0.4: extend artwork to the active 480x480 pixel boundary.
# The hardware's non-emissive black bezel cannot be removed by software.
import runpy
s=runpy.run_path('scripts/build_ecotech_v103.py')['s']
patches=[["d.ellipse(pt((3,3,477,477)),fill=(3,11,17,255))","d.ellipse(pt((0,0,480,480)),fill=(3,11,17,255))"],["for radius,color,width in [(239,(48,72,82,255),1),(233,(49,69,79,255),2)]:","for radius,color,width in [(239,(0,128,151,255),2),(235,(35,93,109,255),1)]:"],["r1=239 if main else (239 if thick else 239)","r1=240 if main else (240 if thick else 240)"],["version={'code':4,'name':'1.0.3'}","version={'code':5,'name':'1.0.4'}"],["ECOTECH_Balance2_1.0.3_normal.png","ECOTECH_Balance2_1.0.4_normal.png"],["ECOTECH_Balance2_1.0.3_aod.png","ECOTECH_Balance2_1.0.4_aod.png"]]
for before, after in patches:
    assert s.count(before)==1, (before,s.count(before))
    s=s.replace(before,after)
exec(compile(s,'ecotech_v104_source.py','exec'))

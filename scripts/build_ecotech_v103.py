# EcoTech v1.0.3: no orphan weather digit; aligned seconds; fill round display edge.
import runpy
s=runpy.run_path('scripts/build_ecotech_v102.py')['s']
replacements=[["for radius,color,width in [(235,(45,57,63,255),2),(224,(32,44,52,255),2)]:","for radius,color,width in [(239,(48,72,82,255),1),(233,(49,69,79,255),2)]:"],["r0=218 if main else (224 if thick else 226)","r0=225 if main else (232 if thick else 235)"],["r1=234 if main else (234 if thick else 230)","r1=239 if main else (239 if thick else 239)"],["d.ellipse(pt((24,22,456,454)),fill=(3,11,17,255))","d.ellipse(pt((3,3,477,477)),fill=(3,11,17,255))"],[" const digits=[0,1,2,3,4,5,6,7,8,9].map(i=>'images/weather/'+i+'.png')\n w.weather=ui.createWidget(ui.widget.TEXT_IMG,{\n   x:px(374),y:px(116),w:px(50),h:px(27),type:ui.data_type.WEATHER_CURRENT,\n   font_array:digits,negative_image:'images/weather/minus.png',\n   align_h:ui.align.CENTER_H,h_space:0,show_level:N\n })\n label(420,116,12,25,17,LIGHT,'°',N)\n"," // Do not show a native WEATHER_CURRENT number here: it rendered an orphan \"1\" beside the brand.\n // The upper-right region still opens the system weather application on tap.\n"],[" w.sec=label(398,191,48,45,29,CYAN,'00',N)"," w.sec=label(397,204,59,61,37,CYAN,'00',N)"],["version={'code':3,'name':'1.0.2'}","version={'code':4,'name':'1.0.3'}"],["centered('17',(398,191,446,236),29,CYAN)","centered('17',(397,204,456,265),37,CYAN)"],["centered('24',(375,116,425,143),20,CWHITE)\n",""],["ECOTECH_Balance2_1.0.2_normal.png","ECOTECH_Balance2_1.0.3_normal.png"],["ECOTECH_Balance2_1.0.2_aod.png","ECOTECH_Balance2_1.0.3_aod.png"]]
for old, new in replacements:
    count=s.count(old)
    assert count==1, (old[:80],count)
    s=s.replace(old,new)
exec(compile(s,'ecotech_v103_source.py','exec'))

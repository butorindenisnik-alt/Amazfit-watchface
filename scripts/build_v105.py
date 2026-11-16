import base64
import json
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path("zepp-project")
ASSETS = ROOT / "assets/default-target/images"
ASSETS.mkdir(parents=True, exist_ok=True)

original = Image.open(BytesIO(base64.b64decode(Path("assets/deal_gnb_v103.jpg.b64").read_text()))).convert("RGBA")
assert original.size == (480, 480), f"Wrong source image dimensions: {original.size}"
# 7% optical zoom: remove the unused dark margin without changing screen coordinates.
bg = original.resize((512,512),Image.Resampling.LANCZOS).crop((16,16,496,496))
# Preserve the original corrected drilling geometry; modify only margins and HUD.
mask=Image.new("RGBA",(480,480),(0,0,0,0))
m=ImageDraw.Draw(mask)
# Clear the old rectangular panel, leaving the rim at left/right untouched.
m.rounded_rectangle((59,313,421,420),radius=8,fill=(2,3,6,255))
bg.alpha_composite(mask)
d=ImageDraw.Draw(bg)
WHITE=(238,241,248,255)
YELLOW=(255,199,16,255)
STEEL=(89,96,111,255)
# Compact trapezoidal HUD remains inside the circular safe area.
d.line((82,323,398,323),fill=STEEL,width=2)
d.line((117,425,363,425),fill=(53,58,67,255),width=2)
for x in (144,239,335):
    d.line((x,340,x,411),fill=(72,77,88,255),width=2)
# Battery
d.rounded_rectangle((81,347,110,366),radius=3,outline=WHITE,width=2)
d.rectangle((111,352,115,360),fill=WHITE)
d.polygon([(96,348),(88,359),(95,358),(92,366),(104,353),(98,353)],fill=YELLOW)
# Steps icon — compact, no overlap with value underneath.
for x,y,rx,ry in [(177,346,10,14),(192,347,11,14),(174,359,9,11),(191,361,9,11)]:
    d.ellipse((x,y,x+rx,y+ry),fill=YELLOW)
# Heart
d.polygon([(289,373),(270,355),(272,345),(280,344),(288,349),(296,344),(306,347),(307,356)],fill=YELLOW)
d.line([(274,355),(282,355),(285,350),(289,361),(294,355),(303,355)],fill=(8,10,14,255),width=2)
# Weather icon
d.ellipse((378,342,398,362),outline=YELLOW,width=3)
d.ellipse((367,353,386,370),fill=(8,10,15,255),outline=WHITE,width=2)
d.ellipse((379,352,402,373),fill=(8,10,15,255),outline=WHITE,width=2)
d.rounded_rectangle((365,362,406,375),radius=6,fill=(8,10,15,255),outline=WHITE,width=2)
# Repaint a fine lower rim that the old rectangular HUD partly obscured.
d.arc((12,12,468,468),start=22,end=158,fill=(177,183,194,255),width=2)
bg.convert("RGB").save(ASSETS/"background.png", optimize=True)
# Native numeric glyphs for weather in watchface data_type WEATHER_CURRENT.
from PIL import ImageFont
font_paths=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
glyphdir=ASSETS/"weather"
glyphdir.mkdir(exist_ok=True)
for char in "0123456789":
    layer=Image.new("RGBA",(19,34),(0,0,0,0))
    draw=ImageDraw.Draw(layer)
    ft=next((ImageFont.truetype(p,25) for p in font_paths if Path(p).exists()),ImageFont.load_default())
    bounds=draw.textbbox((0,0),char,font=ft)
    draw.text(((19-(bounds[2]-bounds[0]))/2-bounds[0],(34-(bounds[3]-bounds[1]))/2-bounds[1]),char,font=ft,fill=WHITE)
    layer.save(glyphdir/(char+".png"))
minus=Image.new("RGBA",(13,34),(0,0,0,0))
ImageDraw.Draw(minus).line((2,18,11,18),fill=WHITE,width=3)
minus.save(glyphdir/"minus.png")
# Premium black AOD, minimal yellow line and industrial silhouette.
aod=Image.new("RGBA",(480,480),(0,0,0,255))
ad=ImageDraw.Draw(aod)
ad.arc((47,47,433,433),start=192,end=348,fill=(72,80,94,255),width=2)
ad.line([(95,182),(385,182)],fill=(255,190,0,255),width=2)
ad.rounded_rectangle((142,149,182,159),radius=3,fill=(255,190,0,255))
ad.line((171,154,220,180),fill=(185,193,205,255),width=2)
ad.line((173,162,218,184),fill=(255,190,0,255),width=2)
ad.line((220,182,265,194),fill=(255,190,0,255),width=2)
ad.line((265,194,323,194),fill=(255,190,0,255),width=2)
ad.rounded_rectangle((141,159,181,165),radius=3,fill=(80,85,94,255))
aod.save(ASSETS/"aod_bg.png")

APP={
  "configVersion":"v3",
  "app":{
    "appId":7761421, "appName":"DEAL_GNB Balance 2",
    "appType":"watchface", "version":{"code":6,"name":"1.0.5"},
    "vender":"DEAL_GNB",
    "description":"Expanded dial artwork, native current temperature and premium AOD",
    "icon":"images/background.png"
  },
  "permissions":["data:user.hd.step","data:user.hd.heart_rate"],
  "runtime":{"apiVersion":{"compatible":"2.0","target":"4.2","minVersion":"2.0"}},
  "targets":{
    "default-target":{
      "module":{"watchface":{
        "path":"watchface/default-target/index",
        "main":1,"editable":0,"lockscreen":1
      }},
      "platforms":[
        {"name":"Amazfit Balance 2","deviceSource":9568512},
        {"name":"Amazfit Balance 2","deviceSource":9568513},
        {"name":"Amazfit Balance 2","deviceSource":9568515}
      ],
      "designWidth":480
    }
  },
  "i18n":{"ru-RU":{"name":"DEAL_ГНБ Balance 2"},"en-US":{"name":"DEAL_GNB Balance 2"}},
  "defaultLanguage":"ru-RU",
  "debug":False
}
(ROOT/"app.json").write_text(json.dumps(APP,ensure_ascii=False,indent=2),encoding="utf-8")
(ROOT/"app.js").write_text("App({globalData:{},onCreate(){},onDestroy(){}})\n",encoding="utf-8")
SCRIPT=r"""
import ui from '@zos/ui'
import { px } from '@zos/utils'
import { Time, Battery, Step, HeartRate, Weather } from '@zos/sensor'

const NL=ui.show_level.ONLY_NORMAL
const AL=ui.show_level.ONAL_AOD
const WHITE=0xF4F4F8, YELLOW=0xFFD21A
const WD=['','ПН','ВТ','СР','ЧТ','ПТ','СБ','ВС']
const MONTH=['','ЯНВ','ФЕВ','МАР','АПР','МАЙ','ИЮН','ИЮЛ','АВГ','СЕН','ОКТ','НОЯ','ДЕК']
function z(n){return String(n).padStart(2,'0')}
function label(x,y,w,h,size,color,text,level){
  return ui.createWidget(ui.widget.TEXT,{
    x:px(x),y:px(y),w:px(w),h:px(h),
    text:String(text),color,text_size:px(size),
    text_style:ui.text_style.NONE,
    align_h:ui.align.CENTER_H,align_v:ui.align.CENTER_V,show_level:level
  })
}
function set(w,val){if(w)w.setProperty(ui.prop.TEXT,String(val))}
function safe(fn){try{fn()}catch(err){}}
let widgets={}, timeSensor
WatchFace({
  build(){
    timeSensor=new Time()
    // Exact physical 480x480 screen coordinates.
    ui.createWidget(ui.widget.IMG,{
      x:0,y:0,w:480,h:480,
      src:'images/background.png',auto_scale:true,auto_scale_obj_fit:true,
      show_level:NL
    })
    // The time is larger than before; lower values are under their corresponding icons.
    widgets.clock=label(11,182,458,112,111,WHITE,'00:00',NL)
    widgets.date=label(55,290,370,36,23,YELLOW,'',NL)
    widgets.bat=label(59,378,80,38,27,WHITE,'--%',NL)
    widgets.steps=label(145,378,96,38,27,WHITE,'--',NL)
    widgets.heart=label(240,378,96,38,27,WHITE,'--',NL)
    // Native Zepp watch-face temperature binding. Avoid the deprecated app sensor.
    const digits=[0,1,2,3,4,5,6,7,8,9].map(n=>'images/weather/'+n+'.png')
    widgets.weather=ui.createWidget(ui.widget.TEXT_IMG,{
      x:px(338),y:px(382),w:px(96),h:px(34),
      type:ui.data_type.WEATHER_CURRENT,
      font_array:digits,negative_image:'images/weather/minus.png',
      align_h:ui.align.CENTER_H,h_space:0,show_level:NL
    })
    label(405,378,16,38,23,WHITE,'°',NL)

    // Independent screen-off artwork; no full-colour HUD in Always-On mode.
    ui.createWidget(ui.widget.IMG,{
      x:0,y:0,w:480,h:480,
      src:'images/aod_bg.png',
      auto_scale:true,auto_scale_obj_fit:true,
      show_level:AL
    })
    label(114,111,252,40,25,YELLOW,'DEAL_ГНБ',AL)
    widgets.aodClock=label(26,183,428,128,112,WHITE,'00:00',AL)
    widgets.aodDate=label(92,310,296,36,23,YELLOW,'',AL)

    const refresh=()=>{
      const t=z(timeSensor.getHours())+':'+z(timeSensor.getMinutes())
      const day=z(timeSensor.getDate())+' '+MONTH[timeSensor.getMonth()]+' '+timeSensor.getFullYear()+'  '+(WD[timeSensor.getDay()]||'')
      const shortday=z(timeSensor.getDate())+' '+MONTH[timeSensor.getMonth()]
      set(widgets.clock,t);set(widgets.date,day)
      set(widgets.aodClock,t);set(widgets.aodDate,shortday)
    }
    refresh()
    safe(()=>timeSensor.onPerMinute(refresh))
    safe(()=>{
      const s=new Battery()
      const render=()=>set(widgets.bat,s.getCurrent()+'%')
      render();s.onChange(render)
    })
    safe(()=>{
      const s=new Step()
      const render=()=>set(widgets.steps,s.getCurrent())
      render();s.onChange(render)
    })
    safe(()=>{
      const s=new HeartRate()
      const render=()=>{
        const v=s.getLast()
        set(widgets.heart,Number.isFinite(v)&&v>0?v:'--')
      }
      render();s.onLastChange(render)
    })

  }
})
"""
dest=ROOT/"watchface/default-target/index.js"
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(SCRIPT.strip()+"\n",encoding="utf-8")
Path("previews").mkdir(exist_ok=True)
bg.convert("RGB").save("previews/DEAL_GNB_v1.0.5_background.png",optimize=True)
aod.save("previews/DEAL_GNB_v1.0.5_aod.png",optimize=True)
print("Built source; background", (ASSETS/"background.png").stat().st_size,
      "app lockscreen",APP["targets"]["default-target"]["module"]["watchface"]["lockscreen"])

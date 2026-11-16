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
bg = original.copy()
# Preserve the corrected rig and its drilling head. The chassis/rod is NOT redrawn.
# Replace only the lower HUD whose older icons and digits overlapped.
mask = Image.new("RGBA", (480, 480), (0,0,0,0))
md = ImageDraw.Draw(mask)
md.rounded_rectangle((40,300,440,436),radius=16,fill=(3,5,10,255))
bg.alpha_composite(mask)
d = ImageDraw.Draw(bg)
WHITE=(235,238,244,255)
YELLOW=(255,202,22,255)
BORDER=(100,108,124,255)
# Luminous framing is drawn beneath the live data, in the same 480px grid.
d.line([(48,330),(432,330)],fill=BORDER,width=2)
d.rounded_rectangle((42,332,438,437),radius=16,outline=BORDER,width=2)
centers=(94,193,288,387)
for x in (143,239,338):
    d.line((x,340,x,422), fill=(64,69,80,255),width=2)
# Icons centered precisely above their own numbers.
# battery
d.rounded_rectangle((74,346,109,365),radius=3,outline=WHITE,width=3)
d.rectangle((110,353,115,359),fill=WHITE)
d.polygon([(92,347),(85,357),(92,357),(89,365),(101,352),(95,352)],fill=YELLOW)
# steps
d.ellipse((180,343,192,355),fill=YELLOW)
d.ellipse((197,347,207,360),fill=YELLOW)
d.ellipse((176,358,186,369),fill=YELLOW)
d.ellipse((192,359,202,372),fill=YELLOW)
# heart
d.polygon([(288,373),(272,357),(270,347),(277,343),(287,348),(297,343),(306,348),(305,358)],fill=YELLOW)
d.line((274,355,282,355,285,349,290,361,295,355,303,355),fill=(9,11,16,255),width=2)
# weather
d.ellipse((383,344,401,362),outline=YELLOW,width=3)
d.ellipse((365,352,385,368),fill=(9,11,16,255),outline=WHITE,width=3)
d.ellipse((377,352,399,369),fill=(9,11,16,255),outline=WHITE,width=3)
d.rounded_rectangle((363,361,407,374),radius=6,fill=(9,11,16,255),outline=WHITE,width=2)
# Keep the outer dial ring visible; no geometric resize of the 480x480 asset.
bg.convert("RGB").save(ASSETS/"background.png",optimize=True)

APP={
  "configVersion":"v3",
  "app":{
    "appId":7761421, "appName":"DEAL_GNB Balance 2",
    "appType":"watchface", "version":{"code":5,"name":"1.0.4"},
    "vender":"DEAL_GNB",
    "description":"Expanded centered dial HUD, weather forecast and custom AOD",
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
    widgets.clock=label(19,183,442,118,105,WHITE,'00:00',NL)
    widgets.date=label(58,293,364,36,22,YELLOW,'',NL)
    widgets.bat=label(46,386,96,40,27,WHITE,'--%',NL)
    widgets.steps=label(143,386,100,40,26,WHITE,'--',NL)
    widgets.heart=label(239,386,98,40,27,WHITE,'--',NL)
    widgets.weather=label(337,386,102,40,19,WHITE,'--°',NL)

    // AOD is a separate logical layer. app.json lockscreen MUST equal 1.
    ui.createWidget(ui.widget.FILL_RECT,{
      x:0,y:0,w:480,h:480,color:0x000000,show_level:AL
    })
    widgets.aodClock=label(62,198,356,100,81,WHITE,'00:00',AL)
    widgets.aodDate=label(128,304,224,30,18,YELLOW,'',AL)
    label(142,352,196,24,18,YELLOW,'DEAL_ГНБ',AL)

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
    // Zepp watchface Weather provides the day forecast high/low.
    // Display a forecast range, NOT a fabricated instantaneous temperature.
    safe(()=>{
      const s=new Weather()
      const render=()=>{
        const r=s.getForecastWeather()
        const it=r&&r.forecastData&&r.forecastData.data&&r.forecastData.data[0]
        if(it&&Number.isFinite(it.high)&&Number.isFinite(it.low)){
          set(widgets.weather,Math.round(it.low)+'/'+Math.round(it.high)+'°')
        }
      }
      render()
    })
  }
})
"""
dest=ROOT/"watchface/default-target/index.js"
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(SCRIPT.strip()+"\n",encoding="utf-8")
Path("previews").mkdir(exist_ok=True)
bg.convert("RGB").save("previews/DEAL_GNB_v1.0.4_background.png",optimize=True)
print("Built source; background", (ASSETS/"background.png").stat().st_size,
      "app lockscreen",APP["targets"]["default-target"]["module"]["watchface"]["lockscreen"])

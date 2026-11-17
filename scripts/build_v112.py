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
# Remove the curved comet/swoosh printed ABOVE the DEAL_ГНБ logo.
# Restrict restoration to the small arc strip: the logo itself starts lower
# and the drilling rig/ground remain completely untouched.
# The surrounding background in this band is nearly black.
from PIL import ImageStat
clean_color = tuple(int(v) for v in ImageStat.Stat(bg.crop((154,29,168,48)).convert("RGB")).median)
clean = Image.new("RGBA", (172, 30), (*clean_color, 255))
# Feather boundaries 3px to avoid any rectangular seam in dark dial.
arc_mask=Image.new("L",(172,30),0)
arc_draw=ImageDraw.Draw(arc_mask)
arc_draw.rounded_rectangle((4,4,167,26),radius=5,fill=255)
arc_mask=arc_mask.filter(ImageFilter.GaussianBlur(2))
bg.paste(clean,(165,22),arc_mask)
# Remove legacy HUD borders, which remained under the battery frame.
# Mask only the INTERNAL dial below the date: keep the outer index ring intact.
clean=Image.new("RGBA",(480,480),(0,0,0,0))
clean_mask=Image.new("L",(480,480),0)
mask_draw=ImageDraw.Draw(clean_mask)
mask_draw.ellipse((31,31,449,449),fill=255)
mask_draw.rectangle((0,0,480,306),fill=0)
# Ink black just inside the ring, not across tick marks.
clean.paste((3,4,9,255),(0,0,480,480))
bg.paste(clean,(0,0),clean_mask)
d=ImageDraw.Draw(bg)
WHITE=(238,241,248,255)
YELLOW=(255,199,16,255)
STEEL=(87,95,109,255)
# A single thin top divider and distinct vertical column dividers.
d.line((91,327,389,327),fill=STEEL,width=2)
for x in (164,252,344):
    d.line((x,343,x,410),fill=(66,71,82,255),width=2)
# No bottom or oblique contour crosses the battery percentage or the ring.
# Four pictograms are centered within the safe circular bottom zone.
# Battery
d.rounded_rectangle((118,342,145,360),radius=3,outline=WHITE,width=2)
d.rectangle((146,348,150,356),fill=WHITE)
d.polygon([(132,344),(124,353),(131,353),(128,360),(141,350),(136,350)],fill=YELLOW)
# Steps
for x,y,rx,ry in [(182,341,10,14),(198,341,11,14),(178,355,9,11),(195,358,9,11)]:
    d.ellipse((x,y,x+rx,y+ry),fill=YELLOW)
# Heart
d.polygon([(289,366),(272,353),(273,344),(281,341),(289,346),(296,341),(307,345),(306,353)],fill=YELLOW)
d.line([(277,350),(283,350),(286,345),(290,356),(295,350),(302,350)],fill=(8,10,14,255),width=2)
# Weather
d.ellipse((365,340,383,357),outline=YELLOW,width=2)
d.ellipse((349,348,366,364),fill=(8,10,15,255),outline=WHITE,width=2)
d.ellipse((360,350,383,369),fill=(8,10,15,255),outline=WHITE,width=2)
d.rounded_rectangle((348,356,388,369),radius=6,fill=(8,10,15,255),outline=WHITE,width=2)
bg.convert("RGB").save(ASSETS/"background.png",optimize=True)
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
# AOD design based on approved premium industrial concept. All clock digits are
# DYNAMIC images in IMG_TIME; never bake a static clock into the background.
aod=Image.new("RGBA",(480,480),(0,0,0,255))
ad=ImageDraw.Draw(aod)
Y=(252,198,20,255)
S=(230,233,240,255)
# Large DEAL_ГНБ logo without curved decoration. Nothing above it.
fbold=next((p for p in font_paths if Path(p).exists()),None)
def get_font(n):
    return ImageFont.truetype(fbold,n) if fbold else ImageFont.load_default()
ft=get_font(45)
w1=ad.textlength("DEAL_",font=ft)
w2=ad.textlength("ГНБ",font=ft)
x=(480-w1-w2)/2
ad.text((x,62),"DEAL_",font=ft,fill=S)
ad.text((x+w1,62),"ГНБ",font=ft,fill=Y)
# Real corrected rig from original artwork. Alpha derived from luminosity makes
# surrounding black unobtrusive and avoids a rectangular background.
source=original.crop((58,90,426,187)).resize((400,106),Image.Resampling.LANCZOS)
lum=source.convert("L").point(lambda z: max(0,min(255,int((z-10)*1.6))))
source.putalpha(lum)
aod.alpha_composite(source,(40,125))
ad=ImageDraw.Draw(aod)
ad.line((69,205,411,205),fill=Y,width=3)
ad.line((69,205,94,205),fill=(155,160,169,255),width=2)
# Colon belongs to the fixed art, the four outline digits are automatic.
ad.rounded_rectangle((229,269,242,283),radius=3,fill=Y)
ad.rounded_rectangle((229,314,242,328),radius=3,fill=Y)
ad.line((85,355,161,355),fill=Y,width=2)
ad.line((319,355,395,355),fill=Y,width=2)
ad.line((122,445,194,445),fill=(130,138,149,255),width=2)
ad.line((286,445,358,445),fill=(130,138,149,255),width=2)
aod.save(ASSETS/"aod_bg.png")

# System-drawn outlined gold numerals in AOD (0-9); black empty interior.
outdir=ASSETS/"aod_digits"
outdir.mkdir(exist_ok=True)
for number in range(10):
    layer=Image.new("RGBA",(82,135),(0,0,0,0))
    dd=ImageDraw.Draw(layer)
    f=get_font(119)
    bb=dd.textbbox((0,0),str(number),font=f,stroke_width=4)
    xx=(82-(bb[2]-bb[0]))/2-bb[0]
    yy=(135-(bb[3]-bb[1]))/2-bb[1]
    dd.text((xx,yy),str(number),font=f,fill=(0,0,0,255),stroke_width=4,stroke_fill=Y)
    layer.save(outdir/(str(number)+".png"))
# Static AOD reference preview for visual check only (not bundled as watch face).
reference=aod.copy()
for n,xx in zip("2323",[47,129,270,352]):
    reference.alpha_composite(Image.open(outdir/(n+".png")),(xx,218))
rad=ImageDraw.Draw(reference)
fd=get_font(40)
date="16.11"
tw=rad.textlength(date,font=fd)
rad.text(((480-tw)/2,363),date,font=fd,fill=S)
fw=get_font(23)
weekday="ПОНЕДЕЛЬНИК"
tw=rad.textlength(weekday,font=fw)
rad.text(((480-tw)/2,413),weekday,font=fw,fill=Y)

# One transparent image for watchface touch overlays.
Image.new("RGBA",(1,1),(0,0,0,0)).save(ASSETS/"tap_clear.png")

APP={
  "configVersion":"v3",
  "app":{
    "appId":7761421, "appName":"DEAL_GNB Balance 2",
    "appType":"watchface", "version":{"code":13,"name":"1.1.2"},
    "vender":"DEAL_GNB",
    "description":"Four tappable areas: timer, calendar, heart rate and weather",
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
import { Time, Battery, Step, HeartRate } from '@zos/sensor'
import * as timer from '@zos/timer'
import { launchApp, SYSTEM_APP_COUNTDOWN, SYSTEM_APP_HR, SYSTEM_APP_WEATHER, SYSTEM_APP_CALENDAR } from '@zos/router'

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
    widgets.clock=label(13,183,421,116,124,WHITE,'00:00',NL)
    widgets.seconds=label(375,229,76,70,43,YELLOW,'00',NL)
    widgets.date=label(55,290,370,36,23,YELLOW,'',NL)
    widgets.bat=label(106,369,60,40,21,WHITE,'--%',NL)
    widgets.steps=label(166,369,77,40,25,WHITE,'--',NL)
    widgets.heart=label(260,369,70,40,25,WHITE,'--',NL)
    // Native Zepp watch-face temperature binding. Avoid the deprecated app sensor.
    const digits=[0,1,2,3,4,5,6,7,8,9].map(n=>'images/weather/'+n+'.png')
    widgets.weather=ui.createWidget(ui.widget.TEXT_IMG,{
      x:px(332),y:px(373),w:px(53),h:px(33),
      type:ui.data_type.WEATHER_CURRENT,
      font_array:digits,negative_image:'images/weather/minus.png',
      align_h:ui.align.CENTER_H,h_space:0,show_level:NL
    })
    label(385,371,12,35,19,WHITE,'°',NL)

    // AOD: full-screen dark artistic rig + truly dynamic outlined numerals.
    ui.createWidget(ui.widget.IMG,{
      x:0,y:0,w:480,h:480,src:'images/aod_bg.png',
      auto_scale:true,auto_scale_obj_fit:true,show_level:AL
    })
    const contours=[0,1,2,3,4,5,6,7,8,9].map(n=>'images/aod_digits/'+n+'.png')
    ui.createWidget(ui.widget.IMG_TIME,{
      hour_startX:px(47),hour_startY:px(218),
      hour_array:contours,hour_space:0,hour_zero:1,hour_align:ui.align.LEFT,
      minute_startX:px(270),minute_startY:px(218),
      minute_array:contours,minute_space:0,minute_zero:1,
      minute_align:ui.align.LEFT,minute_follow:0,show_level:AL
    })
    widgets.aodDate=label(110,357,260,51,41,WHITE,'16.11',AL)
    widgets.aodWeek=label(40,409,400,43,24,YELLOW,'ПОНЕДЕЛЬНИК',AL)

    const FULL=['','ПОНЕДЕЛЬНИК','ВТОРНИК','СРЕДА','ЧЕТВЕРГ','ПЯТНИЦА','СУББОТА','ВОСКРЕСЕНЬЕ']
    const refresh=()=>{
      const t=z(timeSensor.getHours())+':'+z(timeSensor.getMinutes())
      const day=z(timeSensor.getDate())+' '+MONTH[timeSensor.getMonth()]+' '+timeSensor.getFullYear()+'  '+(WD[timeSensor.getDay()]||'')
      set(widgets.clock,t);set(widgets.date,day)
      set(widgets.aodDate,z(timeSensor.getDate())+'.'+z(timeSensor.getMonth()))
      set(widgets.aodWeek,FULL[timeSensor.getDay()]||'')
    }
    refresh()
    safe(()=>timeSensor.onPerMinute(refresh))
    // Seconds run in normal watchface only, never included in AOD.
    // The timer is stopped while the face is not visible when supported.
    let secTimer=null
    const secTick=()=>set(widgets.seconds,z(timeSensor.getSeconds()))
    secTick()
    safe(()=>{secTimer=timer.createTimer(1000,1000,secTick,{})})

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
    // Three invisible touch zones for NORMAL display only.
    // The overlays come last so touches are not intercepted by metric labels.
    // System App IDs are official Zepp OS 3.0+ constants.
    const jump = (appId) => {
      try {
        launchApp({ appId, native: true })
      } catch (e) {
        // Do not break the watchface if a system shortcut is unavailable.
      }
    }
    const tapZone=(x,y,w,h,appId)=>{
      const overlay=ui.createWidget(ui.widget.IMG,{
        x:px(x),y:px(y),w:px(w),h:px(h),
        src:'images/tap_clear.png',show_level:NL,
        enable:true
      })
      overlay.addEventListener(ui.event.CLICK_UP,()=>jump(appId))
      return overlay
    }
    // Main clock: right-hand minutes only, NOT hours or little seconds.
    tapZone(255,202,117,84,SYSTEM_APP_COUNTDOWN)
    // Bottom two individual complications: avoid neighbouring dividers.
    tapZone(258,338,74,75,SYSTEM_APP_HR)
    tapZone(340,338,74,75,SYSTEM_APP_WEATHER)
    // Centered date band: avoids minutes (ending y286) and other metrics.
    tapZone(85,287,310,43,SYSTEM_APP_CALENDAR)

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
bg.convert("RGB").save("previews/DEAL_GNB_v1.1.2_background.png",optimize=True)
reference.save("previews/DEAL_GNB_v1.1.2_aod.png",optimize=True)
print("Built source; background", (ASSETS/"background.png").stat().st_size,
      "app lockscreen",APP["targets"]["default-target"]["module"]["watchface"]["lockscreen"])

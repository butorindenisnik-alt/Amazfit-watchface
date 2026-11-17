# EcoTech Balance 2 v1.0.6 — fix intermittent one-hour lag on normal screen.
# AOD already uses the firmware-managed IMG_TIME. The normal face now does too.
# This avoids JS onPerMinute missing an hour rollover while the watch wakes from AOD.
from pathlib import Path
import runpy, json
from PIL import Image, ImageDraw, ImageFont

runpy.run_path('scripts/build_ecotech_v105.py')

root=Path('zepp-project')
assets=root/'assets/default-target/images'
js_path=root/'watchface/default-target/index.js'
app_path=root/'app.json'
js=js_path.read_text(encoding='utf-8')

old_hours=" w.hours=label(40,155,168,114,114,LIGHT,'00',N)"
old_minutes=" w.minutes=label(236,155,166,114,114,CYAN,'00',N)"
old_update="   upd(w.hours,pad(t.getHours()));upd(w.minutes,pad(t.getMinutes()))"
for old in (old_hours,old_minutes,old_update):
    assert js.count(old)==1, ('Cannot locate expected clock code',old)

# One native clock widget for BOTH hour and minute: exactly the same mechanism
# that has proved reliable on the Always-On Display of these watches.
native_clock=""" const hourImages=[0,1,2,3,4,5,6,7,8,9].map(i=>'images/normal_time/hour/'+i+'.png')
 const minuteImages=[0,1,2,3,4,5,6,7,8,9].map(i=>'images/normal_time/minute/'+i+'.png')
 ui.createWidget(ui.widget.IMG_TIME,{
   hour_startX:px(40),hour_startY:px(155),hour_array:hourImages,
   hour_space:0,hour_zero:1,hour_align:ui.align.LEFT,
   minute_startX:px(236),minute_startY:px(155),minute_array:minuteImages,
   minute_space:0,minute_zero:1,minute_align:ui.align.LEFT,
   minute_follow:0,show_level:N
 })
"""
js=js.replace(old_hours,native_clock)
js=js.replace(old_minutes," // Minutes displayed by the system clock widget above.")
js=js.replace(old_update,"   // Hour/minute digits are firmware-managed; refresh only date labels here.")

# Keep the one-second seconds widget; it is independent of the clock and AOD.
# When the watch wakes from AOD, its normal time no longer depends on JS callbacks.
assert js.count('ui.widget.IMG_TIME')==2
assert 'upd(w.hours' not in js and 'upd(w.minutes' not in js
assert 't.getHours()' not in js
assert 't.onPerMinute(refresh)' in js
assert "w.sec=label(397,204,59,61,37,CYAN,'00',N)" in js
assert js.count('hit(')==4
js_path.write_text(js,encoding='utf-8')

fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fontfile=fontfile if Path(fontfile).exists() else '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf'
assert Path(fontfile).exists(), 'Missing bold font for the native digital clock digits'

def make_digit(char, width, height, color, font_size):
    img=Image.new('RGBA',(width,height),(0,0,0,0))
    painter=ImageDraw.Draw(img)
    font=ImageFont.truetype(fontfile,font_size)
    bb=painter.textbbox((0,0),str(char),font=font)
    painter.text(((width-(bb[2]-bb[0]))/2-bb[0],
                  (height-(bb[3]-bb[1]))/2-bb[1]),str(char),fill=color,font=font)
    return img

# Optical widths chosen to match the previously accepted 480px layout.
# 2*84=168 px for hours, 2*83=166 px for minutes.
HOUR=(241,249,252,255)
MINUTE=(0,188,214,255)
for role,w,c in [('hour',84,HOUR),('minute',83,MINUTE)]:
    dest=assets/'normal_time'/role
    dest.mkdir(parents=True,exist_ok=True)
    for num in range(10):
        make_digit(num,w,114,c,111).save(dest/(str(num)+'.png'))

app=json.loads(app_path.read_text(encoding='utf-8'))
assert app['app']['appId']==7761543
app['app']['version']={'code':7,'name':'1.0.6'}
app['app']['description']='System-native normal and AOD clocks; no missed-hour callbacks'
app_path.write_text(json.dumps(app,ensure_ascii=False,indent=2),encoding='utf-8')

# Visual mockup of the native time at 10:24, without altering the saved background.
def put_center(draw,text,box,size,color):
    x0,y0,x1,y1=box
    font=ImageFont.truetype(fontfile,size)
    bb=draw.textbbox((0,0),text,font=font)
    x=(x0+x1-(bb[2]-bb[0]))/2-bb[0]
    y=(y0+y1-(bb[3]-bb[1]))/2-bb[1]
    draw.text((x,y),text,font=font,fill=color)

preview=Image.open(assets/'background.png').convert('RGBA')
for idx,digit in enumerate('10'):
    preview.alpha_composite(Image.open(assets/'normal_time/hour'/(digit+'.png')),(40+84*idx,155))
for idx,digit in enumerate('24'):
    preview.alpha_composite(Image.open(assets/'normal_time/minute'/(digit+'.png')),(236+83*idx,155))
draw=ImageDraw.Draw(preview)
put_center(draw,':',(198,155,242,269),101,HOUR)
put_center(draw,'17',(397,204,456,265),37,MINUTE)
put_center(draw,'ВТ, 17 НОЯ',(142,271,338,298),18,HOUR)
put_center(draw,'8 420',(81,311,177,345),24,HOUR)
put_center(draw,'87%',(212,333,268,362),20,HOUR)
put_center(draw,'72',(360,312,425,344),26,HOUR)
outdir=Path('previews')
outdir.mkdir(parents=True,exist_ok=True)
preview.convert('RGB').save(outdir/'ECOTECH_Balance2_1.0.6_normal.png',optimize=True)
Image.open(assets/'aod_bg.png').save(outdir/'ECOTECH_Balance2_1.0.6_aod.png',optimize=True)
print('EcoTech v1.0.6: native IMG_TIME drives normal hours/minutes and AOD; seconds live, 4 shortcuts intact')

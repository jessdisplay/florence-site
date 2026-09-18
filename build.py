"""Builds every Florence page from one header, one footer and per-page bodies.
Run: python3 build.py   One writer per file: never hand-edit the .html outputs."""
import re, os

NAV = [("tile.html","The Tile"),("bed.html","The Bed"),("lights.html","The Lights"),
       ("families.html","Families"),("providers.html","Providers")]

def shell(fn, title, desc, body, bar=False):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h==fn else ""}>{t}</a>' for h,t in NAV)
    barhtml = ('<div class="bar"><div class="wrap"><div><b>Home, for longer.</b><span>It notices a fall, a racing heart, a night out of bed. No camera. Nothing to wear.</span></div>'
               '<a class="btn ink" href="talk.html">Talk to us</a></div></div>') if bar else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body{' class="has-bar"' if bar else ''}>
<header class="nav"><div class="wrap"><a class="word" href="./">florence</a><nav aria-label="Main">{links}<a class="pill" href="talk.html">Talk to us</a></nav></div></header>
<main>
{body}
</main>
<footer><div class="wrap"><span>Florence. Draft site, September 2026.</span><span>Images are concept visualisations. Product in development.</span></div></footer>
{barhtml}
<script src="site.js"></script>
</body>
</html>
'''

PULSE = '<div class="pulse foot" aria-hidden="true">' + "".join(f'<i style="--h:{h}%"></i>' for h in (30,46,38,82,100,52,34,42,36,78,96,50,32,40)) + '</div>'

def top(h1, lede, img=None, alt="", cta=True, bg="var(--grey)"):
    c = '<div class="cta"><a class="btn ink" href="talk.html">Talk to us</a></div>' if cta else ""
    i = f'<img src="img/{img}" alt="{alt}" width="2400" height="1350" fetchpriority="high">' if img else '<div style="height:clamp(56px,8vw,104px)"></div>'
    return f'<section class="top" style="background:{bg}"><div class="wrap"><h1>{h1}</h1><p class="lede">{lede}</p>{c}</div>{i}</section>'

def nextup(h2, p, href, label):
    return f'<section class="close"><div class="wrap rise"><h2>{h2}</h2><p>{p}</p><div class="cta"><a class="btn ink" href="{href}">{label}</a></div></div></section>'

HOME = '''
<section class="frame"><img src="img/room-bright.jpg" alt="A bright, airy living room with a cream sofa and sheer curtains. The Florence tile sits small and quiet on the white ceiling" width="2400" height="1350" fetchpriority="high"></section>
<div class="tiles">
  <a class="ptile rise" href="tile.html"><div class="t"><h3>The Tile</h3><p>One on the ceiling. Fitted like a smoke alarm.</p><div class="cta"><span class="btn text">See the tile</span></div></div><div class="im"><img src="img/tile-hero.jpg" alt="The Florence tile floating on a pale grey background" loading="lazy"></div></a>
  <a class="ptile rise" href="bed.html"><div class="t"><h3>The Bed</h3><p>A care bed that looks like furniture.</p><div class="cta"><span class="btn text">See the bed</span></div></div><div class="im"><img src="img/bed-bright.jpg" alt="The Florence bed with walnut head and foot boards in a bright bedroom" loading="lazy"></div></a>
  <a class="ptile full rise" href="lights.html"><div class="t"><h3>The Lights</h3><p>Lighting you'd choose anyway, with the noticing built in.</p><div class="cta"><span class="btn text">See the lights</span></div></div><div class="im"><img src="img/lights-bright.jpg" alt="The Florence lights in brushed aluminium and opal glass" loading="lazy"></div></a>
</div>
'''

TILE = top("The Tile.", "One slim square on the ceiling. It notices, and tells the right person.", "tile-hero.jpg", "The Florence tile: graphite face, brushed aluminium edge, thin teal ring", bg="#F3F2F5") + f'''
<section class="sec" id="notices"><div class="wrap">
  <div class="head center rise"><h2>The moments that matter. None of the rest.</h2></div>
  <div class="bento">
    <article class="card photo c3 tallc rise"><img src="img/pathlights.jpg" alt="A hallway at night with low warm lights along the floor" loading="lazy"><div class="txt"><h3>A fall at 2 am</h3><p>It knows the minute it happens, not at nine when someone calls in.</p></div></article>
    <article class="card tint c3 rise"><div class="txt"><h3>Heart and breath</h3><p>Resting heart rate and breathing, read from across the room. No strap, no patch, no watch to charge.</p>{PULSE}</div></article>
    <article class="card c2 rise"><div class="txt"><span class="big">40 min</span><h3>Too long in the bathroom</h3><p>Time is the signal. It counts the minutes so nobody has to knock.</p></div></article>
    <article class="card c2 rise"><div class="txt"><h3>How the night went</h3><p>Sleep, restlessness and trips out of bed. A slow change over weeks is often the first sign.</p></div></article>
    <article class="card c2 rise"><div class="txt"><h3>The room itself</h3><p>Too hot, too cold, too stuffy. Comfort is health.</p><div class="chips foot"><span>Temperature</span><span>Humidity</span><span>Air quality</span></div></div></article>
  </div>
</div></section>
<section class="sec grey" id="privacy" style="text-align:center"><div class="wrap">
  <div class="head center rise"><h2>It reports the event. <span style="color:var(--ink-2)">Never the footage.</span></h2></div>
  <div class="three" style="margin-top:0">
    <div class="rise"><b>No camera</b><span>There is no picture to leak, watch or object to.</span></div>
    <div class="rise"><b>Thinks in the room</b><span>The sensing is worked out inside the tile itself.</span></div>
    <div class="rise"><b>Only the event leaves</b><span>"A fall, 2:06 am, hallway." That is the whole message.</span></div>
  </div>
</div></section>
<section class="sec"><div class="wrap two">
  <div class="pic rise" style="background:#F8F5F1"><img src="img/profile.jpg" alt="The tile seen edge-on, showing how slim it is" loading="lazy"></div>
  <div class="rise"><div class="head" style="margin-bottom:12px"><h2>Slim enough to forget.</h2></div>
    <div class="list"><div><b>One a room</b><span>No hub to find a shelf for.</span></div><div><b>Nothing to wear</b><span>So nothing to refuse, lose or forget to charge.</span></div><div><b>One quiet line of light</b><span>The only sign it's there.</span></div></div></div>
</div></section>
''' + nextup("Who gets told?", "A quiet note in the morning. A loud one only when it counts.", "families.html", "For families")

BED = top("The Bed.", "A care bed that isn't one. Solid walnut, proper linen, and every sensor a good night nurse would want.", "bed-bright.jpg", "The Florence bed with walnut head and foot boards and white linen in a bright bedroom", bg="#E9E7E8") + f'''
<section class="sec"><div class="wrap two">
  <div class="pic port rise"><img src="img/bed-detail.jpg" alt="Close-up of the walnut foot board with its rounded corner and cut-out hand hold" loading="lazy"></div>
  <div class="rise"><div class="head" style="margin-bottom:12px"><span class="eyebrow">Made like furniture</span><h2>Walnut where you'd expect steel.</h2></div>
    <div class="list"><div><b>Hand holds, not grab rails</b><span>Cut into the timber, where a hand goes anyway.</span></div><div><b>Rails that fold away</b><span>Up at night if they're needed. Out of sight by day.</span></div><div><b>Rises and lowers</b><span>Low to get in, higher to get out, right for a carer's back.</span></div></div></div>
</div></section>
<section class="sec grey"><div class="wrap">
  <div class="head center rise"><h2>The night, without a wire on anyone.</h2></div>
  <div class="bento">
    <article class="card photo c4 tallc rise"><img src="img/bed-night.jpg" alt="The bedroom at 2am with a soft warm glow under the bed lighting the floor and a pair of slippers" loading="lazy"><div class="txt"><h3>Feet on the floor</h3><p>A low light comes on under the bed the moment someone sits up to get out. Most night falls start in the dark.</p></div></article>
    <article class="card tint c2 rise"><div class="txt"><h3>Heart and breath</h3><p>Read through the mattress, all night.</p>{PULSE}</div></article>
    <article class="card c2 rise"><div class="txt"><h3>How she slept</h3><p>Hours, restlessness and time out of bed, so a slow change shows up early.</p></div></article>
    <article class="card c2 rise"><div class="txt"><h3>Moisture</h3><p>A quiet note to the carer. No alarm, no fuss, no waiting until morning.</p></div></article>
    <article class="card c2 rise"><div class="txt"><h3>Weight</h3><p>Tracked by the bed itself. Nobody has to stand on scales.</p></div></article>
  </div>
</div></section>
<section class="sec"><div class="wrap two flip">
  <div class="rise"><div class="head" style="margin-bottom:0"><h2>She gets up when she likes.</h2><p>And the people who love her know that she did.</p></div></div>
  <div class="pic port rise"><img src="img/bed-morning.jpg" alt="A woman in her eighties in a lilac cardigan sits on the edge of her walnut bed in the morning sun, putting on her slippers" loading="lazy"></div>
</div></section>
<section class="sec grey"><div class="wrap"><div class="full rise" style="background:#fff"><img src="img/bed-studio.jpg" alt="The Florence bed on a cream studio background" loading="lazy"></div><p class="fine">Concept design. Specifications in development.</p></div></section>
''' + nextup("Pair it with the lights.", "The bed knows the night. The lights know the rest of the house.", "lights.html", "See the lights")

LIGHTS = top("The Lights.", "A light first. A lookout second.", "lights-bright.jpg", "The Florence lights: ceiling light, pendant, bedside lamp, floor lamp and wall light in brushed aluminium and opal glass", bg="#EFEFF1") + '''
<section class="story"><div class="wrap rise"><p>Every room already has a light in the middle of the ceiling. <em>It has the best view in the house.</em></p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="pieces">
    <article class="piece wide rise"><div class="ph"><img src="img/ceilinglight.jpg" alt="A round ceiling light glowing warm over a calm bedroom at dusk" loading="lazy"></div><h3>Ceiling</h3><p>One in the bedroom does most of the work.</p></article>
    <article class="piece rise"><div class="ph"><img src="img/bedlamp.jpg" alt="A small opal glass bedside lamp on a walnut nightstand" loading="lazy"></div><h3>Bedside</h3><p>Closest to sleep, so it reads the night best.</p></article>
    <article class="piece rise"><div class="ph"><img src="img/pendant.jpg" alt="A thin disc pendant over a round oak dining table" loading="lazy"></div><h3>Pendant</h3><p>Over the table, where the day actually happens.</p></article>
    <article class="piece rise"><div class="ph"><img src="img/floorlamp.jpg" alt="A slender floor lamp beside a leather reading chair" loading="lazy"></div><h3>Reading</h3><p>By the favourite chair.</p></article>
    <article class="piece rise"><div class="ph"><img src="img/pathlights.jpg" alt="Small low wall lights washing a hallway floor at night" loading="lazy"></div><h3>Path</h3><p>Comes on low when feet touch the floor at night.</p></article>
    <article class="piece wide rise"><div class="ph"><img src="img/bedhead.jpg" alt="A walnut bedhead with a soft glow along its top edge" loading="lazy"></div><h3>Bedhead</h3><p>Light and sensing built into the joinery.</p></article>
  </div>
  <p class="fine">Concept collection. Designs in development.</p>
</div></section>
<section class="sec grey"><div class="wrap two">
  <div class="pic rise"><img src="img/lightmacro.jpg" alt="Underside of the ceiling light with a small graphite sensor tile at its centre" loading="lazy"></div>
  <div class="rise"><div class="head" style="margin-bottom:0"><h2>The same small tile inside.</h2><p>One sensor sits at the heart of each light. A thin line of light is the only sign it's there.</p></div><div class="cta"><a class="btn text" href="tile.html">See the tile</a></div></div>
</div></section>
''' + nextup("Then there's the bed.", "A care bed that looks like furniture.", "bed.html", "See the bed")

FAMILIES = top("Know she's okay. Without asking.", "A quiet note for you. Her independence left alone.", None, cta=False, bg="var(--white)") + '''
<section class="sec" style="padding-top:0"><div class="wrap two">
  <div class="pic port rise"><img src="img/daughter.jpg" alt="A woman in her kitchen in the morning, coffee in hand, glancing at her phone with a small relieved smile" loading="lazy"></div>
  <div class="rise"><div class="head" style="margin-bottom:0"><h2>Two kinds of message.</h2><p>A quiet one most mornings. A loud one only when it counts.</p></div>
    <div class="notes" aria-label="Example notifications">
      <div class="note"><div class="app" aria-hidden="true">f</div><b>Florence <time>7:42 am</time></b><span>Mum's up and about. She slept 7 h 10 min. All normal.</span></div>
      <div class="note alert"><div class="app" aria-hidden="true">f</div><b>Florence <time>2:06 am</time></b><span>Mum may have fallen in the hallway. Anna next door has been called.</span></div>
    </div></div>
</div></section>
<section class="sec grey"><div class="wrap"><div class="bento">
  <article class="card photo c4 rise" style="min-height:clamp(380px,36vw,520px)"><img src="img/living.jpg" alt="An older woman reads in a leather chair in a sunlit living room" loading="lazy"><div class="txt"><h3>And the good days</h3><p>Up, about and busy. The ordinary days are the ones families most want to hear about.</p></div></article>
  <article class="card c2 rise"><div class="txt"><h3>Tells the right person</h3><p>The alert goes to whoever can actually help.</p><div class="chips foot"><span>Family</span><span>A neighbour</span><span>Carer</span></div></div></article>
</div></div></section>
''' + nextup("No camera. Ever.", "It reports the event, never the footage.", "tile.html#privacy", "How privacy works")

PROVIDERS = top("A night shift that can be everywhere.", "For aged care and disability housing.", "bed-hero.jpg", "The Florence bed in a timber-lined room with a window seat in afternoon sun", cta=False, bg="var(--white)") + '''
<section class="sec"><div class="wrap two">
  <div class="rise"><div class="head" style="margin-bottom:12px"><h2>Fitted like a light. Forgotten like one.</h2></div>
    <div class="list"><div><b>One a room</b><span>No hub to find a shelf for.</span></div><div><b>Nothing for residents to wear</b><span>So nothing to refuse, lose or forget to charge.</span></div><div><b>Alerts that reach the floor</b><span>The right staff member, the right room, the minute it happens.</span></div><div><b>Rooms that still look like home</b><span>Families notice that on the tour.</span></div></div></div>
  <div class="pic rise" style="background:#F8F5F1"><img src="img/profile.jpg" alt="The slim Florence tile seen edge-on" loading="lazy"></div>
</div></section>
''' + nextup("Tell us about the building.", "We'll show you where Florence would go.", "talk.html", "Talk to us")

TALK = top("Talk to us.", "Tell us about the home or the building, and we'll show you where Florence would go.", None, cta=False, bg="var(--white)") + '''
<section class="sec" style="padding-top:0;text-align:center"><div class="wrap"><p class="fine" style="font-size:17px">Contact details to come. This is a draft site.</p></div></section>
'''

PAGES = [
 ("index.html","Florence","Florence quietly looks out for the people at home. No camera. Nothing to wear.",HOME,True),
 ("tile.html","The Tile · Florence","One slim square on the ceiling that notices a fall, a racing heart or a night out of bed.",TILE,False),
 ("bed.html","The Bed · Florence","A care bed that looks like furniture, with sensing in the frame and the mattress.",BED,False),
 ("lights.html","The Lights · Florence","Lighting you would choose anyway, with quiet sensing built in.",LIGHTS,False),
 ("families.html","Families · Florence","Know she's okay, without asking.",FAMILIES,False),
 ("providers.html","Providers · Florence","For aged care and disability housing: a night shift that can be everywhere.",PROVIDERS,False),
 ("talk.html","Talk to us · Florence","Get in touch with Florence.",TALK,False),
]

if __name__ == "__main__":
    allhtml = ""
    for fn,t,d,b,bar in PAGES:
        page = shell(fn,t,d,b,bar)
        assert "—" not in page and "–" not in page, fn
        open(fn,"w").write(page); allhtml += page
    used = set(re.findall(r'img/([\w-]+\.jpg)', allhtml)); have = set(os.listdir("img"))
    hrefs = set(re.findall(r'href="([\w-]+\.html)', allhtml)); pages = {p[0] for p in PAGES}
    assert not used - have, ("missing images", used - have)
    assert not hrefs - pages, ("dead links", hrefs - pages)
    print("built", len(PAGES), "pages | unused images:", sorted(have - used))

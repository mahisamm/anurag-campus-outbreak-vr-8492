"""
Injects the Blender 5.3 zombie/weapon assets and the full 6-level First-Person & Meta Quest 3 VR
Zombie Outbreak game engine into Play-PC.html (creating a backup of the original Explorer first).
"""
import base64
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_HTML = os.path.join(ROOT, "Play-PC.html")
BACKUP_HTML = os.path.join(ROOT, "Play-PC-Explorer-Backup.html")
ASSETS_JSON = os.path.join(ROOT, "zombie_assets.json")
MURAL_JPG = os.path.join(ROOT, "dblock_mural_real.jpg")
CBLOCK_MURAL_JPG = os.path.join(ROOT, "cblock_mural_real.jpg")

# =============================================================================
# DEPLOYMENT MODE SWITCH (DO NOT DELETE ZOMBIE CODE — JUST FLIP THIS FLAG!)
#   True  -> Official Guided Campus Tour Edition (Aerial Flyover + 3D Golf Cart
#            Buggy + Road-Only Tour + Live AI Voice Guide; ALL zombie/combat
#            features are completely hidden in Play-PC.html & index.html!)
#   False -> Full Zombie Outbreak FP & Meta Quest 3 VR Game (for local play!)
# =============================================================================
CAMPUS_TOUR_ONLY = True

dblock_mural_uri = ""
if os.path.exists(MURAL_JPG):
    with open(MURAL_JPG, "rb") as mf:
        dblock_mural_uri = "data:image/jpeg;base64," + base64.b64encode(mf.read()).decode("ascii")

cblock_mural_uri = ""
if os.path.exists(CBLOCK_MURAL_JPG):
    with open(CBLOCK_MURAL_JPG, "rb") as mf:
        cblock_mural_uri = "data:image/jpeg;base64," + base64.b64encode(mf.read()).decode("ascii")

# Make sure we always patch from the clean original Explorer backup if it exists
if not os.path.exists(BACKUP_HTML):
    shutil.copy2(SRC_HTML, BACKUP_HTML)
    print("Backed up original Play-PC.html -> Play-PC-Explorer-Backup.html")

with open(BACKUP_HTML, "r", encoding="utf-8") as f:
    html = f.read()

with open(ASSETS_JSON, "r", encoding="utf-8") as f:
    zombie_assets = json.load(f)

# ---------------------------------------------------------------------------
# 1. CSS additions for FPS Combat HUD, Weapon Hotbar, Boss Bar, Damage/Block Flash
# ---------------------------------------------------------------------------
EXTRA_CSS = """
#combat-hud{position:fixed;inset:0;pointer-events:none;z-index:22;display:none}
.zombie-mode #combat-hud{display:block}
.zombie-mode.active #hud-controls{display:none}
.zombie-mode #status{max-width:290px;font-size:11.5px;padding:6px 11px}
.zombie-mode #status .coords{display:none}
#combo-badge{
  position:fixed;right:16px;bottom:145px;padding:6px 14px;border-radius:10px;
  background:linear-gradient(135deg,rgba(234,88,12,0.92),rgba(220,38,38,0.92));
  border:1px solid #fde047;color:#fff;font:800 15px system-ui;letter-spacing:0.6px;
  box-shadow:0 6px 18px rgba(0,0,0,0.45);display:none;
}
#dmg-feed{
  position:fixed;left:50%;top:44%;transform:translate(-50%,-50%);
  pointer-events:none;z-index:26;text-align:center;
  font:800 16px/1.2 system-ui;color:#fef08a;text-shadow:0 2px 8px rgba(0,0,0,0.85);
  opacity:0;transition:opacity .15s,transform .15s;
}
#end-overlay{
  position:fixed;inset:0;z-index:45;display:none;align-items:center;justify-content:center;
  background:rgba(6,12,20,0.68);backdrop-filter:blur(4px);pointer-events:auto;
}
#end-overlay.won-mode{
  background:radial-gradient(circle at center,rgba(10,24,40,0.22),rgba(6,12,20,0.52));
  backdrop-filter:none;align-items:flex-end;padding-bottom:7vh;
}
#end-card{
  width:min(520px,92vw);padding:26px 28px;border-radius:16px;text-align:center;
  background:linear-gradient(160deg,rgba(14,28,42,0.92),rgba(24,16,24,0.90));
  border:1px solid rgba(114,239,221,0.55);box-shadow:0 20px 55px rgba(0,0,0,0.7);
}
#end-title{font:900 28px/1.15 system-ui;color:#ff6b6b;margin:0 0 8px}
#end-overlay.won-mode #end-title{
  font:900 clamp(44px,6.5vw,76px)/1.05 Georgia,serif;
  color:#fde047;letter-spacing:3px;
  text-shadow:0 0 28px rgba(250,204,21,0.85),0 4px 16px rgba(0,0,0,0.85);
}
#end-sub{font:800 15px/1.3 system-ui;color:#72efdd;letter-spacing:1.4px;margin-bottom:8px;display:none}
#end-overlay.won-mode #end-sub{display:block}
#end-stats{font:600 14px/1.7 system-ui;color:#d6edf8;margin:12px 0 20px}
#end-actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
#btn-restart-game,#btn-explore-campus{
  padding:11px 22px;border-radius:10px;border:none;cursor:pointer;font:800 14.5px system-ui;
}
#btn-restart-game{background:linear-gradient(135deg,#0ea5e9,#14b8a6);color:#04151f}
#btn-explore-campus{background:rgba(30,58,82,0.95);color:#e2f4ff;border:1px solid rgba(114,239,221,0.5)}
#btn-explore-campus:hover{background:rgba(48,92,126,0.98)}
#intro-overlay{
  position:fixed;inset:0;z-index:42;display:none;pointer-events:none;
  background:radial-gradient(ellipse at 50% 60%,rgba(14,165,233,0.06),rgba(2,6,14,0.48) 85%);
}
#intro-overlay.playing{display:block}
.cine-bar{
  position:fixed;left:0;right:0;height:9.5vh;background:linear-gradient(180deg,#03070e,#070d18);
  transition:transform .6s cubic-bezier(.2,.8,.2,1);pointer-events:none;
  border-color:rgba(114,239,221,0.22);
}
#cine-top{top:0;border-bottom:1px solid rgba(114,239,221,0.22)}
#cine-bot{bottom:0;border-top:1px solid rgba(114,239,221,0.22)}
#intro-progress-track{
  position:fixed;left:0;right:0;bottom:9.5vh;height:3px;background:rgba(255,255,255,0.1);z-index:44;
}
#intro-progress-fill{
  height:100%;width:0%;background:linear-gradient(90deg,#ef4444,#f59e0b,#38bdf8,#72efdd);
  box-shadow:0 0 12px rgba(114,239,221,0.9);transition:width .08s linear;
}
#intro-story-box{
  position:fixed;left:50%;bottom:12.5vh;transform:translateX(-50%);
  width:min(840px,92vw);padding:20px 28px 18px;border-radius:16px;text-align:center;
  background:linear-gradient(155deg,rgba(7,15,26,0.92),rgba(26,10,16,0.88));
  border:1px solid rgba(114,239,221,0.45);
  box-shadow:0 18px 55px rgba(0,0,0,0.75),inset 0 1px 0 rgba(255,255,255,0.12);
  backdrop-filter:blur(14px);overflow:hidden;
}
#intro-story-box::after{
  content:'';position:absolute;top:0;left:-60%;width:45%;height:100%;
  background:linear-gradient(105deg,transparent,rgba(114,239,221,0.12),transparent);
  animation:introSheen 3.2s ease-in-out infinite;pointer-events:none;
}
@keyframes introSheen{0%{left:-60%}60%,100%{left:125%}}
@keyframes beatReveal{
  0%{opacity:0;transform:translateY(10px) scale(0.96);filter:blur(4px)}
  100%{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}
}
.beat-anim{animation:beatReveal .55s cubic-bezier(.2,.85,.25,1) both}
#intro-crest{
  display:inline-flex;align-items:center;gap:8px;padding:4px 12px;border-radius:999px;
  background:rgba(239,68,68,0.16);border:1px solid rgba(251,191,36,0.5);
  margin-bottom:8px;
}
#intro-crest-badge{
  background:linear-gradient(135deg,#ef4444,#f59e0b);color:#fff;font:900 11px system-ui;
  padding:2px 7px;border-radius:5px;letter-spacing:1px;
}
#intro-kicker{font:800 11.5px/1.2 system-ui;color:#fde047;letter-spacing:2.6px;text-transform:uppercase}
#intro-headline{
  font:900 clamp(21px,2.9vw,34px)/1.12 Georgia,serif;color:#ffffff;letter-spacing:1.1px;margin:2px 0 0;
  text-shadow:0 0 24px rgba(56,189,248,0.45),0 3px 12px rgba(0,0,0,0.85);
}
#intro-divider{
  width:110px;height:2.5px;margin:9px auto 9px;border-radius:2px;
  background:linear-gradient(90deg,transparent,#ef4444,#fbbf24,#38bdf8,transparent);
}
#intro-sub{font:600 13.5px/1.45 system-ui;color:#cfeaf7;max-width:680px;margin:0 auto}
#intro-cols{
  display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px;text-align:left;
}
.intro-col{
  background:rgba(255,255,255,0.045);border:1px solid rgba(114,239,221,0.22);
  border-radius:10px;padding:8px 11px;
}
.intro-col-lbl{font:800 10px/1.2 system-ui;color:#72efdd;letter-spacing:1.4px;text-transform:uppercase;margin-bottom:3px}
.intro-col-txt{font:600 11.5px/1.35 system-ui;color:#e2f1fa}
@media (max-width:680px){#intro-cols{grid-template-columns:1fr}}
#btn-skip-intro{
  position:fixed;right:22px;bottom:2.4vh;z-index:45;pointer-events:auto;
  padding:9px 20px;border-radius:10px;border:1px solid rgba(114,239,221,0.6);
  background:linear-gradient(135deg,rgba(15,32,48,0.95),rgba(20,46,66,0.95));
  color:#e0f7fa;font:800 12.5px system-ui;letter-spacing:0.6px;cursor:pointer;
  box-shadow:0 6px 20px rgba(0,0,0,0.5);
}
#btn-skip-intro:hover{background:#0ea5e9;color:#04151f}
.intro-active #combat-hud,.intro-active #top-left-hud,.intro-active #minimap-wrap,.intro-active #crosshair,.intro-active #hint{opacity:0 !important;pointer-events:none !important}
body.zombie-mode #top-left-hud{top:108px !important;opacity:0.92}
#wave-banner{
  position:fixed;top:14px;left:50%;transform:translateX(-50%);
  padding:9px 20px;border-radius:14px;text-align:center;min-width:min(440px,46vw);
  background:linear-gradient(145deg,rgba(10,18,30,0.93),rgba(32,12,18,0.92));
  border:1px solid rgba(255,95,95,0.55);box-shadow:0 10px 30px rgba(0,0,0,0.58);
  backdrop-filter:blur(12px);
}
#wave-title{font:900 14.5px/1.2 'Segoe UI',system-ui,sans-serif;color:#ff6b6b;letter-spacing:1.3px;text-transform:uppercase}
#wave-cols{
  display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:6px;
  padding-top:6px;border-top:1px solid rgba(255,255,255,0.12);
}
.wave-col{display:flex;flex-direction:column;align-items:center}
.wave-col-k{font:700 9.5px/1.1 system-ui;color:#94a3b8;letter-spacing:1.1px;text-transform:uppercase}
.wave-col-v{font:900 13.5px/1.25 'Consolas',monospace;color:#f8fafc;margin-top:2px;font-variant-numeric:tabular-nums}
#wave-sub{display:none}
#boss-bar-wrap{
  position:fixed;top:92px;left:50%;transform:translateX(-50%);width:min(460px,62vw);
  display:none;background:rgba(16,10,14,0.92);border:1px solid rgba(245,158,11,0.75);
  border-radius:10px;padding:7px 12px;box-shadow:0 8px 24px rgba(0,0,0,0.65);
}
#boss-bar-label{font:800 12px system-ui;color:#fbbf24;letter-spacing:1.2px;display:flex;justify-content:space-between;margin-bottom:5px}
#boss-bar-bg{height:12px;background:rgba(255,255,255,0.12);border-radius:6px;overflow:hidden}
#boss-bar-fill{height:100%;width:100%;background:linear-gradient(90deg,#dc2626,#f59e0b);transition:width .12s}
#top-hp-bar{
  position:fixed;top:14px;left:16px;z-index:36;width:278px;
  padding:10px 14px;border-radius:14px;
  background:linear-gradient(145deg,rgba(14,18,28,0.95),rgba(36,12,18,0.92));
  border:1.5px solid rgba(255,77,109,0.7);
  box-shadow:0 10px 28px rgba(0,0,0,0.58),0 0 18px rgba(255,59,92,0.2);
  backdrop-filter:blur(12px);
}
#top-hp-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
#top-hp-left{display:flex;align-items:center;gap:8px}
#heart-icon{
  font-size:22px;line-height:1;color:#ff2e55;
  text-shadow:0 0 14px rgba(255,46,85,0.95);
  display:inline-block;animation:heartPulse 1.25s ease-in-out infinite;
}
#top-hp-bar.low-hp{border-color:#ff1e38;box-shadow:0 0 26px rgba(255,30,56,0.55)}
#top-hp-bar.low-hp #heart-icon{animation:heartPulse 0.42s ease-in-out infinite;color:#ff1e38}
#top-hp-hearts{font-size:16px;letter-spacing:2.5px;color:#ff4d6d;text-shadow:0 0 8px rgba(255,77,109,0.75)}
#top-hp-num{font:900 13.5px 'Consolas',monospace;color:#fff1f2;font-variant-numeric:tabular-nums}
#top-hp-track{height:11px;background:rgba(255,255,255,0.14);border-radius:6px;overflow:hidden;box-shadow:inset 0 1px 3px rgba(0,0,0,0.5)}
#top-hp-fill{height:100%;width:100%;background:linear-gradient(90deg,#ef4444,#f97316,#22c55e);transition:width .14s;box-shadow:0 0 10px rgba(34,197,94,0.45)}
#top-hp-meta{display:flex;justify-content:space-between;font:700 10px system-ui;color:#fda4af;letter-spacing:0.9px;margin-top:5px;text-transform:uppercase}
@keyframes heartPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.24)}}
#vitals-hud{
  position:fixed;left:16px;bottom:48px;width:250px;
  background:rgba(10,20,30,0.9);border:1px solid rgba(114,239,221,0.35);
  border-radius:12px;padding:10px 13px;backdrop-filter:blur(10px);
}
.vital-row{margin-bottom:6px}.vital-row:last-child{margin-bottom:0}
.vital-lbl{display:flex;justify-content:space-between;font:700 11px system-ui;color:#d6edf8;margin-bottom:3px}
.vital-bar{height:9px;background:rgba(255,255,255,0.12);border-radius:5px;overflow:hidden}
#hp-fill{height:100%;width:100%;background:linear-gradient(90deg,#ef4444,#22c55e);transition:width .12s}
#shield-fill{height:100%;width:100%;background:linear-gradient(90deg,#0284c7,#38bdf8);transition:width .12s}
#weapon-hud{
  position:fixed;right:16px;bottom:48px;
  background:rgba(10,20,30,0.9);border:1px solid rgba(114,239,221,0.35);
  border-radius:12px;padding:10px 14px;backdrop-filter:blur(10px);min-width:290px;
}
#weapon-active{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:7px}
#weapon-name{font:800 15px system-ui;color:#72efdd;letter-spacing:0.4px}
#weapon-ammo{font:800 16px 'Consolas',monospace;color:#fde047}
#weapon-slots{display:flex;gap:5px;flex-wrap:wrap}
.w-slot{
  padding:4px 8px;border-radius:6px;font:700 10.5px system-ui;
  background:rgba(255,255,255,0.08);color:#9cc2d8;border:1px solid rgba(255,255,255,0.12);
}
.w-slot.equipped{background:linear-gradient(135deg,#0ea5e9,#14b8a6);color:#04151f;border-color:#72efdd}
.w-slot.empty{opacity:0.4}
#pickup-prompt{
  position:fixed;left:50%;bottom:125px;transform:translateX(-50%);
  padding:8px 18px;border-radius:10px;background:rgba(12,24,34,0.92);
  border:1px solid #fbbf24;color:#fef08a;font:700 13px system-ui;
  box-shadow:0 6px 20px rgba(0,0,0,0.5);display:none;
}
#center-toast{
  position:fixed;left:50%;top:34%;transform:translate(-50%,-50%);z-index:35;
  padding:12px 24px;border-radius:14px;text-align:center;
  background:rgba(10,18,28,0.94);border:1px solid rgba(114,239,221,0.55);
  color:#fff;font:800 18px/1.25 system-ui;letter-spacing:0.8px;
  box-shadow:0 12px 38px rgba(0,0,0,0.65);opacity:0;transition:opacity .25s;pointer-events:none;
}
#center-toast.show{opacity:1}
#screen-flash{position:fixed;inset:0;pointer-events:none;z-index:21;opacity:0;transition:opacity .12s}
#hit-marker{
  position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
  width:24px;height:24px;pointer-events:none;z-index:23;opacity:0;transition:opacity .08s;
}
#hit-marker::before,#hit-marker::after{
  content:'';position:absolute;top:11px;left:0;width:24px;height:2px;background:#ff4d4d;
  box-shadow:0 0 6px #ff4d4d;
}
#hit-marker::before{transform:rotate(45deg)}
#hit-marker::after{transform:rotate(-45deg)}
"""

html = html.replace("</style>", EXTRA_CSS + "\n</style>", 1)

# ---------------------------------------------------------------------------
# 2. Update HTML title, Time-of-day selector, Mode selector, Combat HUD DOM
# ---------------------------------------------------------------------------
html = html.replace(
    "<title>Anurag University — 3D Campus Explorer & Digital Twin</title>",
    "<title>Anurag University — Campus Outbreak FP & Meta Quest 3 VR</title>",
    1
)

html = html.replace(
    '<option value="golden">Golden Sunset (5:15 PM)</option>',
    '<option value="golden">Golden Sunset (5:15 PM)</option>\n      <option value="outbreak" selected>Outbreak Dusk (Zombie Alert)</option>',
    1
)
html = html.replace(
    '<option value="noon" selected>Bright Campus Noon</option>',
    '<option value="noon">Bright Campus Noon</option>',
    1
)

html = html.replace(
    '<option value="creative" selected>Creative Flight & Walk</option>',
    '<option value="zombie" selected>Zombie Outbreak (6 Levels + CEO Boss)</option>\n      <option value="creative">Creative Flight & Walk</option>',
    1
)

html = html.replace(
    '<button id="walk">Explore Campus</button>',
    '<button id="walk">Play Game (PC)</button>',
    1
)

html = html.replace(
    "Quest Touch controllers · Left stick moves. Right stick snap-turns and changes height in Creative. Trigger bends the index finger, grip closes the hand, and A toggles GPS. B changes mode. Y advances to the next viewpoint outside the ring challenge. Lift your left wrist for status.",
    "Meta Quest 3 & PC Combat · Left Hand = Tactical Energy Shield (hold up to block, Left Trigger / thrust = Shield Bash). Right Hand = Lightsaber, Pistol, Rifle, Shotgun & Ground Rods/Branches (Right Trigger fires, swing physically in VR, Right Grip grabs ground weapons, A switches weapon, B reloads). Lift left wrist for live VR HUD."
)

COMBAT_HUD_HTML = """
<div id="screen-flash"></div>
<div id="hit-marker"></div>
<div id="combat-hud">
  <div id="top-hp-bar">
    <div id="top-hp-row">
      <div id="top-hp-left">
        <span id="heart-icon">♥</span>
        <span id="top-hp-hearts">♥♥♥♥♥</span>
      </div>
      <span id="top-hp-num">100 / 100</span>
    </div>
    <div id="top-hp-track"><div id="top-hp-fill"></div></div>
    <div id="top-hp-meta"><span id="top-hp-status">VITALITY · OPTIMAL</span><span id="top-hp-shield-mini">SHIELD 100%</span></div>
  </div>
  <div id="wave-banner">
    <div id="wave-title">ENTER ANURAG UNIVERSITY GATE</div>
    <div id="wave-sub">Walk forward inside the campus to begin Phase 1 (2:00 Survival)!</div>
    <div id="wave-cols">
      <div class="wave-col"><span class="wave-col-k">PHASE TIMER</span><span class="wave-col-v" id="wc-timer">2:00</span></div>
      <div class="wave-col"><span class="wave-col-k">HOSTILES / KILLS</span><span class="wave-col-v" id="wc-kills">0 / 0</span></div>
      <div class="wave-col"><span class="wave-col-k">SCORE</span><span class="wave-col-v" id="wc-score">0</span></div>
    </div>
  </div>
  <div id="boss-bar-wrap">
    <div id="boss-bar-label"><span>CEO · EXECUTIVE BOSS</span><span id="boss-hp-text">1200 / 1200</span></div>
    <div id="boss-bar-bg"><div id="boss-bar-fill"></div></div>
  </div>
  <div id="vitals-hud">
    <div class="vital-row">
      <div class="vital-lbl"><span>HEALTH</span><span id="hp-val">100 / 100</span></div>
      <div class="vital-bar"><div id="hp-fill"></div></div>
    </div>
    <div class="vital-row">
      <div class="vital-lbl"><span>HI-TECH SHIELD [RMB / L-TRIG]</span><span id="shield-val">100%</span></div>
      <div class="vital-bar"><div id="shield-fill"></div></div>
    </div>
  </div>
  <div id="weapon-hud">
    <div id="weapon-active">
      <span id="weapon-name">PLASMA LIGHTSABER</span>
      <span id="weapon-ammo">∞</span>
    </div>
    <div id="weapon-slots">
      <span class="w-slot equipped" data-w="0">[1] Saber</span>
      <span class="w-slot" data-w="1">[2] Pistol</span>
      <span class="w-slot" data-w="2">[3] Rifle</span>
      <span class="w-slot" data-w="3">[4] Shotgun</span>
      <span class="w-slot empty" data-w="4">[5] Pickup</span>
    </div>
  </div>
  <div id="pickup-prompt">[E] Pick up Iron Rod</div>
  <div id="combo-badge">2x COMBO!</div>
  <div id="dmg-feed"></div>
  <div id="center-toast"></div>
  <div id="end-overlay">
    <div id="end-card">
      <h2 id="end-title">YOU DIED!</h2>
      <div id="end-sub">ANURAG UNIVERSITY IS SAVED · CELEBRATE!</div>
      <div id="end-stats"></div>
      <div id="end-actions">
        <button id="btn-restart-game">Restart Game [R]</button>
        <button id="btn-explore-campus">Explore Campus [X]</button>
      </div>
    </div>
  </div>
</div>
<div id="intro-overlay">
  <div id="cine-top" class="cine-bar"></div>
  <div id="cine-bot" class="cine-bar"></div>
  <div id="intro-progress-track"><div id="intro-progress-fill"></div></div>
  <div id="intro-story-box">
    <div id="intro-crest"><span id="intro-crest-badge">AU</span><span id="intro-kicker">ANURAG UNIVERSITY · EMERGENCY BROADCAST</span></div>
    <h2 id="intro-headline">WELCOME TO ANURAG UNIVERSITY</h2>
    <div id="intro-divider"></div>
    <div id="intro-sub">Venkatapur Campus · Aerial Reconnaissance</div>
    <div id="intro-cols">
      <div class="intro-col"><div class="intro-col-lbl">01 · SURVIVAL MISSION</div><div class="intro-col-txt">Walk through the Main Gate, survive 5 escalating 2-min phases &amp; defeat THE CEO.</div></div>
      <div class="intro-col"><div class="intro-col-lbl">02 · TACTICAL ARSENAL</div><div class="intro-col-txt">Lightsaber [1], Pistol [2], Rifle [3], Shotgun [4] &amp; pickable Rods/Branches [E].</div></div>
      <div class="intro-col"><div class="intro-col-lbl">03 · VR &amp; PC DEFENSE</div><div class="intro-col-txt">Left-Trigger / RMB raises Cyan Energy Shield · Space / Y to Jump · Swing in VR!</div></div>
    </div>
  </div>
  <button id="btn-skip-intro">Skip Intro [Space]</button>
</div>
"""

html = html.replace('<div id="crosshair"></div>', '<div id="crosshair"></div>' + COMBAT_HUD_HTML, 1)

# ---------------------------------------------------------------------------
# 3. Embed Blender 5.3 Zombie & Weapon Meshes right after BLENDER_BAKED_MESHES is parsed
# ---------------------------------------------------------------------------
ZOMBIE_ASSETS_JS = (
    "\nvar ZOMBIE_BLENDER_ASSETS = " + json.dumps(zombie_assets, separators=(",", ":")) + ";\n"
    "for (let zk in ZOMBIE_BLENDER_ASSETS) { blenderGeos[zk] = buildBlenderGeo(ZOMBIE_BLENDER_ASSETS[zk]); }\n"
)

anchor_meshes = 'if (typeof BLENDER_BAKED_MESHES !== "undefined") {\n  for (let k in BLENDER_BAKED_MESHES) {\n    blenderGeos[k] = buildBlenderGeo(BLENDER_BAKED_MESHES[k]);\n  }\n}'
if anchor_meshes not in html:
    # Handle CRLF
    anchor_meshes = anchor_meshes.replace("\n", "\r\n")
assert anchor_meshes in html, "Could not find BLENDER_BAKED_MESHES anchor!"
html = html.replace(anchor_meshes, anchor_meshes + ZOMBIE_ASSETS_JS, 1)

# ---------------------------------------------------------------------------
# 4. Attach Left-Hand Tactical Energy Shield & Right-Hand Multi-Weapon Rig
#    inside createRealisticArmAndHand(side)
# ---------------------------------------------------------------------------
ARM_RETURN_ANCHOR = "  return { root, elbowPivot, wristPivot, fingers, thumbRoot, thumbJ2, phoneGroup, setFingerCurl };"
assert ARM_RETURN_ANCHOR in html, "Could not find createRealisticArmAndHand return anchor!"

ARM_GEAR_JS = """
  // --- COMBAT GEAR: Left Hand Tactical Energy Shield / Right Hand Multi-Weapon Rig ---
  let shieldGroup = null, shieldRimMat = null, shieldVisorMat = null;
  let weaponMount = null, weaponModels = null, saberBlade = null, saberCore = null, muzzleFlash = null;

  if (side === -1) {
    // Ultra-slim glowing cyan tech wristband emitter (no bulky box on hand, never overlaps watch!)
    let emitterRing = new et(new gn(0.032, 0.0045, 8, 22), new Yi({ color: 0x38bdf8 }));
    emitterRing.position.set(0, 0.002, -0.005);
    wristPivot.add(emitterRing);

    // Deployable Transparent Hi-Tech Holographic Hex-Grid Shield (opens on trigger / RMB / F)
    shieldGroup = new fi();
    shieldGroup.position.set(-0.02, 0.04, -0.14);
    shieldGroup.rotation.set(0.04, 0.06, 0.0);
    shieldGroup.scale.set(0.001, 0.001, 0.001);
    shieldGroup.visible = false;

    // Procedural Holographic Hex-Grid Canvas Texture
    let hc = document.createElement("canvas"); hc.width = 256; hc.height = 384;
    let hg = hc.getContext("2d");
    hg.clearRect(0, 0, 256, 384);
    let grad = hg.createRadialGradient(128, 192, 18, 128, 192, 195);
    grad.addColorStop(0, "rgba(56, 189, 248, 0.16)");
    grad.addColorStop(0.75, "rgba(14, 165, 233, 0.28)");
    grad.addColorStop(1, "rgba(114, 239, 221, 0.62)");
    hg.fillStyle = grad;
    hg.fillRect(6, 6, 244, 372);
    // Sci-fi hexagonal grid lines
    hg.strokeStyle = "rgba(125, 249, 255, 0.42)";
    hg.lineWidth = 1.5;
    let rHex = 22, dxHex = rHex * 1.5, dyHex = rHex * Math.sqrt(3);
    for (let row = -1; row < 12; row++) {
      for (let col = -1; col < 10; col++) {
        let cx = col * dxHex;
        let cy = row * dyHex + (col % 2 ? dyHex * 0.5 : 0);
        hg.beginPath();
        for (let k = 0; k < 6; k++) {
          let a = (Math.PI / 3) * k;
          let px = cx + Math.cos(a) * rHex, py = cy + Math.sin(a) * rHex;
          if (k === 0) hg.moveTo(px, py); else hg.lineTo(px, py);
        }
        hg.closePath(); hg.stroke();
      }
    }
    // Glowing tech border
    hg.strokeStyle = "#72efdd"; hg.lineWidth = 6;
    hg.strokeRect(6, 6, 244, 372);
    let hexTex = new dn(hc); hexTex.colorSpace = vt;

    shieldVisorMat = new Yi({ map: hexTex, transparent: true, opacity: 0.58, side: Gt, depthWrite: false });
    let holoPanel = new et(new _i(0.42, 0.62), shieldVisorMat);
    holoPanel.position.set(0, 0.02, -0.02);
    shieldGroup.add(holoPanel);

    // Subtle curved holographic frame struts (thin & glowing, never blocks view)
    shieldRimMat = new Yi({ color: 0x38bdf8, transparent: true, opacity: 0.85 });
    let topBar = new et(new Ni(0.43, 0.011, 0.011), shieldRimMat);
    topBar.position.set(0, 0.33, -0.02);
    shieldGroup.add(topBar);
    let botBar = new et(new Ni(0.43, 0.011, 0.011), shieldRimMat);
    botBar.position.set(0, -0.29, -0.02);
    shieldGroup.add(botBar);
    let leftBar = new et(new Ni(0.011, 0.62, 0.011), shieldRimMat);
    leftBar.position.set(-0.21, 0.02, -0.02);
    shieldGroup.add(leftBar);
    let rightBar = new et(new Ni(0.011, 0.62, 0.011), shieldRimMat);
    rightBar.position.set(0.21, 0.02, -0.02);
    shieldGroup.add(rightBar);

    wristPivot.add(shieldGroup);
  } else {
    // Right Hand Multi-Weapon Mount anchored cleanly inside the curled palm hollow!
    // Wrist rolls +1.36 rad (thumb UP, palm LEFT, fingers wrapping around grip), so weaponMount counter-rolls -1.36 rad!
    weaponMount = new fi();
    weaponMount.position.set(0.0, -0.026, -0.056);
    weaponMount.rotation.set(0, 0, -1.36);
    wristPivot.add(weaponMount);

    let hiltMat = new Jt({ color: 0xb0bac7, roughness: 0.24, metalness: 0.85 });
    let gunDarkMat = new Jt({ color: 0x2c3644, emissive: 0x0a1018, emissiveIntensity: 0.35, roughness: 0.35, metalness: 0.72 });
    let gunAccentMat = new Jt({ color: 0x475569, emissive: 0x0c131c, emissiveIntensity: 0.3, roughness: 0.42, metalness: 0.62 });
    let rodMat = new Jt({ color: 0x5c473e, roughness: 0.56, metalness: 0.72 });
    let branchMat = new Jt({ color: 0x523720, roughness: 0.9, metalness: 0.02 });

    // 0: Plasma Lightsaber — Centered cleanly inside closed fist (hilt Y: -0.13 .. +0.17, blade rises above thumb/index!)
    let saberGrp = new fi();
    saberGrp.position.set(0.0, -0.008, -0.004);
    saberGrp.rotation.set(-0.28, 0, 0);
    let hiltMesh = blenderGeos.lightsaber_hilt
      ? new et(blenderGeos.lightsaber_hilt, hiltMat)
      : new et(new pn(0.018, 0.018, 0.24, 14), hiltMat);
    saberGrp.add(hiltMesh);

    // Emitter mouth glow ring
    let emitterGlow = new et(new gn(0.022, 0.0055, 8, 18), new Yi({ color: 0x72efdd }));
    emitterGlow.rotation.x = Math.PI / 2;
    emitterGlow.position.set(0, 0.165, 0);
    saberGrp.add(emitterGlow);

    // Telescoping blade pivot anchored cleanly at the emitter mouth (Y = 0.165) — solid, realistic, zero glitch!
    let saberBladePivot = new fi();
    saberBladePivot.position.set(0, 0.165, 0);
    let bladeOuterMat = new Yi({ color: 0x22d3ee, transparent: true, opacity: 0.72 });
    let bladeCoreMat = new Yi({ color: 0xffffff });

    saberBlade = new et(new pn(0.011, 0.014, 0.96, 16), bladeOuterMat);
    saberBlade.position.set(0, 0.48, 0);
    saberBladePivot.add(saberBlade);
    saberCore = new et(new pn(0.0055, 0.0075, 0.94, 12), bladeCoreMat);
    saberCore.position.set(0, 0.47, 0);
    saberBladePivot.add(saberCore);
    let bladeTip = new et(new fn(0.011, 12, 10), bladeOuterMat);
    bladeTip.position.set(0, 0.96, 0);
    saberBladePivot.add(bladeTip);
    saberGrp.add(saberBladePivot);
    saberGrp.userData.bladePivot = saberBladePivot;
    weaponMount.add(saberGrp);

    // 1: Tactical 9mm Pistol (pistol grip Y: -0.11..0 sits squarely inside closed fist, slide & green sight above index!)
    let pistolGrp = new fi();
    pistolGrp.position.set(0.0, 0.036, -0.008);
    let pistolMesh = blenderGeos.pistol
      ? new et(blenderGeos.pistol, gunDarkMat)
      : new et(new Ni(0.032, 0.12, 0.2), gunDarkMat);
    pistolGrp.add(pistolMesh);
    let pSight = new et(new Ni(0.006, 0.006, 0.006), new Yi({ color: 0x22c55e }));
    pSight.position.set(0, 0.075, -0.145);
    pistolGrp.add(pSight);
    weaponMount.add(pistolGrp);

    // 2: Pulse Assault Rifle (pistol grip inside closed fist, receiver & red-dot sight cleanly above wrist!)
    let rifleGrp = new fi();
    rifleGrp.position.set(0.0, 0.042, -0.016);
    let rifleMesh = blenderGeos.assault_rifle
      ? new et(blenderGeos.assault_rifle, gunDarkMat)
      : new et(new Ni(0.045, 0.14, 0.58), gunDarkMat);
    rifleGrp.add(rifleMesh);
    let redDot = new et(new fn(0.005, 8, 8), new Yi({ color: 0xff3b30 }));
    redDot.position.set(0, 0.10, -0.065);
    rifleGrp.add(redDot);
    weaponMount.add(rifleGrp);

    // 3: Combat Shotgun (grip seated cleanly inside fist, barrel & pump aligned straight downrange!)
    let shotGrp = new fi();
    shotGrp.position.set(0.0, 0.032, -0.018);
    let shotMesh = blenderGeos.shotgun
      ? new et(blenderGeos.shotgun, gunAccentMat)
      : new et(new Ni(0.048, 0.13, 0.62), gunAccentMat);
    shotGrp.add(shotMesh);
    weaponMount.add(shotGrp);

    // 4: Campus Iron Rod Pickup (full sword/club fist grip!)
    let rodGrp = new fi();
    rodGrp.position.set(0.0, -0.008, -0.004);
    rodGrp.rotation.set(-0.28, 0, 0);
    let rodMesh = blenderGeos.iron_rod
      ? new et(blenderGeos.iron_rod, rodMat)
      : new et(new pn(0.014, 0.014, 0.95, 10), rodMat);
    rodGrp.add(rodMesh);
    weaponMount.add(rodGrp);

    // 5: Campus Fallen Branch Pickup (full club fist grip!)
    let branchGrp = new fi();
    branchGrp.position.set(0.0, -0.008, -0.004);
    branchGrp.rotation.set(-0.28, 0, 0);
    let branchMesh = blenderGeos.fallen_branch
      ? new et(blenderGeos.fallen_branch, branchMat)
      : new et(new pn(0.02, 0.012, 0.92, 10), branchMat);
    branchGrp.add(branchMesh);
    weaponMount.add(branchGrp);

    // Multi-Layered Starburst Muzzle Flash + Tactical Laser Sight
    muzzleFlash = new fi();
    let mfCore = new et(new fn(0.042, 8, 8), new Yi({ color: 0xffffff }));
    muzzleFlash.add(mfCore);
    let mfMat = new Yi({ color: 0xffb703, transparent: true, opacity: 0.92, side: Gt, depthWrite: false });
    let mfCone = new et(new oa(0.065, 0.22, 8), mfMat);
    mfCone.rotation.x = -Math.PI / 2;
    mfCone.position.z = -0.09;
    muzzleFlash.add(mfCone);
    for (let k = 0; k < 3; k++) {
      let fin = new et(new _i(0.18, 0.055), mfMat);
      fin.rotation.z = k * (Math.PI / 3);
      muzzleFlash.add(fin);
    }
    muzzleFlash.visible = false;
    weaponMount.add(muzzleFlash);

    let laserBeam = new et(new pn(0.0022, 0.0022, 24, 6), new Yi({ color: 0xff3b30, transparent: true, opacity: 0.42 }));
    laserBeam.rotation.x = Math.PI / 2;
    laserBeam.position.set(0, 0.052, -12.3);
    laserBeam.visible = false;
    weaponMount.add(laserBeam);

    weaponModels = [saberGrp, pistolGrp, rifleGrp, shotGrp, rodGrp, branchGrp];
    weaponModels.forEach((m, idx) => (m.visible = idx === 0));
    weaponMount.userData.laserBeam = laserBeam;
  }

  return { root, elbowPivot, wristPivot, fingers, thumbRoot, thumbJ2, phoneGroup, setFingerCurl, shieldGroup, shieldRimMat, shieldVisorMat, weaponMount, weaponModels, saberBlade, saberCore, muzzleFlash };
"""

html = html.replace(ARM_RETURN_ANCHOR, ARM_GEAR_JS, 1)

# ---------------------------------------------------------------------------
# 5. Add Outbreak Dusk lighting option
# ---------------------------------------------------------------------------
TIME_ANCHOR = '  } else {\n    Cn.position.set(-65, 115, 62);'
if TIME_ANCHOR not in html:
    TIME_ANCHOR = TIME_ANCHOR.replace("\n", "\r\n")
assert TIME_ANCHOR in html, "Could not find time-mode anchor!"

OUTBREAK_TIME_JS = """  } else if (mode === "outbreak") {
    Cn.position.set(-85, 36, 52);
    Cn.color.setHex(0xffb899);
    Cn.intensity = 1.65;
    skyUniforms.topColor.value.setHex(0x111b2b);
    skyUniforms.horizonColor.value.setHex(0x4a2a32);
    Ht.fog.color.setHex(0x2b1f28);
  } else {
    Cn.position.set(-65, 115, 62);"""
html = html.replace(TIME_ANCHOR, OUTBREAK_TIME_JS, 1)

# ---------------------------------------------------------------------------
# 6. Inject the Full Zombie Outbreak Combat Engine, AI, Faculty ID Cards,
#    Ground Pickups, WebAudio SFX, PC & Meta Quest 3 Combat Sync!
# ---------------------------------------------------------------------------
LOOP_ANCHOR = "// MAIN REAL-TIME SIMULATION & BIOMECHANICAL POV ANIMATION LOOP"
assert LOOP_ANCHOR in html, "Could not find animation loop anchor!"

ZOMBIE_ENGINE_JS = r"""
// ============================================================================
// ANURAG UNIVERSITY: CAMPUS OUTBREAK — 6-LEVEL ZOMBIE GAME ENGINE (PC + QUEST 3)
// ============================================================================
const ZOMBIE_LEVELS = [
  { level: 1, name: "Lab Assistants", badge: "LAB ASST", dept: "ECE / CSE LABS", count: 6, hp: 90, armor: 0.0, speed: 2.35, dmg: 9, scale: 1.02, skin: 0x6ba854, coat: 0x9ec5e8, pants: 0x1e293b, tie: 0x1d4ed8, hair: 0x1a1a1d, glasses: false, badgeCol: "#16a34a", lanyard: 0x16a34a, isBoss: false },
  { level: 2, name: "Jr. Professors", badge: "JR. PROF", dept: "ASST. FACULTY", count: 8, hp: 150, armor: 0.12, speed: 2.75, dmg: 12, scale: 1.05, skin: 0x5c9a49, coat: 0xe6eef6, pants: 0x262c36, tie: 0x991b1b, hair: 0x221e1c, glasses: false, badgeCol: "#2563eb", lanyard: 0x2563eb, isBoss: false },
  { level: 3, name: "Professors", badge: "PROFESSOR", dept: "SENIOR FACULTY", count: 9, hp: 240, armor: 0.22, speed: 3.0, dmg: 16, scale: 1.08, skin: 0x528c42, coat: 0x2b3e56, pants: 0x181d26, tie: 0x7f1d1d, hair: 0x5b6472, glasses: true, badgeCol: "#9333ea", lanyard: 0x9333ea, isBoss: false },
  { level: 4, name: "Academic / Placement Incharges", badge: "PLACEMENT", dept: "TRAINING & PLACEMENT", count: 10, hp: 360, armor: 0.32, speed: 3.4, dmg: 20, scale: 1.11, skin: 0x4b8248, coat: 0x1f2937, pants: 0x111827, tie: 0xd97706, hair: 0x1f1f24, glasses: false, badgeCol: "#d97706", lanyard: 0xd97706, isBoss: false },
  { level: 5, name: "HODs (Head of Department)", badge: "H.O.D", dept: "DEPT. HEAD", count: 8, hp: 520, armor: 0.42, speed: 3.3, dmg: 26, scale: 1.18, skin: 0x427542, coat: 0x172030, pants: 0x0f131a, tie: 0xdc2626, hair: 0x6b7280, glasses: true, badgeCol: "#dc2626", lanyard: 0xdc2626, isBoss: false },
  { level: 6, name: "THE CEO · FINAL BOSS", badge: "CEO · BOSS", dept: "EXECUTIVE OFFICE", count: 1, hp: 2200, armor: 0.48, speed: 3.55, dmg: 32, scale: 1.44, skin: 0x386b3c, coat: 0x0f141c, pants: 0x090c10, tie: 0xf59e0b, hair: 0x111318, glasses: false, badgeCol: "#eab308", lanyard: 0xeab308, isBoss: true }
];

const WEAPON_DEFS = [
  { id: 0, key: "saber", name: "PLASMA LIGHTSABER", type: "melee", dmg: 26, range: 2.55, cooldown: 0.42, knockback: 2.8, mag: Infinity, muzzleZ: -0.5 },
  { id: 1, key: "pistol", name: "TACTICAL 9MM PISTOL", type: "gun", dmg: 34, range: 65, cooldown: 0.24, auto: false, pellets: 1, spread: 0.012, mag: 15, reload: 1.1, muzzleZ: -0.22 },
  { id: 2, key: "rifle", name: "PULSE ASSAULT RIFLE", type: "gun", dmg: 26, range: 80, cooldown: 0.105, auto: true, pellets: 1, spread: 0.022, mag: 30, reload: 1.5, muzzleZ: -0.58 },
  { id: 3, key: "shotgun", name: "COMBAT SHOTGUN", type: "gun", dmg: 22, range: 32, cooldown: 0.68, auto: false, pellets: 6, spread: 0.075, mag: 8, reload: 1.65, muzzleZ: -0.62 },
  { id: 4, key: "iron_rod", name: "IRON CONSTRUCTION ROD", type: "melee", dmg: 38, range: 2.65, cooldown: 0.52, knockback: 4.8, mag: Infinity, muzzleZ: -0.5 },
  { id: 5, key: "fallen_branch", name: "FALLEN TREE BRANCH", type: "melee", dmg: 32, range: 2.6, cooldown: 0.48, knockback: 4.2, mag: Infinity, muzzleZ: -0.5 }
];

// Rich Layered WebAudio Synthesizer (Zombie Groans, Boss Roar, Lightsaber Hum/Whoosh/Clash, Punchy Gunshots, Reload, Shield)
let audioCtx = null, saberHumNode = null, saberHumGain = null;
function ensureAudio() {
  if (!audioCtx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC) audioCtx = new AC();
  }
  if (audioCtx && audioCtx.state === "suspended") audioCtx.resume().catch(() => {});
  return audioCtx;
}
function updateSaberHum(active) {
  const ctx = audioCtx;
  if (!ctx || ctx.state !== "running") return;
  if (active && !saberHumNode) {
    const o1 = ctx.createOscillator(), o2 = ctx.createOscillator(), g = ctx.createGain(), f = ctx.createBiquadFilter();
    o1.type = "sawtooth"; o1.frequency.value = 88;
    o2.type = "triangle"; o2.frequency.value = 132.5;
    f.type = "lowpass"; f.frequency.value = 260;
    g.gain.value = 0.032;
    o1.connect(f); o2.connect(f); f.connect(g); g.connect(ctx.destination);
    o1.start(); o2.start();
    saberHumNode = [o1, o2]; saberHumGain = g;
  } else if (saberHumGain) {
    saberHumGain.gain.setTargetAtTime(active ? 0.032 : 0.0001, ctx.currentTime, 0.06);
  }
}
function playSFX(kind) {
  const ctx = ensureAudio();
  if (!ctx) return;
  const now = ctx.currentTime;
  const gain = ctx.createGain();
  gain.connect(ctx.destination);

  if (kind === "saber_ignite") {
    // Slow dramatic 1.25s Lightsaber Ignition Rise!
    const o1 = ctx.createOscillator(), o2 = ctx.createOscillator(), filt = ctx.createBiquadFilter();
    o1.type = "sawtooth"; o2.type = "triangle";
    o1.frequency.setValueAtTime(62, now);
    o1.frequency.exponentialRampToValueAtTime(195, now + 0.45);
    o1.frequency.linearRampToValueAtTime(118, now + 1.2);
    o2.frequency.setValueAtTime(95, now);
    o2.frequency.exponentialRampToValueAtTime(280, now + 0.55);
    o2.frequency.linearRampToValueAtTime(155, now + 1.2);
    filt.type = "bandpass"; filt.frequency.setValueAtTime(240, now);
    filt.frequency.exponentialRampToValueAtTime(920, now + 0.65);
    filt.frequency.linearRampToValueAtTime(420, now + 1.2);
    filt.Q.value = 1.8;
    gain.gain.setValueAtTime(0.01, now);
    gain.gain.linearRampToValueAtTime(0.22, now + 0.25);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 1.25);
    o1.connect(filt); o2.connect(filt); filt.connect(gain);
    o1.start(now); o2.start(now); o1.stop(now + 1.28); o2.stop(now + 1.28);
  } else if (kind === "saber" || kind === "saber_clash") {
    // Rich Lightsaber Plasma Whoosh + Sizzle Clash
    const o1 = ctx.createOscillator(), o2 = ctx.createOscillator(), filt = ctx.createBiquadFilter();
    o1.type = "sawtooth"; o2.type = "square";
    o1.frequency.setValueAtTime(kind === "saber_clash" ? 310 : 145, now);
    o1.frequency.exponentialRampToValueAtTime(kind === "saber_clash" ? 95 : 420, now + 0.08);
    o1.frequency.exponentialRampToValueAtTime(92, now + 0.28);
    o2.frequency.setValueAtTime(220, now);
    o2.frequency.exponentialRampToValueAtTime(110, now + 0.28);
    filt.type = "bandpass"; filt.frequency.value = kind === "saber_clash" ? 1100 : 520; filt.Q.value = 2.2;
    gain.gain.setValueAtTime(kind === "saber_clash" ? 0.24 : 0.16, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.29);
    o1.connect(filt); o2.connect(filt); filt.connect(gain);
    o1.start(now); o2.start(now); o1.stop(now + 0.3); o2.stop(now + 0.3);
  } else if (kind === "pistol" || kind === "rifle" || kind === "shotgun") {
    // Layered Realistic Gunshot: High-crack Noise Burst + Sub-bass Punch + Shotgun Pump
    const dur = kind === "shotgun" ? 0.28 : kind === "pistol" ? 0.14 : 0.095;
    const buf = ctx.createBuffer(1, Math.floor(ctx.sampleRate * dur), ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (d.length * 0.22));
    const src = ctx.createBufferSource(); src.buffer = buf;
    const filt = ctx.createBiquadFilter(); filt.type = "lowpass";
    filt.frequency.setValueAtTime(kind === "shotgun" ? 1350 : kind === "pistol" ? 2800 : 2200, now);
    filt.frequency.exponentialRampToValueAtTime(260, now + dur);
    gain.gain.setValueAtTime(kind === "shotgun" ? 0.44 : kind === "pistol" ? 0.28 : 0.24, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + dur);
    src.connect(filt); filt.connect(gain); src.start(now);
    // Low punch oscillator
    const punch = ctx.createOscillator(), pg = ctx.createGain();
    punch.type = "sine";
    punch.frequency.setValueAtTime(kind === "shotgun" ? 135 : 185, now);
    punch.frequency.exponentialRampToValueAtTime(36, now + 0.11);
    pg.gain.setValueAtTime(kind === "shotgun" ? 0.42 : 0.24, now);
    pg.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
    punch.connect(pg); pg.connect(ctx.destination); punch.start(now); punch.stop(now + 0.13);
  } else if (kind === "reload") {
    [0, 0.16, 0.34].forEach((tOff, idx) => {
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.type = "square"; o.frequency.value = [520, 340, 780][idx];
      g.gain.setValueAtTime(0.10, now + tOff); g.gain.exponentialRampToValueAtTime(0.001, now + tOff + 0.055);
      o.connect(g); g.connect(ctx.destination); o.start(now + tOff); o.stop(now + tOff + 0.06);
    });
  } else if (kind === "zgroan" || kind === "zdeath" || kind === "boss_roar") {
    // Formant-Filtered Undead Zombie Groan / Death Snarl / Deep Boss Roar
    const isBoss = kind === "boss_roar", isDeath = kind === "zdeath";
    const dur = isBoss ? 0.95 : isDeath ? 0.45 : 0.58;
    const o1 = ctx.createOscillator(), o2 = ctx.createOscillator(), f = ctx.createBiquadFilter();
    o1.type = "sawtooth"; o2.type = "sawtooth";
    const base = isBoss ? 68 : (isDeath ? 125 : 92 + Math.random() * 28);
    o1.frequency.setValueAtTime(base, now);
    o1.frequency.linearRampToValueAtTime(base * (isDeath ? 0.52 : 0.78), now + dur);
    o2.frequency.setValueAtTime(base * 1.04, now);
    o2.frequency.linearRampToValueAtTime(base * 0.72, now + dur);
    f.type = "bandpass"; f.Q.value = 3.2;
    f.frequency.setValueAtTime(isBoss ? 360 : 540, now);
    f.frequency.linearRampToValueAtTime(isBoss ? 190 : 260, now + dur);
    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(isBoss ? 0.30 : 0.15, now + 0.07);
    gain.gain.exponentialRampToValueAtTime(0.001, now + dur);
    o1.connect(f); o2.connect(f); f.connect(gain);
    o1.start(now); o2.start(now); o1.stop(now + dur + 0.02); o2.stop(now + dur + 0.02);
  } else if (kind === "rod" || kind === "branch") {
    const osc = ctx.createOscillator();
    osc.type = kind === "rod" ? "triangle" : "sine";
    osc.frequency.setValueAtTime(kind === "rod" ? 560 : 210, now);
    osc.frequency.exponentialRampToValueAtTime(kind === "rod" ? 140 : 65, now + 0.16);
    gain.gain.setValueAtTime(0.26, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.19);
  } else if (kind === "block" || kind === "bash" || kind === "shield_on") {
    const osc = ctx.createOscillator();
    osc.type = "sine";
    osc.frequency.setValueAtTime(kind === "bash" ? 280 : kind === "shield_on" ? 360 : 740, now);
    osc.frequency.exponentialRampToValueAtTime(kind === "bash" ? 70 : kind === "shield_on" ? 620 : 320, now + 0.22);
    gain.gain.setValueAtTime(kind === "shield_on" ? 0.12 : 0.24, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.25);
  } else if (kind === "hit" || kind === "headshot") {
    const osc = ctx.createOscillator();
    osc.type = "square";
    osc.frequency.setValueAtTime(kind === "headshot" ? 960 : 290, now);
    osc.frequency.exponentialRampToValueAtTime(kind === "headshot" ? 1380 : 120, now + 0.09);
    gain.gain.setValueAtTime(0.16, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.11);
  } else if (kind === "hurt") {
    const osc = ctx.createOscillator();
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(140, now);
    osc.frequency.linearRampToValueAtTime(55, now + 0.22);
    gain.gain.setValueAtTime(0.24, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.25);
  } else if (kind === "jump" || kind === "land") {
    const osc = ctx.createOscillator();
    osc.type = "sine";
    if (kind === "jump") {
      osc.frequency.setValueAtTime(160, now);
      osc.frequency.exponentialRampToValueAtTime(420, now + 0.14);
      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
    } else {
      osc.frequency.setValueAtTime(115, now);
      osc.frequency.exponentialRampToValueAtTime(42, now + 0.12);
      gain.gain.setValueAtTime(0.22, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
    }
    osc.connect(gain); osc.start(now); osc.stop(now + 0.17);
  } else if (kind === "firework") {
    // Realistic Firework Burst Boom + Sparkling Crackle!
    const dur = 0.42;
    const buf = ctx.createBuffer(1, Math.floor(ctx.sampleRate * dur), ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) {
      const env = Math.exp(-i / (d.length * 0.28));
      const crackle = (i > d.length * 0.25 && Math.random() < 0.08) ? 1.8 : 1.0;
      d[i] = (Math.random() * 2 - 1) * env * crackle;
    }
    const src = ctx.createBufferSource(); src.buffer = buf;
    const filt = ctx.createBiquadFilter(); filt.type = "lowpass";
    filt.frequency.setValueAtTime(1600, now);
    filt.frequency.exponentialRampToValueAtTime(320, now + dur);
    gain.gain.setValueAtTime(0.32, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + dur);
    src.connect(filt); filt.connect(gain); src.start(now);
    const boom = ctx.createOscillator(), bg = ctx.createGain();
    boom.type = "sine"; boom.frequency.setValueAtTime(115, now); boom.frequency.exponentialRampToValueAtTime(34, now + 0.22);
    bg.gain.setValueAtTime(0.35, now); bg.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
    boom.connect(bg); bg.connect(ctx.destination); boom.start(now); boom.stop(now + 0.25);
  } else if (kind === "levelup" || kind === "pickup" || kind === "victory") {
    const freqs = kind === "victory" ? [523, 659, 784, 1046, 784, 1046] : kind === "levelup" ? [440, 554, 659, 880] : [520, 740];
    freqs.forEach((frq, idx) => {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = "triangle"; o.frequency.value = frq;
      g.gain.setValueAtTime(0.15, now + idx * 0.11);
      g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.11 + 0.30);
      o.connect(g); g.connect(ctx.destination);
      o.start(now + idx * 0.11); o.stop(now + idx * 0.11 + 0.32);
    });
  }
}

// Realistic Procedural Textures for Thrown Laptops & Engineering Textbooks (Round 3+ Faculty Attacks!)
let laptopScreenTex = null, laptopKeyTex = null;
const bookTexCache = [];
function initThrowablesTextures() {
  if (laptopScreenTex) return;
  // Laptop Screen: Glowing IDE / Exam Error screen
  const sc = document.createElement("canvas"); sc.width = 256; sc.height = 160;
  const sg = sc.getContext("2d");
  sg.fillStyle = "#0b192c"; sg.fillRect(0, 0, 256, 160);
  sg.fillStyle = "#1d4ed8"; sg.fillRect(0, 0, 256, 22);
  sg.fillStyle = "#ffffff"; sg.font = "bold 12px monospace";
  sg.fillText("ANURAG LABS · EXAM SYSTEM", 10, 15);
  sg.fillStyle = "#38bdf8"; sg.font = "11px monospace";
  sg.fillText("int main() { // FATAL ERR", 12, 46);
  sg.fillStyle = "#4ade80"; sg.fillText("  attendance = 0%;", 12, 66);
  sg.fillStyle = "#f87171"; sg.font = "bold 15px sans-serif";
  sg.fillText("DETAINED! RE-EXAM!", 28, 106);
  sg.fillStyle = "#fbbf24"; sg.fillRect(16, 126, 224, 14);
  laptopScreenTex = new dn(sc); laptopScreenTex.colorSpace = vt;

  // Laptop Keyboard Deck
  const kc = document.createElement("canvas"); kc.width = 256; kc.height = 160;
  const kg = kc.getContext("2d");
  kg.fillStyle = "#94a3b8"; kg.fillRect(0, 0, 256, 160);
  kg.fillStyle = "#1e293b"; kg.fillRect(16, 14, 224, 86);
  kg.fillStyle = "#334155";
  for (let r = 0; r < 5; r++) {
    for (let c = 0; c < 13; c++) kg.fillRect(22 + c * 16.5, 20 + r * 15, 13, 11);
  }
  kg.fillStyle = "#64748b"; kg.fillRect(88, 110, 80, 40); // Trackpad
  laptopKeyTex = new dn(kc); laptopKeyTex.colorSpace = vt;

  // Hardcover Engineering Textbooks
  const titles = [
    ["DATA", "STRUCTURES", "#991b1b", "#fde047"],
    ["DBMS &", "SQL LAB", "#1e3a8a", "#7dd3fc"],
    ["CIRCUIT", "THEORY", "#065f46", "#bbf7d0"],
    ["ENGG.", "MATHS III", "#581c87", "#f5d0fe"]
  ];
  for (const [t1, t2, bg, fg] of titles) {
    const bc = document.createElement("canvas"); bc.width = 256; bc.height = 340;
    const bgc = bc.getContext("2d");
    bgc.fillStyle = bg; bgc.fillRect(0, 0, 256, 340);
    bgc.fillStyle = "rgba(0,0,0,0.22)"; bgc.fillRect(0, 0, 26, 340); // Spine crease
    bgc.strokeStyle = fg; bgc.lineWidth = 5; bgc.strokeRect(36, 22, 200, 296);
    bgc.fillStyle = "#ffffff"; bgc.font = "bold 20px sans-serif"; bgc.textAlign = "center";
    bgc.fillText("ANURAG UNIV", 136, 64);
    bgc.fillStyle = fg; bgc.font = "bold 32px serif";
    bgc.fillText(t1, 136, 145);
    bgc.fillText(t2, 136, 186);
    bgc.fillStyle = "#e2e8f0"; bgc.font = "bold 16px sans-serif";
    bgc.fillText("FACULTY EDITION", 136, 286);
    const tex = new dn(bc); tex.colorSpace = vt;
    bookTexCache.push({ tex, bg });
  }
}

function createThrownLaptop() {
  initThrowablesTextures();
  const g = new fi();
  const alumMat = new Jt({ color: 0xb8c2cc, roughness: 0.32, metalness: 0.78 });
  const keyMat = new Jt({ map: laptopKeyTex, roughness: 0.55, metalness: 0.25 });
  const scrMat = new Yi({ map: laptopScreenTex });
  // Base deck
  const base = new et(new Ni(0.36, 0.018, 0.24), [alumMat, alumMat, keyMat, alumMat, alumMat, alumMat]);
  g.add(base);
  // Open hinged screen lid (tilted ~108 deg open!)
  const lidPivot = new fi();
  lidPivot.position.set(0, 0.01, -0.118);
  lidPivot.rotation.x = -0.30;
  const lidBack = new et(new Ni(0.36, 0.23, 0.014), alumMat);
  lidBack.position.set(0, 0.115, 0);
  lidPivot.add(lidBack);
  const screen = new et(new _i(0.33, 0.20), scrMat);
  screen.position.set(0, 0.115, 0.009);
  lidPivot.add(screen);
  g.add(lidPivot);
  return g;
}

function createThrownBook() {
  initThrowablesTextures();
  const pick = bookTexCache[Math.floor(Math.random() * bookTexCache.length)];
  const g = new fi();
  const coverMat = new Jt({ map: pick.tex, roughness: 0.72 });
  const spineMat = new Jt({ color: pick.bg, roughness: 0.78 });
  const pagesMat = new Jt({ color: 0xf5f0e1, roughness: 0.92 });
  // Thick hardcover book with crisp white paper pages visible on 3 edges!
  const pages = new et(new Ni(0.22, 0.044, 0.29), pagesMat);
  g.add(pages);
  const topCover = new et(new Ni(0.235, 0.008, 0.305), coverMat);
  topCover.position.y = 0.025;
  g.add(topCover);
  const botCover = new et(new Ni(0.235, 0.008, 0.305), spineMat);
  botCover.position.y = -0.025;
  g.add(botCover);
  const spine = new et(new Ni(0.012, 0.056, 0.305), spineMat);
  spine.position.x = -0.114;
  g.add(spine);
  return g;
}

// High-Resolution Procedural Faculty ID Card Textures
const idCardTexCache = new Map();
function getFacultyIdCardTexture(lvlDef) {
  if (idCardTexCache.has(lvlDef.level)) return idCardTexCache.get(lvlDef.level);
  const c = document.createElement("canvas");
  c.width = 256; c.height = 384;
  const g = c.getContext("2d");
  // White PVC card base with subtle grime
  g.fillStyle = "#f1f5f0"; g.fillRect(0, 0, 256, 384);
  // Top university banner
  g.fillStyle = lvlDef.badgeCol; g.fillRect(0, 0, 256, 76);
  g.fillStyle = "#ffffff"; g.font = "bold 22px sans-serif"; g.textAlign = "center";
  g.fillText("ANURAG UNIV", 128, 34);
  g.font = "bold 14px sans-serif";
  g.fillText("FACULTY ID CARD", 128, 60);
  // Zombie faculty portrait box
  g.fillStyle = "#1c2620"; g.fillRect(58, 94, 140, 136);
  // Green undead face silhouette inside portrait
  g.fillStyle = "#5c8c4a";
  g.beginPath(); g.arc(128, 150, 38, 0, Math.PI * 2); g.fill();
  g.fillStyle = "#ef4444";
  g.beginPath(); g.arc(114, 146, 5, 0, Math.PI * 2); g.arc(142, 146, 5, 0, Math.PI * 2); g.fill();
  g.fillStyle = "#1e293b"; g.fillRect(88, 190, 80, 40);
  // Role badge strip
  g.fillStyle = lvlDef.badgeCol; g.fillRect(16, 246, 224, 48);
  g.fillStyle = "#ffffff"; g.font = "bold 28px sans-serif";
  g.fillText(lvlDef.badge, 128, 280);
  // Dept + Barcode
  g.fillStyle = "#1e293b"; g.font = "bold 15px sans-serif";
  g.fillText(lvlDef.dept, 128, 318);
  for (let x = 32; x < 224; x += 6) {
    g.fillRect(x, 334, (x % 12 === 0) ? 4 : 2, 32);
  }
  // Subtle blood splatter corner
  g.fillStyle = "rgba(155,22,22,0.45)";
  g.beginPath(); g.arc(216, 118, 22, 0, Math.PI * 2); g.fill();
  const tex = new dn(c); tex.colorSpace = vt;
  idCardTexCache.set(lvlDef.level, tex);
  return tex;
}

// Game State
const ZGAME = {
  active: false,
  levelIdx: 0,
  score: 0,
  kills: 0,
  headshots: 0,
  combo: 0,
  bestCombo: 0,
  comboTimer: 0,
  shake: 0,
  jumpVel: 0,
  jumpY: 0,
  keyShieldDown: false,
  medkits: [],
  groanTimer: 2.5,
  introPlaying: false,
  introTime: 0,
  introDur: 10.5,
  introDoneOnce: false,
  vrStoryBanner: null,
  vrWinBanner: null,
  vrDeathBanner: null,
  fireworks: [],
  fireworkTimer: 0,
  hp: 100,
  maxHp: 100,
  shield: 100,
  shieldBlocking: false,
  shieldDeploy: 0,
  vrShieldTrigger: false,
  shieldBashCd: 0,
  shieldBashAnim: 0,
  weaponIdx: 0,          // 0=saber, 1=pistol, 2=rifle, 3=shotgun, 4=iron_rod, 5=fallen_branch
  pickupWeaponIdx: -1,   // 4 or 5 when player has picked up a campus rod/branch
  ammo: [Infinity, 15, 30, 8, Infinity, Infinity],
  reloading: 0,
  reloadTotal: 1.2,
  fireCd: 0,
  swingAnim: 0,
  swingDir: 1,
  recoilAnim: 0,
  saberIgnite: 0,
  weaponDrawAnim: 0,
  muzzleTimer: 0,
  trailTimer: 0,
  mouseLeftDown: false,
  mouseRightDown: false,
  zombies: [],
  projectiles: [],
  particles: [],
  pickups: [],
  gameOver: false,
  victory: false,
  campusEntered: false,
  waveDelay: 0,
  phaseTimer: 120,
  spawnTimer: 2.5,
  bossSummonedMinions: false,
  vrPrevRightPos: new A(),
  vrPrevTipPos: new A(),
  vrPrevLeftPos: new A(),
  vrRightVel: 0,
  vrLeftVel: 0,
  vrSwingCd: 0,
  toastTimer: 0
};

function showToast(msg, dur = 2.6) {
  const el = kt("center-toast");
  if (!el) return;
  el.textContent = msg;
  el.classList.add("show");
  ZGAME.toastTimer = dur;
}
function flashScreen(color, alpha = 0.35) {
  const el = kt("screen-flash");
  if (!el) return;
  el.style.background = color;
  el.style.opacity = String(alpha);
  setTimeout(() => { el.style.opacity = "0"; }, 110);
}
function showHitMarker(isHeadshot, dmgText = "") {
  const el = kt("hit-marker");
  if (el) {
    el.style.opacity = "1";
    el.style.transform = isHeadshot ? "translate(-50%,-50%) scale(1.45)" : "translate(-50%,-50%) scale(1)";
    setTimeout(() => { el.style.opacity = "0"; }, 110);
  }
  const df = kt("dmg-feed");
  if (df && dmgText) {
    df.textContent = dmgText;
    df.style.color = isHeadshot ? "#fde047" : "#f8fafc";
    df.style.opacity = "1";
    df.style.transform = "translate(-50%,-62%) scale(1.08)";
    clearTimeout(df._t);
    df._t = setTimeout(() => { df.style.opacity = "0"; df.style.transform = "translate(-50%,-50%) scale(1)"; }, 420);
  }
}

// Spawn FX Particles & Bullet Tracers
const sparkGeo = new fn(0.045, 6, 6);
const tracerGeo = new pn(0.012, 0.012, 1, 6);
function spawnBurst(pos, color, count = 8, speed = 3.8) {
  const mat = new Yi({ color });
  for (let i = 0; i < count; i++) {
    const m = new et(sparkGeo, mat);
    m.position.copy(pos);
    Ht.add(m);
    ZGAME.particles.push({
      mesh: m,
      vel: new A((Math.random() - 0.5) * speed, Math.random() * speed * 0.8 + 0.6, (Math.random() - 0.5) * speed),
      life: 0.35 + Math.random() * 0.25
    });
  }
}
function spawnTracer(start, end, color = 0xffe066) {
  const dist = start.distanceTo(end);
  if (dist < 0.1) return;
  const mat = new Yi({ color, transparent: true, opacity: 0.85 });
  const m = new et(tracerGeo, mat);
  m.position.copy(start).lerp(end, 0.5);
  m.scale.set(1, dist, 1);
  const dir = new A().subVectors(end, start).normalize();
  m.quaternion.setFromUnitVectors(new A(0, 1, 0), dir);
  Ht.add(m);
  ZGAME.particles.push({ mesh: m, vel: new A(0, 0, 0), life: 0.065, isTracer: true });
}
function spawnShockwave(pos, color = 0x38bdf8, maxScale = 4.2) {
  const m = new et(new xa(0.45, 0.62, 24), new Yi({ color, side: Gt, transparent: true, opacity: 0.85 }));
  m.rotation.x = -Math.PI / 2;
  m.position.set(pos.x, pos.y + 0.18, pos.z);
  Ht.add(m);
  ZGAME.particles.push({ mesh: m, vel: new A(0, 0, 0), life: 0.36, isRing: true, maxScale });
}

// Eject Spinning Brass/Shotgun Shell Casing
const shellGeo = new pn(0.006, 0.006, 0.026, 6);
function spawnShellCasing(origin, forward, isShotgun) {
  const mat = new Jt({ color: isShotgun ? 0xdc2626 : 0xfbbf24, roughness: 0.28, metalness: 0.82 });
  const m = new et(shellGeo, mat);
  if (isShotgun) m.scale.set(1.6, 1.4, 1.6);
  const right = new A().crossVectors(forward, new A(0, 1, 0)).normalize();
  m.position.copy(origin).addScaledVector(forward, 0.32).addScaledVector(right, 0.14).add(new A(0, -0.06, 0));
  Ht.add(m);
  const vel = right.multiplyScalar(1.6 + Math.random() * 0.9).add(new A(0, 1.4 + Math.random() * 0.6, 0));
  ZGAME.particles.push({ mesh: m, vel, life: 0.75, spin: new A(14, 18, 12) });
}

// Glowing Lightsaber Plasma Slash Trail Segment
const trailGeo = new _i(0.11, 0.78);
function spawnSaberTrail(pos, quat, color = 0x22d3ee) {
  const mat = new Yi({ color, transparent: true, opacity: 0.42, side: Gt, depthWrite: false });
  const m = new et(trailGeo, mat);
  m.position.copy(pos);
  m.quaternion.copy(quat);
  Ht.add(m);
  ZGAME.particles.push({ mesh: m, vel: new A(0, 0, 0), life: 0.16, maxLife: 0.16, isFade: true });
}

// Campus Ground Pickups: Iron Construction Rods & Fallen Tree Branches
function populateCampusPickups() {
  for (const p of ZGAME.pickups) Ht.remove(p.root);
  ZGAME.pickups.length = 0;

  const spots = [
    // Near A-Block Plaza & Main Approach
    [-6, 24, "iron_rod"], [4, 22, "fallen_branch"], [-12, 30, "fallen_branch"], [10, 29, "iron_rod"],
    // Near Volleyball Courts & Avenue Trees
    [-22, 18, "fallen_branch"], [-28, 28, "iron_rod"], [19, 16, "fallen_branch"], [26, 26, "iron_rod"],
    // G-Block Approach & Library Road
    [22, 2, "iron_rod"], [25, -14, "fallen_branch"], [-30, 8, "iron_rod"], [-34, -12, "fallen_branch"],
    // Main Road & Courtyard
    [-3, 44, "iron_rod"], [8, 48, "fallen_branch"], [-16, 46, "fallen_branch"], [38, 26, "iron_rod"]
  ];

  const rodMat = new Jt({ color: 0x6b5347, roughness: 0.55, metalness: 0.72 });
  const branchMat = new Jt({ color: 0x5c3d22, roughness: 0.88, metalness: 0.02 });
  const ringMat = new Yi({ color: 0xfbbf24, side: Gt, transparent: true, opacity: 0.72 });

  for (const [x, z, kind] of spots) {
    if (yo(x, z)) continue;
    const root = new fi();
    const gy = groundAt(x, z);
    root.position.set(x, gy + 0.06, z);

    const mesh = new et(
      kind === "iron_rod" ? (blenderGeos.iron_rod || new pn(0.015, 0.015, 0.95, 10))
                          : (blenderGeos.fallen_branch || new pn(0.02, 0.012, 0.92, 10)),
      kind === "iron_rod" ? rodMat : branchMat
    );
    mesh.rotation.set(Math.PI * 0.46, Math.random() * Math.PI * 2, 0.15);
    mesh.position.y = 0.08;
    root.add(mesh);

    const ring = new et(new xa(0.36, 0.48, 20), ringMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = 0.02;
    root.add(ring);

    Ht.add(root);
    ZGAME.pickups.push({
      root, mesh, ring, x, z, kind,
      weaponIdx: kind === "iron_rod" ? 4 : 5,
      label: kind === "iron_rod" ? "Iron Construction Rod" : "Fallen Tree Branch",
      available: true
    });
  }

  // Campus First-Aid Medkits (+35 HP when walked over!)
  for (const mk of ZGAME.medkits) Ht.remove(mk.root);
  ZGAME.medkits.length = 0;
  const medSpots = [[-2, 16], [14, 24], [-18, 26], [24, -6], [-28, 12], [0, 38]];
  const boxMat = new Jt({ color: 0xf8fafc, roughness: 0.4 });
  const crossMat = new Yi({ color: 0x22c55e });
  for (const [mx, mz] of medSpots) {
    if (yo(mx, mz)) continue;
    const root = new fi();
    root.position.set(mx, groundAt(mx, mz) + 0.28, mz);
    const box = new et(new Ni(0.36, 0.24, 0.24), boxMat);
    root.add(box);
    const c1 = new et(new Ni(0.16, 0.05, 0.255), crossMat); root.add(c1);
    const c2 = new et(new Ni(0.05, 0.16, 0.255), crossMat); root.add(c2);
    Ht.add(root);
    ZGAME.medkits.push({ root, x: mx, z: mz, active: true });
  }
}

// Clean Stylized Cartoon Human Faculty Zombie Builder (Formal Shirt/Suit + Tie + Trousers + Articulated Knees/Elbows + Faculty ID Card!)
function createFacultyZombie(lvlDef, x, z) {
  const root = new fi();
  const s = lvlDef.scale;
  const gy = groundAt(x, z);
  root.position.set(x, gy, z);
  root.scale.set(s, s, s);

  const zSkin = new Jt({ color: lvlDef.skin, roughness: 0.62, metalness: 0.04 });
  const zCoat = new Jt({ color: lvlDef.coat, roughness: 0.72, metalness: 0.06 });
  const zShirtWhite = new Jt({ color: 0xf1f5f9, roughness: 0.68 });
  const zPants = new Jt({ color: lvlDef.pants, roughness: 0.80 });
  const zShoe = new Jt({ color: 0x111418, roughness: 0.45, metalness: 0.15 });
  const zBelt = new Jt({ color: 0x1a1512, roughness: 0.5 });
  const zHair = new Jt({ color: lvlDef.hair || 0x1c1917, roughness: 0.85 });
  const zTie = new Jt({ color: lvlDef.tie || 0x991b1b, roughness: 0.52 });
  const eyeColor = lvlDef.isBoss ? 0xff2222 : (lvlDef.level >= 4 ? 0xffaa00 : 0xd9ff33);
  const zEye = new Yi({ color: eyeColor });

  // 1. Articulated Cartoon Human Legs (Hip + Knee + Formal Trousers + Dress Shoes!)
  const legs = [];
  for (const side of [-1, 1]) {
    const hip = new fi();
    hip.position.set(side * 0.115, 0.86, 0);
    const thigh = new et(new sa(0.078, 0.30, 6, 12), zPants);
    thigh.position.y = -0.21;
    thigh.castShadow = true;
    hip.add(thigh);

    const knee = new fi();
    knee.position.set(0, -0.42, 0);
    const shin = new et(new sa(0.065, 0.30, 6, 12), zPants);
    shin.position.y = -0.20;
    shin.castShadow = true;
    knee.add(shin);

    // Formal Black Dress Shoe
    const shoe = new et(new sa(0.056, 0.12, 6, 10), zShoe);
    shoe.rotation.x = Math.PI / 2;
    shoe.scale.set(1.05, 1.0, 0.78);
    shoe.position.set(0, -0.40, 0.045);
    knee.add(shoe);

    hip.add(knee);
    root.add(hip);
    legs.push({ hip, knee });
  }

  // 2. Stylized Cartoon Masculine Formal Torso (Shirt/Blazer + Belt + Collar + Tie + Faculty ID Card!)
  const torso = new fi();
  torso.position.set(0, 0.86, 0);

  // Pelvis / Waist + Leather Belt + Gold Buckle
  const waist = new et(new pn(0.16, 0.155, 0.16, 16), zPants);
  waist.scale.set(1.22, 1, 0.82);
  waist.position.set(0, 0.04, 0);
  torso.add(waist);

  const belt = new et(new pn(0.168, 0.168, 0.048, 16), zBelt);
  belt.scale.set(1.22, 1, 0.84);
  belt.position.set(0, 0.10, 0);
  torso.add(belt);
  const buckle = new et(new Ni(0.055, 0.042, 0.025), new Jt({ color: 0xfbbf24, roughness: 0.25, metalness: 0.85 }));
  buckle.position.set(0, 0.10, 0.142);
  torso.add(buckle);

  // Broad Formal Chest (tapered masculine V-shape)
  const chest = new et(new pn(0.215, 0.165, 0.48, 16), zCoat);
  chest.scale.set(1.18, 1, 0.72);
  chest.position.set(0, 0.35, 0);
  chest.castShadow = true;
  torso.add(chest);

  // Crisp White Dress Shirt V-Front & Collar
  const vShirt = new et(new Ni(0.13, 0.24, 0.03), zShirtWhite);
  vShirt.position.set(0, 0.46, 0.145);
  torso.add(vShirt);
  const collar = new et(new pn(0.088, 0.102, 0.055, 16), zShirtWhite);
  collar.position.set(0, 0.60, 0);
  torso.add(collar);

  // Formal Necktie (knot + hanging blade)
  const tieKnot = new et(new Ni(0.048, 0.045, 0.028), zTie);
  tieKnot.position.set(0, 0.54, 0.162);
  torso.add(tieKnot);
  const tieBlade = new et(new Ni(0.044, 0.30, 0.020), zTie);
  tieBlade.position.set(0, 0.38, 0.160);
  torso.add(tieBlade);

  // FACULTY ID CARD + COLORED LANYARD (Swinging cleanly on chest!)
  const lanyardMat = new Jt({ color: lvlDef.lanyard, roughness: 0.55 });
  const strapL = new et(new Ni(0.014, 0.22, 0.012), lanyardMat);
  strapL.position.set(-0.052, 0.49, 0.158); strapL.rotation.z = -0.25;
  torso.add(strapL);
  const strapR = new et(new Ni(0.014, 0.22, 0.012), lanyardMat);
  strapR.position.set(0.052, 0.49, 0.158); strapR.rotation.z = 0.25;
  torso.add(strapR);

  const idCardPivot = new fi();
  idCardPivot.position.set(0, 0.38, 0.176);
  const idCard = new et(new Ni(0.12, 0.165, 0.010), new Yi({ map: getFacultyIdCardTexture(lvlDef) }));
  idCard.position.set(0, -0.084, 0);
  idCardPivot.add(idCard);
  torso.add(idCardPivot);

  root.add(torso);

  // 3. Expressive Cartoon Human Zombie Head (Neck + Head + Ears + Hair + Angry Brows + Glowing Eyes + Teeth!)
  const headGroup = new fi();
  headGroup.position.set(0, 1.48, 0);

  const neck = new et(new pn(0.062, 0.072, 0.10, 12), zSkin);
  neck.position.set(0, 0.03, 0);
  headGroup.add(neck);

  const cranium = new et(new fn(0.145, 18, 14), zSkin);
  cranium.scale.set(0.92, 1.08, 0.96);
  cranium.position.set(0, 0.18, 0);
  cranium.castShadow = true;
  headGroup.add(cranium);

  // Nose & Ears
  const nose = new et(new fn(0.024, 8, 8), zSkin);
  nose.scale.set(0.85, 1.25, 1.15);
  nose.position.set(0, 0.165, 0.14);
  headGroup.add(nose);
  for (const side of [-1, 1]) {
    const ear = new et(new fn(0.028, 8, 8), zSkin);
    ear.scale.set(0.55, 1.15, 0.85);
    ear.position.set(side * 0.132, 0.175, 0);
    headGroup.add(ear);
  }

  // Expressive Cartoon Undead Eyes (dark rings + glowing pupils + angry eyebrows!)
  const bagMat = new Jt({ color: 0x1e301c, roughness: 0.9 });
  for (const side of [-1, 1]) {
    const bag = new et(new fn(0.032, 10, 8), bagMat);
    bag.scale.set(1.15, 0.9, 0.45);
    bag.position.set(side * 0.048, 0.195, 0.122);
    headGroup.add(bag);
    const eye = new et(new fn(0.017, 10, 8), zEye);
    eye.position.set(side * 0.048, 0.195, 0.134);
    headGroup.add(eye);
    const brow = new et(new Ni(0.056, 0.015, 0.018), zHair);
    brow.position.set(side * 0.048, 0.232, 0.134);
    brow.rotation.z = -side * 0.24;
    headGroup.add(brow);
  }

  // Snarling Zombie Mouth + White Cartoon Teeth
  const mouth = new et(new Ni(0.078, 0.032, 0.022), new Yi({ color: 0x2b0a0a }));
  mouth.position.set(0, 0.108, 0.128);
  headGroup.add(mouth);
  const teeth = new et(new Ni(0.068, 0.011, 0.024), new Yi({ color: 0xeef2d8 }));
  teeth.position.set(0, 0.118, 0.130);
  headGroup.add(teeth);

  // Clean Styled Male Faculty Hair
  const hairTop = new et(new fn(0.148, 16, 12), zHair);
  hairTop.scale.set(0.96, 0.58, 1.02);
  hairTop.position.set(0, 0.275, -0.012);
  headGroup.add(hairTop);
  const hairBack = new et(new fn(0.138, 14, 10), zHair);
  hairBack.scale.set(0.94, 0.78, 0.65);
  hairBack.position.set(0, 0.21, -0.068);
  headGroup.add(hairBack);

  // Faculty Glasses (Professors & HODs)
  if (lvlDef.glasses) {
    const glMat = new Jt({ color: 0x0f172a, roughness: 0.25, metalness: 0.75 });
    for (const side of [-1, 1]) {
      const rim = new et(new gn(0.032, 0.0048, 6, 16), glMat);
      rim.position.set(side * 0.048, 0.195, 0.146);
      headGroup.add(rim);
    }
    const bridge = new et(new Ni(0.032, 0.006, 0.006), glMat);
    bridge.position.set(0, 0.198, 0.146);
    headGroup.add(bridge);
  }

  // CEO Boss Golden Crown
  if (lvlDef.isBoss) {
    const crown = new et(new gn(0.155, 0.016, 8, 22), new Yi({ color: 0xf59e0b }));
    crown.rotation.x = Math.PI / 2;
    crown.position.set(0, 0.36, 0);
    headGroup.add(crown);
  }
  root.add(headGroup);

  // 4. Articulated Reaching Cartoon Arms (Shoulder + Formal Sleeve + Elbow + Cuff + Green Zombie Hand!)
  const arms = [];
  for (const side of [-1, 1]) {
    const sh = new fi();
    sh.position.set(side * 0.275, 1.38, 0);
    const upper = new et(new sa(0.060, 0.24, 6, 10), zCoat);
    upper.position.set(0, -0.15, 0);
    upper.castShadow = true;
    sh.add(upper);

    const elbow = new fi();
    elbow.position.set(0, -0.30, 0);
    const fore = new et(new sa(0.052, 0.22, 6, 10), zCoat);
    fore.position.set(0, -0.13, 0);
    elbow.add(fore);

    const cuff = new et(new pn(0.048, 0.048, 0.032, 12), zShirtWhite);
    cuff.position.set(0, -0.25, 0);
    elbow.add(cuff);

    const hand = new et(new fn(0.054, 10, 8), zSkin);
    hand.scale.set(0.85, 1.15, 0.72);
    hand.position.set(0, -0.31, 0);
    elbow.add(hand);

    elbow.rotation.x = -0.38; // Natural bent zombie grabbing elbows
    sh.rotation.x = -1.18;    // Reaching straight forward toward player!
    sh.add(elbow);
    root.add(sh);
    arms.push({ sh, elbow });
  }

  // 5. Diegetic Floating HP Bar above Zombie
  const hpBarBg = new et(new _i(0.56, 0.07), new Yi({ color: 0x0f172a, side: Gt }));
  hpBarBg.position.set(0, 2.02, 0);
  const hpBarFill = new et(new _i(0.52, 0.045), new Yi({ color: lvlDef.isBoss ? 0xf59e0b : 0xef4444, side: Gt }));
  hpBarFill.position.set(0, 0, 0.004);
  hpBarBg.add(hpBarFill);
  hpBarBg.visible = lvlDef.isBoss;
  root.add(hpBarBg);

  Ht.add(root);
  return {
    root, torso, headGroup, idCardPivot, arms, legs, hpBarBg, hpBarFill,
    lvlDef, hp: lvlDef.hp, maxHp: lvlDef.hp,
    speed: lvlDef.speed * (0.9 + Math.random() * 0.2),
    alive: true, deathTimer: 0, attackCd: 0, hitFlash: 0, meleeHitCd: 0,
    phase: Math.random() * Math.PI * 2,
    knockVel: new A(),
    boltCd: 3.2, slamCd: 5.5,
    canThrow: lvlDef.level >= 3 && (lvlDef.isBoss || Math.random() < 0.62),
    throwCd: 2.2 + Math.random() * 2.8,
    skinMat: zSkin, baseSkinHex: lvlDef.skin
  };
}

// Strictly inside Anurag University campus walls (NEVER outside on Venkatapur Main Road Z > 58!)
function isInsideCampus(x, z) {
  return x >= -112 && x <= 102 && z >= -92 && z <= 58;
}

function findZombieSpawnAround(px, pz, minDist = 16, maxDist = 30) {
  const baseX = so.clamp(px, -95, 85);
  const baseZ = Math.min(pz, 46); // Keep spawn anchor well inside the campus gate
  for (let tries = 0; tries < 55; tries++) {
    const ang = Math.random() * Math.PI * 2;
    const dist = minDist + Math.random() * (maxDist - minDist);
    const sx = baseX + Math.cos(ang) * dist;
    const sz = baseZ + Math.sin(ang) * dist;
    if (isInsideCampus(sx, sz) && !yo(sx, sz)) return [sx, sz];
  }
  // Safe fallback inside A-Block Central Plaza
  return [-3 + (Math.random() - 0.5) * 18, 26 + (Math.random() - 0.5) * 12];
}

function clearZombiesAndFX() {
  for (const z of ZGAME.zombies) Ht.remove(z.root);
  ZGAME.zombies.length = 0;
  for (const pr of ZGAME.projectiles) Ht.remove(pr.mesh);
  ZGAME.projectiles.length = 0;
  for (const pt of ZGAME.particles) Ht.remove(pt.mesh);
  ZGAME.particles.length = 0;
  for (const fw of ZGAME.fireworks) Ht.remove(fw.mesh);
  ZGAME.fireworks.length = 0;
  if (ZGAME.vrWinBanner) ZGAME.vrWinBanner.visible = false;
  if (ZGAME.vrDeathBanner) ZGAME.vrDeathBanner.visible = false;
}

// Spectacular 3D Campus Victory Fireworks & Giant 3D "YOU WON!" Sky Banner (PC + Meta Quest 3!)
const FW_COLORS = [0xfde047, 0x22d3ee, 0xff4d6d, 0x4ade80, 0xc084fc, 0xfb923c, 0xffffff];
const fwSparkGeo = new fn(0.16, 6, 6);
function launchCampusFirework() {
  // Launch rockets from around A-Block Plaza, Courtyard, Volleyball Courts & Main Gate!
  const spots = [[-3, 18], [-22, 20], [18, 20], [-14, 38], [12, 38], [-3, 4], [28, 8], [-30, 10]];
  const [sx, sz] = spots[Math.floor(Math.random() * spots.length)];
  const col = FW_COLORS[Math.floor(Math.random() * FW_COLORS.length)];
  const rocket = new et(new pn(0.08, 0.12, 0.75, 6), new Yi({ color: col }));
  rocket.position.set(sx + (Math.random() - 0.5) * 10, groundAt(sx, sz) + 1.2, sz + (Math.random() - 0.5) * 10);
  Ht.add(rocket);
  ZGAME.fireworks.push({
    mesh: rocket,
    vy: 22 + Math.random() * 10,
    targetY: 22 + Math.random() * 15,
    color: col
  });
}

function explodeFirework(pos, color) {
  playSFX("firework");
  const col2 = FW_COLORS[Math.floor(Math.random() * FW_COLORS.length)];
  const mat1 = new Yi({ color });
  const mat2 = new Yi({ color: col2 });
  for (let i = 0; i < 34; i++) {
    const m = new et(fwSparkGeo, i % 3 === 0 ? mat2 : mat1);
    m.position.copy(pos);
    Ht.add(m);
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const spd = 7.5 + Math.random() * 9.5;
    ZGAME.particles.push({
      mesh: m,
      vel: new A(Math.sin(phi) * Math.cos(theta) * spd, Math.cos(phi) * spd + 2.5, Math.sin(phi) * Math.sin(theta) * spd),
      life: 1.15 + Math.random() * 0.55
    });
  }
  spawnShockwave(new A(pos.x, pos.y, pos.z), color, 7.5);
}

function show3DWinSkyBanner() {
  if (!ZGAME.vrWinBanner) {
    const c = document.createElement("canvas"); c.width = 1024; c.height = 384;
    const g = c.getContext("2d");
    g.fillStyle = "rgba(8,18,32,0.88)"; g.fillRect(0, 0, 1024, 384);
    g.strokeStyle = "#fde047"; g.lineWidth = 10; g.strokeRect(8, 8, 1008, 368);
    g.fillStyle = "#fde047"; g.font = "900 132px Georgia,serif"; g.textAlign = "center";
    g.fillText("YOU WON!", 512, 178);
    g.fillStyle = "#72efdd"; g.font = "bold 42px sans-serif";
    g.fillText("ANURAG UNIVERSITY IS SAVED!", 512, 262);
    g.fillStyle = "#ffffff"; g.font = "bold 28px sans-serif";
    g.fillText("ALL 6 PHASES & THE CEO DEFEATED · PRESS R / B TO PLAY AGAIN", 512, 332);
    const tex = new dn(c); tex.colorSpace = vt;
    const mesh = new et(new _i(16, 6), new Yi({ map: tex, transparent: true, side: Gt }));
    mesh.position.set(-3, 15.5, 18);
    Ht.add(mesh);
    ZGAME.vrWinBanner = mesh;
  }
  ZGAME.vrWinBanner.visible = true;
}

function updateVictoryFireworks(dt) {
  if (!ZGAME.victory) return;
  ZGAME.fireworkTimer -= dt;
  if (ZGAME.fireworkTimer <= 0) {
    ZGAME.fireworkTimer = 0.42 + Math.random() * 0.45;
    launchCampusFirework();
  }
  for (let i = ZGAME.fireworks.length - 1; i >= 0; i--) {
    const fw = ZGAME.fireworks[i];
    fw.mesh.position.y += fw.vy * dt;
    if (fw.mesh.position.y >= fw.targetY) {
      explodeFirework(fw.mesh.position.clone(), fw.color);
      Ht.remove(fw.mesh);
      ZGAME.fireworks.splice(i, 1);
    }
  }
  if (ZGAME.vrWinBanner && ZGAME.vrWinBanner.visible) {
    ZGAME.vrWinBanner.lookAt(xt.position.x, 15.5, xt.position.z);
  }
}

function formatTimer(sec) {
  const s = Math.max(0, Math.ceil(sec));
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${m}:${r < 10 ? "0" : ""}${r}`;
}

function spawnZombieWave(levelIdx) {
  ZGAME.levelIdx = levelIdx;
  ZGAME.bossSummonedMinions = false;
  const lvl = ZOMBIE_LEVELS[levelIdx];
  ZGAME.phaseTimer = lvl.isBoss ? 0 : 120; // 2 minutes (120s) to survive each phase 1-5; Boss phase until CEO is defeated!
  ZGAME.spawnTimer = 2.8;

  // Respawn campus medkits each phase so players can scavenge across campus
  for (const mk of ZGAME.medkits) { mk.active = true; mk.root.visible = true; }

  const px = xt.position.x, pz = xt.position.z;
  const initialCount = lvl.isBoss ? 1 : Math.min(5, lvl.count);
  for (let i = 0; i < initialCount; i++) {
    const [sx, sz] = findZombieSpawnAround(px, pz, lvl.isBoss ? 22 : 16, lvl.isBoss ? 28 : 30);
    ZGAME.zombies.push(createFacultyZombie(lvl, sx, sz));
  }
  showToast(
    lvl.isBoss ? "FINAL BOSS: DEFEAT THE CEO!" : `LEVEL ${lvl.level}: ${lvl.name.toUpperCase()} · SURVIVE 2:00!`,
    3.2
  );
  playSFX(lvl.isBoss ? "boss_roar" : "levelup");
  updateCombatHUD();
}

// Cinematic Aerial-to-First-Person Story Intro Controller
const INTRO_BEATS = [
  { t: 0.0, kicker: "ANURAG UNIVERSITY · VENKATAPUR CAMPUS", head: "WELCOME TO ANURAG UNIVERSITY", sub: "A peaceful evening across A-Block, Central Plaza & the Sports Grounds... until the bio-lab alarm sounded." },
  { t: 3.5, kicker: "BIO-CONTAINMENT BREACH DETECTED", head: "SAVE YOURSELF FROM THE INFECTED FACULTY!", sub: "Lab Assistants · Jr. Professors · Professors · Placement Incharges · HODs · and THE CEO have turned!" },
  { t: 7.2, kicker: "ENTERING FIRST-PERSON COMBAT", head: "EQUIP YOUR HI-TECH SHIELD & LIGHTSABER", sub: "Defend the campus across all 6 levels · Grab fallen rods & branches · Defeat the CEO!" }
];

function createVRStoryBanner() {
  if (ZGAME.vrStoryBanner) return ZGAME.vrStoryBanner;
  const c = document.createElement("canvas"); c.width = 1024; c.height = 320;
  const tex = new dn(c); tex.colorSpace = vt;
  const mesh = new et(new _i(4.0, 1.25), new Yi({ map: tex, transparent: true, side: Gt, depthTest: false }));
  mesh.position.set(0, 1.95, -4.1);
  mesh.renderOrder = 25;
  mesh.userData = { canvas: c, ctx: c.getContext("2d"), tex, lastBeat: -1 };
  xt.add(mesh);
  ZGAME.vrStoryBanner = mesh;
  return mesh;
}

function redrawVRStoryBanner(beat, progress) {
  const mesh = createVRStoryBanner();
  const { ctx: g, tex } = mesh.userData;
  g.clearRect(0, 0, 1024, 320);
  const grad = g.createLinearGradient(0, 0, 1024, 320);
  grad.addColorStop(0, "rgba(7,15,28,0.94)");
  grad.addColorStop(1, "rgba(30,10,18,0.92)");
  g.fillStyle = grad; g.fillRect(0, 0, 1024, 320);
  g.strokeStyle = "#72efdd"; g.lineWidth = 5; g.strokeRect(5, 5, 1014, 310);
  // Glowing AU Crest badge
  g.fillStyle = "#ef4444"; g.fillRect(36, 26, 62, 34);
  g.fillStyle = "#ffffff"; g.font = "900 22px sans-serif"; g.textAlign = "center";
  g.fillText("AU", 67, 51);
  g.fillStyle = "#fde047"; g.font = "800 24px sans-serif"; g.textAlign = "left";
  g.fillText(beat.kicker, 114, 51);
  // Headline
  g.textAlign = "center";
  g.fillStyle = "#ffffff"; g.font = "900 44px Georgia,serif";
  g.fillText(beat.head, 512, 134);
  // Accent divider
  const dGrad = g.createLinearGradient(260, 0, 764, 0);
  dGrad.addColorStop(0, "rgba(239,68,68,0)"); dGrad.addColorStop(0.5, "#fbbf24"); dGrad.addColorStop(1, "rgba(56,189,248,0)");
  g.fillStyle = dGrad; g.fillRect(260, 154, 504, 4);
  // Subtitle
  g.fillStyle = "#cfeaf7"; g.font = "600 23px sans-serif";
  g.fillText(beat.sub.slice(0, 78), 512, 202);
  g.fillStyle = "#72efdd"; g.font = "700 20px sans-serif";
  g.fillText("Press A to Skip  ·  L-Trigger: Energy Shield  ·  Swing Saber / R-Trigger: Fire", 512, 252);
  // Live cinema progress bar
  g.fillStyle = "rgba(255,255,255,0.16)"; g.fillRect(40, 286, 944, 10);
  g.fillStyle = "#38bdf8"; g.fillRect(40, 286, Math.max(8, 944 * progress), 10);
  tex.needsUpdate = true;
}

// Head-Locked VR Top-Left Floating Heart Health Visor HUD (tracks live Ye.xr.getCamera() every VR frame!)
function createVRTopLeftHealthHUD() {
  if (ZGAME.vrTopLeftHud) return ZGAME.vrTopLeftHud;
  const c = document.createElement("canvas"); c.width = 512; c.height = 192;
  const tex = new dn(c); tex.colorSpace = vt;
  const mesh = new et(new _i(0.24, 0.09), new Yi({ map: tex, transparent: true, depthTest: false, depthWrite: false }));
  mesh.renderOrder = 30;
  mesh.visible = false;
  mesh.userData = { canvas: c, ctx: c.getContext("2d"), tex, lastKey: "" };
  Ht.add(mesh);
  ZGAME.vrTopLeftHud = mesh;
  return mesh;
}

const _vrHudPos = new A(), _vrHudQuat = new Ot(), _vrHudOff = new A(), _vrHudTilt = new Ot().setFromAxisAngle(new A(0, 1, 0), 0.22);

function updateVRTopLeftHealthHUD() {
  const hud = createVRTopLeftHealthHUD();
  const show = Boolean(Ye.xr.isPresenting && ZGAME.active && !ZGAME.introPlaying && !ZGAME.gameOver);
  hud.visible = show;
  if (!show) return;

  // Lock rock-solid to the live Meta Quest 3 WebXR headset pose in the upper-left peripheral view!
  const xrCam = Ye.xr.getCamera();
  if (xrCam) {
    xrCam.getWorldPosition(_vrHudPos);
    xrCam.getWorldQuaternion(_vrHudQuat);
    _vrHudOff.set(-0.24, 0.155, -0.72).applyQuaternion(_vrHudQuat);
    hud.position.copy(_vrHudPos).add(_vrHudOff);
    hud.quaternion.copy(_vrHudQuat).multiply(_vrHudTilt);
  }
  const hpInt = Math.ceil(ZGAME.hp);
  const shInt = Math.ceil(ZGAME.shield);
  const lvl = ZOMBIE_LEVELS[ZGAME.levelIdx] || ZOMBIE_LEVELS[0];
  const timerStr = !ZGAME.campusEntered ? "GATE" : (lvl.isBoss ? "BOSS" : formatTimer(ZGAME.phaseTimer));
  const key = `${hpInt}|${shInt}|${timerStr}|${ZGAME.kills}`;
  if (hud.userData.lastKey === key) return;
  hud.userData.lastKey = key;

  const { ctx: g, tex } = hud.userData;
  g.clearRect(0, 0, 512, 192);
  // Glassmorphic dark panel with glowing crimson border
  const low = ZGAME.hp <= 35;
  g.fillStyle = low ? "rgba(48,10,18,0.92)" : "rgba(10,16,28,0.88)";
  g.fillRect(6, 6, 500, 180);
  g.strokeStyle = low ? "#ff1e38" : "rgba(255,77,109,0.88)";
  g.lineWidth = 6; g.strokeRect(6, 6, 500, 180);

  // Big Glowing Heart + 5 RPG Hearts + Numeric HP
  const filled = Math.max(0, Math.min(5, Math.ceil(ZGAME.hp / 20)));
  g.fillStyle = "#ff2e55"; g.font = "900 44px sans-serif"; g.textAlign = "left";
  g.fillText("♥", 22, 58);
  g.fillStyle = "#ff4d6d"; g.font = "900 34px sans-serif";
  g.fillText("♥".repeat(filled) + "♡".repeat(5 - filled), 68, 54);
  g.fillStyle = "#fff1f2"; g.font = "900 30px Consolas,monospace"; g.textAlign = "right";
  g.fillText(`${hpInt}/${ZGAME.maxHp}`, 488, 54);

  // Smooth Gradient HP Bar
  const hpPct = Math.max(0, Math.min(1, ZGAME.hp / ZGAME.maxHp));
  g.fillStyle = "rgba(255,255,255,0.16)"; g.fillRect(22, 74, 466, 22);
  const hpGrad = g.createLinearGradient(22, 0, 488, 0);
  hpGrad.addColorStop(0, "#ef4444"); hpGrad.addColorStop(0.5, "#f97316"); hpGrad.addColorStop(1, "#22c55e");
  g.fillStyle = hpGrad; g.fillRect(22, 74, Math.max(4, 466 * hpPct), 22);

  // Cyan Shield Mini Bar
  const shPct = Math.max(0, Math.min(1, ZGAME.shield / 100));
  g.fillStyle = "rgba(255,255,255,0.14)"; g.fillRect(22, 110, 466, 12);
  g.fillStyle = "#38bdf8"; g.fillRect(22, 110, Math.max(2, 466 * shPct), 12);

  // Clean 3-Column Bottom Status Row: SHIELD | TIMER | KILLS
  g.font = "800 22px Consolas,monospace";
  g.textAlign = "left"; g.fillStyle = "#72efdd"; g.fillText(`SHD ${shInt}%`, 22, 162);
  g.textAlign = "center"; g.fillStyle = "#fde047"; g.fillText(`TIME ${timerStr}`, 262, 162);
  g.textAlign = "right"; g.fillStyle = "#f8fafc"; g.fillText(`KILLS ${ZGAME.kills}`, 488, 162);
  tex.needsUpdate = true;
}

function startStoryIntro() {
  ZGAME.introPlaying = true;
  ZGAME.introTime = 0;
  ZGAME.lastIntroBeatIdx = -1;
  document.body.classList.add("intro-active");
  if (kt("intro-overlay")) kt("intro-overlay").classList.add("playing");
  // Hide 1st-person hands during aerial flyover
  fpHands.forEach(a => (a.root.visible = false));
  if (Ye.xr.isPresenting) {
    createVRStoryBanner().visible = true;
    redrawVRStoryBanner(INTRO_BEATS[0], 0);
  }
  playSFX("levelup");
}

function finishStoryIntro() {
  if (!ZGAME.introPlaying) return;
  ZGAME.introPlaying = false;
  ZGAME.introDoneOnce = true;
  document.body.classList.remove("intro-active");
  if (kt("intro-overlay")) kt("intro-overlay").classList.remove("playing");
  if (ZGAME.vrStoryBanner) ZGAME.vrStoryBanner.visible = false;
  // Snap cleanly to 1st-Person Player Start at Main Gate facing A-Block
  xo(0);
  if (Ye.xr.isPresenting) {
    // In Meta Quest 3 local-floor VR, headset tracks real standing height — keep camPivot at 0!
    camPivot.position.set(0, 0, 0);
    camPivot.rotation.set(0, 0, 0);
    Mi.position.set(0, 0, 0);
  } else {
    if (povMode !== "1st") { povMode = "1st"; updateCameraPOV(); }
    Mi.position.set(0, 0, 0);
    Mi.rotation.set(0, 0, 0);
  }
  syncWeaponVisuals();
  updateVRTopLeftHealthHUD();
  playSFX("saber");
  showToast("ENTER THE CAMPUS GATE TO START LEVEL 1!", 2.8);
}

if (kt("btn-skip-intro")) kt("btn-skip-intro").onclick = () => finishStoryIntro();

function updateStoryIntro(dt) {
  if (!ZGAME.introPlaying) return false;
  ZGAME.introTime += dt;
  const t = Math.min(1, ZGAME.introTime / ZGAME.introDur);

  // Update cinematic story captions with kinetic beat reveal + live progress bar!
  let beatIdx = 0;
  for (let i = 0; i < INTRO_BEATS.length; i++) { if (ZGAME.introTime >= INTRO_BEATS[i].t) beatIdx = i; }
  const beat = INTRO_BEATS[beatIdx];
  if (kt("intro-progress-fill")) kt("intro-progress-fill").style.width = `${(t * 100).toFixed(1)}%`;
  if (ZGAME.lastIntroBeatIdx !== beatIdx) {
    ZGAME.lastIntroBeatIdx = beatIdx;
    if (kt("intro-kicker")) kt("intro-kicker").textContent = beat.kicker;
    if (kt("intro-headline")) {
      const hl = kt("intro-headline");
      hl.textContent = beat.head;
      hl.classList.remove("beat-anim");
      void hl.offsetWidth;
      hl.classList.add("beat-anim");
    }
    if (kt("intro-sub")) {
      const sb = kt("intro-sub");
      sb.textContent = beat.sub;
      sb.classList.remove("beat-anim");
      void sb.offsetWidth;
      sb.classList.add("beat-anim");
    }
  }
  if (Ye.xr.isPresenting) redrawVRStoryBanner(beat, t);

  // Target First-Person Spawn (Main Gate facing A-Block)
  const [_, endX, endZ, endYaw, endPitch = 0.07] = ld[0];
  const endY = groundAt(endX, endZ);

  if (Ye.xr.isPresenting) {
    // Gentle elevated VR aerial descent into Main Gate (keeps headset rotation 100% free & comfortable!)
    const ease = t * t * (3 - 2 * t);
    const rx = so.lerp(28, endX, ease);
    const rz = so.lerp(-18, endZ, ease);
    const ry = so.lerp(24, endY, ease);
    xt.position.set(rx, ry, rz);
    xt.rotation.y = endYaw;
    if (ZGAME.vrStoryBanner) ZGAME.vrStoryBanner.visible = true;
  } else {
    // Sweeping 3-Act Aerial Drone Flyover -> Smooth Dive into 1st-Person POV!
    const smooth = (x) => x * x * (3 - 2 * x);
    let cx, cy, cz, lx, ly, lz;
    if (t < 0.38) {
      // Act 1: High aerial sweep over the entire Anurag University campus
      const u = smooth(t / 0.38);
      cx = so.lerp(56, -42, u);
      cy = so.lerp(46, 30, u);
      cz = so.lerp(-32, 34, u);
      lx = so.lerp(-4, -3, u);
      ly = so.lerp(4, 5, u);
      lz = so.lerp(0, 10, u);
    } else if (t < 0.72) {
      // Act 2: Dramatic swoop down past A-Block palm plaza & courtyard
      const u = smooth((t - 0.38) / 0.34);
      cx = so.lerp(-42, endX + 12, u);
      cy = so.lerp(30, 11, u);
      cz = so.lerp(34, endZ + 14, u);
      lx = so.lerp(-3, endX, u);
      ly = so.lerp(5, 3.2, u);
      lz = so.lerp(10, 14, u);
    } else {
      // Act 3: Seamless dive straight into First-Person Eye Height (1.66m)!
      const u = smooth((t - 0.72) / 0.28);
      cx = so.lerp(endX + 12, endX, u);
      cy = so.lerp(11, endY + 1.66, u);
      cz = so.lerp(endZ + 14, endZ, u);
      lx = endX - Math.sin(endYaw) * 28;
      ly = so.lerp(3.2, endY + 1.66 + Math.sin(endPitch) * 28, u);
      lz = endZ - Math.cos(endYaw) * 28;
    }
    xt.position.set(cx, cy - 1.66, cz);
    xt.rotation.set(0, 0, 0);
    camPivot.position.set(0, 1.66, 0);
    camPivot.rotation.set(0, 0, 0);
    Mi.position.set(0, 0, 0);
    Mi.lookAt(lx, ly, lz);
    fpHands.forEach(a => (a.root.visible = false));
  }

  if (ZGAME.introTime >= ZGAME.introDur) {
    finishStoryIntro();
  }
  return true;
}

function startZombieGame(playIntro = false) {
  if (window.CAMPUS_TOUR_ONLY) return;
  clearZombiesAndFX();
  ZGAME.active = true;
  ZGAME.gameOver = false;
  ZGAME.victory = false;
  ZGAME.levelIdx = 0;
  ZGAME.score = 0;
  ZGAME.kills = 0;
  ZGAME.headshots = 0;
  ZGAME.combo = 0;
  ZGAME.bestCombo = 0;
  ZGAME.comboTimer = 0;
  ZGAME.shake = 0;
  ZGAME.jumpVel = 0;
  ZGAME.jumpY = 0;
  ZGAME.keyShieldDown = false;
  if (kt("end-overlay")) kt("end-overlay").style.display = "none";
  if (kt("combo-badge")) kt("combo-badge").style.display = "none";
  ZGAME.hp = ZGAME.maxHp;
  ZGAME.shield = 100;
  ZGAME.ammo = [Infinity, 15, 30, 8, Infinity, Infinity];
  ZGAME.reloading = 0;
  ZGAME.pickupWeaponIdx = -1;
  ZGAME.waveDelay = 0;
  ZGAME.campusEntered = false;
  ZGAME.phaseTimer = 120;
  selectWeapon(0);
  populateCampusPickups();
  // Ensure 1st-Person POV for combat
  if (povMode !== "1st") { povMode = "1st"; updateCameraPOV(); }
  // Apply Outbreak Dusk atmosphere
  kt("time-mode").value = "outbreak";
  kt("time-mode").dispatchEvent(new Event("change"));
  document.body.classList.add("zombie-mode");
  updateCombatHUD();
  if (playIntro) startStoryIntro();
}

function stopZombieGame() {
  ZGAME.active = false;
  if (ZGAME.vrTopLeftHud) ZGAME.vrTopLeftHud.visible = false;
  clearZombiesAndFX();
  for (const p of ZGAME.pickups) Ht.remove(p.root);
  ZGAME.pickups.length = 0;
  document.body.classList.remove("zombie-mode");
}

function syncWeaponVisuals() {
  const showCombat = !window.CAMPUS_TOUR_ONLY && bo.value === "zombie";
  const allHands = [...fpHands, ...Array.from(trackedHands.values()).map(h => h.arm)];
  for (const arm of allHands) {
    if (arm.shieldGroup) arm.shieldGroup.visible = showCombat && ZGAME.shieldDeploy > 0.03;
    if (arm.weaponMount) {
      arm.weaponMount.visible = showCombat;
      if (arm.weaponModels) {
        arm.weaponModels.forEach((m, i) => (m.visible = showCombat && i === ZGAME.weaponIdx));
      }
      if (arm.weaponMount.userData.laserBeam) {
        const w = WEAPON_DEFS[ZGAME.weaponIdx];
        arm.weaponMount.userData.laserBeam.visible = showCombat && w && w.type === "gun";
      }
      if (arm.muzzleFlash) arm.muzzleFlash.visible = showCombat && ZGAME.muzzleTimer > 0;
    }
  }
}

function selectWeapon(idx) {
  if (idx === 4 && ZGAME.pickupWeaponIdx >= 4) idx = ZGAME.pickupWeaponIdx;
  if ((idx === 4 || idx === 5) && ZGAME.pickupWeaponIdx !== idx) return;
  ZGAME.weaponIdx = idx;
  ZGAME.reloading = 0;
  ZGAME.weaponDrawAnim = 1.0;
  if (idx === 0) {
    ZGAME.saberIgnite = 0.01;
    playSFX("saber_ignite");
  } else {
    playSFX("pickup");
  }
  syncWeaponVisuals();
  updateCombatHUD();
}

function cycleWeapon(dir = 1) {
  const available = [0, 1, 2, 3];
  if (ZGAME.pickupWeaponIdx >= 4) available.push(ZGAME.pickupWeaponIdx);
  const cur = Math.max(0, available.indexOf(ZGAME.weaponIdx));
  const next = available[(cur + dir + available.length) % available.length];
  selectWeapon(next);
}

function pulseHaptics(side, strength = 0.6, durationMs = 70) {
  if (!Ye.xr.isPresenting) return;
  const hand = trackedHands.get(side);
  const act = hand?.source?.gamepad?.hapticActuators?.[0];
  if (act && act.pulse) act.pulse(strength, durationMs).catch(() => {});
}

function tryPickupNearbyWeapon() {
  if (!ZGAME.active || ZGAME.gameOver) return false;
  const px = Ye.xr.isPresenting ? oi.x : xt.position.x;
  const pz = Ye.xr.isPresenting ? oi.z : xt.position.z;
  let best = null, bestD = 2.8;
  for (const p of ZGAME.pickups) {
    if (!p.available) continue;
    const d = Math.hypot(p.x - px, p.z - pz);
    if (d < bestD) { bestD = d; best = p; }
  }
  if (!best) return false;
  best.available = false;
  best.root.visible = false;
  ZGAME.pickupWeaponIdx = best.weaponIdx;
  selectWeapon(best.weaponIdx);
  playSFX("pickup");
  pulseHaptics("right", 0.7, 90);
  showToast(`PICKED UP ${best.label.toUpperCase()}!`, 1.8);
  return true;
}

function triggerReload() {
  const w = WEAPON_DEFS[ZGAME.weaponIdx];
  if (!w || w.type !== "gun" || ZGAME.reloading > 0 || ZGAME.ammo[w.id] === w.mag) return;
  ZGAME.reloading = w.reload;
  ZGAME.reloadTotal = w.reload;
  playSFX("reload");
  updateCombatHUD();
}

function damageZombie(z, dmg, hitPos, knockDir, knockAmt = 1.8, isHeadshot = false) {
  if (!z.alive) return;
  // Higher faculty phases have tougher armor resistance (harder to kill as phases progress!)
  const armorFactor = 1.0 - (z.lvlDef.armor || 0);
  const finalDmg = Math.max(4, dmg * armorFactor);
  z.hp -= finalDmg;
  z.hitFlash = 0.14;
  z.hpBarBg.visible = true;
  if (knockDir) z.knockVel.addScaledVector(knockDir, knockAmt / z.lvlDef.scale);
  spawnBurst(hitPos, isHeadshot ? 0xfef08a : 0x4ade80, isHeadshot ? 11 : 6, 4.2);
  playSFX(isHeadshot ? "headshot" : "hit");
  showHitMarker(isHeadshot, isHeadshot ? `HEADSHOT! -${Math.round(finalDmg)}` : `-${Math.round(finalDmg)}`);

  // CEO Boss Phase 2: Summon Lab Assistants at 50% HP!
  if (z.lvlDef.isBoss && !ZGAME.bossSummonedMinions && z.hp < z.maxHp * 0.5 && z.hp > 0) {
    ZGAME.bossSummonedMinions = true;
    showToast("CEO SUMMONS LAB ASSISTANT REINFORCEMENTS!", 2.5);
    for (let i = 0; i < 3; i++) {
      const [sx, sz] = findZombieSpawnAround(z.root.position.x, z.root.position.z, 5, 10);
      ZGAME.zombies.push(createFacultyZombie(ZOMBIE_LEVELS[0], sx, sz));
    }
  }

  if (z.hp <= 0) {
    z.alive = false;
    z.deathTimer = 1.6;
    z.hpBarBg.visible = false;
    playSFX(z.lvlDef.isBoss ? "boss_roar" : "zdeath");
    ZGAME.kills++;
    if (isHeadshot) ZGAME.headshots++;
    ZGAME.combo++;
    ZGAME.comboTimer = 4.2;
    if (ZGAME.combo > ZGAME.bestCombo) ZGAME.bestCombo = ZGAME.combo;
    const mult = Math.min(4, 1 + Math.floor(ZGAME.combo / 2) * 0.5);
    ZGAME.score += Math.round(((z.lvlDef.isBoss ? 1000 : z.lvlDef.level * 100) + (isHeadshot ? 50 : 0)) * mult);
    spawnBurst(hitPos, 0x22c55e, 14, 5.2);
    const cb = kt("combo-badge");
    if (cb && ZGAME.combo >= 2) {
      cb.style.display = "block";
      cb.textContent = `${ZGAME.combo}x STREAK! (${mult.toFixed(1)}x PTS)`;
    }
  }
  updateCombatHUD();
}

// Real 3D Physical Blade/Rod Segment Collision for Meta Quest 3 VR Hand Swings (No trigger needed!)
function checkVRPhysicalMeleeHit(hand, dt) {
  const w = WEAPON_DEFS[ZGAME.weaponIdx];
  if (!w || w.type !== "melee" || !hand || !hand.anchor.visible) return;

  // Compute real world-space hilt & blade-tip positions matching the calibrated -0.28 rad lightsaber/rod/branch grip!
  const mount = hand.arm.weaponMount;
  if (!mount) return;
  mount.updateWorldMatrix(true, false);
  const hiltWorld = new A(0, -0.01, -0.004).applyMatrix4(mount.matrixWorld);
  const tipLocal = new A(0, 1.04, -0.30);
  const tipWorld = tipLocal.applyMatrix4(mount.matrixWorld);

  const safeDt = Math.max(0.008, dt || 0.016);
  const tipSpeed = tipWorld.distanceTo(ZGAME.vrPrevTipPos) / safeDt;
  ZGAME.vrPrevTipPos.copy(tipWorld);

  // Require a REAL intentional slash/swing (tipSpeed > 1.85 m/s) — lightly touching the saber deals ZERO damage!
  if (tipSpeed < 1.85) return;

  const seg = new A().subVectors(tipWorld, hiltWorld);
  const segLenSq = Math.max(0.001, seg.lengthSq());
  let hitAny = false;

  for (const z of ZGAME.zombies) {
    if (!z.alive || z.meleeHitCd > 0) continue;
    const sc = z.lvlDef.scale;
    // Check closest point on blade segment to zombie torso & head
    const zBody = new A(z.root.position.x, z.root.position.y + 1.15 * sc, z.root.position.z);
    const t = so.clamp(new A().subVectors(zBody, hiltWorld).dot(seg) / segLenSq, 0, 1);
    const closest = hiltWorld.clone().addScaledVector(seg, t);
    const dXZ = Math.hypot(closest.x - zBody.x, closest.z - zBody.z);
    const dY = Math.abs(closest.y - zBody.y);

    if (dXZ < 0.52 * sc && dY < 0.88 * sc) {
      z.meleeHitCd = 0.55;
      const isHead = closest.y > z.root.position.y + 1.48 * sc;
      const speedBonus = so.clamp(tipSpeed / 4.2, 0.8, 1.35);
      const knockDir = new A(zBody.x - hiltWorld.x, 0, zBody.z - hiltWorld.z).normalize();
      damageZombie(z, w.dmg * speedBonus * (isHead ? 1.45 : 1.0), closest, knockDir, w.knockback, isHead);
      spawnBurst(closest, w.key === "saber" ? 0x22d3ee : 0xfde047, 10, 4.8);
      hitAny = true;
    }
  }
  if (hitAny) {
    playSFX(w.key === "saber" ? "saber_clash" : w.key === "iron_rod" ? "rod" : "branch");
    pulseHaptics("right", 0.95, 110);
  }
}

function performMeleeAttack(origin, forward) {
  const w = WEAPON_DEFS[ZGAME.weaponIdx];
  if (!w || w.type !== "melee") return;
  ZGAME.fireCd = w.cooldown;
  ZGAME.swingAnim = 1.0;
  ZGAME.swingDir = -ZGAME.swingDir; // Alternate diagonal slash directions for fluid combo!
  playSFX(w.key === "saber" ? "saber" : w.key === "iron_rod" ? "rod" : "branch");
  pulseHaptics("right", 0.5, 60);

  let hitAny = false;
  for (const z of ZGAME.zombies) {
    if (!z.alive) continue;
    const zPos = new A(z.root.position.x, z.root.position.y + 1.15 * z.lvlDef.scale, z.root.position.z);
    const toZ = new A().subVectors(zPos, origin);
    const dist = toZ.length();
    if (dist > w.range + 0.45 * z.lvlDef.scale) continue;
    const dir = toZ.clone().normalize();
    if (dir.dot(forward) < 0.15 && dist > 1.35) continue;
    const isHead = Math.random() < 0.25;
    damageZombie(z, w.dmg * (isHead ? 1.5 : 1), zPos, new A(dir.x, 0, dir.z).normalize(), w.knockback, isHead);
    hitAny = true;
  }
  if (hitAny) pulseHaptics("right", 0.95, 110);
}

function performGunFire(origin, forward) {
  const w = WEAPON_DEFS[ZGAME.weaponIdx];
  if (!w || w.type !== "gun" || ZGAME.reloading > 0) return;
  if (ZGAME.ammo[w.id] <= 0) { triggerReload(); return; }

  ZGAME.ammo[w.id]--;
  ZGAME.fireCd = w.cooldown;
  ZGAME.recoilAnim = 1.0;
  ZGAME.muzzleTimer = w.key === "shotgun" ? 0.085 : 0.055;
  if (w.key === "shotgun") ZGAME.shake = Math.max(ZGAME.shake, 0.14);
  else if (w.key === "pistol") ZGAME.shake = Math.max(ZGAME.shake, 0.045);
  else ZGAME.shake = Math.max(ZGAME.shake, 0.032);
  playSFX(w.key);
  pulseHaptics("right", w.key === "shotgun" ? 0.95 : 0.65, w.key === "shotgun" ? 110 : 55);
  spawnShellCasing(origin, forward, w.key === "shotgun");

  // Position & randomize starburst muzzle flash rotation on active arm
  const activeRightArms = [fpHands[1], trackedHands.get("right")?.arm].filter(Boolean);
  for (const arm of activeRightArms) {
    if (arm.muzzleFlash) {
      arm.muzzleFlash.position.set(0, 0.055, w.muzzleZ);
      arm.muzzleFlash.rotation.z = Math.random() * Math.PI * 2;
      const mfScale = w.key === "shotgun" ? 1.55 : w.key === "rifle" ? 1.15 : 0.85;
      arm.muzzleFlash.scale.set(mfScale, mfScale, mfScale);
    }
  }

  for (let p = 0; p < w.pellets; p++) {
    const dir = forward.clone();
    dir.x += (Math.random() - 0.5) * w.spread;
    dir.y += (Math.random() - 0.5) * w.spread;
    dir.z += (Math.random() - 0.5) * w.spread;
    dir.normalize();

    let bestZ = null, bestT = w.range, bestHead = false, bestHitPos = null;
    for (const z of ZGAME.zombies) {
      if (!z.alive) continue;
      const sc = z.lvlDef.scale;
      // Check headshot sphere first
      const headC = new A(z.root.position.x, z.root.position.y + 1.62 * sc, z.root.position.z);
      const toH = new A().subVectors(headC, origin);
      const tH = toH.dot(dir);
      if (tH > 0.2 && tH < bestT) {
        const perpSq = toH.lengthSq() - tH * tH;
        const hr = 0.24 * sc;
        if (perpSq < hr * hr) {
          bestT = tH; bestZ = z; bestHead = true;
          bestHitPos = origin.clone().addScaledVector(dir, tH);
          continue;
        }
      }
      // Check torso sphere/capsule approximation
      const bodyC = new A(z.root.position.x, z.root.position.y + 1.05 * sc, z.root.position.z);
      const toB = new A().subVectors(bodyC, origin);
      const tB = toB.dot(dir);
      if (tB > 0.2 && tB < bestT) {
        const perpSq = toB.lengthSq() - tB * tB;
        const br = 0.42 * sc;
        if (perpSq < br * br) {
          bestT = tB; bestZ = z; bestHead = false;
          bestHitPos = origin.clone().addScaledVector(dir, tB);
        }
      }
    }

    const tracerStart = origin.clone().addScaledVector(dir, 0.45).add(new A(0, -0.05, 0));
    const tracerEnd = bestHitPos || origin.clone().addScaledVector(dir, Math.min(35, w.range));
    spawnTracer(tracerStart, tracerEnd, w.key === "rifle" ? 0x38bdf8 : 0xfde047);

    if (bestZ) {
      const dmg = bestHead ? w.dmg * 2.0 : w.dmg;
      damageZombie(bestZ, dmg, bestHitPos, new A(dir.x, 0, dir.z).normalize(), w.key === "shotgun" ? 3.5 : 1.1, bestHead);
    }
  }
  if (ZGAME.ammo[w.id] === 0) triggerReload();
  updateCombatHUD();
}

function triggerShieldBash() {
  if (!ZGAME.active || ZGAME.gameOver || ZGAME.shieldBashCd > 0 || ZGAME.shield < 20) return;
  ZGAME.shieldBashCd = 1.6;
  ZGAME.shieldBashAnim = 1.0;
  ZGAME.shield = Math.max(0, ZGAME.shield - 18);
  playSFX("bash");
  pulseHaptics("left", 0.9, 130);

  const px = Ye.xr.isPresenting ? oi.x : xt.position.x;
  const py = xt.position.y;
  const pz = Ye.xr.isPresenting ? oi.z : xt.position.z;
  spawnShockwave(new A(px, py, pz), 0x38bdf8, 5.2);

  for (const z of ZGAME.zombies) {
    if (!z.alive) continue;
    const dx = z.root.position.x - px, dz = z.root.position.z - pz;
    const d = Math.hypot(dx, dz);
    if (d < 4.5) {
      const push = new A(dx / Math.max(0.1, d), 0, dz / Math.max(0.1, d));
      damageZombie(z, 28, new A(z.root.position.x, z.root.position.y + 1.1, z.root.position.z), push, 7.5, false);
    }
  }
  updateCombatHUD();
}

function showVRDeathBanner() {
  const c = document.createElement("canvas"); c.width = 1024; c.height = 448;
  const g = c.getContext("2d");
  g.fillStyle = "rgba(18,6,10,0.94)"; g.fillRect(0, 0, 1024, 448);
  g.strokeStyle = "#ef4444"; g.lineWidth = 10; g.strokeRect(8, 8, 1008, 432);
  g.fillStyle = "#ff4d4d"; g.font = "900 120px Georgia,serif"; g.textAlign = "center";
  g.fillText("YOU DIED!", 512, 152);
  const lvl = ZOMBIE_LEVELS[ZGAME.levelIdx] || ZOMBIE_LEVELS[0];
  g.fillStyle = "#f8fafc"; g.font = "bold 34px sans-serif";
  g.fillText(`PHASE ${lvl.level} (${lvl.badge})  ·  KILLS: ${ZGAME.kills}  ·  SCORE: ${ZGAME.score}`, 512, 232);
  g.fillStyle = "#0ea5e9"; g.fillRect(72, 286, 410, 100);
  g.fillStyle = "#04151f"; g.font = "900 34px sans-serif";
  g.fillText("[B] RESTART GAME", 277, 348);
  g.fillStyle = "#1e3a52"; g.fillRect(542, 286, 410, 100);
  g.strokeStyle = "#72efdd"; g.lineWidth = 4; g.strokeRect(542, 286, 410, 100);
  g.fillStyle = "#e2f4ff"; g.font = "900 34px sans-serif";
  g.fillText("[X] EXPLORE CAMPUS", 747, 348);
  const tex = new dn(c); tex.colorSpace = vt;
  if (!ZGAME.vrDeathBanner) {
    const mesh = new et(new _i(2.4, 1.05), new Yi({ map: tex, transparent: true, side: Gt }));
    Ht.add(mesh);
    ZGAME.vrDeathBanner = mesh;
  } else {
    ZGAME.vrDeathBanner.material.map = tex;
    ZGAME.vrDeathBanner.material.needsUpdate = true;
  }
  // Place 2.3m right in front of player's current head position & facing direction!
  const px = Ye.xr.isPresenting ? oi.x : xt.position.x;
  const pz = Ye.xr.isPresenting ? oi.z : xt.position.z;
  const yaw = Ye.xr.isPresenting ? xt.rotation.y : vs;
  ZGAME.vrDeathBanner.position.set(px - Math.sin(yaw) * 2.3, xt.position.y + 1.55, pz - Math.cos(yaw) * 2.3);
  ZGAME.vrDeathBanner.lookAt(px, xt.position.y + 1.55, pz);
  ZGAME.vrDeathBanner.visible = true;
}

function enterExploreMode() {
  if (kt("end-overlay")) kt("end-overlay").style.display = "none";
  if (ZGAME.vrDeathBanner) ZGAME.vrDeathBanner.visible = false;
  bo.value = "creative";
  To();
  kt("time-mode").value = "noon";
  kt("time-mode").dispatchEvent(new Event("change"));
  if (!Ye.xr.isPresenting) cd();
}

function showEndScreen(won) {
  const ov = kt("end-overlay");
  if (ov) {
    ov.classList.toggle("won-mode", !!won);
    kt("end-title").textContent = won ? "YOU WON!" : "YOU DIED!";
    kt("end-title").style.color = won ? "#fde047" : "#ff4d4d";
    const lvl = ZOMBIE_LEVELS[ZGAME.levelIdx] || ZOMBIE_LEVELS[0];
    kt("end-stats").innerHTML = `Phase Reached: <b>Level ${lvl.level} (${lvl.name})</b><br>Total Kills: <b>${ZGAME.kills}</b> · Headshots: <b>${ZGAME.headshots}</b><br>Best Kill Streak: <b>${ZGAME.bestCombo}x</b><br>Final Score: <b style="color:#fde047">${ZGAME.score}</b>`;
    ov.style.display = "flex";
  }
  if (won) {
    show3DWinSkyBanner();
    ZGAME.fireworkTimer = 0.2;
    for (let k = 0; k < 4; k++) launchCampusFirework();
    playSFX("victory");
  } else if (Ye.xr.isPresenting) {
    showVRDeathBanner();
  }
}
if (kt("btn-restart-game")) kt("btn-restart-game").onclick = () => { startZombieGame(); cd(); };
if (kt("btn-explore-campus")) kt("btn-explore-campus").onclick = () => enterExploreMode();

function damagePlayer(amount) {
  if (ZGAME.gameOver || ZGAME.victory) return;
  if (ZGAME.shieldBlocking && ZGAME.shield > 5) {
    ZGAME.shield = Math.max(0, ZGAME.shield - amount * 0.85);
    const chip = Math.floor(amount * 0.10);
    ZGAME.hp = Math.max(1, ZGAME.hp - chip);
    ZGAME.shake = Math.max(ZGAME.shake, 0.08);
    playSFX("block");
    pulseHaptics("left", 0.85, 100);
    flashScreen("rgba(56,189,248,0.42)", 0.38);
    showHitMarker(false, "SHIELD BLOCKED!");
  } else {
    ZGAME.hp = Math.max(0, ZGAME.hp - amount);
    ZGAME.shake = Math.max(ZGAME.shake, 0.22);
    playSFX("hurt");
    pulseHaptics("left", 0.7, 90);
    pulseHaptics("right", 0.7, 90);
    flashScreen("rgba(239,68,68,0.55)", 0.48);
  }
  if (ZGAME.hp <= 0) {
    ZGAME.gameOver = true;
    showEndScreen(false);
    document.exitPointerLock?.();
  }
  updateCombatHUD();
}

function triggerPlayerJump() {
  if (!ZGAME.active || ZGAME.introPlaying || ZGAME.gameOver || ZGAME.jumpY > 0.02) return;
  ZGAME.jumpVel = 7.6;
  playSFX("jump");
  pulseHaptics("left", 0.35, 45);
  pulseHaptics("right", 0.35, 45);
  const px = Ye.xr.isPresenting ? oi.x : xt.position.x;
  const pz = Ye.xr.isPresenting ? oi.z : xt.position.z;
  spawnBurst(new A(px, groundAt(px, pz) + 0.08, pz), 0xcbd5e1, 6, 2.4);
}

function updateCombatHUD() {
  if (!ZGAME.active) return;
  const lvl = ZOMBIE_LEVELS[ZGAME.levelIdx] || ZOMBIE_LEVELS[0];
  const aliveCount = ZGAME.zombies.filter(z => z.alive).length;
  if (!ZGAME.campusEntered) {
    kt("wave-title").textContent = "ENTER ANURAG UNIVERSITY GATE";
    if (kt("wc-timer")) kt("wc-timer").textContent = "WALK IN";
    if (kt("wc-kills")) kt("wc-kills").textContent = `0 / 0`;
    if (kt("wc-score")) kt("wc-score").textContent = `${ZGAME.score}`;
  } else {
    kt("wave-title").textContent = lvl.isBoss ? "FINAL BOSS · DEFEAT THE CEO" : `LEVEL ${lvl.level} · ${lvl.name.toUpperCase()}`;
    if (kt("wc-timer")) kt("wc-timer").textContent = lvl.isBoss ? "BOSS FIGHT" : formatTimer(ZGAME.phaseTimer);
    if (kt("wc-kills")) kt("wc-kills").textContent = `${aliveCount} / ${ZGAME.kills}`;
    if (kt("wc-score")) kt("wc-score").textContent = `${ZGAME.score}`;
  }
  const hpPct = Math.max(0, (ZGAME.hp / ZGAME.maxHp) * 100);
  const hpTxt = `${Math.ceil(ZGAME.hp)} / ${ZGAME.maxHp}`;
  kt("hp-val").textContent = hpTxt;
  kt("hp-fill").style.width = `${hpPct}%`;
  // Top-Left Heart Health Bar update (PC + VR Visor)!
  if (kt("top-hp-num")) kt("top-hp-num").textContent = hpTxt;
  if (kt("top-hp-fill")) kt("top-hp-fill").style.width = `${hpPct}%`;
  if (kt("top-hp-hearts")) {
    const filled = Math.max(0, Math.min(5, Math.ceil(ZGAME.hp / 20)));
    kt("top-hp-hearts").textContent = "♥".repeat(filled) + "♡".repeat(5 - filled);
  }
  if (kt("top-hp-status")) kt("top-hp-status").textContent = ZGAME.hp <= 35 ? "CRITICAL · FIND MEDKIT!" : (ZGAME.hp <= 65 ? "VITALITY · CAUTION" : "VITALITY · OPTIMAL");
  if (kt("top-hp-shield-mini")) kt("top-hp-shield-mini").textContent = `SHIELD ${Math.ceil(ZGAME.shield)}%`;
  if (kt("top-hp-bar")) kt("top-hp-bar").classList.toggle("low-hp", ZGAME.hp <= 35);
  updateVRTopLeftHealthHUD();
  kt("shield-val").textContent = `${Math.ceil(ZGAME.shield)}%${ZGAME.shieldBlocking ? " · BLOCKING" : ""}`;
  kt("shield-fill").style.width = `${ZGAME.shield}%`;

  const w = WEAPON_DEFS[ZGAME.weaponIdx];
  kt("weapon-name").textContent = w.name;
  kt("weapon-ammo").textContent = ZGAME.reloading > 0 ? "RELOADING..." : (w.mag === Infinity ? "∞" : `${ZGAME.ammo[w.id]} / ${w.mag}`);

  document.querySelectorAll(".w-slot").forEach(el => {
    const slot = Number(el.dataset.w);
    const isPickupSlot = slot === 4;
    const isEq = isPickupSlot ? (ZGAME.weaponIdx >= 4) : (ZGAME.weaponIdx === slot);
    el.classList.toggle("equipped", isEq);
    if (isPickupSlot) {
      el.classList.toggle("empty", ZGAME.pickupWeaponIdx < 4);
      el.textContent = ZGAME.pickupWeaponIdx === 4 ? "[5] Iron Rod" : ZGAME.pickupWeaponIdx === 5 ? "[5] Branch" : "[5] Pickup";
    }
  });

  // CEO Boss Bar
  const boss = ZGAME.zombies.find(z => z.alive && z.lvlDef.isBoss);
  const bossWrap = kt("boss-bar-wrap");
  if (boss) {
    bossWrap.style.display = "block";
    kt("boss-hp-text").textContent = `${Math.ceil(boss.hp)} / ${boss.maxHp}`;
    kt("boss-bar-fill").style.width = `${Math.max(0, (boss.hp / boss.maxHp) * 100)}%`;
  } else {
    bossWrap.style.display = "none";
  }
}

function getPCAimRay() {
  const origin = new A();
  Mi.getWorldPosition(origin);
  const forward = new A(0, 0, -1).applyQuaternion(Mi.getWorldQuaternion(new Ot())).normalize();
  return { origin, forward };
}

function getVRRightAimRay() {
  const hand = trackedHands.get("right");
  if (!hand || !hand.anchor.visible) return getPCAimRay();
  const src = hand.arm.weaponMount || hand.anchor;
  src.updateWorldMatrix(true, false);
  const origin = new A();
  src.getWorldPosition(origin);
  const q = new Ot();
  src.getWorldQuaternion(q);
  const forward = new A(0, 0, -1).applyQuaternion(q).normalize();
  return { origin, forward };
}

function updateZombieGame(dt, timeSec) {
  if (!ZGAME.active) return;
  if (ZGAME.introPlaying) { updateStoryIntro(dt); return; }
  if (!En && !Ye.xr.isPresenting && !ZGAME.victory) return;

  if (ZGAME.toastTimer > 0) {
    ZGAME.toastTimer -= dt;
    if (ZGAME.toastTimer <= 0) kt("center-toast").classList.remove("show");
  }
  if (ZGAME.fireCd > 0) ZGAME.fireCd = Math.max(0, ZGAME.fireCd - dt);
  if (ZGAME.shieldBashCd > 0) ZGAME.shieldBashCd = Math.max(0, ZGAME.shieldBashCd - dt);
  if (ZGAME.vrSwingCd > 0) ZGAME.vrSwingCd = Math.max(0, ZGAME.vrSwingCd - dt);
  if (ZGAME.swingAnim > 0) ZGAME.swingAnim = Math.max(0, ZGAME.swingAnim - dt * 3.6);
  if (ZGAME.recoilAnim > 0) ZGAME.recoilAnim = Math.max(0, ZGAME.recoilAnim - dt * 6.8);
  if (ZGAME.weaponDrawAnim > 0) ZGAME.weaponDrawAnim = Math.max(0, ZGAME.weaponDrawAnim - dt * 4.5);
  if (ZGAME.trailTimer > 0) ZGAME.trailTimer = Math.max(0, ZGAME.trailTimer - dt);
  if (ZGAME.shieldBashAnim > 0) ZGAME.shieldBashAnim = Math.max(0, ZGAME.shieldBashAnim - dt * 3.2);

  // Slow, Smooth, Cinematic Lightsaber Launch/Ignition (~1.4 seconds steady extension!)
  const wantSaber = ZGAME.active && ZGAME.weaponIdx === 0 && !ZGAME.introPlaying;
  if (wantSaber) {
    ZGAME.saberIgnite = Math.min(1, ZGAME.saberIgnite + dt * 0.72);
  } else {
    ZGAME.saberIgnite = Math.max(0, ZGAME.saberIgnite - dt * 2.2);
  }
  const easedIgnite = ZGAME.saberIgnite * ZGAME.saberIgnite * (3 - 2 * ZGAME.saberIgnite);
  for (const arm of [...fpHands, ...Array.from(trackedHands.values()).map(h => h.arm)]) {
    const sg = arm.weaponModels?.[0];
    if (sg && sg.userData.bladePivot) {
      sg.userData.bladePivot.scale.set(1, Math.max(0.001, easedIgnite), 1);
    }
  }
  if (ZGAME.muzzleTimer > 0) {
    ZGAME.muzzleTimer = Math.max(0, ZGAME.muzzleTimer - dt);
    syncWeaponVisuals();
  }
  if (ZGAME.reloading > 0) {
    ZGAME.reloading -= dt;
    if (ZGAME.reloading <= 0) {
      const w = WEAPON_DEFS[ZGAME.weaponIdx];
      ZGAME.ammo[w.id] = w.mag;
      ZGAME.reloading = 0;
      updateCombatHUD();
    }
  }
  // Shield energy regen
  if (!ZGAME.shieldBlocking && ZGAME.shield < 100) {
    ZGAME.shield = Math.min(100, ZGAME.shield + dt * 11);
  }

  // PC continuous fire (Rifle) or single swing
  if (!Ye.xr.isPresenting && En && !ZGAME.gameOver && ZGAME.mouseLeftDown && ZGAME.fireCd <= 0) {
    const w = WEAPON_DEFS[ZGAME.weaponIdx];
    const { origin, forward } = getPCAimRay();
    if (w.type === "melee") {
      performMeleeAttack(origin, forward);
      ZGAME.mouseLeftDown = false;
    } else if (w.auto) {
      performGunFire(origin, forward);
    }
  }

  // Shield blocking & deploy state:
  // - PC: Hold Right-Click (RMB) to open transparent hi-tech shield
  // - Meta Quest 3: Press Right Controller Trigger (or Left Trigger) to open transparent hi-tech shield
  if (!Ye.xr.isPresenting) {
    ZGAME.shieldBlocking = (ZGAME.mouseRightDown || ZGAME.keyShieldDown) && ZGAME.shield > 5;
  } else {
    ZGAME.shieldBlocking = ZGAME.vrShieldTrigger && ZGAME.shield > 5;
  }
  if (ZGAME.comboTimer > 0) {
    ZGAME.comboTimer -= dt;
    if (ZGAME.comboTimer <= 0) {
      ZGAME.combo = 0;
      if (kt("combo-badge")) kt("combo-badge").style.display = "none";
    }
  }
  if (ZGAME.shake > 0) ZGAME.shake = Math.max(0, ZGAME.shake - dt * 1.4);

  // Jump Physics with Takeoff & Landing Effects (Works on BOTH PC Space & Meta Quest 3 Y button!)
  if (bo.value === "zombie") {
    if (ZGAME.jumpY > 0 || ZGAME.jumpVel !== 0) {
      ZGAME.jumpY += ZGAME.jumpVel * dt;
      ZGAME.jumpVel -= 19.5 * dt;
      if (ZGAME.jumpY <= 0) {
        ZGAME.jumpY = 0;
        ZGAME.jumpVel = 0;
        ZGAME.shake = Math.max(ZGAME.shake, 0.055);
        playSFX("land");
        pulseHaptics("left", 0.45, 55);
        pulseHaptics("right", 0.45, 55);
        const lpx = Ye.xr.isPresenting ? oi.x : xt.position.x;
        const lpz = Ye.xr.isPresenting ? oi.z : xt.position.z;
        spawnShockwave(new A(lpx, groundAt(lpx, lpz), lpz), 0x94a3b8, 1.8);
      }
    }
  }
  const targetDeploy = ZGAME.shieldBlocking ? 1.0 : 0.0;
  ZGAME.shieldDeploy = so.lerp(ZGAME.shieldDeploy, targetDeploy, Math.min(1, dt * 14));

  // Smoothly expand/collapse transparent holographic shield so it NEVER blocks view when closed
  const allHands = [...fpHands, ...Array.from(trackedHands.values()).map(h => h.arm)];
  for (const arm of allHands) {
    if (arm.shieldGroup) {
      const open = ZGAME.active && ZGAME.shieldDeploy > 0.03;
      arm.shieldGroup.visible = open;
      if (open) {
        const s = 0.08 + ZGAME.shieldDeploy * 0.92;
        arm.shieldGroup.scale.set(s, s, 1);
      }
    }
    if (arm.shieldRimMat) arm.shieldRimMat.color.setHex(ZGAME.shieldBlocking ? 0x72efdd : 0x0284c7);
    if (arm.shieldVisorMat) arm.shieldVisorMat.opacity = 0.25 + ZGAME.shieldDeploy * 0.36;
  }

  const px = Ye.xr.isPresenting ? oi.x : xt.position.x;
  const py = xt.position.y;
  const pz = Ye.xr.isPresenting ? oi.z : xt.position.z;

  // Animate Ground Pickups & show proximity prompt
  let nearPickup = null, nearD = 2.8;
  for (const p of ZGAME.pickups) {
    if (!p.available) continue;
    p.ring.rotation.z = timeSec * 1.8;
    const s = 1 + Math.sin(timeSec * 4) * 0.1;
    p.ring.scale.set(s, s, 1);
    const d = Math.hypot(p.x - px, p.z - pz);
    if (d < nearD) { nearD = d; nearPickup = p; }
  }
  const promptEl = kt("pickup-prompt");
  if (nearPickup && !Ye.xr.isPresenting && !ZGAME.gameOver) {
    promptEl.style.display = "block";
    promptEl.textContent = `[E] Pick up ${nearPickup.label}`;
  } else {
    promptEl.style.display = "none";
  }

  // Continuous subtle Lightsaber plasma hum when Saber is equipped + periodic nearby Zombie Groans!
  updateSaberHum(ZGAME.active && !ZGAME.gameOver && !ZGAME.introPlaying && ZGAME.weaponIdx === 0);
  ZGAME.groanTimer -= dt;
  if (ZGAME.groanTimer <= 0 && ZGAME.zombies.some(z => z.alive)) {
    ZGAME.groanTimer = 2.6 + Math.random() * 2.8;
    const nearZ = ZGAME.zombies.find(z => z.alive && Math.hypot(z.root.position.x - px, z.root.position.z - pz) < 20);
    if (nearZ) playSFX(nearZ.lvlDef.isBoss ? "boss_roar" : "zgroan");
  }

  // Animate & Collect Campus Medkits (+35 HP)
  for (const mk of ZGAME.medkits) {
    if (!mk.active) continue;
    mk.root.rotation.y = timeSec * 1.6;
    mk.root.position.y = groundAt(mk.x, mk.z) + 0.28 + Math.sin(timeSec * 3.2) * 0.06;
    if (ZGAME.hp < ZGAME.maxHp && Math.hypot(mk.x - px, mk.z - pz) < 1.8) {
      mk.active = false;
      mk.root.visible = false;
      ZGAME.hp = Math.min(ZGAME.maxHp, ZGAME.hp + 35);
      playSFX("pickup");
      flashScreen("rgba(34,197,94,0.35)", 0.35);
      showToast("MEDKIT COLLECTED! +35 HP", 1.6);
      updateCombatHUD();
    }
  }

  // Update Zombies AI & Animation (with Boids Horde Separation)
  let aliveCount = 0;
  for (let i = ZGAME.zombies.length - 1; i >= 0; i--) {
    const z = ZGAME.zombies[i];
    if (!z.alive) {
      z.deathTimer -= dt;
      z.root.rotation.x = so.lerp(z.root.rotation.x, -Math.PI * 0.48, dt * 6);
      z.root.position.y = Math.max(groundAt(z.root.position.x, z.root.position.z) - 0.12, z.root.position.y - dt * 0.35);
      if (z.deathTimer <= 0) {
        Ht.remove(z.root);
        ZGAME.zombies.splice(i, 1);
      }
      continue;
    }
    aliveCount++;

    // Hit flash & per-zombie melee swing cooldown recovery
    if (z.meleeHitCd > 0) z.meleeHitCd = Math.max(0, z.meleeHitCd - dt);
    if (z.hitFlash > 0) {
      z.hitFlash -= dt;
      z.skinMat.color.setHex(z.hitFlash > 0 ? 0xff4d4d : z.baseSkinHex);
    }

    // Apply knockback velocity
    if (z.knockVel.lengthSq() > 0.01) {
      const nx = z.root.position.x + z.knockVel.x * dt;
      const nz = z.root.position.z + z.knockVel.z * dt;
      if (!yo(nx, z.root.position.z)) z.root.position.x = nx;
      if (!yo(z.root.position.x, nz)) z.root.position.z = nz;
      z.knockVel.multiplyScalar(Math.max(0, 1 - dt * 6.5));
    }

    // Move toward player
    const dx = px - z.root.position.x;
    const dz = pz - z.root.position.z;
    const dist = Math.hypot(dx, dz);
    const targetYaw = Math.atan2(dx, dz);
    z.root.rotation.y = targetYaw;

    const attackDist = 1.65 * z.lvlDef.scale;
    if (dist > attackDist && !ZGAME.gameOver) {
      const step = z.speed * dt;
      let mx = (dx / dist) * step;
      let mz = (dz / dist) * step;
      // Soft Boids Separation so zombies spread out into a realistic horde
      for (let j = 0; j < ZGAME.zombies.length; j++) {
        if (i === j || !ZGAME.zombies[j].alive) continue;
        const ox = z.root.position.x - ZGAME.zombies[j].root.position.x;
        const oz = z.root.position.z - ZGAME.zombies[j].root.position.z;
        const od = Math.hypot(ox, oz);
        if (od > 0.01 && od < 1.35) {
          const push = (1.35 - od) * dt * 2.2;
          mx += (ox / od) * push;
          mz += (oz / od) * push;
        }
      }
      if (!yo(z.root.position.x + mx, z.root.position.z)) z.root.position.x += mx;
      if (!yo(z.root.position.x, z.root.position.z + mz)) z.root.position.z += mz;
    }
    z.root.position.y = groundAt(z.root.position.x, z.root.position.z);

    // Articulated Cartoon Human Walking Animation (Hips, Bending Knees, Reaching Arms, Swinging ID Card!)
    z.phase += dt * (z.speed * 3.0);
    const lHip = Math.sin(z.phase) * 0.62;
    const rHip = -Math.sin(z.phase) * 0.62;
    z.legs[0].hip.rotation.x = lHip;
    z.legs[1].hip.rotation.x = rHip;
    z.legs[0].knee.rotation.x = Math.max(0, -Math.cos(z.phase)) * 0.72;
    z.legs[1].knee.rotation.x = Math.max(0, Math.cos(z.phase)) * 0.72;
    z.torso.position.y = 0.86 + Math.abs(Math.sin(z.phase)) * 0.045;
    z.torso.rotation.z = Math.sin(z.phase) * 0.07;
    z.torso.rotation.x = 0.10 + Math.abs(Math.cos(z.phase)) * 0.05;
    z.headGroup.rotation.z = Math.sin(z.phase * 1.2) * 0.12;
    const lunge = z.attackCd > 0.65 ? Math.sin((z.attackCd - 0.65) * 9) * 0.55 : 0;
    z.arms[0].sh.rotation.x = -1.18 + Math.sin(z.phase) * 0.18 - lunge;
    z.arms[1].sh.rotation.x = -1.18 - Math.sin(z.phase) * 0.18 - lunge;
    z.idCardPivot.rotation.z = -Math.sin(z.phase) * 0.22;
    z.idCardPivot.rotation.x = -0.14;

    // Billboard HP bar toward camera
    if (z.hpBarBg.visible) {
      z.hpBarBg.lookAt(px, py + 1.5, pz);
      const frac = Math.max(0, z.hp / z.maxHp);
      z.hpBarFill.scale.x = Math.max(0.001, frac);
      z.hpBarFill.position.x = -(1 - frac) * 0.26;
    }

    // Melee Attack on Player
    if (z.attackCd > 0) z.attackCd -= dt;
    if (dist <= attackDist + 0.3 && z.attackCd <= 0 && !ZGAME.gameOver) {
      z.attackCd = z.lvlDef.isBoss ? 1.15 : 1.35;
      damagePlayer(z.lvlDef.dmg);
    }

    // From Round 3 (Professors, Placement Incharges, HODs, CEO): Zombies throw realistic Laptops & Textbooks!
    if (z.canThrow && !ZGAME.gameOver && dist > 6.5 && dist < 29) {
      z.throwCd -= dt;
      if (z.throwCd <= 0) {
        z.throwCd = Math.max(2.6, 5.4 - z.lvlDef.level * 0.45) + Math.random() * 1.8;
        const isLaptop = Math.random() < (z.lvlDef.level >= 4 ? 0.58 : 0.45);
        const projMesh = isLaptop ? createThrownLaptop() : createThrownBook();
        const startPos = new A(z.root.position.x, z.root.position.y + 1.55 * z.lvlDef.scale, z.root.position.z);
        projMesh.position.copy(startPos);
        Ht.add(projMesh);
        // Parabolic lob toward player's chest/head so it arcs realistically through the air!
        const flightTime = so.clamp(dist / 13.5, 0.55, 1.85);
        const vx = (px - startPos.x) / flightTime;
        const vz = (pz - startPos.z) / flightTime;
        const vy = ((py + 1.32) - startPos.y + 0.5 * 9.8 * flightTime * flightTime) / flightTime;
        ZGAME.projectiles.push({
          mesh: projMesh,
          vel: new A(vx, vy, vz),
          gravity: 9.8,
          spin: new A((Math.random() - 0.5) * 9, (Math.random() - 0.5) * 11, (Math.random() - 0.5) * 8),
          life: 3.6,
          dmg: isLaptop ? (14 + z.lvlDef.level * 2) : (10 + z.lvlDef.level * 1.5),
          kind: isLaptop ? "laptop" : "book"
        });
        playSFX("zgroan");
      }
    }

    // CEO Boss Ranged Toxic Bolts & Ground Shockwave
    if (z.lvlDef.isBoss && !ZGAME.gameOver) {
      z.boltCd -= dt;
      if (z.boltCd <= 0 && dist > 6 && dist < 42) {
        z.boltCd = 3.1;
        const boltOrigin = new A(z.root.position.x, z.root.position.y + 1.9, z.root.position.z);
        const dir = new A(px - boltOrigin.x, (py + 1.25) - boltOrigin.y, pz - boltOrigin.z).normalize();
        const bm = new et(new fn(0.22, 10, 10), new Yi({ color: 0xef4444 }));
        bm.position.copy(boltOrigin);
        Ht.add(bm);
        ZGAME.projectiles.push({ mesh: bm, vel: dir.multiplyScalar(14.5), life: 3.5, dmg: 18 });
        playSFX("saber");
      }
      z.slamCd -= dt;
      if (z.slamCd <= 0 && dist < 6.5) {
        z.slamCd = 5.2;
        spawnShockwave(z.root.position, 0xef4444, 6.5);
        playSFX("bash");
        if (dist < 5.5) damagePlayer(22);
      }
    }
  }

  // Update Boss Bolts & Thrown Laptops / Engineering Textbooks
  for (let i = ZGAME.projectiles.length - 1; i >= 0; i--) {
    const pr = ZGAME.projectiles[i];
    pr.life -= dt;
    if (pr.gravity) pr.vel.y -= pr.gravity * dt;
    pr.mesh.position.addScaledVector(pr.vel, dt);
    if (pr.spin) {
      pr.mesh.rotation.x += pr.spin.x * dt;
      pr.mesh.rotation.y += pr.spin.y * dt;
      pr.mesh.rotation.z += pr.spin.z * dt;
    }
    const dToPlayer = Math.hypot(pr.mesh.position.x - px, pr.mesh.position.z - pz);
    if (dToPlayer < 0.95 && Math.abs(pr.mesh.position.y - (py + 1.25)) < 1.15) {
      damagePlayer(pr.dmg);
      const burstCol = pr.kind === "laptop" ? 0x38bdf8 : pr.kind === "book" ? 0xf5f0e1 : 0xef4444;
      spawnBurst(pr.mesh.position, burstCol, 12, 4.6);
      if (pr.kind === "laptop") playSFX("rod");
      else if (pr.kind === "book") playSFX("branch");
      Ht.remove(pr.mesh);
      ZGAME.projectiles.splice(i, 1);
      continue;
    }
    // Smash on ground impact
    const gY = groundAt(pr.mesh.position.x, pr.mesh.position.z);
    if (pr.life <= 0 || pr.mesh.position.y <= gY + 0.08) {
      if (pr.kind) {
        spawnBurst(pr.mesh.position, pr.kind === "laptop" ? 0x38bdf8 : 0xf5f0e1, 7, 3.2);
      }
      Ht.remove(pr.mesh);
      ZGAME.projectiles.splice(i, 1);
    }
  }

  // Update 3D Campus Victory Fireworks if player has won!
  if (ZGAME.victory) updateVictoryFireworks(dt);

  // Update Particles, Shell Casings, Saber Trails & Tracers
  for (let i = ZGAME.particles.length - 1; i >= 0; i--) {
    const pt = ZGAME.particles[i];
    pt.life -= dt;
    if (pt.isRing) {
      const grow = 1 + dt * 14;
      pt.mesh.scale.x = Math.min(pt.maxScale, pt.mesh.scale.x * grow);
      pt.mesh.scale.y = pt.mesh.scale.x;
    } else if (pt.isFade) {
      if (pt.mesh.material) pt.mesh.material.opacity = Math.max(0, (pt.life / (pt.maxLife || 0.16)) * 0.44);
    } else if (!pt.isTracer) {
      pt.vel.y -= 9.8 * dt;
      pt.mesh.position.addScaledVector(pt.vel, dt);
      if (pt.spin) {
        pt.mesh.rotation.x += pt.spin.x * dt;
        pt.mesh.rotation.y += pt.spin.y * dt;
        pt.mesh.rotation.z += pt.spin.z * dt;
      }
    }
    if (pt.life <= 0) {
      Ht.remove(pt.mesh);
      ZGAME.particles.splice(i, 1);
    }
  }

  // Continuous Horde Spawning & 2-Minute Phase Survival Progression — ONLY AFTER ENTERING CAMPUS!
  if (!ZGAME.gameOver && !ZGAME.victory) {
    if (!ZGAME.campusEntered) {
      // Wait until the player crosses inside the Main Gate (Z <= 60) before spawning any zombies!
      if (pz <= 60) {
        ZGAME.campusEntered = true;
        spawnZombieWave(0);
      }
      return;
    }
    const curLvl = ZOMBIE_LEVELS[ZGAME.levelIdx] || ZOMBIE_LEVELS[0];
    if (ZGAME.waveDelay > 0) {
      ZGAME.waveDelay -= dt;
      if (ZGAME.waveDelay <= 0) {
        spawnZombieWave(ZGAME.levelIdx + 1);
      }
    } else if (!curLvl.isBoss) {
      // Levels 1-5: 2-minute survival timer + continuous zombie reinforcements!
      const prevSec = Math.ceil(ZGAME.phaseTimer);
      ZGAME.phaseTimer = Math.max(0, ZGAME.phaseTimer - dt);
      if (Math.ceil(ZGAME.phaseTimer) !== prevSec) updateCombatHUD();

      // Keep spawning fresh zombies inside the campus around the player so they NEVER stop coming!
      ZGAME.spawnTimer -= dt;
      const maxActive = Math.min(12, 6 + curLvl.level);
      if (ZGAME.spawnTimer <= 0) {
        ZGAME.spawnTimer = Math.max(1.5, 3.2 - curLvl.level * 0.32);
        if (aliveCount < maxActive) {
          const batch = aliveCount < 4 ? 2 : 1;
          for (let b = 0; b < batch; b++) {
            const [sx, sz] = findZombieSpawnAround(px, pz, 15, 29);
            ZGAME.zombies.push(createFacultyZombie(curLvl, sx, sz));
          }
          updateCombatHUD();
        }
      }

      // Phase survived when 2:00 timer hits 0:00!
      if (ZGAME.phaseTimer <= 0) {
        // Clear remaining zombies from finished phase cleanly
        for (const z of ZGAME.zombies) {
          if (z.alive) { z.alive = false; z.deathTimer = 0.6; z.hpBarBg.visible = false; }
        }
        ZGAME.waveDelay = 3.2;
        ZGAME.hp = Math.min(ZGAME.maxHp, ZGAME.hp + 35);
        ZGAME.shield = 100;
        const nextLvl = ZOMBIE_LEVELS[ZGAME.levelIdx + 1];
        showToast(`LEVEL ${curLvl.level} SURVIVED! +35 HP · NEXT: ${nextLvl ? nextLvl.name.toUpperCase() : "CEO BOSS"}!`, 3.0);
        playSFX("levelup");
        updateCombatHUD();
      }
    } else {
      // Boss Level (Level 6 - THE CEO): Keep spawning occasional faculty backup while CEO is alive!
      const bossAlive = ZGAME.zombies.some(z => z.alive && z.lvlDef.isBoss);
      if (!bossAlive) {
        ZGAME.victory = true;
        playSFX("levelup");
        showEndScreen(true);
        document.exitPointerLock?.();
      } else {
        ZGAME.spawnTimer -= dt;
        if (ZGAME.spawnTimer <= 0 && aliveCount < 5) {
          ZGAME.spawnTimer = 8.5;
          const minionTier = ZOMBIE_LEVELS[Math.floor(Math.random() * 3)];
          const [sx, sz] = findZombieSpawnAround(px, pz, 16, 26);
          ZGAME.zombies.push(createFacultyZombie(minionTier, sx, sz));
          updateCombatHUD();
        }
      }
    }
  }
}

// Mouse Combat Listeners (PC)
document.addEventListener("mousedown", (ev) => {
  if (!En || Ye.xr.isPresenting || !ZGAME.active || ZGAME.gameOver) return;
  if (ev.button === 0) {
    ZGAME.mouseLeftDown = true;
    if (ZGAME.fireCd <= 0) {
      const w = WEAPON_DEFS[ZGAME.weaponIdx];
      const { origin, forward } = getPCAimRay();
      if (w.type === "melee") performMeleeAttack(origin, forward);
      else performGunFire(origin, forward);
    }
  } else if (ev.button === 2) {
    ZGAME.mouseRightDown = true;
  }
});
document.addEventListener("mouseup", (ev) => {
  if (ev.button === 0) ZGAME.mouseLeftDown = false;
  if (ev.button === 2) ZGAME.mouseRightDown = false;
});
document.addEventListener("contextmenu", (ev) => { if (En && ZGAME.active) ev.preventDefault(); });
document.addEventListener("wheel", (ev) => {
  if (En && ZGAME.active && !Ye.xr.isPresenting) cycleWeapon(ev.deltaY > 0 ? 1 : -1);
});

// Initialize mode now that ZGAME, trackedHands, and WebXR are all ready
To();

// ============================================================================
// MAIN REAL-TIME SIMULATION & BIOMECHANICAL POV ANIMATION LOOP
"""

html = html.replace(LOOP_ANCHOR, ZOMBIE_ENGINE_JS, 1)

# ---------------------------------------------------------------------------
# 7. Hook Zombie Mode into To() (mode switch), Keydown, Minimap, Wrist HUD,
#    Controller Sync (Quest 3), and FP Hands Animation!
# ---------------------------------------------------------------------------

# 7a. Mode switch To() & defer initial To() until ZGAME and trackedHands are initialized
TO_ANCHOR = '  let r = bo.value === "survival";'
assert TO_ANCHOR in html
TO_REPLACE = """  let r = bo.value === "survival";
  if (bo.value === "zombie") { startZombieGame(); } else { stopZombieGame(); syncWeaponVisuals(); }"""
html = html.replace(TO_ANCHOR, TO_REPLACE, 1)

EARLY_TO_ANCHOR = 'kt("stops").onchange = (r) => xo(+r.target.value);\nTo();\nupdateCameraPOV();'
if EARLY_TO_ANCHOR not in html:
    EARLY_TO_ANCHOR = EARLY_TO_ANCHOR.replace("\n", "\r\n")
assert EARLY_TO_ANCHOR in html, "Could not find early To() anchor!"
html = html.replace(EARLY_TO_ANCHOR, 'kt("stops").onchange = (r) => xo(+r.target.value);\nupdateCameraPOV();', 1)

# 7b. Keyboard shortcuts (1-5 weapons, E pickup, Q shield bash, R reload/restart)
KEY_ANCHOR = '  if (r.code === "KeyM") {\n    toggleMapSize();\n    return;\n  }'
if KEY_ANCHOR not in html:
    KEY_ANCHOR = KEY_ANCHOR.replace("\n", "\r\n")
assert KEY_ANCHOR in html
KEY_REPLACE = KEY_ANCHOR + """
  if (ZGAME.active) {
    if (r.code === "Digit1") { selectWeapon(0); return; }
    if (r.code === "Digit2") { selectWeapon(1); return; }
    if (r.code === "Digit3") { selectWeapon(2); return; }
    if (r.code === "Digit4") { selectWeapon(3); return; }
    if (r.code === "Digit5") { if (ZGAME.pickupWeaponIdx >= 4) selectWeapon(ZGAME.pickupWeaponIdx); return; }
    if (r.code === "KeyE") { if (tryPickupNearbyWeapon()) return; }
    if (r.code === "KeyQ") { triggerShieldBash(); return; }
    if (r.code === "KeyF") { ZGAME.keyShieldDown = true; return; }
    if (r.code === "Space") {
      if (ZGAME.introPlaying) { finishStoryIntro(); return; }
      triggerPlayerJump(); return;
    }
    if (r.code === "KeyR") { if (ZGAME.gameOver || ZGAME.victory) { startZombieGame(); cd(); } else { triggerReload(); } return; }
    if (r.code === "KeyX" && (ZGAME.gameOver || ZGAME.victory)) { enterExploreMode(); return; }
  }"""
html = html.replace(KEY_ANCHOR, KEY_REPLACE, 1)

# Release F shield key on keyup & don't let explorer KeyF intercept combat shield
html = html.replace(
    'if (r.code === "KeyH" || r.code === "KeyF") {',
    'if (r.code === "KeyH" || (!ZGAME.active && r.code === "KeyF")) {',
    1
)
html = html.replace(
    'window.onkeyup = (r) => li.delete(r.code);',
    'window.onkeyup = (r) => { li.delete(r.code); if (r.code === "KeyF") ZGAME.keyShieldDown = false; };',
    1
)

# Apply jump height & combat screen shake to 1st-person camera pivot
html = html.replace(
    'camPivot.position.set(bobX, 1.66 + bobY, 0);',
    'const sk = ZGAME.active ? ZGAME.shake : 0; camPivot.position.set(bobX + (Math.random()-.5)*sk, 1.66 + bobY + (ZGAME.active ? ZGAME.jumpY : 0) + (Math.random()-.5)*sk, 0);',
    1
)

# 7c. Update hint text for Zombie mode
HINT_ANCHOR = '? "WASD: Walk  ·  E: Sprint  ·  V: 1st/3rd Person POV  ·  H: GPS Phone/Wave  ·  M: Expand Map  ·  Space/Shift: Fly  ·  Esc: Menu"'
assert HINT_ANCHOR in html
HINT_REPLACE = '? (bo.value === "zombie" ? "WASD: Move · Shift: Sprint · LMB: Fire/Slash · RMB: Shield · Q: Bash · 1-5: Weapons · E: Pick up Rod/Branch · R: Reload · Esc: Menu" : "WASD: Walk · Shift/E: Sprint · V: 1st/3rd Person · M: Map · Esc: Menu")'
html = html.replace(HINT_ANCHOR, HINT_REPLACE, 1)

# 7d. Sprint also works with Shift in Zombie mode
SPRINT_ANCHOR = 'isSprint = li.has("KeyE"),'
assert SPRINT_ANCHOR in html
html = html.replace(SPRINT_ANCHOR, 'isSprint = li.has("ShiftLeft") || li.has("ShiftRight") || (!ZGAME.active && li.has("KeyE")),', 1)

# 7e. Upgrade Minimap to draw live Zombie blips + Ground Pickups
MAP_ANCHOR = '  let [pxm, pzm] = worldToMap(px, pz);'
assert MAP_ANCHOR in html
MAP_ZOMBIES_JS = """  if (ZGAME.active) {
    for (const p of ZGAME.pickups) {
      if (!p.available) continue;
      const [pmx, pmz] = worldToMap(p.x, p.z);
      g.fillStyle = "#fbbf24";
      g.fillRect(pmx - 2.5, pmz - 2.5, 5, 5);
    }
    for (const z of ZGAME.zombies) {
      if (!z.alive) continue;
      const [zmx, zmz] = worldToMap(z.root.position.x, z.root.position.z);
      g.fillStyle = z.lvlDef.isBoss ? "#f59e0b" : "#ef4444";
      g.beginPath();
      g.arc(zmx, zmz, z.lvlDef.isBoss ? 5.5 : 3.2, 0, Math.PI * 2);
      g.fill();
    }
  }
  let [pxm, pzm] = worldToMap(px, pz);"""
html = html.replace(MAP_ANCHOR, MAP_ZOMBIES_JS, 1)

# 7f. Upgrade Left Wrist VR Tactical HUD for Zombie Combat
WRIST_ANCHOR = 'function updateWristDisplay(){'
assert WRIST_ANCHOR in html
WRIST_REPLACE = """function updateWristDisplay(){
  if(!wristDisplay)return;
  if(ZGAME.active){
    const lvl=ZOMBIE_LEVELS[ZGAME.levelIdx]||ZOMBIE_LEVELS[0];
    const alive=ZGAME.zombies.filter(z=>z.alive).length;
    const w=WEAPON_DEFS[ZGAME.weaponIdx];
    const ammoStr=ZGAME.reloading>0?"RELOAD":(w.mag===Infinity?"INF":ZGAME.ammo[w.id]+"/"+w.mag);
    const timerStr = !ZGAME.campusEntered ? "ENTER GATE" : (lvl.isBoss ? "BOSS" : formatTimer(ZGAME.phaseTimer));
    const key=`${Math.ceil(ZGAME.hp)}-${Math.ceil(ZGAME.shield)}-${lvl.level}-${timerStr}-${alive}-${w.id}-${ammoStr}-${ZGAME.gameOver}`;
    if(wristDisplay.last===key)return;
    wristDisplay.last=key;
    const ctx=wristDisplay.ctx;
    ctx.fillStyle="#0b1824";ctx.fillRect(0,0,512,256);
    ctx.fillStyle="#ff6b6b";ctx.font="bold 30px sans-serif";
    ctx.fillText(ZGAME.gameOver?"OVERRUN! PRESS B":`LVL ${lvl.level}: ${lvl.badge}  ${timerStr}`,16,42,480);
    ctx.fillStyle="#ff4d6d";ctx.font="bold 28px sans-serif";
    const hHearts = "♥".repeat(Math.max(0, Math.min(5, Math.ceil(ZGAME.hp / 20))));
    ctx.fillText(`${hHearts} ${Math.ceil(ZGAME.hp)}   SHIELD: ${Math.ceil(ZGAME.shield)}%`,16,92,480);
    ctx.fillStyle="#72efdd";ctx.font="bold 26px sans-serif";
    ctx.fillText(`${w.name}`,16,142,480);
    ctx.fillStyle="#fde047";ctx.font="bold 28px monospace";
    ctx.fillText(`AMMO: ${ammoStr}   SCORE: ${ZGAME.score}`,16,188,480);
    ctx.fillStyle="#cbd5e1";ctx.font="21px sans-serif";
    ctx.fillText("A:Weapon  B:Reload  Grip:Pickup  L-Trig:Bash",16,232,480);
    wristDisplay.map.needsUpdate=true;
    return;
  }"""
html = html.replace(WRIST_ANCHOR, WRIST_REPLACE, 1)

# 7g. Upgrade Meta Quest 3 syncControllerHands for 1:1 Shield, Gun Fire, Physical Saber/Rod Swing, Grip Pickup, and A/B Weapon Controls
VR_SYNC_ANCHOR = '    const pressed=!!buttons?.[4]?.pressed;\n    if(side==="right"&&hand.source===source&&pressed&&!hand.buttonDown)questPhone=!questPhone;\n    const upper=!!buttons?.[5]?.pressed;\n    if(hand.source===source && upper && !hand.upperDown){\n      if(side==="right"){\n        bo.selectedIndex=(bo.selectedIndex+1)%bo.options.length;To();\n      }else if(!kt("stops").disabled){\n        const stops=kt("stops");stops.selectedIndex=(stops.selectedIndex+1)%stops.options.length;xo(+stops.value);\n      }\n    }\n    hand.buttonDown=pressed;hand.upperDown=upper;hand.source=source;'
if VR_SYNC_ANCHOR not in html:
    VR_SYNC_ANCHOR = VR_SYNC_ANCHOR.replace("\n", "\r\n")
assert VR_SYNC_ANCHOR in html, "Could not find VR syncControllerHands anchor!"

VR_SYNC_REPLACE = """    const pressed=!!buttons?.[4]?.pressed;
    const upper=!!buttons?.[5]?.pressed;
    const trigDown=trigger>0.65;
    const gripDown=grip>0.65;

    if(ZGAME.active){
      // Distinct ergonomic VR hand pose: Thumb UP (wristPivot.rotation.z = +1.36) + tight closed fist for Melee vs trigger-finger grip for Guns!
      if(side==="right"){
        const curW = WEAPON_DEFS[ZGAME.weaponIdx];
        const isMelee = curW && curW.type === "melee";
        arm.fingers.forEach((finger,i)=>{
          const c = (!isMelee && i===0) ? (0.34 + trigger*0.62) : Math.max(0.96, grip);
          finger.fRoot.rotation.x=-(.18+c*1.04);
          finger.j2.rotation.x=-(.20+c*1.12);
          finger.j3.rotation.x=-(.12+c*.78);
        });
        arm.thumbRoot.rotation.set(isMelee ? -.44 : -.26, .76, -.26);
        arm.thumbJ2.rotation.x = isMelee ? -.58 : -.32;
        if(arm.wristPivot) arm.wristPivot.rotation.set(isMelee ? -0.10 : 0, 0, 1.36);
      }
      const curPos=hand.anchor.position;
      if(side==="right"){
        const w=WEAPON_DEFS[ZGAME.weaponIdx];
        if(!ZGAME.introPlaying && !ZGAME.gameOver){
          if(w.type==="melee"){
            // Real physical 3D blade-contact damage on hand movement (NO trigger needed!)
            checkVRPhysicalMeleeHit(hand, 0.016);
          } else {
            if(trigDown && (w.auto || !hand.trigDown) && ZGAME.fireCd<=0){
              const {origin,forward}=getVRRightAimRay();
              performGunFire(origin,forward);
            }
          }
          // Right Grip picks up nearby campus Iron Rod or Fallen Branch
          if(gripDown && !hand.gripDown) tryPickupNearbyWeapon();
        }
        // A button cycles Right-Hand Weapons (or skips story intro in VR)
        if(hand.source===source && pressed && !hand.buttonDown){
          if(ZGAME.introPlaying) finishStoryIntro(); else if(!ZGAME.gameOver) cycleWeapon(1);
        }
        // B button reloads gun (or restarts if dead/won)
        if(hand.source===source && upper && !hand.upperDown){
          if(ZGAME.gameOver || ZGAME.victory) startZombieGame(); else triggerReload();
        }
      } else {
        // Left Hand: Shield opens ONLY when Left Trigger is actively pressed!
        ZGAME.vrShieldTrigger = !ZGAME.introPlaying && !ZGAME.gameOver && trigger > 0.55;
        const lSpeed=curPos.distanceTo(ZGAME.vrPrevLeftPos)*60;
        ZGAME.vrPrevLeftPos.copy(curPos);
        if(!ZGAME.introPlaying && !ZGAME.gameOver && (lSpeed>5.2 || (gripDown && !hand.gripDown))) triggerShieldBash();
        // X button: Explore Campus when dead/won, or cycles lighting during gameplay
        if(hand.source===source && pressed && !hand.buttonDown){
          if(ZGAME.gameOver || ZGAME.victory) enterExploreMode();
          else { const tm=kt("time-mode"); tm.selectedIndex=(tm.selectedIndex+1)%tm.options.length; tm.dispatchEvent(new Event("change")); }
        }
        // Y button: Jump in VR!
        if(hand.source===source && upper && !hand.upperDown){
          triggerPlayerJump();
        }
      }
      hand.trigDown=trigDown; hand.gripDown=gripDown;
      if(arm.phoneGroup) arm.phoneGroup.visible=false;
    } else {
      if(side==="right"&&hand.source===source&&pressed&&!hand.buttonDown)questPhone=!questPhone;
      if(hand.source===source && upper && !hand.upperDown){
        if(side==="right"){
          bo.selectedIndex=(bo.selectedIndex+1)%bo.options.length;To();
        }else if(!kt("stops").disabled){
          const stops=kt("stops");stops.selectedIndex=(stops.selectedIndex+1)%stops.options.length;xo(+stops.value);
        }
      }
    }
    hand.buttonDown=pressed;hand.upperDown=upper;hand.source=source;"""

html = html.replace(VR_SYNC_ANCHOR, VR_SYNC_REPLACE, 1)

# Move VR wrist display slightly higher up the forearm so it never clips the wristwatch
html = html.replace(
    'screen.position.set(0,.039,.072);',
    'screen.position.set(0,.048,.125);',
    1
)

# Reset VR left-trigger shield state every frame before polling controllers so it NEVER sticks open!
html = html.replace(
    'function syncControllerHands(frame,space,sources){',
    'function syncControllerHands(frame,space,sources){\n  ZGAME.vrShieldTrigger=false;',
    1
)

# Use Meta Quest 3's calibrated targetRaySpace (natural straight pointing axis) for 1:1 hand & gun sync with ZERO wrist bending!
html = html.replace(
    'const pose=frame.getPose(source.gripSpace,space);',
    'const pose=frame.getPose(source.targetRaySpace||source.gripSpace,space);',
    1
)

# Align VR hands dead-straight along targetRaySpace (-Z forward, 0 roll so wristPivot +1.36 & weaponMount -1.36 cancel to 0.000!)
html = html.replace(
    '  arm.root.position.set(0,.012,.046);\n  arm.root.rotation.z=sign*.72;',
    '  arm.root.position.set(0,-.016,.092);\n  arm.root.rotation.set(0, 0, 0);',
    1
)
html = html.replace(
    '  arm.root.position.set(0,.012,.046);\r\n  arm.root.rotation.z=sign*.72;',
    '  arm.root.position.set(0,-.016,.092);\r\n  arm.root.rotation.set(0, 0, 0);',
    1
)
CTRL_ADD_ANCHOR = '  trackedHands.set(side,hand);return hand;'
assert CTRL_ADD_ANCHOR in html
html = html.replace(CTRL_ADD_ANCHOR, '  trackedHands.set(side,hand);syncWeaponVisuals();return hand;', 1)

# 7h. Animate PC 1st-Person Hands in Combat Mode (Left Shield Guard/Bash + Right Weapon Aim/Swing/Recoil)
FP_HAND_ANCHOR = '    if (side === 1 && handGadgetMode === 1) {'
assert FP_HAND_ANCHOR in html
FP_COMBAT_JS = """    if (ZGAME.active) {
      if (arm.phoneGroup) arm.phoneGroup.visible = false;
      if (side === -1) {
        // Left Hand: Tactical Riot Shield (tucked low-left when idle, raised center-left when blocking)
        let blk = ZGAME.shieldBlocking ? 1 : 0;
        let bash = Math.sin(ZGAME.shieldBashAnim * Math.PI);
        arm.root.position.set(
          so.lerp(-0.34, -0.17, blk),
          so.lerp(-0.33, -0.14, blk) + breathe * 0.005,
          so.lerp(-0.38, -0.46, blk) - bash * 0.22
        );
        arm.root.rotation.set(
          so.lerp(0.22, 0.04, blk) - bash * 0.12,
          so.lerp(0.42, 0.08, blk),
          so.lerp(-0.18, -0.02, blk)
        );
        arm.wristPivot.rotation.set(0, 0, 0);
        arm.setFingerCurl(0.85, false);
      } else {
        // Right Hand: Dynamic Weapon-Specific Animations (2-Combo Saber Slash, Recoil Kick, Tactical Reload Tilt, Draw Raise!)
        let w = WEAPON_DEFS[ZGAME.weaponIdx];
        let sw = Math.sin(ZGAME.swingAnim * Math.PI);
        let rec = ZGAME.recoilAnim;
        let drawDip = ZGAME.weaponDrawAnim * 0.18;
        let relTilt = ZGAME.reloading > 0 ? Math.sin((ZGAME.reloading / Math.max(0.1, ZGAME.reloadTotal)) * Math.PI) : 0;
        let walkSwayX = isWalking ? Math.cos(Bc) * 0.014 : 0;
        let walkSwayY = isWalking ? Math.abs(Math.sin(Bc)) * 0.012 : 0;

        if (w.type === "melee") {
          let dir = ZGAME.swingDir;
          arm.root.position.set(
            0.23 + walkSwayX - sw * (dir > 0 ? 0.28 : -0.14),
            -0.21 - drawDip + walkSwayY + sw * 0.11 + breathe * 0.005,
            -0.38 - sw * 0.16
          );
          arm.root.rotation.set(
            0.18 - sw * 1.18,
            -0.22 + sw * (dir > 0 ? 0.95 : -0.72),
            -0.16 + sw * (dir > 0 ? 0.65 : -0.52)
          );
        } else {
          let kickBack = w.key === "shotgun" ? 0.13 : w.key === "rifle" ? 0.055 : 0.07;
          let kickPitch = w.key === "shotgun" ? 0.36 : w.key === "pistol" ? 0.28 : 0.14;
          arm.root.position.set(
            0.20 + walkSwayX - relTilt * 0.06,
            -0.19 - drawDip - relTilt * 0.12 + walkSwayY + rec * 0.032 + breathe * 0.003,
            -0.37 + rec * kickBack
          );
          arm.root.rotation.set(
            0.04 + rec * kickPitch - relTilt * 0.42 - drawDip * 1.4,
            -0.06 + relTilt * 0.38,
            -0.04 + relTilt * 0.62
          );
        }
        // Natural ergonomic Right-Hand Weapon Grip (Thumb UP, Palm LEFT, Fingers curled tightly around handle!)
        arm.wristPivot.rotation.set(w.type === "melee" ? -0.08 : 0, 0, 1.36);
        const isMeleePC = w.type === "melee";
        arm.fingers.forEach((finger, idx) => {
          const c = (!isMeleePC && idx === 0) ? (0.38 + rec * 0.52) : 1.0;
          finger.fRoot.rotation.x = -(0.18 + c * 1.04);
          finger.j2.rotation.x = -(0.20 + c * 1.12);
          finger.j3.rotation.x = -(0.12 + c * 0.78);
        });
        arm.thumbRoot.rotation.set(isMeleePC ? -0.44 : -0.26, 0.76, -0.26);
        arm.thumbJ2.rotation.x = isMeleePC ? -0.58 : -0.32;
      }
      return;
    }
    if (side === 1 && handGadgetMode === 1) {"""
html = html.replace(FP_HAND_ANCHOR, FP_COMBAT_JS, 1)

# 7i. Call updateZombieGame(e, timeSec) + WebXR-safe GLSL shader ticker inside Ye.setAnimationLoop (works in BOTH PC & Meta Quest 3 VR!)
TICK_ANCHOR = '  updateNavRoute(xt.position.x, xt.position.z, timeSec);'
assert TICK_ANCHOR in html
html = html.replace(TICK_ANCHOR, '  if (window._tickRealisticShaders) window._tickRealisticShaders(e);\n  updateZombieGame(e, timeSec);\n  if (Ye.xr.isPresenting && typeof updateVRTopLeftHealthHUD === "function") updateVRTopLeftHealthHUD();\n  updateNavRoute(xt.position.x, xt.position.z, timeSec);', 1)

# 7j. Keep status text informative in Zombie mode
STATUS_ANCHOR = '  if (t && bo.value !== "survival") {'
assert STATUS_ANCHOR in html
STATUS_REPLACE = """  if (t && bo.value === "zombie") {
    const lv = ZOMBIE_LEVELS[ZGAME.levelIdx] || ZOMBIE_LEVELS[0];
    fo.textContent = `OUTBREAK LVL ${lv.level}: ${lv.badge} · ${zone.toUpperCase()}`;
  } else if (t && bo.value !== "survival") {"""
html = html.replace(STATUS_ANCHOR, STATUS_REPLACE, 1)

# CRITICAL VR FIX: Never black out the VR screen (`hd`) during the aerial intro flyover or above buildings!
html = html.replace(
    'let l = Ye.xr.isPresenting && yo(oi.x, oi.z);',
    'let l = Ye.xr.isPresenting && !ZGAME.introPlaying && xt.position.y < 14 && yo(oi.x, oi.z);',
    1
)

# 7k. Keep dynamic shadow updates reasonable in VR + trigger cinematic aerial-to-FP story intro!
html = html.replace(
    "Ye.shadowMap.autoUpdate=false;Ye.shadowMap.needsUpdate=true;",
    "Ye.shadowMap.autoUpdate=true;syncWeaponVisuals();if(ZGAME.active && !ZGAME.introDoneOnce && !ZGAME.introPlaying)startStoryIntro();",
    1
)
html = html.replace(
    'kt("walk").onclick = cd;',
    'kt("walk").onclick = () => { cd(); if (ZGAME.active && !ZGAME.introDoneOnce && !ZGAME.introPlaying) startStoryIntro(); };',
    1
)
html = html.replace(
    '  if (!l && moveMag > 0) {',
    '  if (!l && moveMag > 0 && !ZGAME.introPlaying) {',
    1
)
html = html.replace(
    '  xt.position.y=followGround?newGround:Math.max(xt.position.y,newGround);',
    '  if(!ZGAME.introPlaying) xt.position.y=(followGround?newGround:Math.max(xt.position.y,newGround))+(Ye.xr.isPresenting&&ZGAME.active?ZGAME.jumpY:0);',
    1
)
html = html.replace(
    '  if (povMode === "1st" && !Ye.xr.isPresenting) {',
    '  if (povMode === "1st" && !Ye.xr.isPresenting && !ZGAME.introPlaying) {',
    1
)
html = html.replace(
    '    let showFP = povMode === "1st" && !Ye.xr.isPresenting;',
    '    let showFP = povMode === "1st" && !Ye.xr.isPresenting && !ZGAME.introPlaying;',
    1
)

# 7l. Photorealistic D-Block (School of Humanities & Science) Architectural & Graphics Upgrade!
DBLOCK_OLD = '''// D-Block Projecting West Stairwell Tower with Iconic Giant Street-Art Mural (Unobstructed!)
gr.push([-67.6, -8.2, -65.0, -1.4, "D Block (CVSR Engineering & Solar Roof)"]);
he(C_WALL_WHITE, -66.2, dBlockH * 0.44, -4.8, 2.2, dBlockH * 0.88, 6.2);
var muralPlane = new et(new _i(5.8, dBlockH * 0.84), new Jt({ map: muralTex, roughness: 0.55 }));
muralPlane.rotation.y = -Math.PI / 2;
muralPlane.position.set(-67.35, dBlockH * 0.44, -4.8);
Ht.add(muralPlane);
ys(["D BLOCK · ECE & EEE", "CVSR SOLAR ROOF & ART MURAL"], -67.36, dBlockH * 0.94, -4.8, 5.8, 1.05, "#1f4762", "#f7f4ea", -Math.PI / 2);'''

if DBLOCK_OLD not in html:
    DBLOCK_OLD = DBLOCK_OLD.replace("\n", "\r\n")
assert DBLOCK_OLD in html, "Could not find D-Block anchor!"

DBLOCK_UPGRADE_JS = f'''// D-BLOCK (SCHOOL OF HUMANITIES & SCIENCE) — HIGH-DETAIL ARCHITECTURAL UPGRADE FROM REAL PHOTO!
var realDBlockMuralTex = muralTex;
(function() {{
  const uri = "{dblock_mural_uri}";
  if (!uri) return;
  const c = document.createElement("canvas"); c.width = 512; c.height = 512;
  const g = c.getContext("2d");
  g.fillStyle = "#9aa5a0"; g.fillRect(0, 0, 512, 512);
  const t = new dn(c); t.colorSpace = vt;
  const im = new Image(); im.src = uri;
  im.onload = () => {{ g.drawImage(im, 0, 0, 512, 512); t.needsUpdate = true; }};
  realDBlockMuralTex = t;
}})();

// 1. Right-Side Projecting Mural Wing (Upper Giant "YOUR FUTURE LOOKS Bright" Mural + Ground Glass Lobby!)
gr.push([-67.6, -9.8, -65.0, -2.6, "D Block · School of Humanities & Science"]);
he(C_WALL_WHITE, -66.2, dBlockH * 0.72, -6.2, 2.3, dBlockH * 0.56, 7.0);
// Real Perspective-Corrected "YOUR FUTURE LOOKS Bright" VR-Goggles Mural!
var muralPlane = new et(new _i(6.8, dBlockH * 0.54), new Jt({{ map: realDBlockMuralTex, roughness: 0.48 }}));
muralPlane.rotation.y = -Math.PI / 2;
muralPlane.position.set(-67.38, dBlockH * 0.72, -6.2);
Ht.add(muralPlane);
// Ground-Floor Floor-to-Ceiling Glass Lobby + "Explore. Collaborate. Learn." Blue Fascia Banner!
he(0x16222c, -66.2, 2.4, -6.2, 2.0, 4.8, 6.6);
var dLobbyGlass = new et(new _i(6.2, 4.4), new Jt({{ color: 0x3b6078, roughness: 0.14, metalness: 0.35, transparent: true, opacity: 0.72 }}));
dLobbyGlass.rotation.y = -Math.PI / 2;
dLobbyGlass.position.set(-67.25, 2.35, -6.2);
Ht.add(dLobbyGlass);
he(C_WALL_WHITE, -67.30, 2.4, -9.45, 0.38, 4.8, 0.42);
he(C_WALL_WHITE, -67.30, 2.4, -2.95, 0.38, 4.8, 0.42);
ys(["Explore. Collaborate. Learn."], -67.32, 2.15, -6.2, 5.8, 0.52, "#1e3a6e", "#f8fafc", -Math.PI / 2);

// 2. Left-Side Double-Height Crisp White Entrance Portico ("SCHOOL OF HUMANITIES & SCIENCE")
he(C_WALL_WHITE, -68.4, 7.6, -13.4, 5.2, 1.05, 7.2); // Portico top lintel slab
he(0x2c333a, -68.4, 7.05, -13.4, 4.9, 0.12, 6.8);    // Recessed dark soffit ceiling
he(C_WALL_WHITE, -70.6, 3.6, -10.1, 0.65, 7.2, 0.65); // Right front pillar
he(C_WALL_WHITE, -70.6, 3.6, -16.7, 0.65, 7.2, 0.65); // Left front pillar
ys(["SCHOOL OF HUMANITIES & SCIENCE"], -71.02, 7.6, -13.4, 6.8, 0.82, "#f1f3f5", "#1c242b", -Math.PI / 2);

// 3. Wide Granite Entrance Steps + Wheelchair Ramp
for (let st = 0; st < 5; st++) {{
  he(0x9ca3af, -69.5 - st * 0.45, 0.14 * (5 - st) * 0.5, -13.4, 0.55, 0.14 * (5 - st), 7.6);
}}
he(0xb0b7c0, -70.4, 0.34, -10.4, 2.6, 0.12, 1.2); // Ramp surface

// 4. Iconic Green Grass Patch + 3D "#AU" Monument (RED "#" + WHITE "AU" on Dark Base!)
he(0x4b7838, -69.8, 0.05, -6.2, 4.2, 0.10, 6.2); // Front lawn strip
he(0x1f2429, -70.6, 0.22, -6.2, 0.45, 0.26, 3.6); // Dark plinth base
// 3D Red "#" Hash Symbol
var redHashMat = new Jt({{ color: 0xdc2626, roughness: 0.35, metalness: 0.15 }});
var whiteAuMat = new Jt({{ color: 0xf8fafc, roughness: 0.32, metalness: 0.12 }});
for (let hz of [-7.45, -7.05]) {{
  let bar = new et(new Ni(0.18, 1.25, 0.16), redHashMat); bar.position.set(-70.6, 0.98, hz); bar.rotation.x = 0.12; Ht.add(bar);
}}
for (let hy of [0.76, 1.16]) {{
  let bar = new et(new Ni(0.18, 0.16, 0.85), redHashMat); bar.position.set(-70.6, hy, -7.25); Ht.add(bar);
}}
// 3D White "A"
let aL = new et(new Ni(0.20, 1.48, 0.18), whiteAuMat); aL.position.set(-70.6, 1.05, -6.38); aL.rotation.x = 0.24; Ht.add(aL);
let aR = new et(new Ni(0.20, 1.48, 0.18), whiteAuMat); aR.position.set(-70.6, 1.05, -5.88); aR.rotation.x = -0.24; Ht.add(aR);
let aBar = new et(new Ni(0.20, 0.16, 0.55), whiteAuMat); aBar.position.set(-70.6, 0.82, -6.13); Ht.add(aBar);
// 3D White "U"
let uL = new et(new Ni(0.20, 1.38, 0.18), whiteAuMat); uL.position.set(-70.6, 1.08, -5.25); Ht.add(uL);
let uR = new et(new Ni(0.20, 1.38, 0.18), whiteAuMat); uR.position.set(-70.6, 1.08, -4.65); Ht.add(uR);
let uBot = new et(new Ni(0.20, 0.20, 0.78), whiteAuMat); uBot.position.set(-70.6, 0.44, -4.95); Ht.add(uBot);

// 5. Dual Vertical Flagpole Banner ("Be MORE THAN ONE" Red | "AU ANURAG UNIVERSITY" Navy)
let bPole = new et(new pn(0.055, 0.065, 4.2, 12), new Jt({{ color: 0xcbd5e1, roughness: 0.25, metalness: 0.85 }}));
bPole.position.set(-71.3, 2.1, -9.8); Ht.add(bPole);
ys(["Be", "MORE", "THAN", "ONE"], -71.3, 2.65, -10.35, 0.92, 2.15, "#b91c1c", "#ffffff", -Math.PI / 2);
ys(["AU", "ANURAG", "UNIVERSITY"], -71.3, 2.65, -9.25, 0.92, 2.15, "#1e293b", "#ffffff", -Math.PI / 2);

// 6. Yellow & Black Striped Road Curb along D-Block Front
for (let cz = -17.5; cz <= -2.5; cz += 0.9) {{
  let isY = Math.round(cz * 2) % 2 === 0;
  he(isY ? 0xeab308 : 0x18181b, -72.2, 0.11, cz, 0.34, 0.22, 0.88);
}}'''

html = html.replace(DBLOCK_OLD, DBLOCK_UPGRADE_JS, 1)

# 7m. High-Detail DR. APJ ABDUL KALAM HALL (Auditorium) Architectural Upgrade from 4 Real Reference Photos!
KALAM_OLD = '''// ============================================================================
// BUILDING 8: APJ ABDUL KALAM AUDITORIUM / INDOOR SPORTS COMPLEX (FAR SW)
// ============================================================================
gr.push([-115, 51, -83, 69, "APJ Abdul Kalam Auditorium & Indoor Stadium"]);
he(C_WALL_WHITE, -100, 4.8, 61.5, 28.0, 9.6, 15.5);
he(0xf7f7f4, -99, 2.3, 52.2, 30.0, 4.6, 4.2);
he(C_ROOF_SLAB, -99, 4.68, 52.2, 30.4, 0.2, 4.5);
for (let i = 0; i < 6; i++) {
  let wx = -109.5 + i * 3.8;
  addDarkGlass(wx, 2.45, 50.06, 2.85, 1.65, 0.08);
}
he(0xb8b4ac, -111.5, 0.45, 49.4, 3.2, 0.9, 1.8);
addDarkGlass(-111.5, 2.2, 50.06, 2.2, 2.5, 0.08);

var audRoof = new et(
  new pn(8.2, 8.2, 28.4, 24, 1, false, 0, Math.PI),
  new Jt({ color: C_ROOF_RED, roughness: 0.65, metalness: 0.12 })
);
audRoof.rotation.z = Math.PI / 2;
audRoof.scale.set(0.52, 1, 1);
audRoof.position.set(-100, 9.5, 61.5);
audRoof.castShadow = true;
Ht.add(audRoof);

for (let czCanopy of [54.5, 64.5]) {
  let can = new et(
    new pn(2.2, 2.2, 5.5, 16, 1, false, 0, Math.PI),
    new Jt({ color: C_ROOF_RED, roughness: 0.68 })
  );
  can.rotation.z = Math.PI / 2;
  can.scale.set(0.55, 1, 1);
  can.position.set(-83.5, 4.2, czCanopy);
  Ht.add(can);
}
he(0xcac4b8, -80.5, 0.09, 59.5, 11.5, 0.1, 18.0);
for (let pz of [54.5, 59.5, 64.5]) {
  fr(rd, 0x7b756d, -78.5, 0.35, pz, 0.95, 0.6, 0.95);
  fr(nd, 0x456b34, -78.5, 0.95, pz, 0.85, 0.75, 0.85);
}
ys(["APJ ABDUL KALAM AUDITORIUM", "INDOOR SPORTS COMPLEX"], -85.8, 6.2, 59.5, 8.2, 1.4, "#7d291f", "#ffffff", Math.PI / 2);'''

if KALAM_OLD not in html:
    KALAM_OLD = KALAM_OLD.replace("\n", "\r\n")
assert KALAM_OLD in html, "Could not find APJ Abdul Kalam Auditorium anchor!"

KALAM_UPGRADE_JS = '''// ============================================================================
// BUILDING 8: DR. APJ ABDUL KALAM HALL — PHOTO-ACCURATE HIGH-DETAIL UPGRADE
// ============================================================================
gr.push([-115, 51, -83, 69.5, "Dr. APJ Abdul Kalam Hall"]);
// Procedural corrugated terracotta-red metal roof texture
var kalamCorrugTex = (function() {
  const c = document.createElement("canvas"); c.width = 256; c.height = 128;
  const g = c.getContext("2d");
  for (let x = 0; x < 256; x += 8) {
    g.fillStyle = "#8e2d24"; g.fillRect(x, 0, 4, 128);
    g.fillStyle = "#b84438"; g.fillRect(x + 4, 0, 2, 128);
    g.fillStyle = "#6c1f18"; g.fillRect(x + 6, 0, 2, 128);
  }
  const t = new dn(c); t.colorSpace = vt; t.wrapS = t.wrapT = jn; t.repeat.set(14, 2);
  return t;
})();

// 1. Crisp White Stucco Auditorium Body + Curved Corrugated Terracotta Barrel-Vault Roof
he(0xf3f4f2, -100, 3.1, 60.5, 28.0, 6.2, 18.6);
var kalamRoofMat = new Jt({ map: kalamCorrugTex, roughness: 0.52, metalness: 0.22 });
var audRoof = new et(new pn(9.4, 9.4, 28.4, 28, 1, false, 0, Math.PI), kalamRoofMat);
audRoof.rotation.z = Math.PI / 2;
audRoof.scale.set(0.38, 1, 1);
audRoof.position.set(-100, 6.15, 60.5);
audRoof.castShadow = true;
Ht.add(audRoof);
// Corrugated red end gable tympanum facing the front courtyard (East, x = -85.95)
var kalamGable = new et(new pn(9.2, 9.2, 0.25, 24, 1, false, 0, Math.PI), kalamRoofMat);
kalamGable.rotation.z = Math.PI / 2;
kalamGable.scale.set(0.37, 1, 1);
kalamGable.position.set(-85.95, 6.15, 60.5);
Ht.add(kalamGable);
// Clean white parapet cornice trim
he(0xe5e7eb, -85.9, 6.18, 60.5, 0.32, 0.24, 18.9);

// 2. Raised Metallic 3D Silver Signage: "Dr. APJ ABDUL KALAM / HALL"
(function() {
  const c = document.createElement("canvas"); c.width = 1024; c.height = 256;
  const g = c.getContext("2d");
  g.fillStyle = "#f3f4f2"; g.fillRect(0, 0, 1024, 256);
  g.textAlign = "center";
  // Soft wall drop-shadow for 3D raised steel letters
  g.fillStyle = "rgba(30,38,48,0.42)"; g.font = "900 72px 'Segoe UI',sans-serif";
  g.fillText("Dr. APJ ABDUL KALAM", 518, 114);
  g.fillText("HALL", 518, 198);
  // Brushed silver metallic letters
  const grad = g.createLinearGradient(0, 45, 0, 200);
  grad.addColorStop(0, "#eef2f6"); grad.addColorStop(0.5, "#94a3b8"); grad.addColorStop(1, "#cbd5e1");
  g.fillStyle = grad;
  g.fillText("Dr. APJ ABDUL KALAM", 512, 108);
  g.fillText("HALL", 512, 192);
  g.strokeStyle = "#475569"; g.lineWidth = 2;
  g.strokeText("Dr. APJ ABDUL KALAM", 512, 108);
  g.strokeText("HALL", 512, 192);
  const t = new dn(c); t.colorSpace = vt;
  const sign = new et(new _i(7.8, 1.95), new Jt({ map: t, roughness: 0.35, metalness: 0.45 }));
  sign.rotation.y = Math.PI / 2;
  sign.position.set(-85.92, 4.55, 57.6);
  Ht.add(sign);
})();

// 3. Three Wide Horizontal White-Framed Sliding Windows (Center-Right Facade)
var kalamWinGlass = new Jt({ color: 0x16222c, roughness: 0.14, metalness: 0.42 });
var kalamFrameMat = new Jt({ color: 0xf8fafc, roughness: 0.38, metalness: 0.25 });
for (let wz of [61.2, 58.0, 54.8]) {
  let wg = new et(new Ni(0.12, 1.65, 2.55), kalamWinGlass); wg.position.set(-85.94, 2.25, wz); Ht.add(wg);
  // White aluminum perimeter frame + center sliding mullion
  he(0xf8fafc, -85.88, 3.08, wz, 0.14, 0.09, 2.66);
  he(0xf8fafc, -85.88, 1.42, wz, 0.14, 0.09, 2.66);
  he(0xf8fafc, -85.88, 2.25, wz - 1.29, 0.14, 1.72, 0.09);
  he(0xf8fafc, -85.88, 2.25, wz + 1.29, 0.14, 1.72, 0.09);
  he(0xf8fafc, -85.88, 2.25, wz, 0.14, 1.68, 0.07);
}

// 4. Left Entrance Wing: Curved Terracotta Canopy, Teak Double Doors, Kalam Portrait Plaque & Dark Granite Steps
var steelMat = new Jt({ color: 0xd8dee4, roughness: 0.35, metalness: 0.65 });
// Curved red metal canopy over left entrance (z = 62.6 .. 69.6)
var entCanopy = new et(new pn(2.15, 2.15, 7.2, 18, 1, false, 0, Math.PI), kalamRoofMat);
entCanopy.rotation.x = Math.PI / 2;
entCanopy.scale.set(1.0, 1.0, 0.36);
entCanopy.position.set(-83.9, 4.25, 66.1);
entCanopy.castShadow = true;
Ht.add(entCanopy);
// Matching right-wing curved red canopy (z = 51.4 .. 53.6)
var rCanopy = new et(new pn(2.15, 2.15, 2.4, 14, 1, false, 0, Math.PI), kalamRoofMat);
rCanopy.rotation.x = Math.PI / 2;
rCanopy.scale.set(1.0, 1.0, 0.36);
rCanopy.position.set(-83.9, 4.25, 52.5);
Ht.add(rCanopy);

// Slender white steel columns + open steel pergola frame bridging across center facade!
for (let pz of [69.4, 66.0, 62.7, 59.4, 56.1, 53.4]) {
  he(0xdce2e8, -81.95, 2.55, pz, 0.16, 5.1, 0.16);
  // Diagonal brace tying column cleanly back into upper white facade
  he(0xdce2e8, -83.95, 4.95, pz, 4.0, 0.14, 0.14);
}
// Continuous horizontal white steel top beam connecting all columns
he(0xdce2e8, -81.95, 5.05, 61.4, 0.18, 0.18, 16.4);

// Two Grand Teak-Wood Double Entrance Doors + Framed Dr. APJ Abdul Kalam Portrait Plaque
var teakMat = new Jt({ color: 0x6b3e26, roughness: 0.58, metalness: 0.08 });
for (let dz of [64.6, 67.6]) {
  he(0x3a2012, -85.94, 2.25, dz, 0.18, 2.85, 2.15); // Dark wood outer frame
  let dL = new et(new Ni(0.14, 2.65, 0.92), teakMat); dL.position.set(-85.88, 2.22, dz - 0.50); Ht.add(dL);
  let dR = new et(new Ni(0.14, 2.65, 0.92), teakMat); dR.position.set(-85.88, 2.22, dz + 0.50); Ht.add(dR);
}
// Framed Dr. Kalam tribute plaque above main door
ys(["Dr. APJ ABDUL KALAM", "DREAM · TRANSFORM"], -85.88, 3.98, 64.6, 1.55, 0.62, "#f8fafc", "#1e293b", Math.PI / 2);

// Covered Dark-Granite Veranda + 5 Wide Dark-Granite Entrance Steps with Terracotta Side Cheeks
he(0x2d3238, -83.9, 0.42, 66.1, 4.1, 0.84, 7.2);
for (let st = 0; st < 5; st++) {
  let hStep = (5 - st) * 0.15;
  he(0x282d33, -81.6 + st * 0.34, hStep * 0.5, 66.1, 0.38, hStep, 7.2);
}
he(0xa64b42, -80.9, 0.38, 62.45, 1.8, 0.76, 0.22); // Terracotta step cheek
he(0xa64b42, -80.9, 0.38, 69.75, 1.8, 0.76, 0.22);

// 5. Terracotta-Edged Raised Green Planter Bed under Windows + Lush Lime-Green Spider Grass Tufts
he(0xa64b42, -83.9, 0.24, 57.2, 4.1, 0.48, 10.6);
he(0x3b6e28, -83.9, 0.49, 57.2, 3.7, 0.08, 10.1);
var spiderGrassMat = new Jt({ color: 0x7cb342, roughness: 0.82 });
for (let gz = 52.8; gz <= 61.8; gz += 1.05) {
  for (let gx of [-84.9, -83.3]) {
    let tuft = new et(new fn(0.42, 7, 6), spiderGrassMat);
    tuft.scale.set(1.15, 0.62, 1.15);
    tuft.position.set(gx + (Math.random() - 0.5) * 0.3, 0.68, gz + (Math.random() - 0.5) * 0.25);
    Ht.add(tuft);
  }
}

// 6. Scored Cream-Beige Concrete Courtyard + Blooming Pink Bougainvillea Bush on Left Edge
he(0xd6cfc0, -76.8, 0.06, 60.5, 13.5, 0.12, 20.0);
let bougLeaf = new et(new fn(1.15, 10, 8), new Jt({ color: 0x2f6b28, roughness: 0.85 }));
bougLeaf.position.set(-77.5, 1.2, 69.2); Ht.add(bougLeaf);
let bougPinkMat = new Jt({ color: 0xd81b60, roughness: 0.65 });
for (let [bx, by, bz] of [[-76.8, 1.6, 68.7], [-77.3, 1.9, 69.4], [-77.9, 1.4, 68.6], [-76.6, 1.1, 69.3]]) {
  let fl = new et(new fn(0.42, 8, 6), bougPinkMat); fl.position.set(bx, by, bz); Ht.add(fl);
}'''

html = html.replace(KALAM_OLD, KALAM_UPGRADE_JS, 1)

# 7n. Iconic Full-Wall Street-Art Mural on C-Block North Wall (facing B-Block) — original B-Block front lawn restored!
CBLOCK_MURAL_JS = f'''
// ============================================================================
// C-BLOCK ICONIC STREET-ART MURAL (FACING B-BLOCK)
// ============================================================================
(function() {{
  const cbUri = "{cblock_mural_uri}";
  if (cbUri) {{
    const mc = document.createElement("canvas"); mc.width = 512; mc.height = 640;
    const mg = mc.getContext("2d");
    mg.fillStyle = "#dfd2a6"; mg.fillRect(0, 0, 512, 640);
    const mt = new dn(mc); mt.colorSpace = vt;
    const mim = new Image(); mim.src = cbUri;
    mim.onload = () => {{ mg.drawImage(mim, 0, 0, 512, 640); mt.needsUpdate = true; }};
    // Clean plastered mural backing slab sitting flush in front of pilasters so ZERO ledges clip the painting!
    he(0xdfd2a6, -61.5, 5.45, 23.74, 8.56, 10.95, 0.44);
    const cbMural = new et(new _i(8.48, 10.9), new Jt({{ map: mt, roughness: 0.48 }}));
    cbMural.rotation.y = Math.PI; // Faces -Z (North, straight towards B-Block!)
    cbMural.position.set(-61.5, 5.45, 23.50);
    Ht.add(cbMural);
  }}
}})();
'''

html = html.replace(
    '// ============================================================================\n// BUILDING 9:',
    CBLOCK_MURAL_JS + '\n// ============================================================================\n// BUILDING 9:',
    1
)
if CBLOCK_MURAL_JS not in html:
    html = html.replace(
        '// ============================================================================\r\n// BUILDING 9:',
        CBLOCK_MURAL_JS + '\r\n// ============================================================================\r\n// BUILDING 9:',
        1
    )

# Add "C-Block · Iconic Street-Art Mural" and "A-Block & B/D-Block Palm Pathway" viewpoints to ld[] stops!
html = html.replace(
    '["D Block · Solar Roof & Street-Art Mural", -75.5, -4.8, -Math.PI / 2, 0.14, 0],',
    '["D Block · Solar Roof & Street-Art Mural", -75.5, -4.8, -Math.PI / 2, 0.14, 0],\n  ["C-Block · Iconic Street-Art Mural", -61.5, 13.8, Math.PI, 0.16, 0],\n  ["A-Block & B/D-Block Palm Pathway", -31.2, 13.5, 0.0, 0.06, 0],',
    1
)

# 7o. Photo-Accurate Palm-Lined Pathway between A-Block and B/D-Block (x = -31.2, z = -22 .. +14)
AB_PATHWAY_JS = '''
// ============================================================================
// A-BLOCK <-> B/D-BLOCK PALM-LINED PATHWAY — PHOTO-ACCURATE DETAIL UPGRADE
// ============================================================================
(function() {
  const px = -31.2, zStart = -22, zEnd = 14, len = zEnd - zStart, midZ = (zStart + zEnd) * 0.5;

  // 1. Warm Cream-Beige Scored Concrete Pathway with Expansion Joint Lines
  he(0xd5cbb8, px, 0.08, midZ, 6.8, 0.12, len + 2.0);
  for (let jz = zStart; jz <= zEnd; jz += 3.6) {
    he(0xb5aa96, px, 0.145, jz, 6.7, 0.015, 0.06);
  }
  he(0xb5aa96, px, 0.145, midZ, 0.06, 0.015, len);

  // 2. West Side (B/D-Block Side, x = -35.2): Dark Stone-Brick Retaining Ledge + Terracotta Flowerpots!
  const brickTex = (function() {
    const c = document.createElement("canvas"); c.width = 256; c.height = 128;
    const g = c.getContext("2d");
    g.fillStyle = "#2b2a26"; g.fillRect(0, 0, 256, 128);
    for (let r = 0; r < 8; r++) {
      let off = (r % 2) * 16;
      for (let col = -1; col < 9; col++) {
        g.fillStyle = (col + r) % 3 === 0 ? "#3f3b32" : "#322f28";
        g.fillRect(col * 32 + off + 2, r * 16 + 2, 28, 12);
      }
    }
    const t = new dn(c); t.colorSpace = vt; t.wrapS = t.wrapT = jn; t.repeat.set(16, 1);
    return t;
  })();
  let brickWall = new et(new Ni(0.95, 1.05, len), new Jt({ map: brickTex, roughness: 0.88 }));
  brickWall.position.set(-35.1, 0.54, midZ);
  brickWall.castShadow = true; brickWall.receiveShadow = true;
  Ht.add(brickWall);
  he(0x6e6a62, -35.1, 1.09, midZ, 1.05, 0.07, len); // Concrete coping slab on top

  // Row of Terracotta Flowerpots with Green Plants perched along the brick ledge!
  const potMat = new Jt({ color: 0x9a4a32, roughness: 0.78 });
  const plantMat = new Jt({ color: 0x3b6e28, roughness: 0.84 });
  for (let pz = zStart + 1.5; pz <= zEnd - 1.5; pz += 3.2) {
    let pot = new et(new pn(0.22, 0.16, 0.28, 10), potMat);
    pot.position.set(-35.1, 1.26, pz); Ht.add(pot);
    let bush = new et(new fn(0.28, 8, 6), plantMat);
    bush.scale.set(1.1, 0.85, 1.1); bush.position.set(-35.1, 1.48, pz); Ht.add(bush);
  }

  // 3. East Side (A-Block Side, x = -27.2): Terracotta-Curbed Planter Strip + Lush Green Grass!
  he(0x9e433a, -27.55, 0.22, midZ, 0.22, 0.44, len);
  he(0x3a6a26, -26.75, 0.34, midZ, 1.45, 0.18, len);
  const grassMat = new Jt({ color: 0x689f38, roughness: 0.85 });
  for (let gz = zStart + 1.0; gz <= zEnd - 1.0; gz += 1.35) {
    let tuft = new et(new fn(0.38, 7, 6), grassMat);
    tuft.scale.set(1.15, 0.58, 1.2); tuft.position.set(-26.85 + (Math.random() - 0.5) * 0.3, 0.52, gz); Ht.add(tuft);
  }

  // 4. Wall-Mounted AC Outdoor Compressor Units on Steel Brackets along A-Block West Wall (x = -25.85)!
  const acBodyMat = new Jt({ color: 0xe8ecee, roughness: 0.42, metalness: 0.22 });
  const acFanMat = new Jt({ color: 0x262b30, roughness: 0.65 });
  const acBrkMat = new Jt({ color: 0x525860, roughness: 0.55, metalness: 0.7 });
  for (let [az, ay] of [[9.5, 1.85], [3.5, 1.85], [-2.5, 5.2], [-8.5, 1.85], [-14.5, 5.2]]) {
    let ac = new et(new Ni(0.42, 0.62, 0.86), acBodyMat);
    ac.position.set(-25.85, ay, az); Ht.add(ac);
    let fan = new et(new pn(0.22, 0.22, 0.06, 14), acFanMat);
    fan.rotation.z = Math.PI / 2; fan.position.set(-26.07, ay, az + 0.12); Ht.add(fan);
    let brk = new et(new Ni(0.48, 0.06, 0.75), acBrkMat);
    brk.position.set(-25.82, ay - 0.34, az); Ht.add(brk);
    let pipe = new et(new pn(0.025, 0.025, 2.2, 6), acBodyMat);
    pipe.position.set(-25.68, ay + 1.1, az - 0.32); Ht.add(pipe);
  }

  // 5. Symmetrical Double Avenue of Tall Royal Palm Trees with Orange/White/Green Tricolor Trunks!
  const palmPositions = [-19, -13.5, -8, -2.5, 3, 8.5, 13];
  for (let idx = 0; idx < palmPositions.length; idx++) {
    let tz = palmPositions[idx];
    for (let tx of [-34.45, -27.75]) {
      entrancePalm(tx, tz, 6.8 + (idx % 2) * 0.7, idx * 1.1 + (tx < -30 ? 0 : 1.7));
      // Iconic Orange / White / Green Indian Tricolor Painted Bands on Lower Trunk!
      let bandG = new et(new pn(0.165, 0.175, 0.32, 12), new Jt({ color: 0x16803c, roughness: 0.72 }));
      bandG.position.set(tx, 0.42, tz); Ht.add(bandG);
      let bandW = new et(new pn(0.162, 0.168, 0.32, 12), new Jt({ color: 0xf8fafc, roughness: 0.72 }));
      bandW.position.set(tx, 0.74, tz); Ht.add(bandW);
      let bandO = new et(new pn(0.158, 0.164, 0.32, 12), new Jt({ color: 0xea580c, roughness: 0.72 }));
      bandO.position.set(tx, 1.06, tz); Ht.add(bandO);
    }
  }

  // 6. Iconic Double-Level Red Elevated Skybridges Spanning Overhead at the North End (z = -18.5)!
  for (let sy of [6.4, 9.8]) {
    he(0xb84a42, px, sy, -18.5, 11.4, 1.55, 2.8);
    he(0xf3f4f6, px, sy + 0.85, -18.5, 11.4, 0.18, 2.95);
    he(0xf3f4f6, px, sy - 0.85, -18.5, 11.4, 0.18, 2.95);
  }
})();
'''

html = html.replace(
    '// ============================================================================\n// BUILDING 9:',
    AB_PATHWAY_JS + '\n// ============================================================================\n// BUILDING 9:',
    1
)
if AB_PATHWAY_JS not in html:
    html = html.replace(
        '// ============================================================================\r\n// BUILDING 9:',
        AB_PATHWAY_JS + '\r\n// ============================================================================\r\n// BUILDING 9:',
        1
    )

# (C-Block Mural & Palm Pathway stops already added above)

# 7p. Comprehensive Campus Detailing Upgrade from Official 19-Min YouTube Campus Tour Video (BAc9tc8UiO0)
VIDEO_CAMPUS_UPGRADE_JS = '''
// ============================================================================
// CAMPUS TOUR VIDEO REFERENCE UPGRADE (BAc9tc8UiO0 — ALL KEY LOCATIONS)
// 1. Main Gate Blue Sliding Gate, Stone Monument & 5-Panel Sports Silhouette Mural (00:25-00:49)
// 2. A-Block Central Courtyard Amphitheater Stage & Giant White Screen (01:29-01:45)
// 3. G-Block / ECE Iconic TEDxAnuragU Entrance, Terracotta Lobby & Red Gazebo (15:21-18:17)
// 4. Pharmacy Medicinal Garden Blue Archway & Raised Herb Beds (09:21-09:29)
// 5. Cricket Ground Wrought-Iron Gate, Thatched Pitch Roller Shed & Mega Block Tower Crane (11:45-13:53)
// 6. Placement Standees, Basketball Colored Pillars, Fitness Tires & West Transmission Pylon (02:25-04:09)
// ============================================================================
(function() {
  // --- 1. MAIN GATE & ENTRANCE AVENUE UPGRADES (00:01 - 00:57) ---
  // 1a. Rolled-Open Blue Steel Main Sliding Gates at Main Entrance (z = 72.1)
  const gateBlueMat = new Jt({ color: 0x1e4b85, roughness: 0.42, metalness: 0.55 });
  for (let side of [-1, 1]) {
    let gx = -3 + side * 4.55;
    he(0x1e4b85, gx, 1.15, 72.2, 2.2, 0.12, 0.14); // top rail
    he(0x1e4b85, gx, 0.25, 72.2, 2.2, 0.12, 0.14); // bottom rail
    for (let bar = -0.9; bar <= 0.91; bar += 0.26) {
      let p = new et(new Ni(0.06, 1.9, 0.06), gateBlueMat);
      p.position.set(gx + bar, 1.05, 72.2); Ht.add(p);
    }
  }
  // 1b. Dark-Granite "ANURAG UNIVERSITY" Stone Monument Wall (Left of Gate, 00:33)
  he(0x3a4048, -14.8, 1.15, 72.2, 6.2, 2.3, 0.72);
  he(0xdce2e8, -14.8, 2.34, 72.2, 6.4, 0.14, 0.84);
  ys(["ANURAG UNIVERSITY", "ESTD. 2002 · HYDERABAD"], -14.8, 1.32, 72.6, 5.4, 1.35, "#2b313a", "#f8fafc", 0);

  // 1c. Vibrant 5-Panel Colorful Sports Silhouette Wall Mural beside Main Gate (00:25, 11:21)
  (function() {
    const c = document.createElement("canvas"); c.width = 1024; c.height = 256;
    const g = c.getContext("2d");
    const panels = [
      { bg: "#f97316", lbl: "VOLLEYBALL", icon: "volleyball" },
      { bg: "#0d9488", lbl: "FOOTBALL", icon: "football" },
      { bg: "#eab308", lbl: "ATHLETICS", icon: "run" },
      { bg: "#2563eb", lbl: "CRICKET", icon: "cricket" },
      { bg: "#dc2626", lbl: "BADMINTON", icon: "badminton" }
    ];
    const pw = 1024 / 5;
    panels.forEach((p, idx) => {
      const x0 = idx * pw;
      g.fillStyle = p.bg; g.fillRect(x0, 0, pw, 256);
      // Geometric diagonal light highlight
      g.fillStyle = "rgba(255,255,255,0.14)";
      g.beginPath(); g.moveTo(x0, 0); g.lineTo(x0 + pw * 0.65, 0); g.lineTo(x0, 220); g.closePath(); g.fill();
      // Stylized bold athlete silhouette
      const cx = x0 + pw * 0.52, cy = 112;
      g.fillStyle = "#111827";
      g.beginPath(); g.arc(cx, cy - 42, 16, 0, Math.PI * 2); g.fill(); // Head
      g.lineWidth = 14; g.lineCap = "round"; g.strokeStyle = "#111827";
      g.beginPath(); g.moveTo(cx, cy - 24); g.lineTo(cx - 4, cy + 28); g.stroke(); // Torso
      // Dynamic limbs per sport
      if (p.icon === "volleyball") {
        g.beginPath(); g.moveTo(cx, cy - 16); g.lineTo(cx - 26, cy - 46); g.moveTo(cx, cy - 16); g.lineTo(cx + 28, cy - 52); g.stroke();
        g.beginPath(); g.moveTo(cx - 4, cy + 28); g.lineTo(cx - 22, cy + 74); g.moveTo(cx - 4, cy + 28); g.lineTo(cx + 18, cy + 70); g.stroke();
        g.fillStyle = "#ffffff"; g.beginPath(); g.arc(cx + 12, cy - 72, 13, 0, Math.PI * 2); g.fill();
      } else if (p.icon === "football") {
        g.beginPath(); g.moveTo(cx, cy - 16); g.lineTo(cx - 32, cy + 6); g.moveTo(cx, cy - 16); g.lineTo(cx + 30, cy - 28); g.stroke();
        g.beginPath(); g.moveTo(cx - 4, cy + 28); g.lineTo(cx - 26, cy + 74); g.moveTo(cx - 4, cy + 28); g.lineTo(cx + 32, cy + 56); g.stroke();
        g.fillStyle = "#ffffff"; g.beginPath(); g.arc(cx + 46, cy + 64, 12, 0, Math.PI * 2); g.fill();
      } else if (p.icon === "run") {
        g.beginPath(); g.moveTo(cx, cy - 16); g.lineTo(cx + 32, cy - 22); g.moveTo(cx, cy - 16); g.lineTo(cx - 30, cy + 12); g.stroke();
        g.beginPath(); g.moveTo(cx - 4, cy + 28); g.lineTo(cx + 34, cy + 62); g.moveTo(cx - 4, cy + 28); g.lineTo(cx - 36, cy + 68); g.stroke();
      } else if (p.icon === "cricket") {
        g.beginPath(); g.moveTo(cx, cy - 16); g.lineTo(cx + 26, cy - 6); g.moveTo(cx, cy - 16); g.lineTo(cx + 18, cy + 12); g.stroke();
        g.beginPath(); g.moveTo(cx - 4, cy + 28); g.lineTo(cx - 20, cy + 74); g.moveTo(cx - 4, cy + 28); g.lineTo(cx + 22, cy + 74); g.stroke();
        g.strokeStyle = "#fde68a"; g.lineWidth = 10;
        g.beginPath(); g.moveTo(cx + 22, cy + 2); g.lineTo(cx + 52, cy - 48); g.stroke(); // Bat
      } else {
        g.beginPath(); g.moveTo(cx, cy - 16); g.lineTo(cx + 26, cy - 48); g.moveTo(cx, cy - 16); g.lineTo(cx - 24, cy + 8); g.stroke();
        g.beginPath(); g.moveTo(cx - 4, cy + 28); g.lineTo(cx - 18, cy + 74); g.moveTo(cx - 4, cy + 28); g.lineTo(cx + 24, cy + 72); g.stroke();
        g.strokeStyle = "#ffffff"; g.lineWidth = 4;
        g.beginPath(); g.moveTo(cx + 26, cy - 48); g.lineTo(cx + 42, cy - 72); g.stroke();
        g.beginPath(); g.ellipse(cx + 48, cy - 82, 10, 14, 0.4, 0, Math.PI * 2); g.stroke(); // Racket
      }
      // Crisp white panel divider & bottom label
      g.fillStyle = "rgba(0,0,0,0.28)"; g.fillRect(x0, 214, pw, 42);
      g.fillStyle = "#ffffff"; g.font = "900 20px 'Segoe UI',sans-serif"; g.textAlign = "center";
      g.fillText(p.lbl, x0 + pw * 0.5, 242);
      if (idx > 0) { g.fillStyle = "#ffffff"; g.fillRect(x0 - 3, 0, 6, 256); }
    });
    const t = new dn(c); t.colorSpace = vt;
    // Boundary wall with 5-panel mural just West of Main Gate (x = -24.5, z = 71.8)
    he(0xf8fafc, -24.5, 1.45, 71.8, 12.6, 2.9, 0.45);
    const muralFront = new et(new _i(12.2, 2.65), new Jt({ map: t, roughness: 0.48 }));
    muralFront.position.set(-24.5, 1.48, 72.05); Ht.add(muralFront);
    const muralBack = new et(new _i(12.2, 2.65), new Jt({ map: t, roughness: 0.48 }));
    muralBack.rotation.y = Math.PI;
    muralBack.position.set(-24.5, 1.48, 71.55); Ht.add(muralBack);
  })();

  // 1d. Main Entrance Avenue: Red-Painted Tree Trunks + Placement Achievement Boards (00:01, 00:41)
  const redTrunkMat = new Jt({ color: 0xb91c1c, roughness: 0.72 });
  const whiteBandMat = new Jt({ color: 0xf8fafc, roughness: 0.72 });
  for (let az of [60, 50, 40, 30]) {
    for (let ax of [-9.4, 3.4]) {
      let bRed = new et(new pn(0.24, 0.27, 1.15, 10), redTrunkMat);
      bRed.position.set(ax, 0.58, az); Ht.add(bRed);
      let bWht = new et(new pn(0.23, 0.24, 0.16, 10), whiteBandMat);
      bWht.position.set(ax, 1.22, az); Ht.add(bWht);
    }
  }
  const placementStats = [
    { z: 58, num: "282+", lbl: "TCS · CAPGEMINI" },
    { z: 48, num: "159+", lbl: "COGNIZANT · ACCENTURE" },
    { z: 38, num: "1800+", lbl: "CAMPUS OFFERS · 52 LPA" }
  ];
  for (const st of placementStats) {
    he(0xdbe2ea, 4.6, 1.4, st.z, 0.12, 2.8, 0.12);
    ys([st.num, st.lbl], 4.6, 2.25, st.z, 2.3, 1.15, "#b91c1c", "#ffffff", -Math.PI / 2);
  }
  // 1e. A-Block Front Plaza Digital Standee Kiosks & Topiary Bushes (00:49, 00:57)
  for (let kx of [-10.2, 4.2]) {
    he(0x111827, kx, 1.15, 18.8, 0.92, 2.15, 0.22);
    he(0x334155, kx, 0.08, 18.8, 1.1, 0.16, 0.65);
    ys(["ANURAG", "UNIVERSITY"], kx, 1.28, 18.93, 0.78, 1.45, "#0f172a", "#38bdf8", 0);
    let topiary = new et(new fn(0.75, 10, 8), new Jt({ color: 0x2e6f28, roughness: 0.82 }));
    topiary.position.set(kx + (kx < 0 ? -1.4 : 1.4), 0.75, 18.6); Ht.add(topiary);
  }

  // --- 2. A-BLOCK CENTRAL COURTYARD AMPHITHEATER STAGE & SCREEN (01:29 - 01:45) ---
  // Elevated granite-trimmed performance stage on North edge of inner courtyard (x = -3, z = -11.0)
  he(0x2d3238, -3, 0.45, -10.8, 12.6, 0.9, 3.8);
  he(0xe2ddd2, -3, 0.93, -10.8, 12.8, 0.08, 4.0);
  // Side steps up onto the stage
  for (let s = 0; s < 4; s++) {
    let sh = (4 - s) * 0.22;
    he(0x475569, -9.6 - s * 0.35, sh * 0.5, -10.8, 0.36, sh, 2.2);
    he(0x475569, 3.6 + s * 0.35, sh * 0.5, -10.8, 0.36, sh, 2.2);
  }
  // Terracotta-brick framed giant crisp white projection screen / backdrop wall!
  he(0x9e3b33, -3, 3.4, -12.45, 11.8, 4.9, 0.48); // Red brick outer frame
  he(0xfdfdfc, -3, 3.45, -12.18, 9.8, 4.05, 0.12); // Crisp bright white projection screen
  he(0x9e3b33, -8.7, 3.4, -12.1, 0.75, 5.1, 0.75); // Left terracotta pillar
  he(0x9e3b33, 2.7, 3.4, -12.1, 0.75, 5.1, 0.75);  // Right terracotta pillar
  he(0x7c2d26, -3, 5.95, -12.15, 12.4, 0.32, 0.95); // Stage top coping beam
  // Courtyard corner Royal Palms with red lower trunks (01:29, 01:37)
  for (let [px, pz] of [[-14.5, 3.8], [8.5, 3.8], [-14.5, -9.8], [8.5, -9.8]]) {
    entrancePalm(px, pz, 7.6, px + pz);
    let rb = new et(new pn(0.17, 0.19, 1.0, 10), redTrunkMat);
    rb.position.set(px, 0.55, pz); Ht.add(rb);
  }

  // --- 3. WIDE 2-LANE EAST AVENUE (x = 24.4) + G-BLOCK (ADMIN), F-BLOCK (EXAM) & E-BLOCK (TEDxAnuragU) ---
  // 3a. Wide 2-Lane Asphalt Campus Avenue between A-Block and G/F/E-Block (wO 01:22, nK 00:26)
  const aveX = 24.4, aveZ = 1.0, aveLen = 70.0;
  he(0x3a3f46, aveX, 0.06, aveZ, 8.4, 0.12, aveLen); // Wide 2-lane dark asphalt surface
  // Crisp dashed white center lane divider
  for (let lz = -31; lz <= 33; lz += 4.2) {
    he(0xf8fafc, aveX, 0.13, lz, 0.16, 0.02, 2.1);
  }
  // Yellow-and-black striped curbs + checkered granite footpaths along BOTH sides of the 2-lane avenue!
  for (let cz = -33; cz <= 35; cz += 1.0) {
    let cCol = Math.abs(Math.round(cz)) % 2 === 0 ? 0xeab308 : 0x1e293b;
    he(cCol, aveX - 4.32, 0.14, cz, 0.24, 0.2, 0.96);
    he(cCol, aveX + 4.32, 0.14, cz, 0.24, 0.2, 0.96);
  }
  he(0x94a3b8, aveX - 5.1, 0.08, aveZ, 1.35, 0.14, aveLen); // West footpath (A-Block side)
  he(0x94a3b8, aveX + 5.1, 0.08, aveZ, 1.35, 0.14, aveLen); // East footpath (E/F/G-Block side)

  // 3b. G-BLOCK: CENTRAL ADMINISTRATIVE BLOCK Portico (wO 01:22 — x = 30.2, z = 14.5)
  he(0xf8fafc, 29.3, 3.6, 11.2, 0.72, 7.2, 0.72); // North portico pillar
  he(0xf8fafc, 29.3, 3.6, 17.8, 0.72, 7.2, 0.72); // South portico pillar
  he(0xf8fafc, 30.0, 7.25, 14.5, 2.6, 0.95, 7.8); // Double-height portico crown
  ys(["CENTRAL ADMINISTRATIVE BLOCK", "G BLOCK · ANURAG UNIVERSITY"], 28.66, 7.28, 14.5, 7.0, 0.74, "#f8fafc", "#1e293b", -Math.PI / 2);
  he(0x162230, 30.25, 2.2, 14.5, 0.24, 4.4, 5.6); // Sleek glass lobby doors
  for (let s = 0; s < 4; s++) {
    let sh = (4 - s) * 0.15;
    he(0x334155, 29.8 - s * 0.32, sh * 0.5, 14.5, 0.36, sh, 6.4); // Wide dark-granite entrance steps
  }
  // Terracotta potted plants flanking G-Block steps (wO 01:22)
  for (let pz of [11.0, 18.0]) {
    let pot = new et(new pn(0.28, 0.2, 0.38, 10), new Jt({ color: 0xa64b3a, roughness: 0.78 }));
    pot.position.set(28.85, 0.2, pz); Ht.add(pot);
    let foliage = new et(new fn(0.42, 8, 6), new Jt({ color: 0x2e6f28, roughness: 0.82 }));
    foliage.position.set(28.85, 0.58, pz); Ht.add(foliage);
  }

  // 3c. F-BLOCK: EXAMINATION BRANCH — Terracotta Lower Walls, Black Granite Stairs & Yellow Soffit (wO 01:32)
  he(0xb34a3a, 30.9, 2.2, -1.6, 0.65, 4.4, 3.2); // Warm terracotta-sandstone South lower wall
  he(0xb34a3a, 30.9, 2.2, -7.4, 0.65, 4.4, 3.2); // Warm terracotta-sandstone North lower wall
  he(0xf8fafc, 29.8, 5.2, -2.2, 0.68, 10.4, 0.68); // Tall white architectural pillar
  he(0xf8fafc, 29.8, 5.2, -6.8, 0.68, 10.4, 0.68);
  he(0xfacc15, 30.5, 6.85, -4.5, 2.4, 0.28, 5.4); // Iconic cantilevered yellow-soffit upper gallery!
  ys(["F BLOCK · EXAMINATION BRANCH"], 29.42, 7.65, -4.5, 5.6, 0.62, "#f8fafc", "#1e293b", -Math.PI / 2);
  for (let st = 0; st < 7; st++) {
    let sh = (st + 1) * 0.26;
    he(0x272c33, 29.3 + st * 0.28, sh * 0.5, -4.5, 0.3, sh, 2.8); // Bold exterior black-granite central staircase!
  }

  // 3d. E-BLOCK: ICONIC "TEDxAnuragU" ENTRANCE, OPEN-SKY ATRIUM & SPACE RESEARCH CENTER (wO 01:52!)
  he(0xf8fafc, 28.9, 3.8, -16.2, 0.72, 7.6, 0.72); // South portico column
  he(0xf8fafc, 28.9, 3.8, -22.8, 0.72, 7.6, 0.72); // North portico column
  he(0xf8fafc, 29.4, 7.55, -19.5, 2.2, 0.85, 7.6); // Portico crown beam
  ys(["E BLOCK · DEPT. OF ELECTRONICS & COMMUNICATION"], 28.26, 7.58, -19.5, 7.1, 0.58, "#f8fafc", "#1e293b", -Math.PI / 2);
  // Grand dark glass entrance + Iconic bold "TEDxAnuragU" horizontal beam sign on E-BLOCK!
  he(0x142230, 29.1, 2.2, -19.5, 0.25, 4.4, 5.8);
  (function() {
    const c = document.createElement("canvas"); c.width = 1024; c.height = 224;
    const g = c.getContext("2d");
    g.fillStyle = "#f1f5f9"; g.fillRect(0, 0, 1024, 224);
    g.fillStyle = "#e62b1e"; g.fillRect(0, 0, 1024, 12); g.fillRect(0, 212, 1024, 12);
    g.textBaseline = "middle";
    g.font = "900 124px 'Segoe UI',Arial,sans-serif";
    g.fillStyle = "#e62b1e"; g.fillText("TED", 86, 104);
    g.font = "900 84px 'Segoe UI',Arial,sans-serif";
    g.fillText("x", 338, 76);
    g.font = "800 110px 'Segoe UI',Arial,sans-serif";
    g.fillStyle = "#111827"; g.fillText("AnuragU", 402, 104);
    g.font = "600 28px 'Segoe UI',sans-serif";
    g.fillStyle = "#475569"; g.fillText("x = independently organized TED event  ·  E-BLOCK ATRIUM", 120, 182);
    const t = new dn(c); t.colorSpace = vt;
    const tedSign = new et(new _i(6.1, 1.34), new Jt({ map: t, roughness: 0.35 }));
    tedSign.rotation.y = -Math.PI / 2;
    tedSign.position.set(28.88, 4.88, -19.5);
    Ht.add(tedSign);
  })();
  // Satellite Design & Development Center for Space Research plaque on E-Block (17:37)
  ys(["SATELLITE DESIGN & DEVELOPMENT", "CENTER FOR SPACE RESEARCH"], 28.92, 2.3, -16.2, 2.1, 0.78, "#0f172a", "#38bdf8", -Math.PI / 2);

  // 3e. Covered Red-Roof Outdoor Campus Gazebo / Kiosk (South of G-Block, clear of 2-lane avenue!)
  const gx = 32.5, gz = 27.5;
  he(0x9e3b33, gx, 0.18, gz, 5.2, 0.36, 5.2); // Red-curbed stone terrace
  he(0xd6cfc0, gx, 0.38, gz, 4.6, 0.08, 4.6); // Concrete floor
  for (let [px, pz] of [[-2.0, -2.0], [2.0, -2.0], [-2.0, 2.0], [2.0, 2.0]]) {
    he(0xf1f5f9, gx + px, 1.75, gz + pz, 0.18, 2.75, 0.18);
  }
  const gazRoof = new et(new oa(3.85, 1.45, 4), new Jt({ color: 0xb53c32, roughness: 0.52, metalness: 0.2 }));
  gazRoof.rotation.y = Math.PI / 4;
  gazRoof.position.set(gx, 3.85, gz); gazRoof.castShadow = true; Ht.add(gazRoof);
  he(0x64748b, gx, 0.78, gz, 1.6, 0.12, 1.6); // Center table
  // Blue & Red Campus Info Display Panels beside Gazebo
  ys(["INNOVATION HUB", "ANURAG STARTUPS"], gx - 3.2, 1.55, gz + 0.5, 2.1, 1.25, "#1d4ed8", "#ffffff", -0.35);
  ys(["NAAC A+ ACCREDITED", "NIRF TOP RANKED"], gx - 3.2, 1.55, gz - 2.1, 2.1, 1.25, "#b91c1c", "#ffffff", 0.35);

  // --- 3f. 2026 VIDEO LANDMARKS: H-BLOCK SOLAR TREE, B-BLOCK PHARMACY, C-BLOCK COURT, CRICKET TRACK & AU BUSES ---
  // H-Block Vertical Warm-Wood Louvered Facade Screen (wO 03:52)
  for (let lz = -34.0; lz <= -25.6; lz += 0.48) {
    he(0xc69c6d, -68.15, 9.2, lz, 0.14, 5.2, 0.12);
  }
  // Iconic Green Solar-Panel Umbrella Charging Tree ("SOLAR TREE") + Red-Roof Juice Kiosk (wO 04:12, 04:22)
  const stX = -62.5, stZ = -41.5;
  he(0x475569, stX, 0.22, stZ, 0.9, 0.44, 0.9); // Concrete pedestal
  let stPole = new et(new pn(0.14, 0.16, 2.8, 12), new Jt({ color: 0x334155, roughness: 0.5, metalness: 0.6 }));
  stPole.position.set(stX, 1.6, stZ); Ht.add(stPole);
  let stCanopy = new et(new oa(2.35, 1.65, 6), new Jt({ color: 0x16a34a, roughness: 0.55 }));
  stCanopy.position.set(stX, 3.25, stZ); stCanopy.castShadow = true; Ht.add(stCanopy);
  // 4 Slanted Dark-Blue Photovoltaic Solar Panels mounted onto the green umbrella!
  const pvMat = new Jt({ color: 0x1e3a8a, roughness: 0.2, metalness: 0.65 });
  for (let a = 0; a < 4; a++) {
    let ang = a * Math.PI / 2 + Math.PI / 4;
    let pv = new et(new Ni(1.15, 0.08, 0.85), pvMat);
    pv.position.set(stX + Math.sin(ang) * 1.15, 3.15, stZ + Math.cos(ang) * 1.15);
    pv.rotation.y = ang; pv.rotation.x = 0.58;
    Ht.add(pv);
    let pvFrame = new et(new Ni(1.22, 0.05, 0.92), new Jt({ color: 0xe2e8f0, metalness: 0.7, roughness: 0.3 }));
    pvFrame.position.set(stX + Math.sin(ang) * 1.12, 3.12, stZ + Math.cos(ang) * 1.12);
    pvFrame.rotation.y = ang; pvFrame.rotation.x = 0.58;
    Ht.add(pvFrame);
  }
  // Red-Roofed Outdoor Snack/Juice Kiosk beside Solar Tree (wO 04:12)
  he(0xe2e8f0, stX - 5.2, 1.35, stZ, 3.2, 2.7, 2.8);
  he(0xb91c1c, stX - 5.2, 2.2, stZ + 1.44, 3.25, 0.65, 0.14);
  let kRoof = new et(new oa(2.85, 1.1, 4), new Jt({ color: 0xdc2626, roughness: 0.48 }));
  kRoof.rotation.y = Math.PI / 4; kRoof.position.set(stX - 5.2, 3.25, stZ); Ht.add(kRoof);
  ys(["CAMPUS JUICE & SNACKS"], stX - 5.2, 2.25, stZ + 1.54, 2.8, 0.42, "#b91c1c", "#fde047", 0);

  // B-Block School of Pharmacy Teak-Wood Glass Lobby + Crimson Sign (wO 07:52, 08:02)
  he(0x7c4a26, -51, 2.0, 13.45, 7.6, 3.6, 0.25); // Warm teak window mullions
  he(0x1e293b, -51, 1.95, 13.38, 7.2, 3.3, 0.12); // Dark glass lobby
  ys(["ANURAG UNIVERSITY", "SCHOOL OF PHARMACY"], -51, 3.95, 13.62, 4.6, 0.88, "#be123c", "#ffffff", 0);
  for (let s = 0; s < 3; s++) {
    let sh = (3 - s) * 0.14;
    he(0x1f2937, -51, sh * 0.5, 14.0 + s * 0.35, 8.2, sh, 0.38);
  }

  // C-Block Front Basketball Court (x = -45.5, z = 52.0, 9.8m x 15.2m — wO 06:52, 07:02, 07:12!)
  (function() {
    const cx = -45.5, cz = 52.0, cw = 9.8, cd = 15.2;
    // 1. Crisp High-Res Painted Basketball Court Surface (Center AU Logo, 3-Point Arcs, Keys & Yellow Free-Throw Circles!)
    const c = document.createElement("canvas"); c.width = 512; c.height = 768;
    const g = c.getContext("2d");
    g.fillStyle = "#1565a8"; g.fillRect(0, 0, 512, 768);
    // Subtle weathered court concrete texture
    g.fillStyle = "rgba(255,255,255,0.035)";
    for (let i = 0; i < 600; i++) g.fillRect((i * 83) % 512, (i * 127) % 768, 12, 4);
    // Outer white boundary & center half-court line
    g.strokeStyle = "#ffffff"; g.lineWidth = 8;
    g.strokeRect(18, 18, 476, 732);
    g.beginPath(); g.moveTo(18, 384); g.lineTo(494, 384); g.stroke();
    // Center circle with crisp AU logo (matching wO 07:02 & 07:12!)
    g.fillStyle = "#f1f5f9";
    g.beginPath(); g.arc(256, 384, 62, 0, Math.PI * 2); g.fill();
    g.strokeStyle = "#e11d48"; g.lineWidth = 6; g.stroke();
    g.fillStyle = "#1e3a8a"; g.font = "900 54px 'Segoe UI',sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
    g.fillText("AU", 256, 386);
    // Both ends: Paint Key, Golden-Yellow Free-Throw Semicircle & 3-Point Arc!
    for (let end of [0, 1]) {
      const yBase = end === 0 ? 18 : 750;
      const dir = end === 0 ? 1 : -1;
      // Red/terracotta paint key
      g.fillStyle = "#b91c1c";
      g.fillRect(184, end === 0 ? 18 : 750 - 152, 144, 152);
      g.strokeStyle = "#ffffff"; g.lineWidth = 6;
      g.strokeRect(184, end === 0 ? 18 : 750 - 152, 144, 152);
      // Iconic golden-yellow free-throw semicircle (wO 07:02!)
      g.fillStyle = "#eab308";
      g.beginPath();
      g.arc(256, yBase + dir * 152, 54, end === 0 ? 0 : Math.PI, end === 0 ? Math.PI : Math.PI * 2);
      g.fill(); g.stroke();
      // White 3-point arc
      g.beginPath();
      g.arc(256, yBase + dir * 48, 192, end === 0 ? 0.14 * Math.PI : 1.14 * Math.PI, end === 0 ? 0.86 * Math.PI : 1.86 * Math.PI);
      g.stroke();
    }
    const courtTex = new dn(c); courtTex.colorSpace = vt;
    const courtMesh = new et(new _i(cw, cd), new Jt({ map: courtTex, roughness: 0.72 }));
    courtMesh.rotation.x = -Math.PI / 2;
    courtMesh.position.set(cx, 0.242, cz);
    courtMesh.receiveShadow = true;
    Ht.add(courtMesh);

    // 2. Two Detailed Blue Steel Curved-Neck Basketball Hoops (North z = 43.8 & South z = 60.2, facing inward!)
    const poleBlue = new Jt({ color: 0x1d4ed8, roughness: 0.35, metalness: 0.65 });
    const rimOrange = new Jt({ color: 0xea580c, roughness: 0.35, metalness: 0.55 });
    const glassBackMat = new Jt({ color: 0xe2f4ff, transparent: true, opacity: 0.52, roughness: 0.08, metalness: 0.35 });
    const netWhite = new Jt({ color: 0xf8fafc, roughness: 0.85, wireframe: true });
    for (let dir of [-1, 1]) {
      const hz = cz + dir * 8.15; // Just behind each baseline on the red apron
      // Heavy blue steel upright post + black safety padding
      let post = new et(new pn(0.11, 0.13, 3.65, 12), poleBlue);
      post.position.set(cx, 1.85, hz); post.castShadow = true; Ht.add(post);
      let pad = new et(new pn(0.16, 0.16, 1.6, 10), new Jt({ color: 0x111827, roughness: 0.85 }));
      pad.position.set(cx, 1.05, hz); Ht.add(pad);
      // Overhead boom arm extending inward over the baseline
      let boom = new et(new Ni(0.14, 0.14, 1.45), poleBlue);
      boom.position.set(cx, 3.55, hz - dir * 0.68); Ht.add(boom);
      // Tempered glass backboard + crisp white perimeter frame & orange shooter's square
      const bz = hz - dir * 1.38;
      let board = new et(new Ni(1.85, 1.12, 0.07), glassBackMat);
      board.position.set(cx, 3.45, bz); Ht.add(board);
      he(0xffffff, cx, 4.02, bz, 1.9, 0.06, 0.09);
      he(0xffffff, cx, 2.88, bz, 1.9, 0.06, 0.09);
      he(0xffffff, cx - 0.92, 3.45, bz, 0.06, 1.16, 0.09);
      he(0xffffff, cx + 0.92, 3.45, bz, 0.06, 1.16, 0.09);
      he(0xea580c, cx, 3.22, bz - dir * 0.04, 0.56, 0.42, 0.02);
      // Bright orange steel basketball rim + hanging white net!
      const rz = bz - dir * 0.34;
      let rim = new et(new gn(0.24, 0.025, 8, 18), rimOrange);
      rim.rotation.x = Math.PI / 2; rim.position.set(cx, 3.05, rz); Ht.add(rim);
      let net = new et(new pn(0.23, 0.14, 0.44, 12, 3, true), netWhite);
      net.position.set(cx, 2.82, rz); Ht.add(net);
    }

    // 3. Orange Basketball resting near center court
    let bball = new et(new fn(0.15, 12, 10), new Jt({ color: 0xea580c, roughness: 0.65 }));
    bball.position.set(cx + 0.8, 0.39, cz + 0.5); bball.castShadow = true; Ht.add(bball);

    // 4. Stepped Concrete Viewing Gallery + Mosaic "ANURAG UNIVERSITY" Wall cleanly BEHIND South baseline (z = 63.4)
    for (let st = 0; st < 3; st++) {
      he(0xcbd5e1, cx, 0.16 + st * 0.22, 61.6 + st * 0.48, 12.6, 0.24, 0.48);
    }
    he(0xd6d1c4, cx, 1.45, 63.4, 12.2, 2.6, 0.5);
    ys(["ANURAG UNIVERSITY", "BASKETBALL & SPORTS PLAZA"], cx, 1.6, 63.1, 9.2, 1.55, "#e7e2d4", "#1e293b", Math.PI);

    // 5. Iconic Colorful Orange/Blue/Red/Yellow Architectural Pillars cleanly along the EAST sideline (x = -37.2, off the court!)
    [0xf97316, 0x2563eb, 0xdc2626, 0xeab308].forEach((col, i) => {
      he(col, -37.2, 1.85, 45.8 + i * 4.1, 0.62, 3.7, 0.62);
    });
  })();

  // Cricket Stadium Wide Red-Clay Circular Athletics Running Track (nK 01:08 aerial!)
  const trackRing = new et(new xa(27.2, 33.5, 48), new Jt({ color: 0xb85d38, roughness: 0.92, side: Gt }));
  trackRing.rotation.x = -Math.PI / 2;
  trackRing.position.set(44, 0.08, -76);
  Ht.add(trackRing);

  // 3 Bright Yellow Anurag University Fleet Buses with Crimson Side Wrap (wO 09:42, 10:02, r5V 05:12)
  const busYelMat = new Jt({ color: 0xfacc15, roughness: 0.38, metalness: 0.18 });
  const busGlassMat = new Jt({ color: 0x0f172a, roughness: 0.15, metalness: 0.5 });
  const busTireMat = new Jt({ color: 0x17191c, roughness: 0.9 });
  for (let bi = 0; bi < 3; bi++) {
    let bx = -76 + bi * 5.2, bz = -68;
    let body = new et(new Ni(2.55, 2.75, 9.8), busYelMat); body.position.set(bx, 1.82, bz); body.castShadow = true; Ht.add(body);
    let win = new et(new Ni(2.62, 0.92, 8.9), busGlassMat); win.position.set(bx, 2.38, bz); Ht.add(win);
    ys(["ANURAG UNIVERSITY", "BE EVERYONE YOU DREAM TO BE"], bx + 1.31, 1.25, bz, 6.8, 0.82, "#991b1b", "#ffffff", Math.PI / 2);
    ys(["ANURAG UNIVERSITY", "BE EVERYONE YOU DREAM TO BE"], bx - 1.31, 1.25, bz, 6.8, 0.82, "#991b1b", "#ffffff", -Math.PI / 2);
    for (let wz of [-3.0, 3.0]) {
      for (let wx of [-1.22, 1.22]) {
        let wh = new et(new pn(0.48, 0.48, 0.34, 14), busTireMat);
        wh.rotation.z = Math.PI / 2; wh.position.set(bx + wx, 0.48, bz + wz); Ht.add(wh);
      }
    }
  }

  // --- 4. PHARMACY MEDICINAL GARDEN (09:21 - 09:29) ---
  // Positioned cleanly in the green pocket north-east of D-Block & south-east of H-Block (x = -33.5, z = -31.5)
  const mgX = -33.5, mgZ = -31.5;
  // Iconic Royal-Blue Archway Signboard: "ANURAG SCHOOL OF PHARMACY — MEDICINAL GARDEN"
  he(0x1e3a8a, mgX - 2.2, 1.85, mgZ + 5.2, 0.18, 3.7, 0.18);
  he(0x1e3a8a, mgX + 2.2, 1.85, mgZ + 5.2, 0.18, 3.7, 0.18);
  (function() {
    const c = document.createElement("canvas"); c.width = 768; c.height = 192;
    const g = c.getContext("2d");
    g.fillStyle = "#1d4ed8"; g.fillRect(0, 0, 768, 192);
    g.strokeStyle = "#ffffff"; g.lineWidth = 8; g.strokeRect(8, 8, 752, 176);
    // White Mortar & Pestle Pharmacy Emblem on Left
    g.fillStyle = "#ffffff";
    g.beginPath(); g.arc(82, 108, 34, 0, Math.PI); g.fill();
    g.fillRect(58, 138, 48, 10);
    g.lineWidth = 10; g.lineCap = "round";
    g.beginPath(); g.moveTo(88, 98); g.lineTo(114, 58); g.stroke();
    g.textAlign = "center";
    g.fillStyle = "#fde047"; g.font = "800 32px 'Segoe UI',sans-serif";
    g.fillText("ANURAG SCHOOL OF PHARMACY", 435, 76);
    g.fillStyle = "#ffffff"; g.font = "900 46px 'Segoe UI',sans-serif";
    g.fillText("MEDICINAL GARDEN", 435, 142);
    const t = new dn(c); t.colorSpace = vt;
    const archF = new et(new _i(4.7, 1.18), new Jt({ map: t, roughness: 0.4 }));
    archF.position.set(mgX, 3.15, mgZ + 5.32); Ht.add(archF);
    const archB = new et(new _i(4.7, 1.18), new Jt({ map: t, roughness: 0.4 }));
    archB.rotation.y = Math.PI; archB.position.set(mgX, 3.15, mgZ + 5.08); Ht.add(archB);
  })();
  // Red-soil raised garden beds, stone stepping slabs & lush medicinal herb rows
  he(0x8d452c, mgX, 0.12, mgZ, 10.4, 0.24, 9.8); // Red soil bed
  for (let sz = mgZ - 4.0; sz <= mgZ + 4.2; sz += 1.35) {
    he(0xcbd5e1, mgX, 0.26, sz, 1.35, 0.08, 0.72); // Stone stepping slabs
  }
  const herbColors = [0x15803d, 0x4d7c0f, 0x16a34a, 0x2f855a];
  for (let side of [-1, 1]) {
    for (let hz = mgZ - 3.6; hz <= mgZ + 3.6; hz += 1.8) {
      let hx = mgX + side * 2.8;
      he(0x78350f, hx, 0.28, hz, 3.2, 0.2, 1.15);
      for (let ox of [-0.9, 0, 0.9]) {
        let herb = new et(new fn(0.42, 7, 6), new Jt({ color: herbColors[Math.abs(Math.round(hz + ox)) % 4], roughness: 0.85 }));
        herb.scale.set(1.1, 0.75, 1.1); herb.position.set(hx + ox, 0.58, hz); Ht.add(herb);
      }
      // Mini white botanical label stake
      he(0xf8fafc, hx - side * 1.45, 0.55, hz, 0.08, 0.45, 0.26);
    }
  }
  // Low green iron perimeter fence posts around the garden
  for (let fx = mgX - 5.2; fx <= mgX + 5.2; fx += 2.6) {
    he(0x166534, fx, 0.6, mgZ - 4.9, 0.08, 1.2, 0.08);
    if (Math.abs(fx - mgX) > 2.0) he(0x166534, fx, 0.6, mgZ + 4.9, 0.08, 1.2, 0.08);
  }
  he(0x166534, mgX, 1.05, mgZ - 4.9, 10.4, 0.06, 0.06);

  // --- 5. CRICKET GROUND IRON GATE, THATCHED PITCH ROLLER SHED & TOWER CRANE (11:45 - 13:53) ---
  // 5a. Wide Black Wrought-Iron Double Entrance Gate between White Pillars (11:45)
  const cgX = 24.5, cgZ = -55.5;
  he(0xf8fafc, cgX - 3.4, 1.45, cgZ, 0.78, 2.9, 0.78);
  he(0xf8fafc, cgX + 3.4, 1.45, cgZ, 0.78, 2.9, 0.78);
  he(0xcbd5e1, cgX - 3.4, 2.96, cgZ, 0.96, 0.16, 0.96);
  he(0xcbd5e1, cgX + 3.4, 2.96, cgZ, 0.96, 0.16, 0.96);
  // Open wrought-iron gate leaves angled welcomingly inward
  for (let s of [-1, 1]) {
    let lx = cgX + s * 2.5;
    he(0x1e293b, lx, 1.15, cgZ - 0.95, 0.1, 2.1, 2.1, s * 0.45);
  }
  // 5b. Thatched-Roof Pitch Roller Shed + Green & Blue Cricket Pitch Roller (12:01, 12:09)
  const rsX = 28.5, rsZ = -62.5;
  for (let [px, pz] of [[-2.1, -1.5], [2.1, -1.5], [-2.1, 1.5], [2.1, 1.5]]) {
    let post = new et(new pn(0.09, 0.1, 2.9, 8), new Jt({ color: 0x6b4423, roughness: 0.9 }));
    post.position.set(rsX + px, 1.45, rsZ + pz); Ht.add(post);
  }
  // Golden-brown pitched thatch canopy roof
  const thatchMat = new Jt({ color: 0xa67c37, roughness: 0.95 });
  const thatchL = new et(new Ni(5.0, 0.24, 2.35), thatchMat);
  thatchL.position.set(rsX, 3.25, rsZ - 0.95); thatchL.rotation.x = -0.34; Ht.add(thatchL);
  const thatchR = new et(new Ni(5.0, 0.24, 2.35), thatchMat);
  thatchR.position.set(rsX, 3.25, rsZ + 0.95); thatchR.rotation.x = 0.34; Ht.add(thatchR);
  // Heavy Blue Steel Drum + Green Tractor Engine Cricket Pitch Roller parked inside!
  const drum = new et(new pn(0.62, 0.62, 1.55, 18), new Jt({ color: 0x1d4ed8, roughness: 0.45, metalness: 0.55 }));
  drum.rotation.x = Math.PI / 2; drum.position.set(rsX + 0.85, 0.64, rsZ); Ht.add(drum);
  const rearDrum = new et(new pn(0.52, 0.52, 1.35, 16), new Jt({ color: 0x1e3a8a, roughness: 0.48, metalness: 0.5 }));
  rearDrum.rotation.x = Math.PI / 2; rearDrum.position.set(rsX - 1.15, 0.54, rsZ); Ht.add(rearDrum);
  he(0x16a34a, rsX - 0.15, 1.25, rsZ, 1.85, 0.78, 1.05); // Bright green engine hood
  he(0x111827, rsX - 1.15, 1.45, rsZ, 0.55, 0.55, 0.62); // Operator seat
  he(0x334155, rsX - 0.72, 1.78, rsZ, 0.08, 0.55, 0.08); // Steering column

  // 5c. Tall Yellow-Steel Lattice Tower Crane beside 10-Story Expansion Mega Block (13:53)
  const crX = 63.5, crZ = -12.5;
  he(0x64748b, crX, 0.6, crZ, 3.6, 1.2, 3.6); // Concrete crane base
  const craneYel = new Jt({ color: 0xeab308, roughness: 0.48, metalness: 0.45 });
  for (let [ox, oz] of [[-0.65, -0.65], [0.65, -0.65], [-0.65, 0.65], [0.65, 0.65]]) {
    let leg = new et(new Ni(0.16, 36.0, 0.16), craneYel);
    leg.position.set(crX + ox, 19.0, crZ + oz); Ht.add(leg);
  }
  for (let cy = 3.5; cy <= 35.5; cy += 3.2) {
    he(0xeab308, crX, cy, crZ, 1.42, 0.14, 1.42);
  }
  // Crane Operator Cabin + Horizontal Jib Arm + Counterweight + Hanging Cable
  he(0xf8fafc, crX + 1.1, 35.8, crZ, 1.6, 2.1, 1.5);
  he(0x1e293b, crX + 1.85, 36.0, crZ, 0.14, 1.1, 1.2); // Cab window
  he(0xeab308, crX + 12.0, 37.4, crZ, 34.0, 1.15, 1.15); // Long horizontal jib reaching over Mega Block
  he(0x475569, crX - 5.2, 37.2, crZ, 3.4, 1.65, 1.45); // Concrete counterweight blocks
  he(0x1e293b, crX + 21.0, 29.5, crZ, 0.08, 15.0, 0.08); // Hanging hoist cable
  he(0xef4444, crX + 21.0, 21.8, crZ, 0.65, 0.65, 0.35); // Red crane hook block

  // --- 6. WEST GROUND PROPS, BASKETBALL PILLARS & TRANSMISSION PYLON (02:25 - 04:09) ---
  // 6a. Red & White Placement Road Standee ("BE EVERYONE YOU DREAM TO BE · 52 LPA", 03:45)
  he(0xf8fafc, -52.5, 1.15, 25.4, 4.4, 1.55, 0.22);
  ys(["BE EVERYONE YOU DREAM TO BE", "1800+ OFFERS · 52 LPA HIGHEST"], -52.5, 1.25, 25.54, 4.1, 1.28, "#b91c1c", "#ffffff", 0);
  ys(["BE EVERYONE YOU DREAM TO BE", "1800+ OFFERS · 52 LPA HIGHEST"], -52.5, 1.25, 25.26, 4.1, 1.28, "#b91c1c", "#ffffff", Math.PI);

  // 6b. Bright Orange/Blue Architectural Pillars lining Basketball Court (02:25, 02:33)
  const bPillars = [0xf97316, 0x2563eb, 0xe2d8c5, 0xf97316, 0x2563eb];
  bPillars.forEach((col, i) => {
    he(col, 83.2, 1.65, -109 + i * 5.5, 0.72, 3.3, 0.72);
  });

  // 6c. Black Fitness Tractor Tires on West Red-Dirt Sports Ground (03:13)
  const tireMat = new Jt({ color: 0x17191c, roughness: 0.92 });
  for (let [tx, tz] of [[-86.5, 23.0], [-84.2, 23.0], [-81.9, 23.0], [-85.3, 25.4]]) {
    let tire = new et(new gn(0.58, 0.24, 10, 18), tireMat);
    tire.rotation.x = Math.PI / 2; tire.position.set(tx, 0.24, tz); Ht.add(tire);
  }

  // 6d. Tall Lattice High-Voltage Steel Transmission Pylon on Far-West Horizon (04:01, 04:09)
  const pyX = -124, pyZ = 44;
  const pylonMat = new Jt({ color: 0x64748b, roughness: 0.55, metalness: 0.65 });
  for (let [ox, oz] of [[-1.6, -1.6], [1.6, -1.6], [-1.6, 1.6], [1.6, 1.6]]) {
    let leg = new et(new pn(0.12, 0.22, 34, 6), pylonMat);
    leg.position.set(pyX + ox * 0.55, 17, pyZ + oz * 0.55);
    leg.rotation.z = ox > 0 ? 0.045 : -0.045;
    leg.rotation.x = oz > 0 ? -0.045 : 0.045;
    Ht.add(leg);
  }
  for (let cy of [20, 26, 31.5]) {
    let w = cy > 30 ? 8.5 : 11.5;
    he(0x64748b, pyX, cy, pyZ, w, 0.35, 0.45);
    he(0x94a3b8, pyX - w * 0.46, cy - 0.65, pyZ, 0.16, 1.1, 0.16);
    he(0x94a3b8, pyX + w * 0.46, cy - 0.65, pyZ, 0.16, 1.1, 0.16);
  }
})();
'''

html = html.replace(
    '// ============================================================================\n// BUILDING 9:',
    VIDEO_CAMPUS_UPGRADE_JS + '\n// ============================================================================\n// BUILDING 9:',
    1
)
if VIDEO_CAMPUS_UPGRADE_JS not in html:
    html = html.replace(
        '// ============================================================================\r\n// BUILDING 9:',
        VIDEO_CAMPUS_UPGRADE_JS + '\r\n// ============================================================================\r\n// BUILDING 9:',
        1
    )

# Add quick-teleport stops for the newly detailed video-tour landmarks!
html = html.replace(
    '["A-Block & B/D-Block Palm Pathway", -31.2, 13.5, 0.0, 0.06, 0],',
    '["A-Block & B/D-Block Palm Pathway", -31.2, 13.5, 0.0, 0.06, 0],\n  ["A-Block Courtyard Amphitheater Stage", -3.0, 2.5, 0.0, 0.08, 0],\n  ["E-Block · TEDxAnuragU & 2-Lane Avenue", 20.8, -19.5, -Math.PI / 2, 0.10, 0],\n  ["G-Block · Central Admin & 2-Lane Avenue", 20.8, 14.5, -Math.PI / 2, 0.09, 0],\n  ["H-Block · Solar Tree & Bus Yard", -54.5, -44.5, 0.65, 0.06, 0],\n  ["Pharmacy Medicinal Garden", -33.5, -22.5, 0.0, 0.06, 0],\n  ["Cricket Gate & Pitch Roller Shed", 24.5, -48.5, 0.0, 0.06, 0],',
    1
)

# 7q. NEXT-GEN 6-LAYER PHOTOREALISTIC GLSL SHADER SUITE
# 1. Procedural HDR-Style Equirectangular IBL Environment Reflections (Ht.environment -> Realistic Reflective Windows & Metals!)
# 2. Global PBR GLSL Injection (onBeforeCompile): Ground Contact AO + World-Space Micro-Grain + Warm Sun Rim & Road Sheen!
# 3. 3D-Lit Volumetric Cumulus Sky Dome Shader (Beer-Lambert Cloud Lighting + Rayleigh/Mie Sun Corona + Dusk Stars!)
# 4. Gerstner-Wave Fresnel Lake Water Shader with Underwater Caustics & Sun Sparkles!
# 5. Volumetric 3D Sun God-Rays / Light-Shafts Shader (Additive Fresnel-Faded Sunbeams!)
# 6. Dynamic High-Res Soft Shadows + Filmic ACES Color Grading synced to all Time-of-Day presets!
REALISTIC_SHADERS_JS = r'''
// ============================================================================
// NEXT-GEN 6-LAYER PHOTOREALISTIC GLSL SHADER SUITE (PC + META QUEST 3 VR)
// ============================================================================
(function() {
  // --- LAYER 1: PROCEDURAL HDR-STYLE EQUIRECTANGULAR IBL ENVIRONMENT REFLECTION MAP ---
  const envCanvas = document.createElement("canvas");
  envCanvas.width = 512; envCanvas.height = 256;
  const envCtx = envCanvas.getContext("2d");
  const envTex = new dn(envCanvas);
  envTex.colorSpace = vt;
  envTex.mapping = 303; // THREE.EquirectangularReflectionMapping

  function redrawIBL(zenith, horizon, ground, sunHex, sunX, sunY) {
    const g = envCtx;
    const grad = g.createLinearGradient(0, 0, 0, 256);
    grad.addColorStop(0.0, zenith);
    grad.addColorStop(0.46, horizon);
    grad.addColorStop(0.51, "#e6edf5");
    grad.addColorStop(0.56, ground);
    grad.addColorStop(1.0, "#1d261a");
    g.fillStyle = grad; g.fillRect(0, 0, 512, 256);
    // Soft bright cloud streaks in upper hemisphere for realistic glass reflections!
    g.fillStyle = "rgba(255,255,255,0.22)";
    for (let i = 0; i < 18; i++) {
      g.beginPath();
      g.ellipse((i * 71) % 512, 34 + (i * 23) % 72, 38 + (i % 4) * 14, 7 + (i % 3) * 4, 0, 0, Math.PI * 2);
      g.fill();
    }
    // Blazing solar reflection hotspot
    const sg = g.createRadialGradient(sunX, sunY, 2, sunX, sunY, 54);
    sg.addColorStop(0, "#ffffff");
    sg.addColorStop(0.22, sunHex);
    sg.addColorStop(1, "rgba(255,255,255,0)");
    g.fillStyle = sg; g.fillRect(0, 0, 512, 160);
    envTex.needsUpdate = true;
  }
  redrawIBL("#1652a8", "#b4dcf8", "#4d6142", "rgba(255,244,210,0.85)", 148, 56);
  Ht.environment = envTex;
  if ("environmentIntensity" in Ht) Ht.environmentIntensity = 1.15;

  // --- LAYER 2: 3D-LIT VOLUMETRIC CUMULUS SKY DOME SHADER (BEER-LAMBERT + RAYLEIGH/MIE + STARS) ---
  const skyUniforms = {
    uTime: { value: 0 },
    uSunDir: { value: new A(-0.45, 0.72, 0.42).normalize() },
    uZenithCol: { value: new Pe(0x1652a8) },
    uHorizonCol: { value: new Pe(0xb4dcf8) },
    uSunCol: { value: new Pe(0xfff6dc) },
    uCloudTopCol: { value: new Pe(0xffffff) },
    uCloudBotCol: { value: new Pe(0x88a2bd) },
    uCloudDensity: { value: 0.54 },
    uStarAlpha: { value: 0.0 }
  };

  const skyMat = new Rt({
    side: 1, // THREE.BackSide
    depthWrite: false,
    fog: false,
    uniforms: skyUniforms,
    vertexShader: `
      varying vec3 vWorldDir;
      void main() {
        vec4 wp = modelMatrix * vec4(position, 1.0);
        vWorldDir = normalize(position);
        gl_Position = projectionMatrix * viewMatrix * wp;
      }
    `,
    fragmentShader: `
      uniform float uTime;
      uniform vec3 uSunDir;
      uniform vec3 uZenithCol;
      uniform vec3 uHorizonCol;
      uniform vec3 uSunCol;
      uniform vec3 uCloudTopCol;
      uniform vec3 uCloudBotCol;
      uniform float uCloudDensity;
      uniform float uStarAlpha;
      varying vec3 vWorldDir;

      float hash21(vec2 p) {
        p = fract(p * vec2(127.1, 311.7));
        p += dot(p, p + 34.53);
        return fract(p.x * p.y);
      }
      float noise2(vec2 p) {
        vec2 i = floor(p), f = fract(p);
        f = f * f * (3.0 - 2.0 * f);
        return mix(
          mix(hash21(i), hash21(i + vec2(1.0, 0.0)), f.x),
          mix(hash21(i + vec2(0.0, 1.0)), hash21(i + vec2(1.0, 1.0)), f.x),
          f.y
        );
      }
      float fbm(vec2 p) {
        float v = 0.0, a = 0.5;
        mat2 rot = mat2(0.8, 0.6, -0.6, 0.8);
        for (int i = 0; i < 5; i++) {
          v += a * noise2(p);
          p = rot * p * 2.05 + vec2(19.3, 41.7);
          a *= 0.5;
        }
        return v;
      }

      void main() {
        vec3 dir = normalize(vWorldDir);
        vec3 sDir = normalize(uSunDir);
        float h = clamp(dir.y, 0.0, 1.0);
        // Physical Rayleigh horizon-to-zenith atmospheric scattering
        vec3 sky = mix(uHorizonCol, uZenithCol, pow(h, 0.48));
        // Warm Mie forward-scattering halo + crisp glowing solar disc
        float sunDot = max(dot(dir, sDir), 0.0);
        sky += uSunCol * (pow(sunDot, 5.0) * 0.22 + pow(sunDot, 42.0) * 0.48 + pow(sunDot, 320.0) * 1.15);
        sky += uSunCol * smoothstep(0.9988, 0.9997, sunDot) * 2.2;

        // Twinkling high-altitude starfield during Outbreak Dusk
        if (uStarAlpha > 0.01 && dir.y > 0.06) {
          vec2 stUV = floor(dir.xz / (dir.y + 0.2) * 160.0);
          float star = smoothstep(0.994, 0.999, hash21(stUV));
          float twinkle = 0.65 + 0.35 * sin(uTime * 3.0 + hash21(stUV + 9.0) * 20.0);
          sky += vec3(0.95, 0.97, 1.0) * star * twinkle * uStarAlpha * smoothstep(0.06, 0.3, dir.y);
        }

        // 3D-Lit Volumetric Cumulus Clouds with Beer-Lambert Silver-Lining!
        if (dir.y > 0.02) {
          vec2 uv = dir.xz / (dir.y + 0.16) * 1.32 + vec2(uTime * 0.011, uTime * 0.0045);
          float d1 = fbm(uv);
          float d2 = fbm(uv + sDir.xz * 0.09); // Sample offset toward sun for self-shadowing!
          float cloudMask = smoothstep(0.45, 0.78, d1) * smoothstep(0.02, 0.20, dir.y) * uCloudDensity;
          float selfLit = clamp((d1 - d2) * 2.8 + 0.55, 0.0, 1.0);
          vec3 cloudCol = mix(uCloudBotCol, uCloudTopCol, selfLit);
          // Bright silver-gold rim lining near the sun
          cloudCol += uSunCol * pow(sunDot, 6.0) * (1.0 - d1 * 0.55) * 0.45;
          sky = mix(sky, cloudCol, clamp(cloudMask, 0.0, 0.92));
        }
        if (dir.y < 0.0) {
          sky = mix(uHorizonCol * 0.84, uHorizonCol * 0.55, clamp(-dir.y * 4.5, 0.0, 1.0));
        }
        gl_FragColor = vec4(sky, 1.0);
      }
    `
  });
  const skyDome = new et(new fn(480, 36, 22), skyMat);
  skyDome.frustumCulled = false;
  skyDome.renderOrder = -10;
  Ht.add(skyDome);

  // --- LAYER 3: GERSTNER-WAVE FRESNEL WATER SHADER WITH CAUSTICS & SUN GLINTS ---
  const waterUniforms = {
    uTime: { value: 0 },
    uSunDir: { value: skyUniforms.uSunDir.value },
    uSunCol: { value: skyUniforms.uSunCol.value },
    uSkyCol: { value: skyUniforms.uHorizonCol.value },
    uDeepCol: { value: new Pe(0x072c40) },
    uShallowCol: { value: new Pe(0x16788e) }
  };
  const realisticWaterMat = new Rt({
    transparent: true,
    uniforms: waterUniforms,
    vertexShader: `
      uniform float uTime;
      varying vec3 vWorldPos;
      void main() {
        vec4 wp = modelMatrix * vec4(position, 1.0);
        // Gentle real-time Gerstner vertical swell
        wp.y += sin(wp.x * 0.45 + uTime * 1.4) * 0.03 + cos(wp.z * 0.52 - uTime * 1.15) * 0.025;
        vWorldPos = wp.xyz;
        gl_Position = projectionMatrix * viewMatrix * wp;
      }
    `,
    fragmentShader: `
      uniform float uTime;
      uniform vec3 uSunDir;
      uniform vec3 uSunCol;
      uniform vec3 uSkyCol;
      uniform vec3 uDeepCol;
      uniform vec3 uShallowCol;
      varying vec3 vWorldPos;

      float caustic(vec2 uv, float t) {
        float c1 = sin(uv.x * 3.1 + t * 1.4 + sin(uv.y * 2.6 - t * 1.1));
        float c2 = cos(uv.y * 3.4 - t * 1.3 + cos(uv.x * 2.9 + t * 1.6));
        return pow(clamp(0.5 + 0.5 * (c1 * c2), 0.0, 1.0), 4.0);
      }

      void main() {
        vec2 p = vWorldPos.xz * 0.42;
        float w1 = sin(p.x * 1.9 + uTime * 1.45) * cos(p.y * 1.6 - uTime * 1.2);
        float w2 = sin((p.x * 1.3 + p.y * 1.1) * 2.8 - uTime * 2.1) * 0.55;
        float w3 = cos((p.x * 0.9 - p.y * 2.5) + uTime * 1.75) * 0.4;
        vec3 N = normalize(vec3((w1 + w2) * 0.095, 1.0, (w2 - w3) * 0.095));
        vec3 V = normalize(cameraPosition - vWorldPos);
        vec3 L = normalize(uSunDir);

        float fresnel = 0.05 + 0.95 * pow(1.0 - max(dot(N, V), 0.0), 4.2);
        vec3 base = mix(uDeepCol, uShallowCol, 0.38 + 0.26 * w1);
        // Shimmering underwater caustic lattice
        base += vec3(0.18, 0.45, 0.52) * caustic(p * 0.85, uTime) * 0.42;
        vec3 col = mix(base, uSkyCol * 1.05, clamp(fresnel * 0.88, 0.0, 0.92));
        // Sharp specular sun glints + broader sparkle
        vec3 H = normalize(L + V);
        float specSharp = pow(max(dot(N, H), 0.0), 220.0) * 2.2;
        float specSoft = pow(max(dot(N, H), 0.0), 32.0) * 0.35;
        col += uSunCol * (specSharp + specSoft);
        gl_FragColor = vec4(col, 0.93);
      }
    `
  });
  if (typeof lakeGeo !== "undefined") {
    const realisticLake = new et(lakeGeo, realisticWaterMat);
    realisticLake.position.y = 0.04;
    Ht.add(realisticLake);
  }

  // --- LAYER 4: VOLUMETRIC 3D SUN GOD-RAYS / LIGHT-SHAFTS SHADER ---
  const rayUniforms = {
    uTime: { value: 0 },
    uRayCol: { value: new Pe(0xfff2cc) },
    uRayOpacity: { value: 0.14 }
  };
  const godRayMat = new Rt({
    transparent: true,
    depthWrite: false,
    side: Gt,
    blending: 2, // THREE.AdditiveBlending
    uniforms: rayUniforms,
    vertexShader: `
      varying vec2 vUv;
      varying vec3 vNormalV;
      varying vec3 vViewDir;
      void main() {
        vUv = uv;
        vec4 mvPos = modelViewMatrix * vec4(position, 1.0);
        vNormalV = normalize(normalMatrix * normal);
        vViewDir = normalize(-mvPos.xyz);
        gl_Position = projectionMatrix * mvPos;
      }
    `,
    fragmentShader: `
      uniform float uTime;
      uniform vec3 uRayCol;
      uniform float uRayOpacity;
      varying vec2 vUv;
      varying vec3 vNormalV;
      varying vec3 vViewDir;
      void main() {
        // Ultra-soft Fresnel cylindrical edge fade so there are NEVER hard polygon edges!
        float edge = pow(abs(dot(vNormalV, vViewDir)), 2.2);
        float vertFade = smoothstep(0.0, 0.32, vUv.y) * smoothstep(1.0, 0.12, vUv.y);
        float shimmer = 0.78 + 0.22 * sin(vUv.x * 18.0 + uTime * 0.55) * cos(vUv.y * 8.0 - uTime * 0.35);
        float alpha = edge * vertFade * shimmer * uRayOpacity;
        gl_FragColor = vec4(uRayCol, alpha);
      }
    `
  });
  const raySpots = [
    [-3, 48], [-3, 24], [-3, -3.5], [24.4, 14], [24.4, -14],
    [-31.2, 4], [-56, -4], [-86, 56], [44, -68]
  ];
  const rayGeo = new pn(2.2, 7.4, 34, 14, 1, true);
  for (const [rx, rz] of raySpots) {
    const shaft = new et(rayGeo, godRayMat);
    shaft.position.set(rx, 16.5, rz);
    shaft.rotation.set(0.24, 0.0, -0.34); // Slanted along sun angle!
    shaft.renderOrder = 6;
    Ht.add(shaft);
  }

  // --- LAYER 5: GLOBAL PBR GLSL SHADER INJECTION (GROUND CONTACT AO + GLASS REFLECTIONS + MICRO-GRAIN) ---
  const stuccoTex = (function() {
    const c = document.createElement("canvas"); c.width = 128; c.height = 128;
    const g = c.getContext("2d");
    const img = g.createImageData(128, 128);
    let seed = 4242;
    for (let i = 0; i < img.data.length; i += 4) {
      seed = (seed * 16807) % 2147483647;
      const v = 108 + (seed % 40);
      img.data[i] = img.data[i+1] = img.data[i+2] = v;
      img.data[i+3] = 255;
    }
    g.putImageData(img, 0, 0);
    const t = new dn(c); t.wrapS = t.wrapT = jn; t.repeat.set(3, 3);
    return t;
  })();

  const enhancedMats = new Set();
  const sharedPbrUniforms = {
    uSunColPbr: { value: new Pe(0xfff5e0) },
    uAoStrength: { value: 0.36 }
  };

  function injectPhotorealisticPBR(mat) {
    if (enhancedMats.has(mat)) return;
    enhancedMats.add(mat);

    // Upgrade architectural glass & glossy dark surfaces to true sky-reflecting IBL glass!
    if (!mat.map && mat.roughness <= 0.25 && mat.color && mat.color.getHex() < 0x35485c) {
      mat.metalness = Math.max(mat.metalness, 0.72);
      mat.roughness = 0.09;
      mat.envMapIntensity = 1.65;
      mat.needsUpdate = true;
      return;
    }
    // Add crisp PBR micro-stucco bump to matte campus masonry
    if (!mat.map && !mat.bumpMap && mat.roughness > 0.45 && mat.metalness < 0.25) {
      mat.bumpMap = stuccoTex;
      mat.bumpScale = 0.018;
    }
    // Inject Ground Contact Ambient Occlusion + World-Space Micro-Grain + Sunlit Rim Wrap via onBeforeCompile!
    const prevCompile = mat.onBeforeCompile;
    mat.onBeforeCompile = function(shader) {
      if (prevCompile) prevCompile(shader);
      shader.uniforms.uSunColPbr = sharedPbrUniforms.uSunColPbr;
      shader.uniforms.uAoStrength = sharedPbrUniforms.uAoStrength;
      shader.vertexShader = shader.vertexShader
        .replace("#include <common>", "#include <common>\nvarying vec3 vAuWPos;\nvarying vec3 vAuWNorm;")
        .replace("#include <begin_vertex>", "#include <begin_vertex>\nvec4 auWp = modelMatrix * vec4(transformed, 1.0);\nvAuWPos = auWp.xyz;\nvAuWNorm = normalize(mat3(modelMatrix) * objectNormal);");
      shader.fragmentShader = shader.fragmentShader
        .replace("#include <common>", "#include <common>\nuniform vec3 uSunColPbr;\nuniform float uAoStrength;\nvarying vec3 vAuWPos;\nvarying vec3 vAuWNorm;")
        .replace("#include <dithering_fragment>", `
          // 1. Photorealistic Ground Contact Ambient Occlusion (walls, pillars, curbs & trunks darken cleanly at y=0!)
          float wallMask = 1.0 - abs(vAuWNorm.y);
          float groundAO = mix(1.0 - uAoStrength, 1.0, smoothstep(0.02, 1.45, vAuWPos.y));
          gl_FragColor.rgb *= mix(1.0, groundAO, wallMask * 0.85);
          // 2. Subtle world-space surface micro-variation (eliminates flat plastic CG look!)
          float micro = sin(vAuWPos.x * 7.3 + vAuWPos.z * 5.9) * cos(vAuWPos.y * 9.1 - vAuWPos.x * 4.2);
          gl_FragColor.rgb *= (1.0 + micro * 0.024);
          // 3. Subtle warm sunlight rim/bounce wrap on upward-facing architectural edges
          float skyBounce = smoothstep(0.25, 0.95, vAuWNorm.y) * 0.06;
          gl_FragColor.rgb += uSunColPbr * skyBounce * 0.16;
          #include <dithering_fragment>
        `);
    };
    mat.customProgramCacheKey = () => "au_photoreal_pbr_v2";
    mat.needsUpdate = true;
  }

  Ht.traverse((obj) => {
    if (obj.isMesh && obj.material && obj.material.isMeshStandardMaterial) {
      injectPhotorealisticPBR(obj.material);
    }
  });

  // --- LAYER 6: HIGHER-RES SOFT SHADOWS & LIVE TIME-OF-DAY SHADER SYNC ---
  if (typeof Cn !== "undefined" && Cn.shadow) {
    Cn.shadow.bias = -0.00035;
    Cn.shadow.normalBias = 0.025;
  }

  function syncRealisticAtmosphere() {
    const tmEl = document.getElementById("time-mode");
    const mode = tmEl ? tmEl.value : "noon";
    if (typeof Cn !== "undefined") {
      skyUniforms.uSunDir.value.copy(Cn.position).normalize();
    }
    if (mode === "morning") {
      skyUniforms.uZenithCol.value.setHex(0x216bc7);
      skyUniforms.uHorizonCol.value.setHex(0xd4ecfc);
      skyUniforms.uSunCol.value.setHex(0xfff0c4);
      skyUniforms.uCloudTopCol.value.setHex(0xfffaf0);
      skyUniforms.uCloudBotCol.value.setHex(0x95b2cf);
      skyUniforms.uCloudDensity.value = 0.50;
      skyUniforms.uStarAlpha.value = 0.0;
      rayUniforms.uRayCol.value.setHex(0xfff3cf);
      rayUniforms.uRayOpacity.value = 0.16;
      sharedPbrUniforms.uSunColPbr.value.setHex(0xfff0c4);
      redrawIBL("#216bc7", "#d4ecfc", "#546b47", "rgba(255,238,190,0.9)", 120, 72);
      Ye.toneMappingExposure = 1.14;
    } else if (mode === "golden") {
      skyUniforms.uZenithCol.value.setHex(0x1e3869);
      skyUniforms.uHorizonCol.value.setHex(0xf49752);
      skyUniforms.uSunCol.value.setHex(0xffad5a);
      skyUniforms.uCloudTopCol.value.setHex(0xffd8a8);
      skyUniforms.uCloudBotCol.value.setHex(0x734a54);
      skyUniforms.uCloudDensity.value = 0.62;
      skyUniforms.uStarAlpha.value = 0.18;
      rayUniforms.uRayCol.value.setHex(0xffb463);
      rayUniforms.uRayOpacity.value = 0.22;
      sharedPbrUniforms.uSunColPbr.value.setHex(0xffb463);
      redrawIBL("#1e3869", "#f49752", "#473b2e", "rgba(255,170,88,0.95)", 360, 96);
      Ye.toneMappingExposure = 1.12;
    } else if (mode === "outbreak") {
      skyUniforms.uZenithCol.value.setHex(0x0c0a1d);
      skyUniforms.uHorizonCol.value.setHex(0x632128);
      skyUniforms.uSunCol.value.setHex(0xf05c3b);
      skyUniforms.uCloudTopCol.value.setHex(0xb8524a);
      skyUniforms.uCloudBotCol.value.setHex(0x281829);
      skyUniforms.uCloudDensity.value = 0.66;
      skyUniforms.uStarAlpha.value = 0.85;
      rayUniforms.uRayCol.value.setHex(0xf06543);
      rayUniforms.uRayOpacity.value = 0.11;
      sharedPbrUniforms.uSunColPbr.value.setHex(0xf06543);
      redrawIBL("#0c0a1d", "#632128", "#241b1e", "rgba(240,92,59,0.85)", 380, 108);
      Ye.toneMappingExposure = 1.06;
    } else {
      // Bright Campus Noon (photorealistic sunlit Deccan sky)
      skyUniforms.uZenithCol.value.setHex(0x1652a8);
      skyUniforms.uHorizonCol.value.setHex(0xb4dcf8);
      skyUniforms.uSunCol.value.setHex(0xfff7e0);
      skyUniforms.uCloudTopCol.value.setHex(0xffffff);
      skyUniforms.uCloudBotCol.value.setHex(0x88a2bd);
      skyUniforms.uCloudDensity.value = 0.54;
      skyUniforms.uStarAlpha.value = 0.0;
      rayUniforms.uRayCol.value.setHex(0xfff4d6);
      rayUniforms.uRayOpacity.value = 0.14;
      sharedPbrUniforms.uSunColPbr.value.setHex(0xfff7e0);
      redrawIBL("#1652a8", "#b4dcf8", "#4d6142", "rgba(255,244,210,0.9)", 148, 56);
      Ye.toneMappingExposure = 1.13;
    }
  }
  const _tmEl = document.getElementById("time-mode");
  if (_tmEl) _tmEl.addEventListener("change", () => setTimeout(syncRealisticAtmosphere, 10));
  syncRealisticAtmosphere();

  // Driven directly by Three.js Ye.setAnimationLoop so clouds, Gerstner water, God-Rays & skyDome animate in BOTH PC & Meta Quest 3 WebXR!
  window._tickRealisticShaders = function(dt) {
    const safeDt = Math.min(0.1, Math.max(0.001, dt || 0.016));
    skyUniforms.uTime.value += safeDt;
    waterUniforms.uTime.value += safeDt;
    rayUniforms.uTime.value += safeDt;
    if (typeof xt !== "undefined") {
      skyDome.position.set(xt.position.x, 0, xt.position.z);
    }
  };
})();
'''

html = html.replace(
    '// ============================================================================\n// BUILDING 9:',
    REALISTIC_SHADERS_JS + '\n// ============================================================================\n// BUILDING 9:',
    1
)
if REALISTIC_SHADERS_JS not in html:
    html = html.replace(
        '// ============================================================================\r\n// BUILDING 9:',
        REALISTIC_SHADERS_JS + '\r\n// ============================================================================\r\n// BUILDING 9:',
        1
    )

# =============================================================================
# 7r. OFFICIAL GUIDED CAMPUS TOUR EDITION (CAMPUS_TOUR_ONLY = True)
# Hides ALL zombie & weapon UI/logic cleanly (while keeping all zombie code
# safely preserved in build_zombie_game.py!) and adds:
#   - Clean welcome screen with ONLY "Start Campus Tour" (+ Meta Quest VR)
#   - 10.5s Sunlit Cinematic Aerial Flyover with live welcoming Voice-Over
#   - Detailed 3D Electric Anurag University Golf Cart / Campus Buggy
#   - Road-only guided route covering ALL 10 major blocks & landmarks
#   - Live AI Tour Guide Voice (Web Speech API) citing official anurag.edu.in facts
#   - Sleek Subtitle & Controls Bar + Live 3D Buggy Dashboard Display for PC & VR!
# =============================================================================
if CAMPUS_TOUR_ONLY:
    html = html.replace(
        "<title>Anurag University — Campus Outbreak FP & Meta Quest 3 VR</title>",
        "<title>Anurag University — Official 3D & VR Guided Campus Tour</title>",
        1
    )
    # Default to Bright Campus Noon and remove Outbreak Dusk & Zombie mode from visible dropdowns
    html = html.replace('<option value="outbreak" selected>Outbreak Dusk (Zombie Alert)</option>', '', 1)
    html = html.replace('<option value="noon">Bright Campus Noon</option>', '<option value="noon" selected>Bright Campus Noon</option>', 1)
    html = html.replace('<option value="zombie" selected>Zombie Outbreak (6 Levels + CEO Boss)</option>\n      ', '', 1)
    html = html.replace('<option value="creative">Creative Flight & Walk</option>', '<option value="creative" selected>Guided Campus Tour & Explorer</option>', 1)
    html = html.replace('<button id="walk">Play Game (PC)</button>', '<button id="walk">Start Campus Tour</button>', 1)
    html = html.replace(
        '01 · SURVIVAL MISSION</div><div class="intro-col-txt">Walk through the Main Gate, survive 5 escalating 2-min phases &amp; defeat THE CEO.',
        '01 · ACADEMIC EXCELLENCE</div><div class="intro-col-txt">NAAC \'A\' Accredited · NIRF Top 151–200 University · NIRF Pharmacy #72 in India.',
        1
    )
    html = html.replace(
        '02 · TACTICAL ARSENAL</div><div class="intro-col-txt">Lightsaber [1], Pistol [2], Rifle [3], Shotgun [4] &amp; pickable Rods/Branches [E].',
        '02 · RECORD PLACEMENTS</div><div class="intro-col-txt">₹53 LPA Highest Package · 2,100+ Job Offers · 97% Placement Rate · 200+ Recruiters.',
        1
    )
    html = html.replace(
        '03 · VR &amp; PC DEFENSE</div><div class="intro-col-txt">Left-Trigger / RMB raises Cyan Energy Shield · Space / Y to Jump · Swing in VR!',
        '03 · ELECTRIC BUGGY TOUR</div><div class="intro-col-txt">100+ Acre Green Campus · 10 Major Blocks by Road · Live AI Voice Guide &amp; 360° Look!',
        1
    )
    html = html.replace('<button id="btn-skip-intro">Skip Intro [Space]</button>', '<button id="btn-skip-intro">Board Buggy Now ›</button>', 1)
    html = html.replace(
        "Meta Quest 3 & PC Combat · Left Hand = Tactical Energy Shield (hold up to block, Left Trigger / thrust = Shield Bash). Right Hand = Lightsaber, Pistol, Rifle, Shotgun & Ground Rods/Branches (Right Trigger fires, swing physically in VR, Right Grip grabs ground weapons, A switches weapon, B reloads). Lift left wrist for live VR HUD.",
        "Welcome to the Official 3D & Meta Quest 3 Guided Campus Tour of Anurag University, Venkatapur, Hyderabad — NAAC 'A' Accredited · NIRF Ranked · 100+ Acre Urban-Tech Campus. Experience an aerial campus flyover, then board our electric campus tour buggy for a narrated road tour of every major block!"
    )

    TOUR_CSS = """
body.campus-tour-only #combat-hud,
body.campus-tour-only #top-hp-bar,
body.campus-tour-only #vitals-hud,
body.campus-tour-only #weapon-hud,
body.campus-tour-only #wave-banner,
body.campus-tour-only #boss-bar-wrap,
body.campus-tour-only #crosshair{display:none !important;opacity:0 !important;pointer-events:none !important}
body.campus-tour-only main .control-grid:first-of-type{display:none !important}
body.campus-tour-only main #walk{
  grid-column:1 / -1;padding:15px 28px;font:900 17px/1.2 'Segoe UI',system-ui,sans-serif;
  letter-spacing:0.8px;text-transform:uppercase;
  background:linear-gradient(135deg,#0ea5e9,#2563eb,#1d4ed8);color:#ffffff;
  border:1px solid rgba(186,230,253,0.75);border-radius:12px;
  box-shadow:0 12px 32px rgba(14,165,233,0.45);cursor:pointer;
}
body.campus-tour-only main #walk:hover{filter:brightness(1.12);transform:translateY(-1px)}
#tour-guide-bar{
  position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:38;
  width:min(860px,94vw);padding:14px 20px;border-radius:16px;display:none;
  background:linear-gradient(150deg,rgba(8,18,32,0.92),rgba(18,28,46,0.90));
  border:1px solid rgba(114,239,221,0.48);
  box-shadow:0 16px 46px rgba(0,0,0,0.62),inset 0 1px 0 rgba(255,255,255,0.12);
  backdrop-filter:blur(14px);pointer-events:auto;
}
#tour-guide-bar.visible{display:block}
#tg-top{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:7px}
#tg-title-wrap{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
#tg-step{
  background:linear-gradient(135deg,#e11d48,#f59e0b);color:#fff;
  font:900 11px system-ui;padding:3px 9px;border-radius:999px;letter-spacing:1.1px;
}
#tg-landmark{font:900 16px/1.2 'Segoe UI',system-ui,sans-serif;color:#ffffff;letter-spacing:0.4px}
#tg-pills{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.tg-pill{
  font:700 10.5px system-ui;color:#72efdd;background:rgba(14,165,233,0.16);
  border:1px solid rgba(114,239,221,0.35);padding:2px 8px;border-radius:6px;letter-spacing:0.4px;
}
#tg-caption{font:500 13.5px/1.45 'Segoe UI',system-ui,sans-serif;color:#e2f2fc;margin-bottom:10px}
#tg-controls{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}
#tg-btns{display:flex;gap:7px;flex-wrap:wrap}
.tg-btn{
  padding:6px 13px;border-radius:8px;border:1px solid rgba(114,239,221,0.42);
  background:rgba(15,34,54,0.9);color:#e0f7fa;font:700 12px system-ui;cursor:pointer;
}
.tg-btn:hover{background:#0ea5e9;color:#04151f}
.tg-btn.primary{background:linear-gradient(135deg,#0ea5e9,#14b8a6);color:#04151f;border-color:#72efdd}
#tg-prog-wrap{flex:1;min-width:140px;height:6px;background:rgba(255,255,255,0.14);border-radius:4px;overflow:hidden}
#tg-prog-fill{height:100%;width:0%;background:linear-gradient(90deg,#38bdf8,#72efdd,#fbbf24);transition:width .2s}
#tour-complete-overlay{
  position:fixed;inset:0;z-index:48;display:none;align-items:center;justify-content:center;
  background:rgba(6,14,24,0.62);backdrop-filter:blur(6px);pointer-events:auto;
}
#tour-complete-overlay.show{display:flex}
#tour-complete-card{
  width:min(560px,92vw);padding:28px 30px;border-radius:18px;text-align:center;
  background:linear-gradient(155deg,rgba(10,22,38,0.95),rgba(20,34,56,0.94));
  border:1.5px solid rgba(114,239,221,0.6);box-shadow:0 24px 64px rgba(0,0,0,0.72);
}
#tour-complete-card h2{font:900 28px/1.15 Georgia,serif;color:#fde047;margin:0 0 8px;letter-spacing:0.6px}
#tour-complete-card p{font:500 14px/1.55 system-ui;color:#d6edf8;margin:0 0 18px}
#tour-complete-actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
"""
    html = html.replace("</style>", TOUR_CSS + "\n</style>", 1)

    TOUR_DOM = """
<div id="tour-guide-bar">
  <div id="tg-top">
    <div id="tg-title-wrap">
      <span id="tg-step">AERIAL FLYOVER</span>
      <span id="tg-landmark">Anurag University · Venkatapur Campus</span>
    </div>
    <span style="font:700 11px system-ui;color:#fbbf24;letter-spacing:0.8px">ELECTRIC BUGGY TOUR · LOOK AROUND 360°</span>
  </div>
  <div id="tg-pills"></div>
  <div id="tg-caption">Preparing your guided campus tour of Anurag University...</div>
  <div id="tg-controls">
    <div id="tg-btns">
      <button class="tg-btn primary" id="btn-tg-pause">Pause</button>
      <button class="tg-btn" id="btn-tg-voice">Voice: ON</button>
      <button class="tg-btn" id="btn-tg-next">Next Stop ›</button>
      <button class="tg-btn" id="btn-tg-replay">Replay Tour</button>
      <button class="tg-btn" id="btn-tg-exit">Free Explore</button>
    </div>
    <div id="tg-prog-wrap"><div id="tg-prog-fill"></div></div>
  </div>
</div>
<div id="tour-complete-overlay">
  <div id="tour-complete-card">
    <h2>Welcome to Anurag University!</h2>
    <p>You have completed the Official Guided Campus Buggy Tour of Anurag University — NAAC 'A' Accredited · NIRF Ranked · ₹53 LPA Highest Package · 2,100+ Offers across 200+ Global Recruiters.</p>
    <div id="tour-complete-actions">
      <button class="tg-btn primary" id="btn-tc-replay" style="padding:11px 22px;font-size:14px">Replay Campus Tour</button>
      <button class="tg-btn" id="btn-tc-explore" style="padding:11px 22px;font-size:14px">Explore Campus Freely</button>
    </div>
  </div>
</div>
"""
    html = html.replace('<div id="hint"></div>', TOUR_DOM + '\n<div id="hint"></div>', 1)

    CAMPUS_TOUR_JS = r'''
// ============================================================================
// OFFICIAL ANURAG UNIVERSITY GUIDED CAMPUS TOUR (AERIAL FLYOVER + 3D GOLF CART BUGGY + AI VOICE GUIDE)
// All Zombie Outbreak code is disabled cleanly via CAMPUS_TOUR_ONLY = true!
// ============================================================================
window.CAMPUS_TOUR_ONLY = true;
document.body.classList.add("campus-tour-only");

// 10 Official Verified Road-Only Campus Tour Stops (Facts sourced directly from anurag.edu.in!)
const AU_TOUR_STOPS = [
  {
    name: "Main Gate & Grand Entrance Avenue",
    pills: ["100+ Acre Green Campus", "NAAC 'A' Accredited", "NIRF Top 151–200"],
    path: [[-3, 67], [-3, 52], [-3, 38], [-3, 27]],
    lookTarget: [-3, 6, 10],
    holdSec: 7.5,
    speech: "Welcome aboard the Anurag University Electric Campus Tour Buggy! Spread across over 100 lush green acres in Venkatapur, Hyderabad, Anurag University is accredited with NAAC A Grade and ranked among India's top 151 to 200 universities by NIRF. Notice our iconic Sports Silhouette Wall and placement achievement boards lining the grand entrance avenue."
  },
  {
    name: "A-Block · School of Engineering & Main Quadrangle",
    pills: ["NIRF Engg 101–150", "AI, ML & Data Science", "30,000+ sq. ft. Library"],
    path: [[-3, 25], [8, 24]],
    lookTarget: [-3, 6, 10],
    holdSec: 8.0,
    speech: "Straight ahead stands A-Block, the flagship home of the School of Engineering. Offering NBA-accredited B.Tech, M.Tech, and Ph.D. programs in Computer Science, Artificial Intelligence, Machine Learning, Data Science, and Cyber Security, A-Block houses our Centre for Advanced Computational Research, a 30,000 square foot central library, and the lively central amphitheater quadrangle."
  },
  {
    name: "G-Block (Central Admin) & F-Block (Examination Branch)",
    pills: ["School of Management", "Startup Incubation", "Wide 2-Lane East Avenue"],
    path: [[18, 24], [24.4, 21], [24.4, 14], [24.4, -3]],
    lookTarget: [38, 6, 4],
    holdSec: 7.5,
    speech: "We are now cruising north along our wide two-lane East Avenue past G-Block, our Central Administrative Block and School of Management established in 2006, alongside F-Block, our modern Examination Branch. Here, future leaders build MBA expertise, corporate leadership skills, and student-driven startups through our dedicated business incubation hub."
  },
  {
    name: "E-Block · ECE, TEDxAnuragU & Space Research + I-Block",
    pills: ["TEDxAnuragU Atrium", "Satellite Space Research", "10-Story I-Block Tower"],
    path: [[24.4, -12], [24.4, -19.5]],
    lookTarget: [42, 6, -19.5],
    holdSec: 8.0,
    speech: "To our right is E-Block, home to the Department of Electronics and Communication Engineering, the famous TEDxAnuragU atrium, and our pioneering Satellite Design and Development Center for Space Research. Rising just beyond it is our brand-new 10-story I-Block expansion mega-tower, built for next-generation innovation."
  },
  {
    name: "Cricket Stadium Ground & Athletics Complex",
    pills: ["Championship Cricket Oval", "Circular Running Track", "Turf & Basketball Courts"],
    path: [[24.4, -32], [24.4, -44]],
    lookTarget: [44, 3, -76],
    holdSec: 7.0,
    speech: "Opening up ahead is Anurag University's expansive Cricket Stadium Ground, encircled by a full red-clay athletics running track, alongside synthetic turf courts and basketball arenas. Sports, teamwork, and holistic student wellness thrive here every single day."
  },
  {
    name: "North Avenue · Medicinal Garden, H-Block & Solar Tree",
    pills: ["Green Solar Charging Tree", "School of Agriculture", "70+ Campus Fleet Buses"],
    path: [[14, -41], [-8, -41], [-33, -41], [-56, -41]],
    lookTarget: [-58, 4, -32],
    holdSec: 8.5,
    speech: "Driving along North Campus Avenue, we pass the School of Pharmacy's lush Medicinal Garden and our 6-story H-Block featuring our eco-friendly Green Solar-Panel Charging Tree. Anurag University also pioneers the ICAR-mapped School of Agricultural Sciences with IoT precision farming, polyhouses, and a fleet of over 70 yellow campus buses connecting all of Hyderabad."
  },
  {
    name: "D-Block · School of Humanities & Science",
    pills: ["Solar-Powered Roof", "YOUR FUTURE LOOKS Bright", "Foundational Sciences"],
    path: [[-72, -36], [-73, -20], [-73, -10]],
    lookTarget: [-54, 6, -10],
    holdSec: 7.0,
    speech: "Turning south along West Avenue, we arrive at D-Block, the School of Humanities and Science, crowned with rooftop solar panels and our inspiring street-art mural reminding every student that Your Future Looks Bright. Here, first-year scholars build rock-solid foundations in mathematics, physics, communication, and design thinking."
  },
  {
    name: "B-Block · School of Pharmacy (NIRF #72 in India)",
    pills: ["NIRF Pharmacy #72", "PCI & NBA Approved", "Neuroscience R&D Centre"],
    path: [[-73, 0], [-73, 10]],
    lookTarget: [-52, 5, 10],
    holdSec: 8.0,
    speech: "Next on our left is B-Block, home to our prestigious School of Pharmacy, established in 2005 and ranked 72nd nationally in India by NIRF. Approved by PCI and accredited by NBA, it leads South India in drug discovery with HPLC analytics, pharmacology laboratories, and a dedicated Neuroscience R&D Centre backed by ICMR and national research grants."
  },
  {
    name: "C-Block · Civil Engineering & Basketball Plaza",
    pills: ["Civil Engineering Wing", "Iconic Street-Art Mural", "AU Basketball Plaza"],
    path: [[-73, 24], [-73, 35], [-52, 35]],
    lookTarget: [-46, 3, 52],
    holdSec: 7.0,
    speech: "Rounding C-Block, our Civil Engineering Department, you can admire our iconic multi-story street-art mural and the vibrant C-Block Basketball Plaza featuring the Anurag University emblem at center court — a favorite gathering spot for students after lectures."
  },
  {
    name: "Dr. APJ Abdul Kalam Hall & Record Placements Finale",
    pills: ["₹53 LPA Highest Package", "2,100+ Job Offers", "200+ Global Recruiters"],
    path: [[-73, 46], [-74, 56], [-42, 46], [-12, 34], [-3, 29]],
    lookTarget: [-3, 6, 12],
    holdSec: 9.5,
    speech: "Passing the grand air-conditioned Dr. A P J Abdul Kalam Auditorium — venue for international conferences, hackathons, and orientations — we return to A-Block Plaza. With a 97 percent placement rate, over 2,100 job offers, a highest package of 53 Lakhs per annum, and over 200 top recruiters including Microsoft, Amazon, Qualcomm, JPMorgan Chase, Goldman Sachs, Cisco, Accenture, and TCS, Anurag University empowers you to be everyone you dream to be. Thank you for joining our tour!"
  }
];

const CAMPUS_TOUR = {
  state: "idle", // "idle" | "aerial" | "riding" | "done"
  aerialTime: 0,
  aerialDur: 10.5,
  paused: false,
  voiceOn: true,
  stopIdx: 0,
  wpIdx: 0,
  holdTimer: 0,
  speed: 8.2, // smooth comfortable buggy cruise speed (m/s)
  buggy: null,
  wheels: [],
  dashCtx: null,
  dashTex: null,
  buggyPos: new A(-3, 0, 67),
  buggyYaw: 0,
  freeYawOffset: 0,
  freePitch: 0.02
};

// Build Detailed 3D Anurag University Electric Campus Golf Cart / Buggy!
function buildTourBuggy() {
  if (CAMPUS_TOUR.buggy) return CAMPUS_TOUR.buggy;
  const g = new fi();
  const whiteMat = new Jt({ color: 0xf8fafc, roughness: 0.25, metalness: 0.18 });
  const blueMat = new Jt({ color: 0x1d4ed8, roughness: 0.3, metalness: 0.35 });
  const redMat = new Jt({ color: 0xdc2626, roughness: 0.32, metalness: 0.25 });
  const chromeMat = new Jt({ color: 0xe2e8f0, roughness: 0.18, metalness: 0.88 });
  const seatMat = new Jt({ color: 0xe7dcc6, roughness: 0.78 });
  const darkMat = new Jt({ color: 0x1e293b, roughness: 0.65, metalness: 0.2 });
  const glassMat = new Jt({ color: 0xbae6fd, transparent: true, opacity: 0.24, roughness: 0.08, metalness: 0.45 });

  // Lower chassis & floorboards
  const floor = new et(new Ni(1.62, 0.16, 3.15), darkMat); floor.position.set(0, 0.34, 0); floor.castShadow = true; g.add(floor);
  // Front hood (sleek pearl white + royal blue nose + crimson AU stripe!)
  const hood = new et(new Ni(1.56, 0.56, 0.95), whiteMat); hood.position.set(0, 0.68, -1.12); hood.castShadow = true; g.add(hood);
  const nose = new et(new Ni(1.58, 0.26, 0.14), blueMat); nose.position.set(0, 0.54, -1.58); g.add(nose);
  const stripe = new et(new Ni(1.60, 0.07, 0.98), redMat); stripe.position.set(0, 0.72, -1.12); g.add(stripe);
  // Rear body deck
  const rearBody = new et(new Ni(1.58, 0.58, 1.15), whiteMat); rearBody.position.set(0, 0.68, 1.0); rearBody.castShadow = true; g.add(rearBody);
  const rearStripe = new et(new Ni(1.60, 0.07, 1.18), blueMat); rearStripe.position.set(0, 0.72, 1.0); g.add(rearStripe);

  // LED Headlights & Red Taillights
  const headMat = new Yi({ color: 0xfffbeb });
  const tailMat = new Yi({ color: 0xef4444 });
  for (let sx of [-0.54, 0.54]) {
    let hl = new et(new pn(0.08, 0.08, 0.06, 12), headMat); hl.rotation.x = Math.PI / 2; hl.position.set(sx, 0.76, -1.60); g.add(hl);
    let tl = new et(new Ni(0.22, 0.09, 0.05), tailMat); tl.position.set(sx, 0.76, 1.59); g.add(tl);
  }

  // Comfortable Cream Padded Front & Rear Bench Seats
  const fSeat = new et(new Ni(1.42, 0.16, 0.56), seatMat); fSeat.position.set(0, 0.76, -0.15); g.add(fSeat);
  const fBack = new et(new Ni(1.42, 0.52, 0.14), seatMat); fBack.position.set(0, 1.08, 0.12); g.add(fBack);
  const rSeat = new et(new Ni(1.42, 0.16, 0.56), seatMat); rSeat.position.set(0, 0.76, 0.85); g.add(rSeat);
  const rBack = new et(new Ni(1.42, 0.52, 0.14), seatMat); rBack.position.set(0, 1.08, 1.12); g.add(rBack);

  // Dashboard Console + Steering Column & Wheel (on driver's left)
  const dash = new et(new Ni(1.48, 0.24, 0.38), darkMat); dash.position.set(0, 1.02, -0.76); g.add(dash);
  const steerCol = new et(new pn(0.03, 0.03, 0.44, 10), chromeMat);
  steerCol.position.set(-0.38, 1.12, -0.62); steerCol.rotation.x = 0.52; g.add(steerCol);
  const steerWheel = new et(new gn(0.16, 0.022, 8, 18), darkMat);
  steerWheel.position.set(-0.38, 1.24, -0.49); steerWheel.rotation.x = 0.52; g.add(steerWheel);

  // Live 3D Glowing Tour Guide Dashboard Screen (visible in BOTH PC & Meta Quest 3 VR!)
  const dc = document.createElement("canvas"); dc.width = 512; dc.height = 192;
  const dCtx = dc.getContext("2d");
  const dTex = new dn(dc); dTex.colorSpace = vt;
  const dScreen = new et(new _i(0.54, 0.20), new Yi({ map: dTex }));
  dScreen.position.set(0.24, 1.16, -0.68);
  dScreen.rotation.x = -0.32;
  g.add(dScreen);
  CAMPUS_TOUR.dashCtx = dCtx;
  CAMPUS_TOUR.dashTex = dTex;

  // 4 Brushed Chrome Canopy Pillars + White Sun Canopy Roof + Clear Tinted Windshield
  for (let [px, pz] of [[-0.72, -0.82], [0.72, -0.82], [-0.72, 1.28], [0.72, 1.28]]) {
    let pil = new et(new pn(0.028, 0.028, 1.26, 8), chromeMat);
    pil.position.set(px, 1.54, pz); g.add(pil);
  }
  const roof = new et(new Ni(1.66, 0.09, 2.38), whiteMat); roof.position.set(0, 2.18, 0.22); roof.castShadow = true; g.add(roof);
  const roofTrim = new et(new Ni(1.68, 0.05, 2.40), blueMat); roofTrim.position.set(0, 2.13, 0.22); g.add(roofTrim);
  const wind = new et(new Ni(1.42, 0.78, 0.03), glassMat);
  wind.position.set(0, 1.56, -0.84); wind.rotation.x = -0.14; g.add(wind);

  // 4 Rotating Rubber Tires with Silver Alloy Rims!
  const tireMat = new Jt({ color: 0x15181c, roughness: 0.92 });
  CAMPUS_TOUR.wheels = [];
  for (let [wx, wz] of [[-0.82, -1.02], [0.82, -1.02], [-0.82, 1.02], [0.82, 1.02]]) {
    const wGrp = new fi();
    wGrp.position.set(wx, 0.29, wz);
    const tire = new et(new pn(0.29, 0.29, 0.20, 16), tireMat); tire.rotation.z = Math.PI / 2; wGrp.add(tire);
    const rim = new et(new pn(0.15, 0.15, 0.22, 12), chromeMat); rim.rotation.z = Math.PI / 2; wGrp.add(rim);
    g.add(wGrp);
    CAMPUS_TOUR.wheels.push(wGrp);
  }

  g.position.copy(CAMPUS_TOUR.buggyPos);
  Ht.add(g);
  CAMPUS_TOUR.buggy = g;
  return g;
}

function updateBuggyDashboard(stepText, title, pills) {
  if (!CAMPUS_TOUR.dashCtx || !CAMPUS_TOUR.dashTex) return;
  const g = CAMPUS_TOUR.dashCtx;
  g.fillStyle = "#081424"; g.fillRect(0, 0, 512, 192);
  g.strokeStyle = "#38bdf8"; g.lineWidth = 6; g.strokeRect(4, 4, 504, 184);
  g.fillStyle = "#ef4444"; g.fillRect(18, 18, 52, 28);
  g.fillStyle = "#ffffff"; g.font = "900 18px sans-serif"; g.textAlign = "center"; g.fillText("AU", 44, 38);
  g.fillStyle = "#fde047"; g.font = "800 20px sans-serif"; g.textAlign = "left"; g.fillText(stepText, 82, 39);
  g.fillStyle = "#ffffff"; g.font = "900 24px 'Segoe UI',sans-serif";
  g.fillText(title.slice(0, 34), 18, 86);
  g.fillStyle = "#72efdd"; g.font = "700 18px sans-serif";
  g.fillText((pills || []).join("  ·  ").slice(0, 48), 18, 128);
  g.fillStyle = "#94a3b8"; g.font = "600 16px Consolas,monospace";
  g.fillText("ANURAG UNIVERSITY ELECTRIC CAMPUS BUGGY · 100% GREEN", 18, 168);
  CAMPUS_TOUR.dashTex.needsUpdate = true;
}

// Natural AI Tour Guide Voice-Over (Web Speech API)
function speakTourGuide(text) {
  try {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    if (!CAMPUS_TOUR.voiceOn || !text) return;
    const u = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices() || [];
    const pref = voices.find(v => /en[-_](IN|US|GB)/i.test(v.lang) && /natural|google|microsoft|zira|heera|ravi|samantha/i.test(v.name))
      || voices.find(v => /en/i.test(v.lang));
    if (pref) u.voice = pref;
    u.rate = 0.98;
    u.pitch = 1.02;
    u.volume = 1.0;
    window.speechSynthesis.speak(u);
  } catch (e) {}
}

function updateTourUI(stepLabel, title, pills, caption, progPct) {
  const bar = document.getElementById("tour-guide-bar");
  if (bar) bar.classList.add("visible");
  if (document.getElementById("tg-step")) document.getElementById("tg-step").textContent = stepLabel;
  if (document.getElementById("tg-landmark")) document.getElementById("tg-landmark").textContent = title;
  if (document.getElementById("tg-caption")) document.getElementById("tg-caption").textContent = caption;
  if (document.getElementById("tg-prog-fill")) document.getElementById("tg-prog-fill").style.width = `${Math.max(0, Math.min(100, progPct))}%`;
  const pWrap = document.getElementById("tg-pills");
  if (pWrap) pWrap.innerHTML = (pills || []).map(p => `<span class="tg-pill">${p}</span>`).join("");
  updateBuggyDashboard(stepLabel, title, pills);
}

function announceCurrentStop() {
  const stop = AU_TOUR_STOPS[CAMPUS_TOUR.stopIdx];
  if (!stop) return;
  const pct = ((CAMPUS_TOUR.stopIdx + 1) / AU_TOUR_STOPS.length) * 100;
  updateTourUI(`STOP ${CAMPUS_TOUR.stopIdx + 1} / ${AU_TOUR_STOPS.length}`, stop.name, stop.pills, stop.speech, pct);
  speakTourGuide(stop.speech);
}

function startGuidedCampusTour() {
  if (document.getElementById("tour-complete-overlay")) document.getElementById("tour-complete-overlay").classList.remove("show");
  const tm = document.getElementById("time-mode");
  if (tm && tm.value !== "noon") { tm.value = "noon"; tm.dispatchEvent(new Event("change")); }
  buildTourBuggy();
  CAMPUS_TOUR.state = "aerial";
  CAMPUS_TOUR.aerialTime = 0;
  CAMPUS_TOUR.paused = false;
  CAMPUS_TOUR.stopIdx = 0;
  CAMPUS_TOUR.wpIdx = 0;
  CAMPUS_TOUR.holdTimer = 0;
  CAMPUS_TOUR.buggyPos.set(-3, 0, 67);
  CAMPUS_TOUR.buggyYaw = 0;
  CAMPUS_TOUR.freeYawOffset = 0;
  CAMPUS_TOUR.freePitch = 0.02;
  if (CAMPUS_TOUR.buggy) {
    CAMPUS_TOUR.buggy.visible = true;
    CAMPUS_TOUR.buggy.position.copy(CAMPUS_TOUR.buggyPos);
    CAMPUS_TOUR.buggy.rotation.set(0, 0, 0);
  }
  if (document.getElementById("btn-tg-pause")) document.getElementById("btn-tg-pause").textContent = "Pause";
  document.body.classList.add("intro-active");
  if (document.getElementById("intro-overlay")) {
    document.getElementById("intro-overlay").classList.add("playing");
    if (document.getElementById("intro-kicker")) document.getElementById("intro-kicker").textContent = "ANURAG UNIVERSITY · OFFICIAL GUIDED CAMPUS TOUR";
    if (document.getElementById("intro-headline")) document.getElementById("intro-headline").textContent = "WELCOME TO ANURAG UNIVERSITY";
    if (document.getElementById("intro-sub")) document.getElementById("intro-sub").textContent = "NAAC 'A' Accredited · NIRF Top Ranked · 100+ Acre Urban-Tech Campus, Venkatapur, Hyderabad";
  }
  const openMsg = "Welcome to Anurag University, Hyderabad — accredited with NAAC A Grade and ranked among India's premier universities by NIRF. Enjoy this aerial overview of our 100-acre green campus before we board our electric tour buggy at the Main Gate!";
  if (document.getElementById("tour-guide-bar")) document.getElementById("tour-guide-bar").classList.remove("visible");
  updateBuggyDashboard("AERIAL OVERVIEW", "Anurag University · Venkatapur", ["NAAC 'A' Grade", "NIRF Top Ranked"]);
  speakTourGuide(openMsg);
}

function boardTourBuggyNow() {
  CAMPUS_TOUR.state = "riding";
  document.body.classList.remove("intro-active");
  if (document.getElementById("intro-overlay")) document.getElementById("intro-overlay").classList.remove("playing");
  if (typeof fpHands !== "undefined") fpHands.forEach(a => (a.root.visible = false));
  CAMPUS_TOUR.stopIdx = 0;
  CAMPUS_TOUR.wpIdx = 0;
  CAMPUS_TOUR.holdTimer = 0;
  CAMPUS_TOUR.buggyPos.set(-3, 0, 67);
  CAMPUS_TOUR.buggyYaw = 0;
  announceCurrentStop();
}

function exitGuidedTourToExplore() {
  CAMPUS_TOUR.state = "idle";
  document.body.classList.remove("intro-active");
  if (document.getElementById("intro-overlay")) document.getElementById("intro-overlay").classList.remove("playing");
  if (document.getElementById("tour-guide-bar")) document.getElementById("tour-guide-bar").classList.remove("visible");
  if (document.getElementById("tour-complete-overlay")) document.getElementById("tour-complete-overlay").classList.remove("show");
  try { if (window.speechSynthesis) window.speechSynthesis.cancel(); } catch (e) {}
  if (typeof fpHands !== "undefined" && !Ye.xr.isPresenting) fpHands.forEach(a => (a.root.visible = true));
}

// Wire Tour Guide Buttons & Opening "Start Campus Tour" Button
if (document.getElementById("btn-skip-intro")) {
  const skipBtn = document.getElementById("btn-skip-intro");
  skipBtn.textContent = "Board Buggy Now ›";
  skipBtn.addEventListener("click", () => { if (CAMPUS_TOUR.state === "aerial") boardTourBuggyNow(); });
}
if (document.getElementById("btn-tg-pause")) {
  document.getElementById("btn-tg-pause").onclick = () => {
    CAMPUS_TOUR.paused = !CAMPUS_TOUR.paused;
    document.getElementById("btn-tg-pause").textContent = CAMPUS_TOUR.paused ? "Resume" : "Pause";
    try { if (window.speechSynthesis) CAMPUS_TOUR.paused ? window.speechSynthesis.pause() : window.speechSynthesis.resume(); } catch (e) {}
  };
}
if (document.getElementById("btn-tg-voice")) {
  document.getElementById("btn-tg-voice").onclick = () => {
    CAMPUS_TOUR.voiceOn = !CAMPUS_TOUR.voiceOn;
    document.getElementById("btn-tg-voice").textContent = CAMPUS_TOUR.voiceOn ? "Voice: ON" : "Voice: OFF";
    if (!CAMPUS_TOUR.voiceOn) { try { window.speechSynthesis.cancel(); } catch (e) {} }
    else if (CAMPUS_TOUR.state === "riding") announceCurrentStop();
  };
}
if (document.getElementById("btn-tg-next")) {
  document.getElementById("btn-tg-next").onclick = () => {
    if (CAMPUS_TOUR.state === "aerial") { boardTourBuggyNow(); return; }
    if (CAMPUS_TOUR.state !== "riding") return;
    if (CAMPUS_TOUR.stopIdx < AU_TOUR_STOPS.length - 1) {
      CAMPUS_TOUR.stopIdx++;
      CAMPUS_TOUR.wpIdx = 0;
      CAMPUS_TOUR.holdTimer = 0;
      announceCurrentStop();
    } else {
      CAMPUS_TOUR.state = "done";
      if (document.getElementById("tour-complete-overlay")) document.getElementById("tour-complete-overlay").classList.add("show");
    }
  };
}
if (document.getElementById("btn-tg-replay")) document.getElementById("btn-tg-replay").onclick = () => startGuidedCampusTour();
if (document.getElementById("btn-tg-exit")) document.getElementById("btn-tg-exit").onclick = () => exitGuidedTourToExplore();
if (document.getElementById("btn-tc-replay")) document.getElementById("btn-tc-replay").onclick = () => startGuidedCampusTour();
if (document.getElementById("btn-tc-explore")) document.getElementById("btn-tc-explore").onclick = () => exitGuidedTourToExplore();

// Hook "Start Campus Tour" (#walk) button cleanly to launch Aerial Flyover -> Buggy Tour!
const _walkBtn = document.getElementById("walk");
if (_walkBtn) {
  _walkBtn.addEventListener("click", () => {
    setTimeout(() => startGuidedCampusTour(), 60);
  });
}

// Mouse drag 360° free-look while riding inside the buggy on PC!
let _tourDragging = false, _tourLastX = 0, _tourLastY = 0;
window.addEventListener("mousedown", (e) => { if (CAMPUS_TOUR.state === "riding" && e.target.tagName === "CANVAS") { _tourDragging = true; _tourLastX = e.clientX; _tourLastY = e.clientY; } });
window.addEventListener("mouseup", () => { _tourDragging = false; });
window.addEventListener("mousemove", (e) => {
  if (CAMPUS_TOUR.state !== "riding") return;
  if (_tourDragging || document.pointerLockElement) {
    const dx = document.pointerLockElement ? e.movementX : (e.clientX - _tourLastX);
    const dy = document.pointerLockElement ? e.movementY : (e.clientY - _tourLastY);
    _tourLastX = e.clientX; _tourLastY = e.clientY;
    CAMPUS_TOUR.freeYawOffset -= dx * 0.0032;
    CAMPUS_TOUR.freePitch = Math.max(-0.45, Math.min(0.55, CAMPUS_TOUR.freePitch - dy * 0.0025));
  }
});

// Per-Frame Campus Tour Ticker (called inside Three.js Ye.setAnimationLoop -> works at 72-90 FPS on BOTH PC & Meta Quest 3 VR!)
window._tickCampusTour = function(dt) {
  const safeDt = Math.min(0.08, Math.max(0.001, dt || 0.016));
  if (CAMPUS_TOUR.state === "idle" || CAMPUS_TOUR.state === "done" || CAMPUS_TOUR.paused) return;

  if (CAMPUS_TOUR.state === "aerial") {
    CAMPUS_TOUR.aerialTime += safeDt;
    const t = Math.min(1, CAMPUS_TOUR.aerialTime / CAMPUS_TOUR.aerialDur);
    if (document.getElementById("intro-progress-fill")) document.getElementById("intro-progress-fill").style.width = `${(t * 100).toFixed(1)}%`;
    const sm = (x) => x * x * (3 - 2 * x);
    let cx, cy, cz, lx, ly, lz;
    if (t < 0.45) {
      const u = sm(t / 0.45);
      cx = so.lerp(62, -48, u); cy = so.lerp(52, 34, u); cz = so.lerp(-36, 36, u);
      lx = so.lerp(0, -3, u); ly = so.lerp(4, 5, u); lz = so.lerp(-6, 8, u);
    } else if (t < 0.78) {
      const u = sm((t - 0.45) / 0.33);
      cx = so.lerp(-48, 10, u); cy = so.lerp(34, 14, u); cz = so.lerp(36, 76, u);
      lx = so.lerp(-3, -3, u); ly = so.lerp(5, 3.5, u); lz = so.lerp(8, 22, u);
    } else {
      const u = sm((t - 0.78) / 0.22);
      cx = so.lerp(10, -2.72, u); cy = so.lerp(14, 1.56, u); cz = so.lerp(76, 66.85, u);
      lx = -3; ly = so.lerp(3.5, 1.8, u); lz = so.lerp(22, 30, u);
    }
    if (Ye.xr.isPresenting) {
      xt.position.set(cx, Math.max(0, cy - 1.6), cz);
      xt.rotation.set(0, 0, 0);
    } else {
      xt.position.set(cx, cy - 1.66, cz);
      xt.rotation.set(0, 0, 0);
      camPivot.position.set(0, 1.66, 0);
      camPivot.rotation.set(0, 0, 0);
      Mi.position.set(0, 0, 0);
      Mi.lookAt(lx, ly, lz);
    }
    if (typeof fpHands !== "undefined") fpHands.forEach(a => (a.root.visible = false));
    if (CAMPUS_TOUR.aerialTime >= CAMPUS_TOUR.aerialDur) boardTourBuggyNow();
    return;
  }

  if (CAMPUS_TOUR.state === "riding") {
    const stop = AU_TOUR_STOPS[CAMPUS_TOUR.stopIdx];
    if (!stop) return;
    const wp = stop.path[CAMPUS_TOUR.wpIdx];
    const tx = wp[0], tz = wp[1];
    const dx = tx - CAMPUS_TOUR.buggyPos.x;
    const dz = tz - CAMPUS_TOUR.buggyPos.z;
    const dist = Math.hypot(dx, dz);

    let moved = 0;
    if (dist > 0.35) {
      // Smoothly steer along the road toward the next road waypoint
      const targetYaw = Math.atan2(-dx, -dz);
      let dYaw = targetYaw - CAMPUS_TOUR.buggyYaw;
      while (dYaw > Math.PI) dYaw -= Math.PI * 2;
      while (dYaw < -Math.PI) dYaw += Math.PI * 2;
      CAMPUS_TOUR.buggyYaw += dYaw * Math.min(1, safeDt * 3.8);
      const stepDist = Math.min(dist, CAMPUS_TOUR.speed * safeDt);
      CAMPUS_TOUR.buggyPos.x += (dx / dist) * stepDist;
      CAMPUS_TOUR.buggyPos.z += (dz / dist) * stepDist;
      moved = stepDist;
      // Gently decay free-look offset slightly only if not dragging so user sees road ahead
    } else {
      // Reached waypoint!
      if (CAMPUS_TOUR.wpIdx < stop.path.length - 1) {
        CAMPUS_TOUR.wpIdx++;
      } else {
        // Showcase pause at the landmark while Tour Guide speaks!
        CAMPUS_TOUR.holdTimer += safeDt;
        const stillSpeaking = window.speechSynthesis && window.speechSynthesis.speaking && CAMPUS_TOUR.voiceOn;
        if (CAMPUS_TOUR.holdTimer >= stop.holdSec && (!stillSpeaking || CAMPUS_TOUR.holdTimer >= stop.holdSec + 10.0)) {
          if (CAMPUS_TOUR.stopIdx < AU_TOUR_STOPS.length - 1) {
            CAMPUS_TOUR.stopIdx++;
            CAMPUS_TOUR.wpIdx = 0;
            CAMPUS_TOUR.holdTimer = 0;
            announceCurrentStop();
          } else {
            CAMPUS_TOUR.state = "done";
            if (document.getElementById("tour-complete-overlay")) document.getElementById("tour-complete-overlay").classList.add("show");
            return;
          }
        }
      }
    }

    // Update 3D Buggy Position, Heading & Spinning Wheels!
    const gy = groundAt(CAMPUS_TOUR.buggyPos.x, CAMPUS_TOUR.buggyPos.z);
    CAMPUS_TOUR.buggyPos.y = gy;
    if (CAMPUS_TOUR.buggy) {
      CAMPUS_TOUR.buggy.position.copy(CAMPUS_TOUR.buggyPos);
      CAMPUS_TOUR.buggy.rotation.set(0, CAMPUS_TOUR.buggyYaw, 0);
      for (const w of CAMPUS_TOUR.wheels) w.rotation.x -= moved / 0.29;
    }

    // Seat the player comfortably in the front passenger seat of the golf cart!
    const seatLocal = new A(0.32, 0, -0.05).applyAxisAngle(new A(0, 1, 0), CAMPUS_TOUR.buggyYaw);
    const sx = CAMPUS_TOUR.buggyPos.x + seatLocal.x;
    const sz = CAMPUS_TOUR.buggyPos.z + seatLocal.z;
    if (Ye.xr.isPresenting) {
      // In Meta Quest 3 VR: move rig smoothly with buggy, keep headset rotation 100% user-controlled for comfort!
      xt.position.set(sx, gy + 0.15, sz);
      xt.rotation.set(0, CAMPUS_TOUR.buggyYaw, 0);
    } else {
      xt.position.set(sx, gy - 0.12, sz);
      xt.rotation.set(0, CAMPUS_TOUR.buggyYaw + CAMPUS_TOUR.freeYawOffset, 0);
      camPivot.position.set(0, 1.66, 0);
      camPivot.rotation.set(CAMPUS_TOUR.freePitch, 0, 0);
      Mi.position.set(0, 0, 0);
      Mi.rotation.set(0, 0, 0);
    }
    if (typeof fpHands !== "undefined") fpHands.forEach(a => (a.root.visible = false));
  }
};

// ============================================================================
// LIVING ANURAG UNIVERSITY CAMPUS POPULATION (STUDENTS WITH BACKPACKS & IDs + FORMAL FACULTY)
// Reuses our articulated human rig (hips, knees, shoulders, elbows, swinging AU ID cards)
// with natural skin tones, backpacks, walking friend groups, and gesturing conversation circles!
// ============================================================================
(function() {
  const SKIN_TONES = [0xd8a175, 0xc68b59, 0xe2ae84, 0xb57a4c, 0xe8ba96, 0x9e6942];
  const STUDENT_TOPS = [0x1e3a8a, 0xf8fafc, 0x334155, 0x991b1b, 0x166534, 0x0284c7, 0xd97706, 0x4c1d95, 0xbe185d, 0x0f766e];
  const STUDENT_PANTS = [0x1e293b, 0x26354d, 0x374151, 0x1f2937, 0x4b5563];
  const BAG_COLORS = [0x111827, 0x1e3a8a, 0x7f1d1d, 0x14532d, 0x374151, 0x0f766e];
  const FACULTY_SHIRTS = [0xf8fafc, 0xdbeafe, 0xe2e8f0, 0xfef3c7, 0xf1f5f9];
  const FACULTY_SUITS = [0x1e293b, 0x1f2937, 0x312e81, 0x3f3f46];

  // Cached crisp Student & Faculty Anurag University ID Card textures
  function makeCampusIdTex(isFaculty) {
    const c = document.createElement("canvas"); c.width = 128; c.height = 176;
    const g = c.getContext("2d");
    g.fillStyle = "#ffffff"; g.fillRect(0, 0, 128, 176);
    g.fillStyle = isFaculty ? "#b91c1c" : "#1d4ed8";
    g.fillRect(0, 0, 128, 38);
    g.fillStyle = "#ffffff"; g.font = "900 13px sans-serif"; g.textAlign = "center";
    g.fillText("ANURAG UNIV", 64, 17);
    g.font = "700 10px sans-serif";
    g.fillText(isFaculty ? "FACULTY ID" : "STUDENT ID", 64, 32);
    // Portrait photo silhouette
    g.fillStyle = "#e2e8f0"; g.fillRect(36, 48, 56, 56);
    g.fillStyle = "#475569"; g.beginPath(); g.arc(64, 68, 13, 0, Math.PI * 2); g.fill();
    g.beginPath(); g.arc(64, 102, 20, Math.PI, 0); g.fill();
    // Name bar & barcode
    g.fillStyle = isFaculty ? "#991b1b" : "#1e40af";
    g.fillRect(14, 114, 100, 22);
    g.fillStyle = "#ffffff"; g.font = "800 12px sans-serif";
    g.fillText(isFaculty ? "PROFESSOR" : "B.TECH / AU", 64, 129);
    g.fillStyle = "#111827";
    for (let bx = 20; bx < 108; bx += 5) g.fillRect(bx, 146, (bx % 3 === 0 ? 3 : 1.5), 18);
    const t = new dn(c); t.colorSpace = vt;
    return t;
  }
  const studentIdMat = new Jt({ map: makeCampusIdTex(false), roughness: 0.35, side: Gt });
  const facultyIdMat = new Jt({ map: makeCampusIdTex(true), roughness: 0.35, side: Gt });
  const eyeWhiteMat = new Jt({ color: 0xf8fafc, roughness: 0.3 });
  const pupilMat = new Jt({ color: 0x111827, roughness: 0.2 });
  const hairDarkMat = new Jt({ color: 0x181512, roughness: 0.85 });
  const shoeDarkMat = new Jt({ color: 0x181a1f, roughness: 0.65 });
  const sneakerMat = new Jt({ color: 0xe5e7eb, roughness: 0.72 });
  const beltMat = new Jt({ color: 0x1f1916, roughness: 0.5 });

  let npcSeed = 777;
  function nRand() { npcSeed = (npcSeed * 16807) % 2147483647; return (npcSeed - 1) / 2147483646; }
  function pick(arr) { return arr[Math.floor(nRand() * arr.length)]; }

  // Build Articulated Human Student or Faculty Member (reusing our stylized human rig!)
  function createCampusHuman(role, x, z, yaw = 0) {
    const isFaculty = role === "faculty";
    const isFemale = nRand() > 0.52;
    const sc = isFaculty ? (0.98 + nRand() * 0.08) : (0.92 + nRand() * 0.09);

    const skinMat = new Jt({ color: pick(SKIN_TONES), roughness: 0.72 });
    const topCol = isFaculty ? pick(FACULTY_SHIRTS) : pick(STUDENT_TOPS);
    const topMat = new Jt({ color: topCol, roughness: 0.68 });
    const pantMat = new Jt({ color: isFaculty ? pick(FACULTY_SUITS) : pick(STUDENT_PANTS), roughness: 0.78 });
    const tieMat = new Jt({ color: isFaculty ? (nRand() > 0.5 ? 0x991b1b : 0x1e3a8a) : 0x334155, roughness: 0.55 });
    const lanyardMat = new Jt({ color: isFaculty ? 0xb91c1c : 0x1d4ed8, roughness: 0.6 });

    const root = new fi();
    root.position.set(x, groundAt(x, z), z);
    root.rotation.y = yaw;
    root.scale.setScalar(sc);

    const pelvis = new fi(); pelvis.position.y = 0.90; root.add(pelvis);

    // Formal/Casual Torso + Collar + Belt
    const torso = new et(new sa(0.155, 0.27, 6, 12), topMat);
    torso.scale.set(1.22, 1.0, 0.80); torso.position.y = 0.30; torso.castShadow = true; pelvis.add(torso);
    const belt = new et(new pn(0.165, 0.165, 0.052, 12), beltMat);
    belt.scale.set(1.18, 1.0, 0.82); belt.position.y = 0.05; pelvis.add(belt);
    const collar = new et(new pn(0.088, 0.102, 0.06, 10), new Jt({ color: 0xf8fafc, roughness: 0.6 }));
    collar.position.y = 0.56; pelvis.add(collar);

    // Faculty Formal Blazer Lapels & Tie (or Book/Folder)
    if (isFaculty) {
      const hasBlazer = nRand() > 0.35;
      if (hasBlazer) {
        const blazerMat = pantMat;
        for (let sx of [-0.115, 0.115]) {
          let lapel = new et(new Ni(0.085, 0.44, 0.19), blazerMat);
          lapel.position.set(sx, 0.30, 0.02); pelvis.add(lapel);
        }
      }
      const tie = new et(new Ni(0.036, 0.25, 0.016), tieMat);
      tie.position.set(0, 0.39, 0.135); pelvis.add(tie);
    }

    // Swinging Anurag University Lanyard & ID Card (BOTH Students AND Faculty!)
    const idPivot = new fi(); idPivot.position.set(0, 0.54, 0.132); pelvis.add(idPivot);
    for (let sx of [-0.045, 0.045]) {
      let strap = new et(new Ni(0.012, 0.22, 0.006), lanyardMat);
      strap.position.set(sx * 0.55, -0.10, 0); strap.rotation.z = sx > 0 ? 0.22 : -0.22; idPivot.add(strap);
    }
    const idCard = new et(new _i(0.072, 0.102), isFaculty ? facultyIdMat : studentIdMat);
    idCard.position.set(0, -0.24, 0.005); idPivot.add(idCard);

    // Detailed 3D College Backpack for Students (Padded body + Front Pocket + Dual Shoulder Straps!)
    if (!isFaculty) {
      const bagMat = new Jt({ color: pick(BAG_COLORS), roughness: 0.78 });
      const bagPack = new et(new Ni(0.27, 0.36, 0.14), bagMat);
      bagPack.position.set(0, 0.31, -0.175); bagPack.castShadow = true; pelvis.add(bagPack);
      const bagPocket = new et(new Ni(0.21, 0.16, 0.05), new Jt({ color: 0x0f172a, roughness: 0.75 }));
      bagPocket.position.set(0, 0.23, -0.255); pelvis.add(bagPocket);
      for (let sx of [-0.11, 0.11]) {
        let sStrap = new et(new Ni(0.036, 0.34, 0.22), bagMat);
        sStrap.position.set(sx, 0.36, -0.02); pelvis.add(sStrap);
      }
    }

    // Neck & Expressive Friendly Human Head + Hair
    const neck = new et(new pn(0.052, 0.06, 0.08, 10), skinMat); neck.position.y = 0.61; pelvis.add(neck);
    const headPivot = new fi(); headPivot.position.y = 0.73; pelvis.add(headPivot);
    const head = new et(new fn(0.135, 14, 12), skinMat); head.scale.set(0.95, 1.08, 0.98); head.castShadow = true; headPivot.add(head);
    // Hair cap + optional female ponytail/bun
    const hair = new et(new fn(0.142, 12, 10, 0, Math.PI * 2, 0, Math.PI * 0.56), hairDarkMat);
    hair.position.set(0, 0.025, -0.015); headPivot.add(hair);
    if (isFemale) {
      const bun = new et(new fn(0.068, 10, 8), hairDarkMat);
      bun.position.set(0, 0.0, -0.145); headPivot.add(bun);
    }
    // Natural Friendly Eyes & Warm Smile
    for (let sx of [-0.046, 0.046]) {
      let ew = new et(new fn(0.019, 8, 8), eyeWhiteMat); ew.position.set(sx, 0.022, 0.118); headPivot.add(ew);
      let ep = new et(new fn(0.010, 8, 8), pupilMat); ep.position.set(sx, 0.022, 0.132); headPivot.add(ep);
    }
    const smile = new et(new Ni(0.044, 0.008, 0.008), new Jt({ color: 0x7c3a2d, roughness: 0.7 }));
    smile.position.set(0, -0.042, 0.126); headPivot.add(smile);

    // Articulated Arms (Shoulders + Elbows + Hands; Faculty sometimes holds a folder/book!)
    const arms = [];
    for (let s of [-1, 1]) {
      const sh = new fi(); sh.position.set(s * 0.225, 0.50, 0); pelvis.add(sh);
      const uArm = new et(new sa(0.048, 0.20, 4, 8), topMat); uArm.position.y = -0.12; sh.add(uArm);
      const elb = new fi(); elb.position.y = -0.25; sh.add(elb);
      const fArm = new et(new sa(0.042, 0.19, 4, 8), isFaculty ? topMat : skinMat); fArm.position.y = -0.11; elb.add(fArm);
      const hand = new et(new fn(0.042, 8, 8), skinMat); hand.position.y = -0.23; elb.add(hand);
      if (isFaculty && s === 1) {
        const folder = new et(new Ni(0.04, 0.28, 0.22), new Jt({ color: 0x1e3a8a, roughness: 0.6 }));
        folder.position.set(0.02, -0.22, 0.06); elb.add(folder);
      }
      arms.push({ sh, elb, side: s });
    }

    // Articulated Legs (Hips + Knees + Dress Shoes / Sneakers)
    const legs = [];
    for (let s of [-1, 1]) {
      const hip = new fi(); hip.position.set(s * 0.095, 0.0, 0); pelvis.add(hip);
      const thigh = new et(new sa(0.064, 0.30, 4, 10), pantMat); thigh.position.y = -0.21; thigh.castShadow = true; hip.add(thigh);
      const knee = new fi(); knee.position.y = -0.43; hip.add(knee);
      const shin = new et(new sa(0.052, 0.30, 4, 10), pantMat); shin.position.y = -0.20; knee.add(shin);
      const shoe = new et(new Ni(0.095, 0.075, 0.21), isFaculty ? shoeDarkMat : (nRand() > 0.45 ? sneakerMat : shoeDarkMat));
      shoe.position.set(0, -0.42, 0.04); knee.add(shoe);
      legs.push({ hip, knee, side: s });
    }

    Ht.add(root);
    return { root, pelvis, headPivot, idPivot, arms, legs, role, phase: nRand() * Math.PI * 2 };
  }

  // --- POPULATE CAMPUS WITH WALKING FRIEND GROUPS, CONVERSATION CIRCLES & FORMAL FACULTY ---
  const walkingGroups = [];
  const talkingCircles = [];

  // 1. Walking Student Friend Groups (Pairs & Trios strolling side-by-side along footpaths & walkways!)
  const walkGroupSpecs = [
    // Main Entrance Avenue West & East footpaths
    { role: "student", count: 3, speed: 1.35, path: [[-10.2, 62], [-10.2, 30], [-10.2, 62]] },
    { role: "student", count: 2, speed: 1.45, path: [[4.4, 30], [4.4, 62], [4.4, 30]] },
    // A-Block <-> B/D-Block Palm-Lined Pathway
    { role: "student", count: 3, speed: 1.32, path: [[-31.2, 13], [-31.2, -20], [-31.2, 13]] },
    { role: "student", count: 2, speed: 1.40, path: [[-31.2, -18], [-31.2, 12], [-31.2, -18]] },
    // Wide 2-Lane East Avenue Footpaths (past G-Block, F-Block & E-Block!)
    { role: "student", count: 3, speed: 1.38, path: [[19.3, 24], [19.3, -24], [19.3, 24]] },
    { role: "student", count: 2, speed: 1.42, path: [[29.5, -24], [29.5, 20], [29.5, -24]] },
    // North Avenue (past Medicinal Garden & H-Block)
    { role: "student", count: 2, speed: 1.35, path: [[-14, -37], [-58, -37], [-14, -37]] },
    // West Avenue (past D-Block, B-Block & C-Block)
    { role: "student", count: 3, speed: 1.36, path: [[-69.5, -20], [-69.5, 22], [-69.5, -20]] },
    // Formal Faculty Strolling Between Academic Blocks!
    { role: "faculty", count: 2, speed: 1.25, path: [[19.4, -14], [19.4, 18], [19.4, -14]] },
    { role: "faculty", count: 1, speed: 1.22, path: [[-14, 21.5], [14, 21.5], [-14, 21.5]] },
    { role: "faculty", count: 1, speed: 1.20, path: [[-69.2, 14], [-69.2, -16], [-69.2, 14]] },
    { role: "faculty", count: 2, speed: 1.18, path: [[-56, 31], [-36, 31], [-56, 31]] }
  ];

  for (const spec of walkGroupSpecs) {
    const startP = spec.path[0];
    const members = [];
    for (let i = 0; i < spec.count; i++) {
      const lat = (i - (spec.count - 1) * 0.5) * 0.72;
      const h = createCampusHuman(spec.role, startP[0] + lat, startP[1], 0);
      members.push({ human: h, latOffset: lat, zOffset: (i % 2) * 0.25 });
    }
    walkingGroups.push({
      members,
      path: spec.path,
      wpIdx: 1,
      pos: new A(startP[0], 0, startP[1]),
      yaw: 0,
      speed: spec.speed
    });
  }

  // 2. Standing Conversation Circles (Students & Faculty talking, nodding & gesturing on Plazas!)
  const circleSpecs = [
    { cx: -8.5, cz: 20.5, roles: ["student", "student", "student"] },         // A-Block Front Plaza
    { cx: 4.5, cz: 20.5, roles: ["faculty", "student", "student"] },          // A-Block Faculty-Student Chat
    { cx: -3.0, cz: -2.0, roles: ["student", "student", "student", "student"] }, // A-Block Central Courtyard
    { cx: 28.0, cz: 10.5, roles: ["faculty", "faculty", "student"] },         // G-Block Admin Portico
    { cx: 27.6, cz: -17.5, roles: ["student", "student", "student"] },        // E-Block TEDxAnuragU Atrium
    { cx: -60.5, cz: -38.5, roles: ["student", "student", "student"] },       // H-Block Green Solar Tree Plaza
    { cx: -66.5, cz: -8.0, roles: ["student", "student", "faculty"] },        // D-Block Mural Plaza
    { cx: -41.5, cz: 46.5, roles: ["student", "student", "student"] },        // C-Block Basketball Plaza
    { cx: -78.5, cz: 59.5, roles: ["faculty", "student", "student"] }         // Dr. APJ Abdul Kalam Hall Plaza
  ];

  for (const cs of circleSpecs) {
    const n = cs.roles.length;
    const rad = n >= 4 ? 0.95 : 0.78;
    const people = [];
    for (let i = 0; i < n; i++) {
      const ang = (i / n) * Math.PI * 2 + 0.3;
      const px = cs.cx + Math.cos(ang) * rad;
      const pz = cs.cz + Math.sin(ang) * rad;
      const faceYaw = Math.atan2(cs.cx - px, cs.cz - pz);
      const h = createCampusHuman(cs.roles[i], px, pz, faceYaw);
      people.push({ human: h, baseYaw: faceYaw, talkSeed: i * 1.9 + cs.cx });
    }
    talkingCircles.push({ people });
  }

  // Animate All Campus Students & Faculty Every Frame inside Ye.setAnimationLoop (PC + Meta Quest 3 VR!)
  let popTime = 0;
  window._tickCampusPopulation = function(dt) {
    const safeDt = Math.min(0.06, Math.max(0.001, dt || 0.016));
    popTime += safeDt;

    // 1. Update Walking Friend Groups & Strolling Faculty
    for (const grp of walkingGroups) {
      const wp = grp.path[grp.wpIdx];
      const dx = wp[0] - grp.pos.x;
      const dz = wp[1] - grp.pos.z;
      const dist = Math.hypot(dx, dz);

      // Politely yield if the Tour Buggy is driving right beside them!
      let yielding = false;
      if (CAMPUS_TOUR.state === "riding" && CAMPUS_TOUR.buggyPos.distanceTo(grp.pos) < 3.6) {
        yielding = true;
      }

      if (!yielding) {
        if (dist < 0.4) {
          grp.wpIdx = (grp.wpIdx + 1) % grp.path.length;
        } else {
          const targetYaw = Math.atan2(dx, dz);
          let dYaw = targetYaw - grp.yaw;
          while (dYaw > Math.PI) dYaw -= Math.PI * 2;
          while (dYaw < -Math.PI) dYaw += Math.PI * 2;
          grp.yaw += dYaw * Math.min(1, safeDt * 5.0);
          const step = Math.min(dist, grp.speed * safeDt);
          grp.pos.x += (dx / dist) * step;
          grp.pos.z += (dz / dist) * step;
        }
      }

      const rightX = Math.cos(grp.yaw), rightZ = -Math.sin(grp.yaw);
      const fwdX = Math.sin(grp.yaw), fwdZ = Math.cos(grp.yaw);

      for (let mIdx = 0; mIdx < grp.members.length; mIdx++) {
        const m = grp.members[mIdx];
        const h = m.human;
        const mx = grp.pos.x + rightX * m.latOffset - fwdX * m.zOffset;
        const mz = grp.pos.z + rightZ * m.latOffset - fwdZ * m.zOffset;
        h.root.position.set(mx, groundAt(mx, mz), mz);
        h.root.rotation.y = grp.yaw;

        if (!yielding) {
          const t = popTime * 5.2 + h.phase;
          const stride = Math.sin(t);
          h.pelvis.position.y = 0.90 + Math.abs(stride) * 0.035;
          h.legs[0].hip.rotation.x = stride * 0.48;
          h.legs[1].hip.rotation.x = -stride * 0.48;
          h.legs[0].knee.rotation.x = Math.max(0, -stride * 0.55);
          h.legs[1].knee.rotation.x = Math.max(0, stride * 0.55);
          // Natural arm swing + occasional friend-chat glance!
          h.arms[0].sh.rotation.x = -stride * 0.36;
          h.arms[1].sh.rotation.x = stride * 0.36;
          h.arms[0].elb.rotation.x = -0.18;
          h.arms[1].elb.rotation.x = -0.18;
          h.idPivot.rotation.z = stride * 0.08;
          h.headPivot.rotation.y = grp.members.length > 1 ? Math.sin(popTime * 1.1 + mIdx * 2.1) * 0.28 : 0;
        } else {
          // Politely stand & glance at the passing Campus Tour Buggy
          h.legs[0].hip.rotation.x *= 0.85; h.legs[1].hip.rotation.x *= 0.85;
          h.arms[0].sh.rotation.x *= 0.85; h.arms[1].sh.rotation.x *= 0.85;
        }
      }
    }

    // 2. Update Standing Conversation Circles (Natural Talking, Nodding & Hand Gestures!)
    for (const circ of talkingCircles) {
      for (const p of circ.people) {
        const h = p.human;
        const t = popTime + p.talkSeed;
        const isSpeaking = Math.sin(t * 0.55) > 0.15;
        h.pelvis.position.y = 0.90 + Math.sin(t * 1.6) * 0.012;
        h.headPivot.rotation.x = isSpeaking ? Math.sin(t * 3.8) * 0.10 : Math.sin(t * 1.9) * 0.08;
        h.headPivot.rotation.y = Math.sin(t * 0.9) * 0.18;
        // Expressive hand gestures when speaking vs relaxed stance when listening
        if (isSpeaking) {
          h.arms[0].sh.rotation.x = -0.45 + Math.sin(t * 3.2) * 0.22;
          h.arms[0].elb.rotation.x = -0.75 + Math.cos(t * 3.2) * 0.2;
          h.arms[1].sh.rotation.x = -0.35 + Math.cos(t * 2.7) * 0.18;
          h.arms[1].elb.rotation.x = -0.65;
        } else {
          h.arms[0].sh.rotation.x = -0.08; h.arms[0].elb.rotation.x = -0.22;
          h.arms[1].sh.rotation.x = -0.08; h.arms[1].elb.rotation.x = -0.22;
        }
      }
    }
  };
})();
'''
    html = html.replace(
        '  if (window._tickRealisticShaders) window._tickRealisticShaders(e);',
        '  if (window._tickRealisticShaders) window._tickRealisticShaders(e);\n  if (window._tickCampusTour) window._tickCampusTour(e);\n  if (window._tickCampusPopulation) window._tickCampusPopulation(e);',
        1
    )
    html = html.replace(
        '// ============================================================================\n// BUILDING 9:',
        CAMPUS_TOUR_JS + '\n// ============================================================================\n// BUILDING 9:',
        1
    )
    if CAMPUS_TOUR_JS not in html:
        html = html.replace(
            '// ============================================================================\r\n// BUILDING 9:',
            CAMPUS_TOUR_JS + '\r\n// ============================================================================\r\n// BUILDING 9:',
            1
        )

with open(SRC_HTML, "w", encoding="utf-8") as f:
    f.write(html)

INDEX_HTML = os.path.join(ROOT, "index.html")
with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully built {SRC_HTML} and {INDEX_HTML} ({len(html):,} bytes)")

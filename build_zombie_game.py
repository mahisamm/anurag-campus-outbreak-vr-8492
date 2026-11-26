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

dblock_mural_uri = ""
if os.path.exists(MURAL_JPG):
    with open(MURAL_JPG, "rb") as mf:
        dblock_mural_uri = "data:image/jpeg;base64," + base64.b64encode(mf.read()).decode("ascii")

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
}
#intro-overlay.playing{display:block}
.cine-bar{
  position:fixed;left:0;right:0;height:10vh;background:#050910;
  transition:transform .5s ease;pointer-events:none;
}
#cine-top{top:0}
#cine-bot{bottom:0}
#intro-story-box{
  position:fixed;left:50%;bottom:13vh;transform:translateX(-50%);
  width:min(760px,90vw);padding:16px 26px;border-radius:14px;text-align:center;
  background:linear-gradient(160deg,rgba(8,18,30,0.88),rgba(24,10,16,0.86));
  border:1px solid rgba(114,239,221,0.45);box-shadow:0 14px 40px rgba(0,0,0,0.65);
  backdrop-filter:blur(10px);
}
#intro-kicker{font:800 12px/1.2 system-ui;color:#fbbf24;letter-spacing:2.2px;text-transform:uppercase;margin-bottom:5px}
#intro-headline{font:800 clamp(18px,2.5vw,28px)/1.2 Georgia,serif;color:#ffffff;letter-spacing:0.6px;margin:0}
#intro-sub{font:600 13px/1.4 system-ui;color:#a5d8ee;margin-top:6px}
#btn-skip-intro{
  position:fixed;right:22px;bottom:2.8vh;z-index:44;pointer-events:auto;
  padding:8px 18px;border-radius:8px;border:1px solid rgba(114,239,221,0.55);
  background:rgba(15,32,48,0.92);color:#e0f7fa;font:700 12.5px system-ui;cursor:pointer;
}
#btn-skip-intro:hover{background:#0ea5e9;color:#04151f}
.intro-active #combat-hud,.intro-active #top-left-hud,.intro-active #minimap-wrap,.intro-active #crosshair,.intro-active #hint{opacity:0 !important;pointer-events:none !important}
#wave-banner{
  position:fixed;top:14px;left:50%;transform:translateX(-50%);
  padding:8px 22px;border-radius:12px;text-align:center;
  background:linear-gradient(135deg,rgba(15,24,36,0.92),rgba(32,14,18,0.92));
  border:1px solid rgba(255,95,95,0.5);box-shadow:0 8px 26px rgba(0,0,0,0.55);
  backdrop-filter:blur(10px);
}
#wave-title{font:800 15px/1.2 'Segoe UI',system-ui,sans-serif;color:#ff6b6b;letter-spacing:1px;text-transform:uppercase}
#wave-sub{font:600 12px/1.3 'Segoe UI',system-ui,sans-serif;color:#e2f1fa;margin-top:2px}
#boss-bar-wrap{
  position:fixed;top:76px;left:50%;transform:translateX(-50%);width:min(460px,62vw);
  display:none;background:rgba(16,10,14,0.9);border:1px solid rgba(245,158,11,0.7);
  border-radius:10px;padding:7px 12px;box-shadow:0 8px 24px rgba(0,0,0,0.65);
}
#boss-bar-label{font:800 12px system-ui;color:#fbbf24;letter-spacing:1.2px;display:flex;justify-content:space-between;margin-bottom:5px}
#boss-bar-bg{height:12px;background:rgba(255,255,255,0.12);border-radius:6px;overflow:hidden}
#boss-bar-fill{height:100%;width:100%;background:linear-gradient(90deg,#dc2626,#f59e0b);transition:width .12s}
#top-hp-bar{
  position:fixed;top:52px;left:16px;z-index:26;width:255px;
  padding:8px 12px;border-radius:12px;
  background:rgba(12,20,30,0.92);border:1px solid rgba(248,113,113,0.52);
  box-shadow:0 8px 22px rgba(0,0,0,0.48);backdrop-filter:blur(10px);
}
#top-hp-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:5px}
#top-hp-left{display:flex;align-items:center;gap:7px}
#heart-icon{
  font-size:18px;line-height:1;color:#ff3b5c;
  text-shadow:0 0 10px rgba(255,59,92,0.85);
  display:inline-block;animation:heartPulse 1.4s ease-in-out infinite;
}
#top-hp-bar.low-hp #heart-icon{animation:heartPulse 0.45s ease-in-out infinite;color:#ff1e38}
#top-hp-hearts{font-size:13px;letter-spacing:2px;color:#ff4d6d;text-shadow:0 0 6px rgba(255,77,109,0.6)}
#top-hp-num{font:800 12.5px 'Consolas',monospace;color:#fef2f2}
#top-hp-track{height:10px;background:rgba(255,255,255,0.14);border-radius:6px;overflow:hidden}
#top-hp-fill{height:100%;width:100%;background:linear-gradient(90deg,#ef4444,#f97316,#22c55e);transition:width .14s}
@keyframes heartPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.22)}}
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
  </div>
  <div id="wave-banner">
    <div id="wave-title">LEVEL 1 · LAB ASSISTANTS</div>
    <div id="wave-sub">Zombies Remaining: 6 · Score: 0</div>
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
  <div id="intro-story-box">
    <div id="intro-kicker">ANURAG UNIVERSITY · EMERGENCY BROADCAST</div>
    <h2 id="intro-headline">WELCOME TO ANURAG UNIVERSITY</h2>
    <div id="intro-sub">Venkatapur Campus · Aerial Reconnaissance</div>
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
    weaponMount = new fi();
    weaponMount.position.set(0.0, -0.004, -0.048);
    wristPivot.add(weaponMount);

    let hiltMat = new Jt({ color: 0xb0bac7, roughness: 0.24, metalness: 0.85 });
    let gunDarkMat = new Jt({ color: 0x2c3644, emissive: 0x0a1018, emissiveIntensity: 0.35, roughness: 0.35, metalness: 0.72 });
    let gunAccentMat = new Jt({ color: 0x475569, emissive: 0x0c131c, emissiveIntensity: 0.3, roughness: 0.42, metalness: 0.62 });
    let rodMat = new Jt({ color: 0x5c473e, roughness: 0.56, metalness: 0.72 });
    let branchMat = new Jt({ color: 0x523720, roughness: 0.9, metalness: 0.02 });

    // 0: Plasma Lightsaber — Triple-Layer Pulsing Plasma Blade + Emitter Flare + Ignition Animation
    let saberGrp = new fi();
    saberGrp.position.set(0, -0.018, -0.022);
    saberGrp.rotation.set(-0.55, 0, 0);
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

    // 1: Tactical 9mm Pistol
    let pistolGrp = new fi();
    pistolGrp.position.set(0, 0.015, -0.01);
    let pistolMesh = blenderGeos.pistol
      ? new et(blenderGeos.pistol, gunDarkMat)
      : new et(new Ni(0.032, 0.12, 0.2), gunDarkMat);
    pistolGrp.add(pistolMesh);
    let pSight = new et(new Ni(0.006, 0.006, 0.006), new Yi({ color: 0x22c55e }));
    pSight.position.set(0, 0.075, -0.145);
    pistolGrp.add(pSight);
    weaponMount.add(pistolGrp);

    // 2: Pulse Assault Rifle
    let rifleGrp = new fi();
    rifleGrp.position.set(0, 0.018, -0.02);
    let rifleMesh = blenderGeos.assault_rifle
      ? new et(blenderGeos.assault_rifle, gunDarkMat)
      : new et(new Ni(0.045, 0.14, 0.58), gunDarkMat);
    rifleGrp.add(rifleMesh);
    let redDot = new et(new fn(0.005, 8, 8), new Yi({ color: 0xff3b30 }));
    redDot.position.set(0, 0.10, -0.065);
    rifleGrp.add(redDot);
    weaponMount.add(rifleGrp);

    // 3: Combat Shotgun
    let shotGrp = new fi();
    shotGrp.position.set(0, 0.018, -0.02);
    let shotMesh = blenderGeos.shotgun
      ? new et(blenderGeos.shotgun, gunAccentMat)
      : new et(new Ni(0.048, 0.13, 0.62), gunAccentMat);
    shotGrp.add(shotMesh);
    weaponMount.add(shotGrp);

    // 4: Campus Iron Rod Pickup (distinct melee club grip)
    let rodGrp = new fi();
    rodGrp.position.set(0, -0.018, -0.022);
    rodGrp.rotation.set(-0.55, 0, 0);
    let rodMesh = blenderGeos.iron_rod
      ? new et(blenderGeos.iron_rod, rodMat)
      : new et(new pn(0.014, 0.014, 0.95, 10), rodMat);
    rodGrp.add(rodMesh);
    weaponMount.add(rodGrp);

    // 5: Campus Fallen Branch Pickup (distinct melee club grip)
    let branchGrp = new fi();
    branchGrp.position.set(0, -0.018, -0.022);
    branchGrp.rotation.set(-0.55, 0, 0);
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
  const c = document.createElement("canvas"); c.width = 1024; c.height = 256;
  const g = c.getContext("2d");
  g.fillStyle = "rgba(8,18,30,0.92)"; g.fillRect(0, 0, 1024, 256);
  g.strokeStyle = "#72efdd"; g.lineWidth = 6; g.strokeRect(6, 6, 1012, 244);
  g.fillStyle = "#fbbf24"; g.font = "bold 28px sans-serif"; g.textAlign = "center";
  g.fillText("WELCOME TO ANURAG UNIVERSITY", 512, 68);
  g.fillStyle = "#ffffff"; g.font = "bold 42px sans-serif";
  g.fillText("SAVE YOURSELF FROM THE INFECTED FACULTY!", 512, 138);
  g.fillStyle = "#a5d8ee"; g.font = "26px sans-serif";
  g.fillText("Press A to Skip  ·  Swing Saber / Fire Guns / Right-Trigger for Shield", 512, 206);
  const tex = new dn(c); tex.colorSpace = vt;
  const mesh = new et(new _i(3.8, 0.95), new Yi({ map: tex, transparent: true, side: Gt }));
  mesh.position.set(0, 2.0, -4.2);
  xt.add(mesh);
  ZGAME.vrStoryBanner = mesh;
  return mesh;
}

function startStoryIntro() {
  ZGAME.introPlaying = true;
  ZGAME.introTime = 0;
  document.body.classList.add("intro-active");
  if (kt("intro-overlay")) kt("intro-overlay").classList.add("playing");
  // Hide 1st-person hands during aerial flyover
  fpHands.forEach(a => (a.root.visible = false));
  if (Ye.xr.isPresenting) {
    createVRStoryBanner().visible = true;
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
  playSFX("saber");
  showToast("ENTER THE CAMPUS GATE TO START LEVEL 1!", 2.8);
}

if (kt("btn-skip-intro")) kt("btn-skip-intro").onclick = () => finishStoryIntro();

function updateStoryIntro(dt) {
  if (!ZGAME.introPlaying) return false;
  ZGAME.introTime += dt;
  const t = Math.min(1, ZGAME.introTime / ZGAME.introDur);

  // Update cinematic story captions
  let beat = INTRO_BEATS[0];
  for (const b of INTRO_BEATS) { if (ZGAME.introTime >= b.t) beat = b; }
  if (kt("intro-kicker")) kt("intro-kicker").textContent = beat.kicker;
  if (kt("intro-headline")) kt("intro-headline").textContent = beat.head;
  if (kt("intro-sub")) kt("intro-sub").textContent = beat.sub;

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
  clearZombiesAndFX();
  for (const p of ZGAME.pickups) Ht.remove(p.root);
  ZGAME.pickups.length = 0;
  document.body.classList.remove("zombie-mode");
}

function syncWeaponVisuals() {
  const showCombat = bo.value === "zombie";
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

  // Compute real world-space hilt & blade-tip positions along the sword/rod/branch melee axis (-0.55 rad)
  const mount = hand.arm.weaponMount;
  if (!mount) return;
  mount.updateWorldMatrix(true, false);
  const hiltWorld = new A(0, -0.01, -0.02).applyMatrix4(mount.matrixWorld);
  const tipLocal = new A(0, 0.90, -0.58);
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
    kt("wave-sub").textContent = "Walk forward inside the campus to begin Phase 1 (2:00 Survival)!";
  } else {
    kt("wave-title").textContent = lvl.isBoss ? "FINAL BOSS · DEFEAT THE CEO" : `LEVEL ${lvl.level} · ${lvl.name.toUpperCase()}`;
    kt("wave-sub").textContent = lvl.isBoss
      ? `Active Enemies: ${aliveCount} · Kills: ${ZGAME.kills} · Score: ${ZGAME.score}`
      : `SURVIVE: ${formatTimer(ZGAME.phaseTimer)} · Active: ${aliveCount} · Kills: ${ZGAME.kills} · Score: ${ZGAME.score}`;
  }
  const hpPct = Math.max(0, (ZGAME.hp / ZGAME.maxHp) * 100);
  const hpTxt = `${Math.ceil(ZGAME.hp)} / ${ZGAME.maxHp}`;
  kt("hp-val").textContent = hpTxt;
  kt("hp-fill").style.width = `${hpPct}%`;
  // Top-Left Heart Health Bar update!
  if (kt("top-hp-num")) kt("top-hp-num").textContent = hpTxt;
  if (kt("top-hp-fill")) kt("top-hp-fill").style.width = `${hpPct}%`;
  if (kt("top-hp-hearts")) {
    const filled = Math.max(0, Math.min(5, Math.ceil(ZGAME.hp / 20)));
    kt("top-hp-hearts").textContent = "♥".repeat(filled) + "♡".repeat(5 - filled);
  }
  if (kt("top-hp-bar")) kt("top-hp-bar").classList.toggle("low-hp", ZGAME.hp <= 35);
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
      // Distinct ergonomic VR hand pose for Guns (index finger on trigger) vs Lightsaber/Rod/Branch (full sword fist grip!)
      if(side==="right"){
        const curW = WEAPON_DEFS[ZGAME.weaponIdx];
        const isMelee = curW && curW.type === "melee";
        arm.fingers.forEach((finger,i)=>{
          const c = (!isMelee && i===0) ? (0.28 + trigger*0.65) : Math.max(0.92, grip);
          finger.fRoot.rotation.x=-(.14+c*.95);
          finger.j2.rotation.x=-(.15+c*1.05);
          finger.j3.rotation.x=-(.08+c*.72);
        });
        arm.thumbRoot.rotation.set(isMelee ? -.42 : -.24, .88, -.28);
        arm.thumbJ2.rotation.x = isMelee ? -.52 : -.28;
        // Distinct slight wrist cant for melee sword swing vs dead-straight gun sight alignment
        if(arm.wristPivot) arm.wristPivot.rotation.set(isMelee ? -0.18 : 0, 0, 0);
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

# Align VR hands straight along targetRaySpace (-Z forward, relaxed natural wrist roll, zero bend needed!)
html = html.replace(
    '  arm.root.position.set(0,.012,.046);\n  arm.root.rotation.z=sign*.72;',
    '  arm.root.position.set(0,-.016,.092);\n  arm.root.rotation.set(0, 0, sign*.14);',
    1
)
html = html.replace(
    '  arm.root.position.set(0,.012,.046);\r\n  arm.root.rotation.z=sign*.72;',
    '  arm.root.position.set(0,-.016,.092);\r\n  arm.root.rotation.set(0, 0, sign*.14);',
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
        arm.wristPivot.rotation.set(0, 0, 0);
        arm.setFingerCurl(0.82, false);
      }
      return;
    }
    if (side === 1 && handGadgetMode === 1) {"""
html = html.replace(FP_HAND_ANCHOR, FP_COMBAT_JS, 1)

# 7i. Call updateZombieGame(e, timeSec) inside main animation loop
TICK_ANCHOR = '  updateNavRoute(xt.position.x, xt.position.z, timeSec);'
assert TICK_ANCHOR in html
html = html.replace(TICK_ANCHOR, '  updateZombieGame(e, timeSec);\n  updateNavRoute(xt.position.x, xt.position.z, timeSec);', 1)

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

with open(SRC_HTML, "w", encoding="utf-8") as f:
    f.write(html)

INDEX_HTML = os.path.join(ROOT, "index.html")
with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully built {SRC_HTML} and {INDEX_HTML} ({len(html):,} bytes)")

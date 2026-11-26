"""
Injects the Blender 5.3 zombie/weapon assets and the full 6-level First-Person & Meta Quest 3 VR
Zombie Outbreak game engine into Play-PC.html (creating a backup of the original Explorer first).
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_HTML = os.path.join(ROOT, "Play-PC.html")
BACKUP_HTML = os.path.join(ROOT, "Play-PC-Explorer-Backup.html")
ASSETS_JSON = os.path.join(ROOT, "zombie_assets.json")
HUMAN_JSON = os.path.join(ROOT, "human_zombie_meshes.json")

# Make sure we always patch from the clean original Explorer backup if it exists
if not os.path.exists(BACKUP_HTML):
    shutil.copy2(SRC_HTML, BACKUP_HTML)
    print("Backed up original Play-PC.html -> Play-PC-Explorer-Backup.html")

with open(BACKUP_HTML, "r", encoding="utf-8") as f:
    html = f.read()

with open(ASSETS_JSON, "r", encoding="utf-8") as f:
    zombie_assets = json.load(f)
if os.path.exists(HUMAN_JSON):
    with open(HUMAN_JSON, "r", encoding="utf-8") as f:
        zombie_assets.update(json.load(f))

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
  background:rgba(6,12,20,0.78);backdrop-filter:blur(8px);pointer-events:auto;
}
#end-card{
  width:min(420px,90vw);padding:26px 28px;border-radius:16px;text-align:center;
  background:linear-gradient(160deg,rgba(14,28,42,0.98),rgba(24,16,24,0.96));
  border:1px solid rgba(114,239,221,0.5);box-shadow:0 20px 55px rgba(0,0,0,0.7);
}
#end-title{font:800 26px/1.2 system-ui;color:#ff6b6b;margin:0 0 8px}
#end-stats{font:600 14px/1.7 system-ui;color:#d6edf8;margin:12px 0 20px}
#btn-restart-game{
  padding:11px 26px;border-radius:10px;border:none;cursor:pointer;
  background:linear-gradient(135deg,#0ea5e9,#14b8a6);color:#04151f;font:800 15px system-ui;
}
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
      <div class="vital-lbl"><span>HI-TECH SHIELD [RMB / R-TRIG]</span><span id="shield-val">100%</span></div>
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
      <h2 id="end-title">OVERRUN!</h2>
      <div id="end-stats"></div>
      <button id="btn-restart-game">Play Again [R]</button>
    </div>
  </div>
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
    // Sleek Hi-Tech Wrist Shield Projector (never blocks view when stowed!)
    let emitterMat = new Jt({ color: 0x1e293b, emissive: 0x0c2438, emissiveIntensity: 0.5, roughness: 0.25, metalness: 0.85 });
    let emitterBase = new et(new Ni(0.065, 0.022, 0.085), emitterMat);
    emitterBase.position.set(-0.022, 0.018, -0.02);
    wristPivot.add(emitterBase);
    let emitterCore = new et(new fn(0.016, 12, 10), new Yi({ color: 0x38bdf8 }));
    emitterCore.position.set(-0.022, 0.032, -0.02);
    wristPivot.add(emitterCore);

    // Deployable Transparent Hi-Tech Holographic Hex-Grid Shield (opens on trigger / RMB)
    shieldGroup = new fi();
    shieldGroup.position.set(-0.02, 0.02, -0.095);
    shieldGroup.rotation.set(0.05, 0.06, 0.0);
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

    // 0: Plasma Lightsaber
    let saberGrp = new fi();
    saberGrp.rotation.set(-0.32, 0, 0);
    let hiltMesh = blenderGeos.lightsaber_hilt
      ? new et(blenderGeos.lightsaber_hilt, hiltMat)
      : new et(new pn(0.018, 0.018, 0.24, 14), hiltMat);
    saberGrp.add(hiltMesh);
    let bladeOuterMat = new Yi({ color: 0x22d3ee, transparent: true, opacity: 0.82 });
    let bladeCoreMat = new Yi({ color: 0xe0faff });
    saberBlade = new et(new pn(0.015, 0.011, 0.96, 14), bladeOuterMat);
    saberBlade.position.set(0, 0.63, 0);
    saberGrp.add(saberBlade);
    saberCore = new et(new pn(0.007, 0.005, 0.94, 10), bladeCoreMat);
    saberCore.position.set(0, 0.63, 0);
    saberGrp.add(saberCore);
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

    // 4: Campus Iron Rod Pickup
    let rodGrp = new fi();
    rodGrp.rotation.set(-0.34, 0, 0);
    let rodMesh = blenderGeos.iron_rod
      ? new et(blenderGeos.iron_rod, rodMat)
      : new et(new pn(0.014, 0.014, 0.95, 10), rodMat);
    rodGrp.add(rodMesh);
    weaponMount.add(rodGrp);

    // 5: Campus Fallen Branch Pickup
    let branchGrp = new fi();
    branchGrp.rotation.set(-0.34, 0, 0);
    let branchMesh = blenderGeos.fallen_branch
      ? new et(blenderGeos.fallen_branch, branchMat)
      : new et(new pn(0.02, 0.012, 0.92, 10), branchMat);
    branchGrp.add(branchMesh);
    weaponMount.add(branchGrp);

    // Shared Muzzle Flash + Tactical Laser Sight (for VR & PC Gun Aiming!)
    muzzleFlash = new et(new oa(0.055, 0.16, 8), new Yi({ color: 0xffd166, transparent: true, opacity: 0.92 }));
    muzzleFlash.rotation.x = -Math.PI / 2;
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
  { level: 1, name: "Lab Assistants", badge: "LAB ASST", dept: "ECE / CSE LABS", count: 6, hp: 55, speed: 2.35, dmg: 8, scale: 1.0, skin: 0x628b48, coat: 0xdce6ee, pants: 0x2f3b47, tie: null, glasses: false, badgeCol: "#16a34a", lanyard: 0x16a34a, isBoss: false },
  { level: 2, name: "Jr. Professors", badge: "JR. PROF", dept: "ASST. FACULTY", count: 8, hp: 85, speed: 2.75, dmg: 11, scale: 1.03, skin: 0x567f42, coat: 0x88b0cc, pants: 0x262a32, tie: 0x8c2323, glasses: false, badgeCol: "#2563eb", lanyard: 0x2563eb, isBoss: false },
  { level: 3, name: "Professors", badge: "PROFESSOR", dept: "SENIOR FACULTY", count: 9, hp: 125, speed: 2.9, dmg: 14, scale: 1.06, skin: 0x4b703a, coat: 0x3b4859, pants: 0x1f242c, tie: 0x5c2424, glasses: true, badgeCol: "#9333ea", lanyard: 0x9333ea, isBoss: false },
  { level: 4, name: "Academic / Placement Incharges", badge: "PLACEMENT", dept: "TRAINING & PLACEMENT", count: 10, hp: 170, speed: 3.35, dmg: 17, scale: 1.09, skin: 0x466d4a, coat: 0x1e293b, pants: 0x141a24, tie: 0xd97706, glasses: false, badgeCol: "#d97706", lanyard: 0xd97706, isBoss: false },
  { level: 5, name: "HODs (Head of Department)", badge: "H.O.D", dept: "DEPT. HEAD", count: 7, hp: 260, speed: 3.1, dmg: 22, scale: 1.18, skin: 0x3a5c3d, coat: 0x171c26, pants: 0x0f131a, tie: 0xb91c1c, glasses: true, badgeCol: "#dc2626", lanyard: 0xdc2626, isBoss: false },
  { level: 6, name: "THE CEO · FINAL BOSS", badge: "CEO · BOSS", dept: "EXECUTIVE OFFICE", count: 1, hp: 1200, speed: 3.45, dmg: 28, scale: 1.48, skin: 0x2f5236, coat: 0x0d1117, pants: 0x090c10, tie: 0xf59e0b, glasses: false, badgeCol: "#eab308", lanyard: 0xeab308, isBoss: true }
];

const WEAPON_DEFS = [
  { id: 0, key: "saber", name: "PLASMA LIGHTSABER", type: "melee", dmg: 48, range: 2.55, cooldown: 0.34, knockback: 3.2, mag: Infinity, muzzleZ: -0.5 },
  { id: 1, key: "pistol", name: "TACTICAL 9MM PISTOL", type: "gun", dmg: 34, range: 65, cooldown: 0.24, auto: false, pellets: 1, spread: 0.012, mag: 15, reload: 1.1, muzzleZ: -0.22 },
  { id: 2, key: "rifle", name: "PULSE ASSAULT RIFLE", type: "gun", dmg: 26, range: 80, cooldown: 0.105, auto: true, pellets: 1, spread: 0.022, mag: 30, reload: 1.5, muzzleZ: -0.58 },
  { id: 3, key: "shotgun", name: "COMBAT SHOTGUN", type: "gun", dmg: 22, range: 32, cooldown: 0.68, auto: false, pellets: 6, spread: 0.075, mag: 8, reload: 1.65, muzzleZ: -0.62 },
  { id: 4, key: "iron_rod", name: "IRON CONSTRUCTION ROD", type: "melee", dmg: 64, range: 2.65, cooldown: 0.48, knockback: 5.2, mag: Infinity, muzzleZ: -0.5 },
  { id: 5, key: "fallen_branch", name: "FALLEN TREE BRANCH", type: "melee", dmg: 52, range: 2.6, cooldown: 0.44, knockback: 4.5, mag: Infinity, muzzleZ: -0.5 }
];

// Procedural WebAudio Combat SFX
let audioCtx = null;
function ensureAudio() {
  if (!audioCtx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC) audioCtx = new AC();
  }
  if (audioCtx && audioCtx.state === "suspended") audioCtx.resume().catch(() => {});
  return audioCtx;
}
function playSFX(kind) {
  const ctx = ensureAudio();
  if (!ctx) return;
  const now = ctx.currentTime;
  const gain = ctx.createGain();
  gain.connect(ctx.destination);
  if (kind === "saber") {
    const osc = ctx.createOscillator();
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(160, now);
    osc.frequency.exponentialRampToValueAtTime(420, now + 0.09);
    osc.frequency.exponentialRampToValueAtTime(110, now + 0.24);
    gain.gain.setValueAtTime(0.14, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.26);
  } else if (kind === "pistol" || kind === "rifle" || kind === "shotgun") {
    const dur = kind === "shotgun" ? 0.22 : kind === "pistol" ? 0.11 : 0.08;
    const buf = ctx.createBuffer(1, Math.floor(ctx.sampleRate * dur), ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (d.length * 0.25));
    const src = ctx.createBufferSource(); src.buffer = buf;
    const filt = ctx.createBiquadFilter(); filt.type = "lowpass";
    filt.frequency.value = kind === "shotgun" ? 950 : kind === "pistol" ? 2100 : 1700;
    gain.gain.setValueAtTime(kind === "shotgun" ? 0.34 : 0.22, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + dur);
    src.connect(filt); filt.connect(gain); src.start(now);
  } else if (kind === "rod" || kind === "branch") {
    const osc = ctx.createOscillator();
    osc.type = kind === "rod" ? "triangle" : "sine";
    osc.frequency.setValueAtTime(kind === "rod" ? 520 : 190, now);
    osc.frequency.exponentialRampToValueAtTime(kind === "rod" ? 130 : 65, now + 0.16);
    gain.gain.setValueAtTime(0.24, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.19);
  } else if (kind === "block" || kind === "bash") {
    const osc = ctx.createOscillator();
    osc.type = "sine";
    osc.frequency.setValueAtTime(kind === "bash" ? 280 : 680, now);
    osc.frequency.exponentialRampToValueAtTime(kind === "bash" ? 75 : 320, now + 0.22);
    gain.gain.setValueAtTime(0.22, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.25);
  } else if (kind === "hit" || kind === "headshot") {
    const osc = ctx.createOscillator();
    osc.type = "square";
    osc.frequency.setValueAtTime(kind === "headshot" ? 920 : 280, now);
    osc.frequency.exponentialRampToValueAtTime(kind === "headshot" ? 1320 : 120, now + 0.09);
    gain.gain.setValueAtTime(0.14, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.11);
  } else if (kind === "hurt") {
    const osc = ctx.createOscillator();
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(140, now);
    osc.frequency.linearRampToValueAtTime(60, now + 0.22);
    gain.gain.setValueAtTime(0.22, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
    osc.connect(gain); osc.start(now); osc.stop(now + 0.25);
  } else if (kind === "levelup" || kind === "pickup") {
    const freqs = kind === "levelup" ? [440, 554, 659, 880] : [520, 740];
    freqs.forEach((frq, idx) => {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = "triangle"; o.frequency.value = frq;
      g.gain.setValueAtTime(0.12, now + idx * 0.08);
      g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.22);
      o.connect(g); g.connect(ctx.destination);
      o.start(now + idx * 0.08); o.stop(now + idx * 0.08 + 0.24);
    });
  }
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
  fireCd: 0,
  swingAnim: 0,
  recoilAnim: 0,
  muzzleTimer: 0,
  mouseLeftDown: false,
  mouseRightDown: false,
  zombies: [],
  projectiles: [],
  particles: [],
  pickups: [],
  gameOver: false,
  victory: false,
  waveDelay: 0,
  bossSummonedMinions: false,
  vrPrevRightPos: new A(),
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

// Build a Realistic Articulated Faculty Zombie using Blender-Modified CC0 Human Anatomy + Faculty ID Card
function createFacultyZombie(lvlDef, x, z) {
  const root = new fi();
  const s = lvlDef.scale;
  const gy = groundAt(x, z);
  root.position.set(x, gy, z);
  root.scale.set(s, s, s);

  const zSkin = new Jt({ color: lvlDef.skin, roughness: 0.68, metalness: 0.04 });
  const zCoat = new Jt({ color: lvlDef.coat, roughness: 0.80, metalness: 0.06 });
  const zPants = new Jt({ color: lvlDef.pants, roughness: 0.86 });
  const zBelt = new Jt({ color: 0x1a1614, roughness: 0.55, metalness: 0.2 });
  const zBlood = new Jt({ color: 0x6e1414, roughness: 0.55 });
  const eyeColor = lvlDef.isBoss ? 0xff1e1e : (lvlDef.level >= 4 ? 0xff9f1c : 0xcaff33);
  const zEye = new Yi({ color: eyeColor });

  // Realistic Anatomical Legs (Blender-modified CC0 human base mesh)
  const legs = [];
  for (const [idx, side] of [[-1, -1], [1, 1]].entries()) {
    const hip = new fi();
    hip.position.set(side[0] * 0.095, 0.86, 0);
    const legGeo = idx === 0 ? blenderGeos.human_leg_l : blenderGeos.human_leg_r;
    if (legGeo) {
      const legMesh = new et(legGeo, zPants);
      legMesh.castShadow = true;
      hip.add(legMesh);
    } else {
      const thigh = new et(new sa(0.075, 0.72, 4, 8), zPants);
      thigh.position.y = -0.42;
      hip.add(thigh);
    }
    root.add(hip);
    legs.push(hip);
  }

  // Realistic Anatomical Torso + Tailored Faculty Attire (Lab Coat / Shirt / Blazer / CEO Suit)
  const torso = new fi();
  torso.position.set(0, 0.86, 0);
  if (blenderGeos.human_torso) {
    const torsoMesh = new et(blenderGeos.human_torso, zCoat);
    torsoMesh.castShadow = true;
    torso.add(torsoMesh);
  } else {
    const chest = new et(new Ni(0.42, 0.56, 0.23), zCoat);
    chest.position.y = 0.32;
    torso.add(chest);
  }

  // Tailored waist belt & jacket hem (blends torso cleanly into trousers)
  const belt = new et(new pn(0.155, 0.162, 0.06, 18), zBelt);
  belt.scale.set(1.18, 1, 0.82);
  belt.position.set(0, 0.06, 0.0);
  torso.add(belt);
  const buckle = new et(new Ni(0.055, 0.045, 0.025), new Jt({ color: 0xd4af37, roughness: 0.25, metalness: 0.85 }));
  buckle.position.set(0, 0.06, 0.132);
  torso.add(buckle);

  // Crisp White Collar & Faculty Tie
  const collar = new et(new pn(0.078, 0.095, 0.055, 16), new Jt({ color: 0xe2e8f0, roughness: 0.7 }));
  collar.position.set(0, 0.61, 0.005);
  torso.add(collar);
  if (lvlDef.tie) {
    const tie = new et(new Ni(0.048, 0.30, 0.024), new Jt({ color: lvlDef.tie, roughness: 0.55 }));
    tie.position.set(0, 0.42, 0.125);
    torso.add(tie);
  }
  // Lab coat lower skirt for Level 1 Lab Assistants
  if (lvlDef.level === 1) {
    const skirt = new et(new pn(0.168, 0.195, 0.34, 18), zCoat);
    skirt.scale.set(1.15, 1, 0.85);
    skirt.position.set(0, -0.10, -0.01);
    torso.add(skirt);
  }
  // Subtle undead bloodstain on coat
  const stain = new et(new fn(0.065, 10, 8), zBlood);
  stain.scale.set(1.2, 0.9, 0.25);
  stain.position.set(0.095, 0.24, 0.118);
  torso.add(stain);

  // FACULTY ID CARD + COLORED LANYARD (Swings naturally on chest)
  const lanyardMat = new Jt({ color: lvlDef.lanyard, roughness: 0.6 });
  const strapL = new et(new Ni(0.014, 0.22, 0.012), lanyardMat);
  strapL.position.set(-0.048, 0.50, 0.122); strapL.rotation.z = -0.24;
  torso.add(strapL);
  const strapR = new et(new Ni(0.014, 0.22, 0.012), lanyardMat);
  strapR.position.set(0.048, 0.50, 0.122); strapR.rotation.z = 0.24;
  torso.add(strapR);

  const idCardPivot = new fi();
  idCardPivot.position.set(0, 0.40, 0.138);
  const idCard = new et(new Ni(0.11, 0.155, 0.008), new Yi({ map: getFacultyIdCardTexture(lvlDef) }));
  idCard.position.set(0, -0.08, 0);
  idCardPivot.add(idCard);
  torso.add(idCardPivot);

  root.add(torso);

  // Realistic Anatomical Human Head & Neck (Blender-modified CC0 human base mesh)
  const headGroup = new fi();
  headGroup.position.set(0, 1.48, 0.0);
  const headMesh = blenderGeos.human_head
    ? new et(blenderGeos.human_head, zSkin)
    : (blenderGeos.zombie_head ? new et(blenderGeos.zombie_head, zSkin) : new et(new fn(0.12, 16, 14), zSkin));
  headMesh.castShadow = true;
  headGroup.add(headMesh);

  // Glowing Sunken Undead Eyes & Dark Sockets (positioned on realistic face at Y~0.165, Z~0.095)
  const sockMat = new Jt({ color: 0x1a2418, roughness: 0.9 });
  for (const side of [-1, 1]) {
    const sock = new et(new fn(0.022, 8, 8), sockMat);
    sock.scale.set(1.15, 0.78, 0.45);
    sock.position.set(side * 0.033, 0.165, 0.090);
    headGroup.add(sock);
    const eye = new et(new fn(0.012, 8, 8), zEye);
    eye.position.set(side * 0.033, 0.165, 0.098);
    headGroup.add(eye);
  }
  // Snarling undead mouth
  const mouth = new et(new Ni(0.052, 0.018, 0.016), new Yi({ color: 0x2b0a0a }));
  mouth.position.set(0, 0.092, 0.094);
  headGroup.add(mouth);

  // Realistic Hair Cap / Professor Glasses / CEO Boss Crown
  const hair = new et(new fn(0.108, 14, 10), new Jt({ color: lvlDef.level >= 3 ? 0x4b5563 : 0x18181b, roughness: 0.88 }));
  hair.scale.set(0.92, 0.56, 1.05);
  hair.position.set(0, 0.245, -0.008);
  headGroup.add(hair);

  if (lvlDef.glasses) {
    const glMat = new Jt({ color: 0x111827, roughness: 0.3, metalness: 0.7 });
    for (const side of [-1, 1]) {
      const rim = new et(new gn(0.024, 0.0038, 6, 14), glMat);
      rim.position.set(side * 0.034, 0.165, 0.106);
      headGroup.add(rim);
    }
    const bridge = new et(new Ni(0.024, 0.005, 0.005), glMat);
    bridge.position.set(0, 0.168, 0.106);
    headGroup.add(bridge);
  }
  if (lvlDef.isBoss) {
    const crown = new et(new gn(0.135, 0.014, 8, 22), new Yi({ color: 0xf59e0b }));
    crown.rotation.x = Math.PI / 2;
    crown.position.set(0, 0.32, 0);
    headGroup.add(crown);
  }
  root.add(headGroup);

  // Realistic Anatomical Arms with Five-Fingered Hands + Tailored Shoulder Sleeves
  const arms = [];
  for (const [idx, side] of [[-1, -1], [1, 1]].entries()) {
    const sh = new fi();
    sh.position.set(side[0] * 0.19, 1.42, 0.0);
    // Smooth shoulder cap sleeve so arm joint blends seamlessly into coat/shirt
    const shCap = new et(new fn(0.068, 12, 10), zCoat);
    shCap.scale.set(1.0, 1.08, 1.0);
    sh.add(shCap);
    const armGeo = idx === 0 ? blenderGeos.human_arm_l : blenderGeos.human_arm_r;
    if (armGeo) {
      const armMesh = new et(armGeo, zSkin);
      armMesh.castShadow = true;
      sh.add(armMesh);
    } else {
      const upper = new et(new sa(0.052, 0.56, 4, 8), zSkin);
      upper.position.set(0, -0.32, 0);
      sh.add(upper);
    }
    // Swing A-pose arms (+X/-X) forward toward +Z so both arms reach straight out toward the player!
    sh.rotation.set(-0.22, -side[0] * 1.28, -side[0] * 0.42);
    root.add(sh);
    arms.push(sh);
  }

  // Diegetic Floating HP Bar above Zombie
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
    alive: true, deathTimer: 0, attackCd: 0, hitFlash: 0,
    phase: Math.random() * Math.PI * 2,
    knockVel: new A(),
    boltCd: 3.2, slamCd: 5.5,
    skinMat: zSkin, baseSkinHex: lvlDef.skin
  };
}

function findZombieSpawnAround(px, pz, minDist = 17, maxDist = 34) {
  for (let tries = 0; tries < 40; tries++) {
    const ang = Math.random() * Math.PI * 2;
    const dist = minDist + Math.random() * (maxDist - minDist);
    const sx = px + Math.cos(ang) * dist;
    const sz = pz + Math.sin(ang) * dist;
    if (!yo(sx, sz)) return [sx, sz];
  }
  return [px + 12, pz + 12];
}

function clearZombiesAndFX() {
  for (const z of ZGAME.zombies) Ht.remove(z.root);
  ZGAME.zombies.length = 0;
  for (const pr of ZGAME.projectiles) Ht.remove(pr.mesh);
  ZGAME.projectiles.length = 0;
  for (const pt of ZGAME.particles) Ht.remove(pt.mesh);
  ZGAME.particles.length = 0;
}

function spawnZombieWave(levelIdx) {
  ZGAME.levelIdx = levelIdx;
  ZGAME.bossSummonedMinions = false;
  const lvl = ZOMBIE_LEVELS[levelIdx];
  const px = xt.position.x, pz = xt.position.z;
  for (let i = 0; i < lvl.count; i++) {
    const [sx, sz] = findZombieSpawnAround(px, pz, lvl.isBoss ? 22 : 16, lvl.isBoss ? 28 : 34);
    ZGAME.zombies.push(createFacultyZombie(lvl, sx, sz));
  }
  showToast(lvl.isBoss ? "FINAL BOSS: THE CEO HAS ARRIVED!" : `LEVEL ${lvl.level}: ${lvl.name.toUpperCase()}`, 3.2);
  playSFX("levelup");
  updateCombatHUD();
}

function startZombieGame() {
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
  selectWeapon(0);
  populateCampusPickups();
  // Ensure 1st-Person POV for combat
  if (povMode !== "1st") { povMode = "1st"; updateCameraPOV(); }
  // Apply Outbreak Dusk atmosphere
  kt("time-mode").value = "outbreak";
  kt("time-mode").dispatchEvent(new Event("change"));
  document.body.classList.add("zombie-mode");
  spawnZombieWave(0);
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
  if (idx === 0) playSFX("saber");
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
  playSFX("pickup");
  updateCombatHUD();
}

function damageZombie(z, dmg, hitPos, knockDir, knockAmt = 1.8, isHeadshot = false) {
  if (!z.alive) return;
  z.hp -= dmg;
  z.hitFlash = 0.14;
  z.hpBarBg.visible = true;
  if (knockDir) z.knockVel.addScaledVector(knockDir, knockAmt / z.lvlDef.scale);
  spawnBurst(hitPos, isHeadshot ? 0xfef08a : 0x4ade80, isHeadshot ? 11 : 6, 4.2);
  playSFX(isHeadshot ? "headshot" : "hit");
  showHitMarker(isHeadshot, isHeadshot ? `HEADSHOT! -${Math.round(dmg)}` : `-${Math.round(dmg)}`);

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

function performMeleeAttack(origin, forward) {
  const w = WEAPON_DEFS[ZGAME.weaponIdx];
  if (!w || w.type !== "melee") return;
  ZGAME.fireCd = w.cooldown;
  ZGAME.swingAnim = 1.0;
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
  ZGAME.muzzleTimer = 0.055;
  playSFX(w.key);
  pulseHaptics("right", w.key === "shotgun" ? 0.95 : 0.65, w.key === "shotgun" ? 110 : 55);

  // Position muzzle flash on active arm
  const activeRightArms = [fpHands[1], trackedHands.get("right")?.arm].filter(Boolean);
  for (const arm of activeRightArms) {
    if (arm.muzzleFlash) arm.muzzleFlash.position.set(0, 0.055, w.muzzleZ);
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

function showEndScreen(won) {
  const ov = kt("end-overlay");
  if (!ov) return;
  kt("end-title").textContent = won ? "CAMPUS SAVED · VICTORY!" : "OVERRUN BY FACULTY ZOMBIES";
  kt("end-title").style.color = won ? "#4ade80" : "#ff6b6b";
  const lvl = ZOMBIE_LEVELS[ZGAME.levelIdx] || ZOMBIE_LEVELS[0];
  kt("end-stats").innerHTML = `Level Reached: <b>Level ${lvl.level} (${lvl.name})</b><br>Total Kills: <b>${ZGAME.kills}</b> · Headshots: <b>${ZGAME.headshots}</b><br>Best Kill Streak: <b>${ZGAME.bestCombo}x</b><br>Final Score: <b style="color:#fde047">${ZGAME.score}</b>`;
  ov.style.display = "flex";
}
if (kt("btn-restart-game")) kt("btn-restart-game").onclick = () => { startZombieGame(); cd(); };

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

function updateCombatHUD() {
  if (!ZGAME.active) return;
  const lvl = ZOMBIE_LEVELS[ZGAME.levelIdx] || ZOMBIE_LEVELS[0];
  const aliveCount = ZGAME.zombies.filter(z => z.alive).length;
  kt("wave-title").textContent = lvl.isBoss ? "FINAL BOSS · THE CEO" : `LEVEL ${lvl.level} · ${lvl.name.toUpperCase()}`;
  kt("wave-sub").textContent = `Zombies Left: ${aliveCount} · Kills: ${ZGAME.kills} · Score: ${ZGAME.score}`;
  kt("hp-val").textContent = `${Math.ceil(ZGAME.hp)} / ${ZGAME.maxHp}`;
  kt("hp-fill").style.width = `${(ZGAME.hp / ZGAME.maxHp) * 100}%`;
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
  const origin = new A();
  hand.anchor.getWorldPosition(origin);
  const q = new Ot();
  hand.anchor.getWorldQuaternion(q);
  const forward = new A(0, 0, -1).applyQuaternion(q).normalize();
  return { origin, forward };
}

function updateZombieGame(dt, timeSec) {
  if (!ZGAME.active) return;
  if (!En && !Ye.xr.isPresenting) return;

  if (ZGAME.toastTimer > 0) {
    ZGAME.toastTimer -= dt;
    if (ZGAME.toastTimer <= 0) kt("center-toast").classList.remove("show");
  }
  if (ZGAME.fireCd > 0) ZGAME.fireCd = Math.max(0, ZGAME.fireCd - dt);
  if (ZGAME.shieldBashCd > 0) ZGAME.shieldBashCd = Math.max(0, ZGAME.shieldBashCd - dt);
  if (ZGAME.vrSwingCd > 0) ZGAME.vrSwingCd = Math.max(0, ZGAME.vrSwingCd - dt);
  if (ZGAME.swingAnim > 0) ZGAME.swingAnim = Math.max(0, ZGAME.swingAnim - dt * 3.4);
  if (ZGAME.recoilAnim > 0) ZGAME.recoilAnim = Math.max(0, ZGAME.recoilAnim - dt * 6.5);
  if (ZGAME.shieldBashAnim > 0) ZGAME.shieldBashAnim = Math.max(0, ZGAME.shieldBashAnim - dt * 3.2);
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

  // PC Jump Physics
  if (!Ye.xr.isPresenting && bo.value === "zombie") {
    if (ZGAME.jumpY > 0 || ZGAME.jumpVel !== 0) {
      ZGAME.jumpY += ZGAME.jumpVel * dt;
      ZGAME.jumpVel -= 19.5 * dt;
      if (ZGAME.jumpY <= 0) { ZGAME.jumpY = 0; ZGAME.jumpVel = 0; }
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

    // Hit flash recovery
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

    // Zombie Shamble, Lunging Arms, Swinging Faculty ID Card & Head Twitch
    z.phase += dt * (z.speed * 2.4);
    z.legs[0].rotation.x = Math.sin(z.phase) * 0.55;
    z.legs[1].rotation.x = -Math.sin(z.phase) * 0.55;
    z.torso.rotation.z = Math.sin(z.phase) * 0.09;
    z.torso.rotation.x = 0.14 + Math.abs(Math.cos(z.phase)) * 0.06;
    z.headGroup.rotation.z = Math.sin(z.phase * 1.4) * 0.14;
    z.idCardPivot.rotation.z = -Math.sin(z.phase) * 0.22;
    z.idCardPivot.rotation.x = -0.18;

    const lunge = z.attackCd > 0.65 ? Math.sin((z.attackCd - 0.65) * 9) * 0.45 : 0;
    z.arms[0].rotation.z = 0.42 + Math.sin(z.phase) * 0.14 + lunge;
    z.arms[1].rotation.z = -0.42 - Math.sin(z.phase) * 0.14 - lunge;

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

  // Update Boss Projectiles
  for (let i = ZGAME.projectiles.length - 1; i >= 0; i--) {
    const pr = ZGAME.projectiles[i];
    pr.life -= dt;
    pr.mesh.position.addScaledVector(pr.vel, dt);
    const dToPlayer = Math.hypot(pr.mesh.position.x - px, pr.mesh.position.z - pz);
    if (dToPlayer < 0.95 && Math.abs(pr.mesh.position.y - (py + 1.25)) < 1.1) {
      damagePlayer(pr.dmg);
      spawnBurst(pr.mesh.position, 0xef4444, 10, 4);
      Ht.remove(pr.mesh);
      ZGAME.projectiles.splice(i, 1);
      continue;
    }
    if (pr.life <= 0) {
      Ht.remove(pr.mesh);
      ZGAME.projectiles.splice(i, 1);
    }
  }

  // Update Particles & Tracers
  for (let i = ZGAME.particles.length - 1; i >= 0; i--) {
    const pt = ZGAME.particles[i];
    pt.life -= dt;
    if (pt.isRing) {
      const grow = 1 + dt * 14;
      pt.mesh.scale.x = Math.min(pt.maxScale, pt.mesh.scale.x * grow);
      pt.mesh.scale.y = pt.mesh.scale.x;
    } else if (!pt.isTracer) {
      pt.vel.y -= 9.8 * dt;
      pt.mesh.position.addScaledVector(pt.vel, dt);
    }
    if (pt.life <= 0) {
      Ht.remove(pt.mesh);
      ZGAME.particles.splice(i, 1);
    }
  }

  // Wave Progression (Level 1 -> 2 -> 3 -> 4 -> 5 -> CEO Boss -> Victory!)
  if (aliveCount === 0 && !ZGAME.gameOver && !ZGAME.victory) {
    if (ZGAME.waveDelay <= 0) {
      if (ZGAME.levelIdx + 1 >= ZOMBIE_LEVELS.length) {
        ZGAME.victory = true;
        playSFX("levelup");
        showEndScreen(true);
        document.exitPointerLock?.();
      } else {
        ZGAME.waveDelay = 3.2;
        ZGAME.hp = Math.min(ZGAME.maxHp, ZGAME.hp + 25);
        showToast(`LEVEL ${ZGAME.levelIdx + 1} CLEARED! +25 HP · NEXT WAVE INCOMING...`, 2.8);
        playSFX("levelup");
      }
    } else {
      ZGAME.waveDelay -= dt;
      if (ZGAME.waveDelay <= 0) {
        spawnZombieWave(ZGAME.levelIdx + 1);
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
    if (r.code === "Space" && ZGAME.jumpY === 0) { ZGAME.jumpVel = 7.2; return; }
    if (r.code === "KeyR") { if (ZGAME.gameOver || ZGAME.victory) { startZombieGame(); cd(); } else { triggerReload(); } return; }
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
    const key=`${Math.ceil(ZGAME.hp)}-${Math.ceil(ZGAME.shield)}-${lvl.level}-${alive}-${w.id}-${ammoStr}-${ZGAME.gameOver}`;
    if(wristDisplay.last===key)return;
    wristDisplay.last=key;
    const ctx=wristDisplay.ctx;
    ctx.fillStyle="#0b1824";ctx.fillRect(0,0,512,256);
    ctx.fillStyle="#ff6b6b";ctx.font="bold 30px sans-serif";
    ctx.fillText(ZGAME.gameOver?"OVERRUN! PRESS B":`LVL ${lvl.level}: ${lvl.badge} (${alive})`,16,42,480);
    ctx.fillStyle="#4ade80";ctx.font="bold 28px sans-serif";
    ctx.fillText(`HP: ${Math.ceil(ZGAME.hp)}   SHIELD: ${Math.ceil(ZGAME.shield)}%`,16,92,480);
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
      const curPos=hand.anchor.position;
      if(side==="right"){
        // Right Controller Trigger opens the Transparent Hi-Tech Shield (and fires guns / swings)
        ZGAME.vrShieldTrigger = trigDown || !!(trackedHands.get("left")?.trigDown);
        // Track physical swing speed for Lightsaber / Iron Rod / Fallen Branch
        const speed=curPos.distanceTo(ZGAME.vrPrevRightPos)*60;
        ZGAME.vrPrevRightPos.copy(curPos);
        const w=WEAPON_DEFS[ZGAME.weaponIdx];
        if(w.type==="melee"){
          if((speed>3.4 || (trigDown && !hand.trigDown)) && ZGAME.vrSwingCd<=0 && ZGAME.fireCd<=0){
            const {origin,forward}=getVRRightAimRay();
            performMeleeAttack(origin,forward);
            ZGAME.vrSwingCd=0.28;
          }
        } else {
          if(trigDown && (w.auto || !hand.trigDown) && ZGAME.fireCd<=0){
            const {origin,forward}=getVRRightAimRay();
            performGunFire(origin,forward);
          }
        }
        // Right Grip picks up nearby campus Iron Rod or Fallen Branch
        if(gripDown && !hand.gripDown) tryPickupNearbyWeapon();
        // A button cycles Right-Hand Weapons
        if(hand.source===source && pressed && !hand.buttonDown) cycleWeapon(1);
        // B button reloads gun (or restarts if game over)
        if(hand.source===source && upper && !hand.upperDown){
          if(ZGAME.gameOver || ZGAME.victory) startZombieGame(); else triggerReload();
        }
      } else {
        // Left Hand: Shield Bash via fast forward thrust or Left Trigger (+ also opens shield)
        const lSpeed=curPos.distanceTo(ZGAME.vrPrevLeftPos)*60;
        ZGAME.vrPrevLeftPos.copy(curPos);
        ZGAME.vrShieldTrigger = trigDown || !!(trackedHands.get("right")?.trigDown);
        if(lSpeed>5.2 || (gripDown && !hand.gripDown)) triggerShieldBash();
        // X button cycles lighting/atmosphere in VR
        if(hand.source===source && pressed && !hand.buttonDown){
          const tm=kt("time-mode"); tm.selectedIndex=(tm.selectedIndex+1)%tm.options.length; tm.dispatchEvent(new Event("change"));
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

# Ensure newly created Quest controller hands also sync weapon/shield visibility
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
        // Right Hand: Lightsaber / Guns / Picked-up Rod or Branch
        let w = WEAPON_DEFS[ZGAME.weaponIdx];
        let sw = Math.sin(ZGAME.swingAnim * Math.PI);
        let rec = ZGAME.recoilAnim;
        if (w.type === "melee") {
          arm.root.position.set(
            0.23 - sw * 0.22,
            -0.21 + sw * 0.08 + breathe * 0.004,
            -0.38 - sw * 0.12
          );
          arm.root.rotation.set(
            0.22 - sw * 1.15,
            -0.25 + sw * 0.85,
            -0.18 + sw * 0.55
          );
        } else {
          arm.root.position.set(
            0.20,
            -0.19 + rec * 0.025 + breathe * 0.003,
            -0.37 + rec * 0.065
          );
          arm.root.rotation.set(
            0.04 + rec * 0.22,
            -0.06,
            -0.04
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

# 7k. Keep dynamic shadow updates reasonable in VR (don't freeze shadow map completely)
html = html.replace(
    "Ye.shadowMap.autoUpdate=false;Ye.shadowMap.needsUpdate=true;",
    "Ye.shadowMap.autoUpdate=true;syncWeaponVisuals();",
    1
)

with open(SRC_HTML, "w", encoding="utf-8") as f:
    f.write(html)

INDEX_HTML = os.path.join(ROOT, "index.html")
with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully built {SRC_HTML} and {INDEX_HTML} ({len(html):,} bytes)")

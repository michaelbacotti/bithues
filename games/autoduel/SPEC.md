# AUTODUEL — Web Remake Specification

## 1. Project Overview

**Name:** Autoduel
**Type:** Top-down vehicular combat racing game with economy layer
**Original:** Origin Systems, 1984 (Apple II)
**This Version:** HTML5 Canvas single-file prototype

The player drives a weaponized car across a road network connecting four towns. They buy and sell equipment, destroy enemy vehicles for scrap, haul cargo for profit, and upgrade their ride. The core loop: Drive → Fight → Salvage → Trade → Upgrade → Repeat.

---

## 2. Visual & Rendering Specification

### Canvas Setup
- **Renderer:** HTML5 Canvas 2D, fills `window.innerWidth × window.innerHeight`
- **Camera:** Follows player car, centered on screen
- **World size:** 3000 × 2000 pixels (virtual game world)
- **Background:** Dark asphalt-gray `#1a1a1a`

### Color Palette (Apple II-inspired, 16-color feel)
- Background/void: `#0d0d0d`
- Asphalt roads: `#2d2d2d`
- Road markings: `#f0c000` (yellow dashes)
- Road edge lines: `#ffffff` (white solid)
- Player car body: `#00aa00` (bright green)
- Enemy cars: `#cc2200` (red)
- Bullets: `#ffff00` (yellow)
- Towns: `#4444aa` (blue zone glow)
- HUD background: `#111111` with `#333333` borders
- Health bar: `#00cc44` (green) → `#cccc00` (yellow) → `#cc0000` (red)
- Fuel bar: `#0088ff` (blue)
- Text: `#f0f0f0`

### World Elements
- **Roads:** Brown `#5c4033` with yellow center dashes, white edge lines. 80px wide.
- **Grass/dirt:** Dark green `#1a3d1a` — off-road slows you down
- **Towns:** Rectangular zones 200×200px with glowing blue border. Label shows name.
- **Car sprites:** Rectangle-based top-down shapes, 30×18px
  - Player: green rectangle with darker front windshield section
  - Enemy: red rectangle, slightly smaller

### Post-Processing / Effects
- Muzzle flash (brief white circle on fire)
- Explosion on car death (orange/red expanding circles)
- Screen shake on taking damage
- Scrap drops spin slowly and fade after 10 seconds

---

## 3. Map & World Layout

### Towns (4 total)
```
        [New Denver]

[Barren Rock] ←──────→ [Dusty Spur]
```

| Town | X | Y | Specialty |
|---|---|---|---|
| Barren Rock | 200 | 500 | Cheap fuel, expensive weapons |
| Dusty Spur | 1200 | 800 | Cheap weapons, expensive armor |
| New Denver | 600 | 1600 | Balanced prices |

### Road Network
- All roads are 80px wide, defined as waypoint paths
- Roads use linear interpolation between waypoints
- Car is constrained to roads; leaving road = grass = slowdown

### Towns Data
Each town has:
- Name, position (x, y), size
- Buy prices (weapons, armor, fuel, repair)
- Sell prices (scrap, cargo)
- 3 prices differ from baseline by ±10-30%

---

## 4. Vehicle & Physics

### Player Car Stats (Starting)
- **Speed:** max 200 px/s, acceleration 120 px/s²
- **Turn rate:** 2.5 rad/s at full speed, less when slow
- **Armor:** 100 points (absorbs damage first)
- **Hull:** 100 points (real damage)
- **Fuel capacity:** 100 units, burn 8 units/s at full throttle
- **Fuel consumption:** proportional to speed
- **Mass:** affects collision pushback

### Physics Model
- Velocity vector (vx, vy) with drag factor 0.98/frame
- Acceleration applies in facing direction
- Turn rate scales with speed (can't turn while stopped)
- Off-road (grass): max speed 60, acceleration halved
- Collision with road edge: bounce back, slight damage

### Damage System
1. Hit lands → subtract from Armor first
2. If Armor = 0, subtract from Hull
3. Hull = 0 → car destroyed → respawn at nearest town (costs 50 credits)
4. Damage flash: car turns red briefly

---

## 5. Combat System

### Machine Gun (Player Starting Weapon)
- **Fire rate:** 4 shots/second
- **Bullet speed:** 500 px/s
- **Damage:** 8 per hit
- **Range:** 400px then despawn
- **Ammo:** Unlimited (starting weapon)
- **Visual:** Yellow rectangle 8×3px, travels forward from car nose

### Enemy AI Cars
- Spawn at random road positions, away from player
- Max 4 enemies on screen at once
- Respawn 5 seconds after death
- **AI behavior:**
  - Drive toward player position (pathfinding along roads)
  - Fire when player is within 350px and within 30° of their facing
  - Fire rate: 2 shots/second
  - Bullet damage: 10
- **Stats:** Speed 150, Armor 50, Hull 50

### Projectiles
- Straight-line movement, no homing
- Despawn on: hitting car, hitting world boundary, range exceeded
- On hit: apply damage, show small spark effect

---

## 6. Town System

### Entering a Town
- Drive into town zone (200×200 area)
- Game pauses, overlay appears with town UI
- ESC or "Exit" button leaves town

### Town UI Layout
```
╔══════════════════════════════════╗
║         TOWN NAME                ║
╠══════════════════════════════════╣
║  [BUY]   [SELL]   [GARAGE]      ║
╠══════════════════════════════════╣
║                                  ║
║  Item list / actions here        ║
║                                  ║
╚══════════════════════════════════╝
```

### BUY Tab
| Item | Base Price | Effect |
|---|---|---|
| Machine Gun | 200 | +10 firepower (stackable, max 3) |
| Armor Plate | 150 | +30 armor (stackable, max 5) |
| Fuel Can | 30 | +20 fuel |
| Repair Kit | 80 | Full hull repair |

- Item shows name, price, current stock (unlimited for MVP)
- Click to purchase → deducted from credits → added to inventory/equipped

### SELL Tab
| Item | Base Price |
|---|---|
| Scrap | 20 per unit |
| Cargo (generic) | 50 per unit |

- Shows inventory quantities
- Sell button for each

### GARAGE Tab
- Shows current car stats
- Repair button (fully restore hull + armor for 50 credits)
- Equip/unequip purchased weapons (for future weapon types)

### Arbitrage Example
- Barren Rock: Fuel 20, Weapons 250
- Dusty Spur: Fuel 40, Weapons 180
- Buy fuel in Barren Rock, sell it in Dusty Spur → 20 profit per can

---

## 7. Economy

### Starting Conditions
- Credits: 500
- Cargo: 0
- Scrap: 0
- Inventory: empty

### Item Values
| Item | Buy | Sell |
|---|---|---|
| Fuel Can | 30 | — |
| Repair Kit | 80 | — |
| Armor Plate | 150 | 75 |
| Machine Gun | 200 | 100 |
| Scrap | — | 20 |
| Cargo | — | 50 |

### Upgrades (Future Phases — not in MVP)
- Speed boost, better guns, nitro, etc.

---

## 8. HUD Specification

### Layout
```
[ARMOR ████████] [HULL ████████] [FUEL ████░░░░]   Credits: $500

Speed: 120 mph                        [MINIMAP]
                                           ┌───┐
                                           │ · │
                                           └───┘

                     [GAME AREA]

```

- **Top-left:** Armor bar, Hull bar, Fuel bar (segmented pixel bars)
- **Top-left below bars:** Speed in mph (derived from velocity magnitude)
- **Top-right:** Minimap 150×100px showing road network, player dot (green), town dots (blue)
- **Bottom-left:** Credits display `$XXX`
- **Bottom-center:** Current mission/cargo indicator (if any)

### Minimap
- Dark background `#0a0a0a` with `#333333` border
- Roads as thin lines `#888888`
- Towns as blue squares
- Player as small green dot
- Enemies not shown (want surprise)

---

## 9. Controls

| Key | Action |
|---|---|
| W / ↑ | Accelerate |
| S / ↓ | Brake / Reverse |
| A / ← | Turn left |
| D / → | Turn right |
| Space | Fire weapon |
| ESC | Pause / Town exit |
| M | Toggle minimap |

---

## 10. Game States

1. **TITLE** — Press SPACE to start, show game name and controls summary
2. **PLAYING** — Normal gameplay, car on road, enemies spawning
3. **TOWN** — Paused overlay, showing town buy/sell/garage UI
4. **PAUSED** — ESC pauses game, ESC again resumes
5. **GAME_OVER** — Car destroyed, show score, press SPACE to respawn (costs 50)

---

## 11. Audio (No audio in MVP)

Placeholder hooks only — no Web Audio implementation in Phase 1.

---

## 12. Technical Architecture

### File Structure
- `SPEC.md` — this file
- `index.html` — single-file game (HTML + CSS + JS)
- `README.md` — how to play

### Core Classes/Objects
```
Game — main state machine, game loop, input handling
World — roads, towns, collision geometry
Camera — follows player, world-to-screen transform
Car — player physics, stats, inventory
Enemy — AI cars, behavior
Bullet — projectile physics
Town — UI state, prices
HUD — render overlay elements
```

### Game Loop
```javascript
function gameLoop(timestamp) {
  const dt = (timestamp - lastTime) / 1000;
  lastTime = timestamp;

  if (state === 'PLAYING') {
    handleInput();
    updatePhysics(dt);
    updateEnemies(dt);
    updateBullets(dt);
    checkCollisions();
    checkTownEntry();
  }

  render();
  requestAnimationFrame(gameLoop);
}
```

### Performance Targets
- 60 FPS on modern browsers
- Canvas size adapts to window resize
- No memory leaks (bullet/enemy pool recycling)

---

## 13. Acceptance Criteria

- [ ] Game loads in browser without errors
- [ ] Player car drives with WASD, physics feel smooth
- [ ] Camera follows car, world scrolls correctly
- [ ] At least 3 enemy cars spawn and chase/attack
- [ ] Bullets fire and deal damage
- [ ] Armor/Hull system works (damage → armor → hull → death)
- [ ] At least 3 towns accessible, each with Buy/Sell/Garage
- [ ] Arbitrage possible (different prices between towns)
- [ ] HUD shows armor, hull, fuel, money, minimap
- [ ] Minimap shows road layout and town positions
- [ ] Destroyed enemies drop scrap
- [ ] Respawn system works (costs credits)
- [ ] Pixel-art aesthetic maintained throughout
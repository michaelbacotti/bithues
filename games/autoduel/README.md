# Autoduel — Web Remake

A faithful HTML5 Canvas remake of Origin Systems' 1984 vehicular combat game.

## How to Play

Open `index.html` in any modern browser.

**NEW PLAYERS start as a pedestrian.** Walk to the GARAGE zone (red dashed square) inside the town, buy a car, then hit the road.

### Game Flow
1. **Title screen** — Click **JOIN THE ROAD** to start
2. **Walking** — You spawn on foot in Barren Rock town. Use WASD/Arrows to walk
3. **Garage** — Walk into the red-dashed **GARAGE** zone to open the shop
4. **Buy Car** — You start with $600. The Rusty Sedan costs $500
5. **Drive** — Exit the garage and you're now driving. Use WASD to drive, SPACE to fire
6. **Combat** — Destroy red enemy cars for cash and scrap
7. **Wrecked?** — You survive as a pedestrian again. Walk back to a garage and buy a new car.

### Controls
| Key | Walking | Driving |
|-----|---------|---------|
| W/↑ | Walk forward | Accelerate |
| S/↓ | Walk backward | Brake/Reverse |
| A/← | Turn/Strafe left | Turn left |
| D/→ | Turn/Strafe right | Turn right |
| SPACE | — | Fire machine gun |
| ESC | Exit garage | — |

### Screens
- **Title** — Animated car drives across road. Click JOIN THE ROAD
- **Walking** — Navigate the town on foot. Find the GARAGE zone
- **Garage** — BUY CAR / SELL / GARAGE (repair, refuel, stats)
- **Driving** — Open road combat. Minimap shows towns (blue) and garage (red)

### Economy
- Starting cash: **$600**
- Rusty Sedan: **$500** (armor:30 hull:70 spd:190)
- Scrap dropped by enemies: sell at garage
- Enemy kills also drop **$50–$160** cash

### Minimap (top right)
- **Blue squares** = Towns
- **Red dots** = Garage zones inside towns
- **Green dot** = You (walking) / You (driving)
- **Red dots** = Enemy vehicles

### Tips
- Each town has different buy/sell prices — trade smart
- Running out of fuel leaves you stranded
- When your car is destroyed, you survive as a pedestrian — don't panic
- Enemies respawn periodically; keep your armor and hull repaired

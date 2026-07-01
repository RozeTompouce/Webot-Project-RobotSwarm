# Production Controller (Uniform Floor Edition) — `production_controller.py`

Geoptimaliseerde Webots-controller voor een egale, lichte arena-vloer.
Combineert LiDAR (`LDS-01`) en camera voor obstakeldetectie, met
filtering van de eigen robotschaduw voor stabielere resultaten op
hoge snelheid.

## Wat doet het script

1. **LiDAR-data**: bepaalt de kortste afstand vóór, links en rechts
   van de robot.
2. **Camera-data**: scant de onderste helft van het camerabeeld op
   donkere pixels (RGB < 180) en telt deze apart voor links en rechts.
   De onderste rand van het beeld (eigen schaduw van de robot) wordt
   genegeerd.
3. **Sensor-fusie**: een zijde geldt als geblokkeerd als óf de LiDAR
   een object dichterbij dan 0,45 m meet, óf er meer dan 8 donkere
   pixels worden gezien aan die kant.
4. **Besturing**:
   - Object recht vooruit dichterbij dan 0,22 m → achteruit rijden.
   - Beide zijden geblokkeerd → ter plekke draaien.
   - Eén zijde geblokkeerd → scherpe bocht naar de vrije kant.
   - Niets geblokkeerd → rechtdoor op volle snelheid (3,5).

## Vereisten

- [Webots](https://cyberbotics.com/) (R2023a of nieuwer aanbevolen)
- Een robotmodel met:
  - een LiDAR-device met de naam `LDS-01`
  - een `camera`-device
  - wielmotoren met de namen `left wheel motor` en `right wheel motor`
- Een **egale, lichte arena-vloer** (geen patronen of schaakbord)

> Twijfel je over de devicenamen in jouw wereld? Draai eerst
> `hardware_scanner.py` als controller en lees de namen af in de
> Webots-console.

## Gebruik

1. Koppel `production_controller.py` als controller aan de robot.
2. Start de simulatie.
3. De robot rijdt automatisch en op hoge snelheid rond, en wijkt
   betrouwbaar uit voor obstakels.

## Belangrijkste parameters

| Constante | Waarde | Betekenis |
|---|---|---|
| `LIDAR_SIDE_SAMPLES` | 40 | Aantal LiDAR-samples dat links/rechts wordt meegenomen |
| `FRONT_STOP_DISTANCE` | 0.22 m | Afstand waarop de robot stopt/terugrijdt |
| `SIDE_BLOCK_DISTANCE` | 0.45 m | Afstand waarop een zijde als geblokkeerd geldt |
| `COLOR_THRESHOLD` | 180 | RGB-waarde onder dit getal telt als "donker object" |
| `PIXEL_BLOCK_THRESHOLD` | 8 | Aantal donkere pixels voordat een zijde geblokkeerd is |
| `SHADOW_MARGIN_PX` | 5 | Onderste rand van het beeld die genegeerd wordt (eigen schaduw) |

## Verschil met `basic_sensor_fusion.py`

| | Basic | Production |
|---|---|---|
| Contrastdrempel (RGB) | < 160 | < 180 |
| Pixeldrempel voor blokkade | > 6 | > 8 |
| Filtert robotschaduw | ❌ | ✅ |
| Geschikt voor | Eerste tests | Productie / arena met egale vloer |

## Bekende beperkingen ⚠️

- Werkt alleen optimaal op een **egale, lichte ondergrond**; op een
  vloer met sterke patronen kan de camera-scan alsnog valse
  obstakels zien.
- De camera-scan is een eenvoudige pixel-telling, geen objectdetectie
  — sterk wisselend omgevingslicht kan de resultaten beïnvloeden.

## Licentie

Voeg hier je gewenste licentie toe (bijv. MIT).

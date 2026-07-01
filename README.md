# Basic Sensor Fusion — `basic_sensor_fusion.py`

Eenvoudige Webots-controller die LiDAR (`LDS-01`) en camera combineert
voor obstakeldetectie en -vermijding. Deze code is bedoeld als
tussenoplossing of tussenversie om het idee van sensor-fusie te testen,
 omdat de camera op dat moment nog niet volledig betrouwbaar leek te
werken door instellingen en configuratieproblemen. Daardoor is de code
niet optimaal getest en functioneerde hij op sommige momenten wel, maar
niet consistent.

## Status van de code

- Dit is een tussencode en geen volledig afgeronde productieversie.
- De camera-integratie is niet volledig bevestigd, omdat de
  camera-instellingen en werking op dat moment onzeker waren.
- De code is vooral bedoeld om te onderzoeken of de combinatie van
  LiDAR en camera bruikbaar is voor obstakelherkenning.
- De resultaten waren wisselend, waardoor verdere verificatie en
  optimalisatie nodig zijn.

## Wat doet het script

1. **LiDAR-data**: bepaalt de kortste afstand vóór, links en rechts
   van de robot.
2. **Camera-data**: scant de onderste helft van het camerabeeld op
   donkere pixels (RGB < 160) en telt deze apart voor links en rechts.
3. **Sensor-fusie**: een zijde geldt als geblokkeerd als óf de LiDAR
   een object dichterbij dan 0,45 m meet, óf er meer dan 6 donkere
   pixels worden gezien aan die kant.
4. **Besturing**:
   - Object recht vooruit dichterbij dan 0,22 m → achteruit rijden.
   - Beide zijden geblokkeerd → ter plekke draaien.
   - Eén zijde geblokkeerd → scherpe bocht naar de vrije kant.
   - Niets geblokkeerd → rechtdoor op volle snelheid.

## Vereisten

- [Webots](https://cyberbotics.com/) (R2023a of nieuwer aanbevolen)
- Een robotmodel met:
  - een LiDAR-device met de naam `LDS-01`
  - een `camera`-device
  - wielmotoren met de namen `left wheel motor` en `right wheel motor`

> Twijfel je over de devicenamen in jouw wereld? Draai eerst
> `hardware_scanner.py` als controller en lees de namen af in de
> Webots-console.

## Gebruik

1. Koppel `basic_sensor_fusion.py` als controller aan de robot.
2. Start de simulatie.
3. De robot rijdt automatisch rond en wijkt uit voor obstakels op
   basis van LiDAR + camera.

## Belangrijkste parameters

| Constante | Waarde | Betekenis |
|---|---|---|
| `LIDAR_SIDE_SAMPLES` | 40 | Aantal LiDAR-samples dat links/rechts wordt meegenomen |
| `FRONT_STOP_DISTANCE` | 0.22 m | Afstand waarop de robot stopt/terugrijdt |
| `SIDE_BLOCK_DISTANCE` | 0.45 m | Afstand waarop een zijde als geblokkeerd geldt |
| `COLOR_THRESHOLD` | 160 | RGB-waarde onder dit getal telt als "donker object" |
| `PIXEL_BLOCK_THRESHOLD` | 6 | Aantal donkere pixels voordat een zijde geblokkeerd is |

## Bekende beperkingen ⚠️

- Gaat uit van een **perfect egale, lichte vloer**. Op een
  patroon- of schaakbordvloer ziet dit script de vloerpatronen zelf
  aan voor obstakels, wat tot foutieve uitwijkmanoeuvres leidt.
- Filtert de eigen schaduw van de robot niet uit het camerabeeld.
- Voor een robuustere versie die deze problemen aanpakt, zie
  `production_controller.py`.

## Licentie

Voeg hier je gewenste licentie toe (bijv. MIT).

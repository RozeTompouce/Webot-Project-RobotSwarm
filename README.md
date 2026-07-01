# RangeFinder-LiDAR Test Controller

Webots-robotcontroller die LiDAR- en RangeFinder (depth-camera) data combineert
tot één sensorfusie-systeem voor obstakeldetectie en autonome navigatie.

## Doel

Dit script is een testcontroller die de betrouwbaarheid van diepte-gebaseerde
obstakeldetectie valideert, als alternatief voor kleurgebaseerde (RGB)
detectie. Door afstand in meters te gebruiken in plaats van kleurcontrast is
het systeem ongevoelig voor schaduw, lichtinval en vloerpatronen.

## Benodigde hardware / devices

Het script verwacht de volgende devices, exact zo benoemd in Webots
(zie `hardware_scanner.py` om namen te verifiëren):

| Device               | Naam in Webots        | Functie                          |
|----------------------|------------------------|-----------------------------------|
| LiDAR                | `LDS-01`               | Afstandsmeting rondom de robot   |
| Depth-camera         | `depth-camera`         | Dieptebeeld (RangeFinder) vooraan|
| Motor links          | `left wheel motor`     | Aandrijving linkerwiel           |
| Motor rechts         | `right wheel motor`    | Aandrijving rechterwiel          |

## Werking

### 1. Initialisatie
De robot, timestep, sensoren en motoren worden opgezet. Beide wielmotoren
worden op `float('inf')` gezet zodat ze op snelheid (in plaats van positie)
aangestuurd kunnen worden.

### 2. LiDAR-data
Per simulatiestap wordt de volledige `getRangeImage()` van de LiDAR
opgesplitst in drie zones:

- **front** — het middelste kwart van de scan (recht voor de robot)
- **left** — de eerste 40 samples
- **right** — de laatste 40 samples

Van elke zone wordt de kortste (dichtstbijzijnde) afstand gebruikt.

### 3. RangeFinder-data (dieptecamera)
Het dieptebeeld wordt pixel-voor-pixel doorlopen binnen een vast scanvlak
(verticaal 40%-75% van de hoogte, horizontaal 15%-85% van de breedte). Voor
elke pixel binnen dit vlak wordt gecontroleerd of de gemeten afstand tussen
**0,10 m en 0,28 m** ligt — dit is de zone waarin een obstakel als relevant
wordt beschouwd. Pixels binnen deze afstand worden geteld als *links* of
*rechts*, afhankelijk van hun positie ten opzichte van het midden van het
beeld.

Omdat deze filtering volledig op fysieke afstand is gebaseerd, spelen kleur,
schaduw en vloerpatroon geen rol — een belangrijk voordeel ten opzichte van
een RGB-camera.

### 4. Sensorfusie-beslissingsmatrix
LiDAR en RangeFinder worden gecombineerd tot een blokkade-status per zijde:

```python
left_blocked  = (left_dist < 0.35)  or (left_pixels  > 5)
right_blocked = (right_dist < 0.35) or (right_pixels > 5)
```

Een zijde geldt als geblokkeerd zodra **één van beide sensoren** een obstakel
signaleert.

### 5. Navigatielogica
Op basis van de blokkade-status wordt een van de volgende gedragingen
gekozen:

| Situatie                              | Gedrag                          |
|----------------------------------------|----------------------------------|
| `front_dist < 0.20`                    | Achteruit / uitwijken            |
| Links **en** rechts geblokkeerd        | Draaien op de plaats             |
| Alleen links geblokkeerd               | Bocht naar rechts                |
| Alleen rechts geblokkeerd              | Bocht naar links                 |
| Geen blokkade                          | Rechtuit rijden                  |

## Configuratie (drempelwaarden)

Onderstaande waarden zitten momenteel hardcoded in het script en kunnen
aangepast worden op basis van testresultaten:

| Parameter                        | Waarde  | Betekenis                                   |
|-----------------------------------|---------|-----------------------------------------------|
| Front-stopafstand                 | 0.20 m  | Afstand waarop de robot achteruit rijdt       |
| Zij-blokkade (LiDAR)               | 0.35 m  | Afstand waarop een zijde als geblokkeerd geldt|
| Depth-filterzone                   | 0.10–0.28 m | Afstand waarbinnen een pixel als obstakel telt |
| Pixel-blokkadedrempel              | 5 px    | Aantal pixels voordat een zijde geblokkeerd is|
| LiDAR-side-samples                 | 40      | Aantal samples links/rechts meegenomen        |

## Gebruik

1. Koppel dit script als controller aan de robot in de Webots-scene.
2. Zorg dat de devicenamen exact overeenkomen met de tabel hierboven.
3. Start de simulatie — de robot navigeert autonoom en wijkt uit voor
   obstakels op basis van de gecombineerde LiDAR- en RangeFinder-data.

## Opmerkingen

- Dit script is een **testcontroller**; voor productiegebruik wordt
  aangeraden de hardcoded waarden naar configuratie-constanten boven het
  script te verplaatsen (zoals in `production_controller.py`).
- Zie de projectdocumentatie voor de vergelijkende analyse tussen deze
  RangeFinder-aanpak en de eerdere RGB-camera-implementatie.

# Hardware Scanner — `hardware_scanner.py`

Webots-controller die eenmalig alle actieve devices van de robot
opvraagt en hun index, type en exacte naam print. Handig om de juiste
device-namen te achterhalen voordat je een navigatiecontroller schrijft.

## Wat doet het script

1. Initialiseert de `Robot`-instantie.
2. Vraagt het totale aantal devices op (`getNumberOfDevices`).
3. Loopt door alle devices en print per device:
   - de index
   - het node-type (`getNodeType`)
   - de exacte naam (`getName`)
4. Doet één simulatiestap en stopt daarna.

## Vereisten

- [Webots](https://cyberbotics.com/) (R2023a of nieuwer aanbevolen)
- Een robotmodel met minstens één device (camera, LiDAR, motor, sensor, …)

## Gebruik

1. Koppel `hardware_scanner.py` als controller aan je robot
   (rechtsklik robot → *Controller* → bestand selecteren, of plaats
   het in de `controllers/<naam>/` map van je project).
2. Start de simulatie.
3. Lees de output af in de Webots-console, bijvoorbeeld:

   ```
   ========================================
     WEBOTS HARDWARE SCANNER GESTART
   ========================================
   Totaal aantal gevonden componenten: 6

   [ID 00] Type: 65 | Naam: 'camera'
   [ID 01] Type: 75 | Naam: 'LDS-01'
   [ID 02] Type: 56 | Naam: 'left wheel motor'
   [ID 03] Type: 56 | Naam: 'right wheel motor'
   ...
   ========================================
     SCAN VOLTOOID - CONTROLLER STOPT
   ========================================
   ```

4. Gebruik de geprinte namen in je andere controllers, bijvoorbeeld
   `robot.getDevice('LDS-01')`.

## Waarom dit script nuttig is

Device-namen verschillen per robotmodel en per Webots-wereld. In
plaats van te gokken of in de PROTO-bestanden te zoeken, geeft dit
script direct en betrouwbaar de exacte namen die je in code moet
gebruiken.

## Licentie

Voeg hier je gewenste licentie toe (bijv. MIT).

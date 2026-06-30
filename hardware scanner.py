"""
Webots Hardware Scanner
========================
Vraagt eenmalig alle actieve devices van de robot op en print
hun index, type en exacte naam. Handig om de juiste device-namen
te achterhalen voor gebruik in andere controllers (camera, LiDAR,
motoren, etc.).

Gebruik:
    Koppel dit script als controller aan de robot in Webots en start
    de simulatie. De output verschijnt in de Webots console.
"""

from controller import Robot


def scan_devices(robot: Robot) -> None:
    """Print een overzicht van alle devices die aan de robot hangen."""
    num_devices = robot.getNumberOfDevices()
    print(f"Totaal aantal gevonden componenten: {num_devices}\n")

    for index in range(num_devices):
        device = robot.getDeviceByIndex(index)
        print(f"[ID {index:02d}] Type: {device.getNodeType()} | Naam: '{device.getName()}'")


def main() -> None:
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    print("=" * 40)
    print("  WEBOTS HARDWARE SCANNER GESTART  ")
    print("=" * 40)

    scan_devices(robot)

    print("=" * 40)
    print("  SCAN VOLTOOID - CONTROLLER STOPT  ")
    print("=" * 40)

    # Eén enkele stap is voldoende; de scan zelf vereist geen simulatielus.
    robot.step(timestep)


if __name__ == "__main__":
    main()

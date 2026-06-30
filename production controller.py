"""
Production Controller - Uniform Floor Edition
================================================
Geoptimaliseerde, high-speed sensor-fusiecontroller voor een egale,
lichte arena-vloer. Combineert LiDAR ('LDS-01') en camera voor
obstakeldetectie, met filtering van de eigen robotschaduw.
"""

from controller import Robot

# --- Configuratie ---------------------------------------------------------
LIDAR_SIDE_SAMPLES = 40        # Aantal lidar-samples dat links/rechts wordt bekeken
FRONT_STOP_DISTANCE = 0.22     # Afstand (m) waarop de robot stopt/terugrijdt
SIDE_BLOCK_DISTANCE = 0.45     # Afstand (m) waarop een zijde als 'geblokkeerd' geldt
COLOR_THRESHOLD = 180          # RGB-waarde onder dit getal telt als 'donker object'
PIXEL_BLOCK_THRESHOLD = 8      # Aantal donkere pixels voordat een zijde geblokkeerd is
SHADOW_MARGIN_PX = 5           # Onderste rand van het beeld die genegeerd wordt (eigen schaduw)

REVERSE_LEFT_SPEED = -1.5
REVERSE_RIGHT_SPEED = -1.0
TURN_AROUND_LEFT_SPEED = -1.5
TURN_AROUND_RIGHT_SPEED = 1.5
SHARP_TURN_FAST_SPEED = 3.0
SHARP_TURN_SLOW_SPEED = 0.3
FORWARD_SPEED = 3.5


def get_lidar_distances(lidar) -> tuple[float, float, float]:
    """Bepaal de kortste afstand voor, links en rechts uit de LiDAR-data."""
    data = lidar.getRangeImage()
    front = min(data[len(data) // 4: 3 * len(data) // 4])
    left = min(data[0:LIDAR_SIDE_SAMPLES])
    right = min(data[len(data) - LIDAR_SIDE_SAMPLES:])
    return front, left, right


def count_dark_pixels(camera) -> tuple[int, int]:
    """
    Tel donkere pixels (= contrast t.o.v. de egale vloer) in de onderste
    helft van het camerabeeld, links/rechts. De alleronderste rand wordt
    genegeerd om de eigen schaduw van de robot uit te filteren.
    """
    image = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()
    mid_x = width // 2

    left_pixels = 0
    right_pixels = 0

    for y in range(int(height * 0.5), height - SHADOW_MARGIN_PX):
        for x in range(int(width * 0.1), int(width * 0.9)):
            r = camera.imageGetRed(image, width, x, y)
            g = camera.imageGetGreen(image, width, x, y)
            b = camera.imageGetBlue(image, width, x, y)

            if r < COLOR_THRESHOLD or g < COLOR_THRESHOLD or b < COLOR_THRESHOLD:
                if x < mid_x:
                    left_pixels += 1
                else:
                    right_pixels += 1

    return left_pixels, right_pixels


def drive(left_wheel, right_wheel, front_dist, left_blocked, right_blocked) -> None:
    """Bepaal en zet de wielsnelheden op basis van de sensor-fusie."""
    if front_dist < FRONT_STOP_DISTANCE:
        left_wheel.setVelocity(REVERSE_LEFT_SPEED)
        right_wheel.setVelocity(REVERSE_RIGHT_SPEED)
    elif left_blocked and right_blocked:
        left_wheel.setVelocity(TURN_AROUND_LEFT_SPEED)
        right_wheel.setVelocity(TURN_AROUND_RIGHT_SPEED)
    elif left_blocked:
        left_wheel.setVelocity(SHARP_TURN_FAST_SPEED)
        right_wheel.setVelocity(SHARP_TURN_SLOW_SPEED)
    elif right_blocked:
        left_wheel.setVelocity(SHARP_TURN_SLOW_SPEED)
        right_wheel.setVelocity(SHARP_TURN_FAST_SPEED)
    else:
        left_wheel.setVelocity(FORWARD_SPEED)
        right_wheel.setVelocity(FORWARD_SPEED)


def main() -> None:
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    camera = robot.getDevice('camera')
    camera.enable(timestep)

    lidar = robot.getDevice('LDS-01')
    lidar.enable(timestep)

    left_wheel = robot.getDevice('left wheel motor')
    right_wheel = robot.getDevice('right wheel motor')
    left_wheel.setPosition(float('inf'))
    right_wheel.setPosition(float('inf'))

    print("[SUCCESS] Production controller actief. Modus: Egale vloer.")

    while robot.step(timestep) != -1:
        front_dist, left_dist, right_dist = get_lidar_distances(lidar)
        left_pixels, right_pixels = count_dark_pixels(camera)

        left_blocked = left_dist < SIDE_BLOCK_DISTANCE or left_pixels > PIXEL_BLOCK_THRESHOLD
        right_blocked = right_dist < SIDE_BLOCK_DISTANCE or right_pixels > PIXEL_BLOCK_THRESHOLD

        drive(left_wheel, right_wheel, front_dist, left_blocked, right_blocked)


if __name__ == "__main__":
    main()

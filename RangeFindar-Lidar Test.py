from controller import Robot

# 1. INITIALISATIE
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Hardware initialiseren
lidar = robot.getDevice('LDS-01')
lidar.enable(timestep)

depth_camera = robot.getDevice('depth-camera')
depth_camera.enable(timestep)

left_wheel = robot.getDevice('left wheel motor')
right_wheel = robot.getDevice('right wheel motor')
left_wheel.setPosition(float('inf'))
right_wheel.setPosition(float('inf'))

# 2. SIMULATIE-LOOP
while robot.step(timestep) != -1:
    
    # --- LIDAR DATA ---
    lidar_data = lidar.getRangeImage()
    front_dist = min(lidar_data[len(lidar_data)//4 : 3*len(lidar_data)//4])
    left_dist  = min(lidar_data[0:40])  
    right_dist = min(lidar_data[len(lidar_data)-40:]) 
    
    # --- RANGEFINDER DATA ---
    depth_image = depth_camera.getRangeImage()
    width = depth_camera.getWidth()
    height = depth_camera.getHeight()
    mid_x = width // 2
    
    left_pixels = 0
    right_pixels = 0
    
    # Dynamisch scanvlak op basis van de werkelijke sensorresolutie
    for y in range(int(height * 0.4), int(height * 0.75)):
        for x in range(int(width * 0.15), int(width * 0.85)):
            pixel_distance = depth_image[x + (y * width)]
            
            # Filterzone: objecten tussen 10cm en 28cm voor de robot
            if 0.10 < pixel_distance < 0.28:
                if x < mid_x:
                    left_pixels += 1
                else:
                    right_pixels += 1

    # --- SENSOR FUSIE BESLISSINGSMATRIX ---
    left_blocked = (left_dist < 0.35) or (left_pixels > 5)
    right_blocked = (right_dist < 0.35) or (right_pixels > 5)
    
    # --- NAVIGATIELOGICA ---
    if front_dist < 0.20:
        # Blokkade recht voor de neus -> Achteruit/uitwijken
        left_wheel.setVelocity(-1.5)
        right_wheel.setVelocity(-1.0)
    elif left_blocked and right_blocked:
        # Volledig ingesloten -> Draaien op de plaats
        left_wheel.setVelocity(-1.5)
        right_wheel.setVelocity(1.5)
    elif left_blocked:
        # Obstakel links -> Bocht naar rechts
        left_wheel.setVelocity(3.2)
        right_wheel.setVelocity(0.5) 
    elif right_blocked:
        # Obstakel rechts -> Bocht naar links
        left_wheel.setVelocity(0.5) 
        right_wheel.setVelocity(3.2)
    else:
        # Weg is vrij -> Rechtuit rijden
        left_wheel.setVelocity(3.5)
        right_wheel.setVelocity(3.5)
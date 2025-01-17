import math

# convert pixel values to measurements
# ultimately we need to convert pixels to a number of steps

vector = [[347.55,159.19],[341.85,162.08]]

def pixels_to_inches(p, axis):

    p_width = 640
    p_height = 360

    i_width = 23 + 5 / 32
    i_height = 13 + 5/32

    p_i_width_ratio = i_width / p_width
    p_i_height_ratio = i_height / p_height

    if axis == 0:
        return p*p_i_width_ratio
    if axis == 1:
        return p*p_i_height_ratio

#print( pixels_to_inches(200, 1) )

def velocity(p1, t1, p2, t2):

    x = ( p2[0] - p1[0] ) / ( t2 - t1)
    y = ( p2[1] - p1[1] ) / ( t2 - t1)

    return math.sqrt( x**2 + y**2 ), [x,y]

#v, components = velocity(vector[0], 0, vector[1], 0.0406)

def forecast(components, time):

    x = components[0]

    y = components[1]
    print("Forecast Insight. Future Y", y*time, "In time", time)

    return [x*time, y*time]

#print(v, components)
#print(forecast(components, 7))
### Track velocity using camera refresh rate
### Detect the current position, velocity, and input into a position function to detect future states.
### Some open loop fine tuning for velocity might be necissary (math based model)

### Task 1 will be kicking a ball from a static place and predicting its path
### Task 2 will be slowly moving a ball

### Kick a ball and calibrate the vision system

### We will need to track the heads of the red players to detect gaps in their defenses

### We can find the positioning of Blue Team based on a mostly open loop model
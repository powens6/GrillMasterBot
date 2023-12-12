import time
import numpy as np
from RoboticArm import RoboticArm
from scipy.interpolate import CubicSpline

def cook_time_on_george_foreman(thickness, doneness):
    """
    Estimates cooking time for a steak on the first side on a George Foreman grill based on its thickness and desired doneness.

    Parameters:
    thickness (float): Thickness of the steak in inches.
    doneness (str): Desired doneness of the steak ('rare', 'medium-rare', 'medium', 'well-done').

    Returns:
    int: Estimated cooking time in minutes for the first side.
    """

    base_times = {
        'rare': 2.5,
        'medium-rare': 3,
        'medium': 4,
        'well-done': 5
    }

    # Check if the doneness input is valid
    if doneness not in base_times:
        return "Invalid doneness level. Please choose from 'rare', 'medium-rare', 'medium', 'well-done'."

    # Calculate the cooking time based on thickness and base time for the desired doneness
    # Assuming the base time is for a 1-inch thick steak
    cooking_time = base_times[doneness] * thickness

    return round(cooking_time, 2)

def spline(point1, point2):
    """
    Generates a set of interpolated points between two given points using a cubic spline with specified start and end velocities.

    This function calculates a cubic spline interpolation between a start point and an end point. The interpolation also considers start and end velocities to ensure a smooth transition. It generates a specified number of points (default is 10) along the spline.

    Parameters:
    point1 (array-like): The starting point of the spline. Should be a sequence of coordinates (e.g., [x, y, z]).
    point2 (array-like): The ending point of the spline. Should be a sequence of coordinates similar to `point1`.

    Returns:
    ndarray: An array of interpolated points along the cubic spline between `point1` and `point2`.

    Note:
    - The velocities at both the start and end points are currently set as fixed values within the function.
    - The number of interpolated points is set to 10 by default.
    """
    start_point = np.array(point1)
    end_point = np.array(point2)       
    start_velocity = np.array([0, 20, 0])   
    end_velocity = np.array([0, 20, 0])    

    t = np.array([0, 1])  # Start and end times
    points = np.array([start_point, end_point])

    # Calculate cubic spline with velocity constraints
    cs = CubicSpline(t, points, bc_type=((1, start_velocity), (1, end_velocity)))

    # Interpolate points
    t_interpolated = np.linspace(0, 1, num=10) 
    interpolated_points = cs(t_interpolated)
    return interpolated_points

def main():
    while True:
        try:
            thickness = float(input("Enter the thickness of your steak (in inches): "))
            doneness = input("Enter your desired doneness (rare, medium-rare, medium, well-done): ")

            cook_time = cook_time_on_george_foreman(thickness, doneness)
            if isinstance(cook_time, str):
                print(cook_time)
                continue

            print("Estimated cooking time on the first side: ", cook_time, "minutes")

            
            commands = [
            [0, 0, 417.4, 0, False],
            [0, 5, 400, 10, False],
            [0, 250, 90, 0, False],
            [0, 325, 90, 0, False],
            [0, 325, 112.70, 8, False],
            [0, 5, 400, 8, False],
            [0, -5, 400, 8, False],
            [0, 5, 400, 8, True],
            [0, 250, 112.70, 8, True],
            [0, 250, 112.70, 0, True],
            [0, 5, 400, 8, True],
            [0, 0, 417.4, 0, False]
            ]

            steakBot = RoboticArm('COM3', 115200)
            steakBot.send_command(0, 0, 417.4, 0)
            time.sleep(cook_time*60)
            for command in commands:
                steakBot.send_command(command[0], command[1], command[2], command[3], command[4])
                time.sleep(1)
            steakBot.close()

        except ValueError:
            print("Please enter a valid number for the thickness.")

        except KeyboardInterrupt:
            print("\nExiting the program.")
            break

if __name__ == "__main__":
    main()
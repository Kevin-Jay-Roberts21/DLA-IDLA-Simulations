# necessary imports
import turtle
from turtle import *
import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

turtle1 = Turtle()
turtle2 = Turtle()

def particle_random_movement(particle_time_info, aggregate, aggregate_boundary, environment_size, number_of_boundary_points, max_bounds, model_type, lattice_type):
    kill_count = 0
    # while loop runs until wandering particle hits the aggregate
    while True:
        if model_type == "DLA":
            bad_particle = True # a particle that spawns in the aggregate
            while bad_particle:

                if lattice_type == "square":

                    # getting random position in the environment
                    random_y = random.randint((environment_size*-10), (environment_size*10))
                    random_x = random.randint((environment_size*-10), (environment_size*10))

                else: # hexagonal lattice
                    random_y = random.randint((environment_size*-10), (environment_size*10))

                    if random_y % 2 == 0: # if even y coordinate
                        if random_y % 4 == 0:
                            random_x = random.randint((environment_size*-10)/2, (environment_size*10)/2) * 2
                        else:
                            random_x = random.choice(range((environment_size*-10) + 1, (environment_size*10), 2))
                    else:
                        if random_y > 0:
                            if ((random_y) + 1) % 4 == 0:
                                random_x = random.choice(range((environment_size*-10) + 1, (environment_size*10), 2))
                            else:
                                random_x = random.randint((environment_size*-10)/2, (environment_size*10)/2) * 2
                        else:
                            if ((random_y) - 1) % 4 == 0:
                                random_x = random.randint((environment_size*-10)/2, (environment_size*10)/2) * 2
                            else:
                                random_x = random.choice(range((environment_size*-10) + 1, (environment_size*10), 2))

                # bad x,y value (x,y coordinate is inside the imaginary "aggregate spare")
                if (random_x*10 <= max_bounds[0] and random_x*10 >= max_bounds[1]) and (random_y*10 <= max_bounds[2] and random_y*10 >= max_bounds[3]):
                    bad_particle = True
                else:
                    bad_particle = False
        else:
            random_y = 0
            random_x = 0

        # animation for wandering particle (black dot)
        turtle1.hideturtle()
        turtle1.shape("circle")
        turtle1.shapesize(0.3)
        turtle1.fillcolor("blue")
        turtle1.color("black")
        turtle1.speed(0)
        turtle1.penup()
        turtle1.setpos(random_x*10, random_y*10)
        turtle1.showturtle()
        turtle1.pendown()
        fillcolor("red")

        # particle wanders around in this while loop until it either hits the boundary of the environment
        # or hits the aggregate
        kill_particle = False
        hit_aggregate = False
        time = 0
        while (kill_particle==False and hit_aggregate==False):
            time += 1
            if lattice_type == "square":
                # implementing random direction the particle takes
                random_movement = random.randint(1, 4)  # get a random number between 1 and 4
                if random_movement == 1:
                    turtle1.setheading(0)
                    turtle1.forward(10)
                elif random_movement == 2:
                    turtle1.setheading(90)
                    turtle1.forward(10)
                elif random_movement == 3:
                    turtle1.setheading(180)
                    turtle1.forward(10)
                else:
                    turtle1.setheading(270)
                    turtle1.forward(10)
            else:
                random_movement = random.randint(1, 3)  # get random number between 1 and 3

                if (turtle1.pos()[1]/10) % 2 != 0:
                    if random_movement == 1:
                        turtle1.goto(turtle1.pos()[0] - 10, turtle1.pos()[1] + 10)
                    elif random_movement == 2:
                        turtle1.goto(turtle1.pos()[0] + 10, turtle1.pos()[1] + 10)
                    else:
                        turtle1.goto(turtle1.pos()[0], turtle1.pos()[1] - 10)
                else:
                    if random_movement == 1:
                        turtle1.goto(turtle1.pos()[0], turtle1.pos()[1] + 10)
                    elif random_movement == 2:
                        turtle1.goto(turtle1.pos()[0] + 10, turtle1.pos()[1] - 10)
                    else:
                        turtle1.goto(turtle1.pos()[0] - 10, turtle1.pos()[1] - 10)

            # after movement, check to see if particle hit boundary or aggregate
            kill_particle = kill_particle_check(round(turtle1.pos()[0]), round(turtle1.pos()[1]), environment_size)
            hit_aggregate = hit_aggregate_check(round(turtle1.pos()[0]), round(turtle1.pos()[1]), aggregate, aggregate_boundary, number_of_boundary_points, max_bounds, lattice_type)

        turtle1.reset()
        turtle1.hideturtle()

        # if particle hit the boundary, kill it
        if kill_particle == True:
            particle_time_info[0].append(time)
            kill_count += 1

        # if particle hit the aggregate, start a new particle
        if hit_aggregate == True:
            particle_time_info[1].append(time)
            particle_time_info[2].append(kill_count)
            break

# function to check if the particle wandered outside of the environment
def kill_particle_check(x_pos, y_pos, environment_size):
    if x_pos > (environment_size * 100) or x_pos < (environment_size * -100) or y_pos > (environment_size * 100) or y_pos < (environment_size * -100):
        return True
    else:
        return False

# function to check if the particle hit the aggregate
def hit_aggregate_check(x_pos, y_pos, aggregate, aggregate_boundary, number_of_boundary_points, max_bounds, lattice_type):
    for i in range(len(aggregate_boundary)):
        if [x_pos, y_pos] == aggregate_boundary[i]:

            # updating aggregate, boundary points, and animation
            update_aggregate(x_pos, y_pos, aggregate)
            new_bdry_points = update_aggregate_boundary(x_pos, y_pos, aggregate, aggregate_boundary, number_of_boundary_points, max_bounds, lattice_type)
            new_aggregate_point = [x_pos, y_pos]
            update_aggregate_picture(new_aggregate_point, new_bdry_points)

            aggregate_boundary.remove([x_pos, y_pos]) # this is not a part of the boundary anymore

            return True
    return False

# function adds red dot to aggregate
def update_aggregate(x_pos, y_pos, aggregate):
    particle_addition = [x_pos, y_pos]
    aggregate.append(particle_addition)

# updates the purple dots
def update_aggregate_boundary(x_pos, y_pos, aggregate, aggregate_boundary, number_of_boundary_points, max_bounds, lattice_type):

    top_left_corner_shift = [x_pos - 10, y_pos + 10]
    top_right_corner_shift = [x_pos + 10, y_pos + 10]
    bottom_right_corner_shift = [x_pos + 10, y_pos - 10]
    bottom_left_corner_shift = [x_pos - 10, y_pos - 10]

    particle_position_shift_up = [x_pos, y_pos + 10]
    particle_position_shift_down = [x_pos, y_pos - 10]
    particle_position_shift_left = [x_pos - 10, y_pos]
    particle_position_shift_right = [x_pos + 10, y_pos]
    new_boundary_points = []

    if lattice_type == "square":

        # checking to see what the state of the dots are around the new "red dot"
        if (particle_position_shift_up not in aggregate) and (particle_position_shift_up not in aggregate_boundary):
            aggregate_boundary.append(particle_position_shift_up)
            new_boundary_points.append(particle_position_shift_up)
            if max_bounds[2] < (y_pos + 10):
                max_bounds[2] += 10
        if (particle_position_shift_down not in aggregate) and (particle_position_shift_down not in aggregate_boundary):
            aggregate_boundary.append(particle_position_shift_down)
            new_boundary_points.append(particle_position_shift_down)
            if max_bounds[3] > (y_pos - 10):
                max_bounds[3] -= 10
        if (particle_position_shift_left not in aggregate) and (particle_position_shift_left not in aggregate_boundary):
            aggregate_boundary.append(particle_position_shift_left)
            new_boundary_points.append(particle_position_shift_left)
            if max_bounds[1] > (x_pos - 10):
                max_bounds[1] -= 10
        if (particle_position_shift_right not in aggregate) and (particle_position_shift_right not in aggregate_boundary):
            aggregate_boundary.append(particle_position_shift_right)
            new_boundary_points.append(particle_position_shift_right)
            if max_bounds[0] < (x_pos + 10):
                max_bounds[0] += 10

        # checking additional positions if aggregate_boundary is 8 dots instead of 4
        if number_of_boundary_points == 8:
            if (top_left_corner_shift not in aggregate) and (top_left_corner_shift not in aggregate_boundary):
                aggregate_boundary.append(top_left_corner_shift)
                new_boundary_points.append(top_left_corner_shift)
            if (top_right_corner_shift not in aggregate) and (top_right_corner_shift not in aggregate_boundary):
                aggregate_boundary.append(top_right_corner_shift)
                new_boundary_points.append(top_right_corner_shift)
            if (bottom_right_corner_shift not in aggregate) and (bottom_right_corner_shift not in aggregate_boundary):
                aggregate_boundary.append(bottom_right_corner_shift)
                new_boundary_points.append(bottom_right_corner_shift)
            if (bottom_left_corner_shift not in aggregate) and (bottom_left_corner_shift not in aggregate_boundary):
                aggregate_boundary.append(bottom_left_corner_shift)
                new_boundary_points.append(bottom_left_corner_shift)
    else:
        if (turtle1.pos()[1]/10) % 2 != 0: # two up shifts and 1 down shift
            if (particle_position_shift_down not in aggregate) and (
                    particle_position_shift_down not in aggregate_boundary):
                aggregate_boundary.append(particle_position_shift_down)
                new_boundary_points.append(particle_position_shift_down)
                if max_bounds[3] > (y_pos - 10):
                    max_bounds[3] -= 10
            if (top_left_corner_shift not in aggregate) and (top_left_corner_shift not in aggregate_boundary):
                aggregate_boundary.append(top_left_corner_shift)
                new_boundary_points.append(top_left_corner_shift)
            if (top_right_corner_shift not in aggregate) and (top_right_corner_shift not in aggregate_boundary):
                aggregate_boundary.append(top_right_corner_shift)
                new_boundary_points.append(top_right_corner_shift)
        else:
            if (particle_position_shift_up not in aggregate) and (particle_position_shift_up not in aggregate_boundary):
                aggregate_boundary.append(particle_position_shift_up)
                new_boundary_points.append(particle_position_shift_up)
                if max_bounds[2] < (y_pos + 10):
                    max_bounds[2] += 10
            if (bottom_right_corner_shift not in aggregate) and (bottom_right_corner_shift not in aggregate_boundary):
                aggregate_boundary.append(bottom_right_corner_shift)
                new_boundary_points.append(bottom_right_corner_shift)
            if (bottom_left_corner_shift not in aggregate) and (bottom_left_corner_shift not in aggregate_boundary):
                aggregate_boundary.append(bottom_left_corner_shift)
                new_boundary_points.append(bottom_left_corner_shift)

    return new_boundary_points

# function that updates aggregate picture
def update_aggregate_picture(new_aggregate_point, new_bdry_points):
    turtle2.penup()
    # adding the aggregate point (just drawing a red dot over a purple one)
    turtle2.width(5)
    turtle2.color("red")
    turtle2.speed(1)
    turtle2.penup()
    turtle2.setpos(new_aggregate_point[0], new_aggregate_point[1])
    turtle2.pendown()
    turtle2.forward(1)
    turtle2.penup()
    turtle2.color("purple")
    # adding additional purple dots
    for i in range(len(new_bdry_points)):
        turtle2.setpos(new_bdry_points[i][0], new_bdry_points[i][1])
        turtle2.pendown()
        turtle2.forward(1)
        turtle2.penup()


def draw_initial_aggregate(aggregate_boundary):

    # drawing initial "red dot" and it's boundary "purple dots"

    turtle2.width(5)
    turtle2.penup()
    turtle2.color("red")
    turtle2.setpos(0, 0)
    turtle2.pendown()
    turtle2.forward(1)
    turtle2.color("purple")
    turtle2.penup()

    for i in range(len(aggregate_boundary)):
        turtle2.setpos(aggregate_boundary[i][0], aggregate_boundary[i][1])
        turtle2.pendown()
        turtle2.forward(1)
        turtle2.penup()

    turtle2.width(1)
    turtle2.color("black")

def data_outputs(particle_time_info, model_type):

    ########################
    ## Defining list info ##
    ########################
    time_of_killed_particles = particle_time_info[0]
    time_of_lived_particles = particle_time_info[1]
    particles_killed = particle_time_info[2]
    total_particles_killed = 0
    total_time_of_lived_particles = 0
    total_time_of_killed_particles = 0
    for i in range(len(particles_killed)):
        total_particles_killed += particles_killed[i]
    for i in range(len(time_of_lived_particles)):
        total_time_of_lived_particles += time_of_lived_particles[i]
    for i in range(len(time_of_killed_particles)):
        total_time_of_killed_particles += time_of_killed_particles[i]
    total_time = total_time_of_lived_particles + total_time_of_killed_particles


    ###################
    ## Plotting info ##
    ###################
    if model_type == "DLA":

        fig = plt.figure(figsize=(13, 6.5))
        gs = gridspec.GridSpec(2, 3, height_ratios=[0.5, 0.2], hspace=0.3)

        axes = []

        axes.append(fig.add_subplot(gs[0, 0]))
        axes[0].plot(time_of_killed_particles)
        axes[0].set_title('Graph 1')
        axes[0].set_xlabel('Number of Particles in Aggregate')
        axes[0].set_ylabel('Particle Wandering Time Before Hitting Environment Boundary')
        axes.append(fig.add_subplot(gs[0, 1]))
        axes[1].plot(time_of_lived_particles)
        axes[1].set_title('Graph 2')
        axes[1].set_xlabel('Number of Particles in Aggregate')
        axes[1].set_ylabel('Particle Wandering Time Before Hitting Aggregate Boundary')
        axes.append(fig.add_subplot(gs[0, 2]))
        axes[2].plot(particles_killed)
        axes[2].set_title('Graph 3')
        axes[2].set_xlabel('Number of Particles in Aggregate')
        axes[2].set_ylabel('Number of Particles Killed Before Hitting Aggregate')

        fig.text(0.5, 0.05,
                 "Total particles killed: " + str(
                     total_particles_killed) + "\n" + "Total time of particles killed: " + str(
                     total_time_of_killed_particles) + "\n" + "Total time of lived particles: " + str(
                     total_time_of_lived_particles) + "\n" + "Total time: " + str(total_time), ha='center', fontsize=12)

        plt.suptitle("Final Data", fontsize=14)

        plt.show()

    else:

        fig = plt.figure(figsize=(7, 7))
        gs = gridspec.GridSpec(2, 1, height_ratios=[0.5, 0.2], hspace=0.2)

        axes = []

        axes.append(fig.add_subplot(gs[0, 0]))
        axes[0].plot(time_of_lived_particles)
        axes[0].set_title('Graph 1')
        axes[0].set_xlabel('Number of Particles in Aggregate')
        axes[0].set_ylabel('Particle Wandering Time Before Hitting Aggregate Boundary')

        fig.text(0.5, 0.05,
                 "Total particles killed: " + str(
                     total_particles_killed) + "\n" + "Total time of particles killed: " + str(
                     total_time_of_killed_particles) + "\n" + "Total time of lived particles: " + str(
                     total_time_of_lived_particles) + "\n" + "Total time: " + str(total_time), ha='center', fontsize=12)

        plt.suptitle("Final Data", fontsize=14)

        plt.show()

def validate_modeltype(model_type):
    try:
        model_type = int(model_type)
        if (model_type != 0) and (model_type != 1):
            messagebox.showerror("Error", "Model Type must be 0 or 1.")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Invalid model type value. Please enter a valid model type.")
        return False

def validate_latticetype(lattice_type):
    try:
        lattice_type = int(lattice_type)
        if (lattice_type != 0) and (lattice_type != 1):
            messagebox.showerror("Error", "Lattice Type must be 0 or 1.")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Invalid lattice type value. Please enter a valid lattice type.")
        return False

def validate_environmentsize(env_size):
    environment_choices = [1, 2, 3, 4, 5, 6, 7, 8]
    try:
        env_size = int(env_size)
        if env_size not in environment_choices:
            messagebox.showerror("Error", "Environment size must be a 1, 2, 3, 4, 5, 6, 7, or 8.")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Invalid environment size value. Please enter a valid environment size.")
        return False

def validate_aggregatesize(agg_size):
    try:
        agg_size = int(agg_size)
        if agg_size < 1:
            messagebox.showerror("Error", "Aggregate size must be a positive integer.")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Invalid aggregate size value. Please enter a valid aggregate size.")
        return False

def validate_boundarypoints(number_of_boundary_points):
    try:
        number_of_boundary_points = int(number_of_boundary_points)
        if (number_of_boundary_points != 4) and (number_of_boundary_points != 8):
            messagebox.showerror("Error", "Number of boundary points must be 4 or 8.")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Invalid number of boundary points value. Please enter a valid number of boundary points.")
        return False

def run_graphics():

    ############
    ## Inputs ##
    ############
    # environment_size will vary, picking 4 (for example) implies that the set up is 400 by 400 pixels
    # environment_size should only be an element on (1, 2, 3, 4, 5, 6, 7, 8), just to ensure software division
    # rounding of a different value won't affect proper functioning of program.

    model_type = modeltype_entry.get()
    lattice_type = latticetype_entry.get()
    env_size = environmentsize_entry.get()
    agg_size = aggregatesize_entry.get()
    number_of_boundary_points = boundarypoints_entry.get()

    # Validate age and name
    if not validate_modeltype(model_type) or not validate_latticetype(lattice_type) or not validate_environmentsize(env_size) or not validate_aggregatesize(agg_size) or not validate_boundarypoints(number_of_boundary_points):
        return

    # Close the Tkinter window
    window.destroy()

    model_type = int(model_type)
    lattice_type = int(lattice_type)
    env_size = int(env_size)
    agg_size = int(agg_size)
    number_of_boundary_points = int(number_of_boundary_points)
    model_type = model_choices[model_type]
    lattice_type = env_type[lattice_type]


    ##################################################
    ## Creating initial Aggregate and it's boundary ##
    ##################################################
    # it's important to note that aggregate_boundary is the boundary of the aggregate and NOT the
    # boundary of the environment. Additionally, I'm defining the aggregate to be just the red dots
    # and not the entire aggregate itself
    aggregate = [[0, 0]]
    aggregate_boundary = [10, -10, 10, -10] # order: max_x, min_x, max_y, min_y
    max_bounds = [10, -10, 10, -10] # max boundary will be the same for 4 and 8 particle boundary

    if lattice_type == "square":
        if number_of_boundary_points == 4:
            aggregate_boundary = [[10, 0], [-10, 0], [0, 10], [0, -10]]
        elif number_of_boundary_points == 8:
            aggregate_boundary = [[10, 0], [-10, 0], [0, 10], [0, -10], [-10, -10], [-10, 10], [10, 10], [10, -10]]
        else:
            quit()  # not allowing any other number of boundary points
    else: # hexagonal lattice
        number_of_boundary_points = 3
        aggregate_boundary = [[0, 10], [-10, -10], [10, -10]]


    ###################################
    ## Drawing the initial aggregate ##
    ###################################
    turtle2.hideturtle()
    turtle2.speed("slow")
    turtle.setup(env_size*100, env_size*100)
    turtle.hideturtle()
    draw_initial_aggregate(aggregate_boundary)


    ####################
    ## Run Simulation ##
    ####################
    # first list is time it takes particle to wander before it leaves boundary for each n iterations
    # second list is time is takes particle to hit the aggregate for each n
    # third is the number of particles killed at each "number of particles in aggregate"
    particle_time_info = [[], [], []]
    # runs until aggregate consists of n+1 particles (because we start with 1 particle)
    for i in range(agg_size):
        particle_random_movement(particle_time_info, aggregate, aggregate_boundary, int(env_size/2), number_of_boundary_points, max_bounds, model_type, lattice_type)
        print("Red Dot Count: " + str(i+2))
        if (max_bounds[0] >= env_size * 100/2) and (max_bounds[1] <= env_size * -100/2):
            print("Exited program because the aggregate has grown beyond the environment boundary.")
            break
        if (max_bounds[2] >= env_size * 100/2) and (max_bounds[3] <= env_size * -100/2):
            print("Exited program because the aggregate has grown beyond the environment boundary.")
            break


    ##################
    ## Collect Data ##
    ##################
    turtle.done() # leaves image open
    data_outputs(particle_time_info, model_type)


####################################
## Main Simulation Initialization ##
####################################
env_type = ["square", "hexagonal"]
model_choices = ["DLA", "IDLA"]

# Create the Tkinter window
window = tk.Tk()

# Configure window settings
window.title("Turtle Drawing")
window.geometry("600x400")  # Increase the dimensions of the window

# Create labels and entry fields for each question
modeltype_label = tk.Label(window, text="Model Type (0 - DLA, 1 - IDLA):")
modeltype_label.pack(anchor="w", padx=10, pady=5)
modeltype_entry = tk.Entry(window)
modeltype_entry.pack(anchor="w", padx=10)

latticetype_label = tk.Label(window, text="Lattice Type (0 - Square, 1 - Hexagonal):")
latticetype_label.pack(anchor="w", padx=10, pady=5)
latticetype_entry = tk.Entry(window)
latticetype_entry.pack(anchor="w", padx=10)

environmentsize_label = tk.Label(window, text="Environment Size (1, 2, 3, 4, 5, 6, 7, 8):")
environmentsize_label.pack(anchor="w", padx=10, pady=5)
environmentsize_entry = tk.Entry(window)
environmentsize_entry.pack(anchor="w", padx=10)

aggregatesize_label = tk.Label(window, text="Aggregate Size (How many red dots?):")
aggregatesize_label.pack(anchor="w", padx=10, pady=5)
aggregatesize_entry = tk.Entry(window)
aggregatesize_entry.pack(anchor="w", padx=10)

boundarypoints_label = tk.Label(window, text="# of Boundary Points (4 or 8):")
boundarypoints_label.pack(anchor="w", padx=10, pady=5)
boundarypoints_entry = tk.Entry(window)
boundarypoints_entry.pack(anchor="w", padx=10)

note = tk.Label(window, text="(Note: if hexagonal lattice is chosen, boundary points is defaulted to 3.)")
note.pack(anchor="w", padx=10, pady=5)

# Create a button to trigger the turtle drawing
draw_button = tk.Button(window, text="Run Simulation", command=run_graphics, width=12, height=2)
draw_button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()
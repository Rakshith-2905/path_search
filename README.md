# Robot Path Planning

A program that creates a game environment where a user can build walls and set a start and stop point. The robot would travel through the map to find a path to the stop point.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Dependencies

Python 2.7  
*See [Installing python](https://www.python.org/download/releases/2.7/) for instructions on how to install python.*  
Pygame 1.9.3  
*See [Installing pygame](https://cit.dixie.edu/cs/1410/pygame-installation.pdf) for instructions on how to install pygame.*  


## How to run

Open a terminal or console. Change the operating directory to where the ```robot_path.py``` file is  and type in

```
python robot_path.py
```

## Program structure

The program first executes the `if __name__ == '__main__':` function. The function checks if there any maps available to load, if not it creates an empty map by calling `game_env()` function. The game_env function reads the map if available and visualizes the walls, start and the stop points. Else it creates a empty map with buttons that aid in building a new map. The list of buttons available are.  

clear : Button to clear the entire map. Can be used to clear the loaded map as well.  
start pt: Button to create a start point(Try not to place multiple start points).  
stop pt: Button to create a stop point.  
wall : Button to create walls, when using this button only the end wall button can be used.  
end_wall : Button to end the wall creating operation.  
delete pt : Button to delete any point on the map.  
save : Button to save the current map.  
run robot: Button to run the robot.  

After this, the main function calls the `game_play()` function.

The game play function monitors every button and performs corresponding actions. If the run robot button is clicked the function `find_path()` is called with the start position of as the parameter.

The find path function finds the next position to move by calling the `adjacent_pos()` function. The `adjacent_pos` function also keeps track of positions with multiple options for next step in the list `vertex_trak`. If there are multiple options, the robot randomly choses an option as its next step. The find position function would update the list `path` and `back_track` that keeps track of the path taken and would recursively call itself with its current position. This would continue till the robot finds the stop point. It would color the grid points in shades of green to indicate the path.

If the robot gets stuck it would go to the latest position it saw with multiple next position options and would take an alternate option. It then updates all the lists that keeps track of the path of the robot.It would color the grid points in shades of red to the trace back of the path.


## Authors

* **Rakshith Subramanyam** -  [github](https://github.com/Rakshith-2905)


## License

None

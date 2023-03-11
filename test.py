from source import Environment

if __name__ == "__main__" :
    env = Environment()
    print(env.grid_map)
    print("Start row : ",env.start_row)
    print("Start column : ",env.start_column)
    print("Goal row : ",env.goal_row)
    print("Goal column : ",env.goal_column)
    
    # change value
    env.grid_map[env.start_row][env.start_column] = -1
    print(env.grid_map[env.start_row][env.start_column])
    
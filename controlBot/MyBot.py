"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Control")
# Then we print our start message to the logs
logging.info("Starting my bot!")
i = 0
while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    i += 1
    logging.info("New turn: " + str(i))
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue
        command = None
        logging.info("ship: " + str(ship.id) + "vector: " + str(ship.nav))
        for planet in game_map.all_planets():
            if ship.can_dock(planet):
                command = ship.dock(planet)
                command_queue.append(command)
                break

        if command is None:
            ship.nav = hlt.collision.unit(ship.nav)
            target = hlt.entity.Position(ship.x + ship.nav[0]*hlt.constants.MAX_SPEED, ship.y + ship.nav[1]*hlt.constants.MAX_SPEED)
            command = ship.navigate(target, game_map, hlt.constants.MAX_SPEED, max_corrections = 24, angular_step=5)
            logging.info(command)
            if command:
                command_queue.append(command)
        logging.info(command)

        # # For each planet in the game (only non-destroyed planets are included)
        # # gets the nearest unowned planet
        # planets = game_map.unowned_planets(ship)
        # if len(planets) == 0:
        #     planets = game_map.dockable_planets(ship)
        # if len(planets) == 0:
        #     #go towards nearest docked enemy ship
        #     enemy = game_map.nearest_enemy_docked(ship)
        #     navigate_command = None
        #     if enemy:
        #         # logging.info("--------------------ship -> enemy--------------------")
        #         # logging.info(ship)
        #         # logging.info(enemy)
        #         navigate_command, pos = ship.betterNav(
        #                 ship.closest_point_to(enemy, min_distance=1),
        #                 game_map,
        #                 int(hlt.constants.MAX_SPEED),
        #                 10)
        #         if navigate_command:
        #             command_queue.append(navigate_command)
        #             game_map.grid[int(pos[0])][int(pos[1])] = game_map.grid[int(ship.x)][int(ship.y)]

        #     continue

        # planet = planets[sorted(planets)[0]][0]
        # # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
        # if ship.can_dock(planet):
        #     # We add the command by appending it to the command_queue
        #     command_queue.append(ship.dock(planet))
        # else:
        #     # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
        #     # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
        #     # We run this navigate command each turn until we arrive to get the latest move.
        #     # Here we move at half our maximum speed to better control the ships
        #     # In order to execute faster we also choose to ignore ship collision calculations during navigation.
        #     # This will mean that you have a higher probability of crashing into ships, but it also means you will
        #     # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
        #     # wish to turn that option off.
        #     navigate_command, pos = ship.betterNav(
        #         ship.closest_point_to(planet),
        #         game_map,
        #         int(hlt.constants.MAX_SPEED),
        #         10)
        #     # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
        #     # or we are trapped (or we reached our destination!), navigate_command will return null;
        #     # don't fret though, we can run the command again the next turn)
        #     if navigate_command:
        #         command_queue.append(navigate_command)
        #         game_map.grid[int(pos[0])][int(pos[1])] = game_map.grid[int(ship.x)][int(ship.y)]

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END

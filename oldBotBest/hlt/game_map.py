from . import collision, entity
import logging
import sys

class Map:
    """
    Map which houses the current game information/metadata.
    
    :ivar my_id: Current player id associated with the map
    :ivar width: Map width
    :ivar height: Map height
    """

    def __init__(self, my_id, width, height):
        """
        :param my_id: User's id (tag)
        :param width: Map width
        :param height: Map height
        """
        self.my_id = my_id
        self.width = width
        self.height = height
        self._players = {}
        self._planets = {}
        self.grid = [[]]

    def get_me(self):
        """
        :return: The user's player
        :rtype: Player
        """
        return self._players.get(self.my_id)

    def get_player(self, player_id):
        """
        :param int player_id: The id of the desired player
        :return: The player associated with player_id
        :rtype: Player
        """
        return self._players.get(player_id)

    def all_players(self):
        """
        :return: List of all players
        :rtype: list[Player]
        """
        return list(self._players.values())

    def get_planet(self, planet_id):
        """
        :param int planet_id:
        :return: The planet associated with planet_id
        :rtype: entity.Planet
        """
        return self._planets.get(planet_id)

    def all_planets(self):
        """
        :return: List of all planets
        :rtype: list[entity.Planet]
        """
        return list(self._planets.values())

    def nearby_entities_by_distance(self, entity):
        """
        :param entity: The source entity to find distances from
        :return: Dict containing all entities with their designated distances
        :rtype: dict
        """
        result = {}
        for foreign_entity in self._all_ships() + self.all_planets():
            if entity == foreign_entity:
                continue
            result.setdefault(entity.calculate_distance_between(foreign_entity), []).append(foreign_entity)
        return result

    def unowned_planets(self, entity):
        """
        :param entity: The source entity to find distances from
        :return: Dict containing all planets with their designated distances
        :rtype: dict
        """
        result = {}
        for planet in self.all_planets():
            if planet.is_owned():
                continue
            result.setdefault(entity.calculate_distance_between(planet), []).append(planet)
        return result

    def nearest_enemy_planet(self, entity):
        nearest = None
        for planet in self.all_planets():
            if planet.is_owned() and planet.owner.id != self.my_id:
                dist = entity.calculate_distance_between(planet)
                if nearest is None or nearest[0] > dist:
                    nearest = (dist, planet)
        if nearest == None:
            return None
        return nearest[1]

    def dockable_planets(self, entity):
        """
        :param entity: The source entity to find distances from
        :return: Dict containing all planets with their designated distances
        :rtype: dict
        """
        result = {}
        for planet in self.all_planets():
            if planet.is_owned():
                if planet.owner.id != self.my_id:
                    continue
                if len(planet._docked_ship_ids) < planet.num_docking_spots:
                    result.setdefault(entity.calculate_distance_between(planet), []).append(planet)
                continue
            result.setdefault(entity.calculate_distance_between(planet), []).append(planet)
        return result

    def nearest_enemy_docked(self, entity):
        """
        :param entity: The source entity to find distances from
        :return: Dict containing all planets with their designated distances
        :rtype: dict
        """
        planet = self.nearest_enemy_planet(entity)
        if planet == None:
            return None
        ship = planet._docked_ships[planet._docked_ship_ids[0]]
        return ship

    def _link(self):
        """
        Updates all the entities with the correct ship and planet objects

        :return:
        """
        for celestial_object in self.all_planets() + self._all_ships():
            celestial_object._link(self._players, self._planets)
            #add positions to grid
            for x,y in celestial_object.coords:
                self.grid[x][y] = sys.maxsize


    def _parse(self, map_string):
        """
        Parse the map description from the game.

        :param map_string: The string which the Halite engine outputs
        :return: nothing
        """
        tokens = map_string.split()

        #adjust parse methods to not reparse planet coords for ones that don't change
        self._players, tokens = Player._parse(tokens)
        self._planets, tokens = entity.Planet._parse(tokens)

        assert(len(tokens) == 0)  # There should be no remaining tokens at this point
        # build uninitialized map grid
        self.grid = [[0 for i in range(0, self.height)] for j in range(0, self.width)]

        self._link()


    def _all_ships(self):
        """
        Helper function to extract all ships from all players

        :return: List of ships
        :rtype: List[Ship]
        """
        all_ships = []
        for player in self.all_players():
            all_ships.extend(player.all_ships())
        return all_ships

    def _enemy_ships(self):
        
        return enemies

    def _intersects_entity(self, target):
        """
        Check if the specified entity (x, y, r) intersects any planets. Entity is assumed to not be a planet.

        :param entity.Entity target: The entity to check intersections with.
        :return: The colliding entity if so, else None.
        :rtype: entity.Entity
        """
        for celestial_object in self._all_ships() + self.all_planets():
            if celestial_object is target:
                continue
            d = celestial_object.calculate_distance_between(target)
            if d <= celestial_object.radius + target.radius + 0.1:
                return celestial_object
        return None

    def obstacles_between(self, ship, target, ignore=()):
        """
        Check whether there is a straight-line path to the given point, without planetary obstacles in between.

        :param entity.Ship ship: Source entity
        :param entity.Entity target: Target entity
        :param entity.Entity ignore: Which entity type to ignore
        :return: The list of obstacles between the ship and target
        :rtype: list[entity.Entity]
        """
        obstacles = []
        entities = ([] if issubclass(entity.Planet, ignore) else self.all_planets()) \
            + ([] if issubclass(entity.Ship, ignore) else self._all_ships())
        for foreign_entity in entities:
            if foreign_entity == ship or foreign_entity == target:
                continue
            if collision.intersect_segment_circle(ship, target, foreign_entity, fudge=ship.radius + 0.1):
                obstacles.append(foreign_entity)
        return obstacles


class Player:
    """
    :ivar id: The player's unique id
    """
    def __init__(self, player_id, ships={}):
        """
        :param player_id: User's id
        :param ships: Ships user controls (optional)
        """
        self.id = player_id
        self._ships = ships

    def all_ships(self):
        """
        :return: A list of all ships which belong to the user
        :rtype: list[entity.Ship]
        """
        return list(self._ships.values())

    def get_ship(self, ship_id):
        """
        :param int ship_id: The ship id of the desired ship.
        :return: The ship designated by ship_id belonging to this user.
        :rtype: entity.Ship
        """
        return self._ships.get(ship_id)

    @staticmethod
    def _parse_single(tokens):
        """
        Parse one user given an input string from the Halite engine.

        :param list[str] tokens: The input string as a list of str from the Halite engine.
        :return: The parsed player id, player object, and remaining tokens
        :rtype: (int, Player, list[str])
        """
        player_id, *remainder = tokens
        player_id = int(player_id)
        ships, remainder = entity.Ship._parse(player_id, remainder)
        player = Player(player_id, ships)
        return player_id, player, remainder

    @staticmethod
    def _parse(tokens):
        """
        Parse an entire user input string from the Halite engine for all users.

        :param list[str] tokens: The input string as a list of str from the Halite engine.
        :return: The parsed players in the form of player dict, and remaining tokens
        :rtype: (dict, list[str])
        """
        num_players, *remainder = tokens
        num_players = int(num_players)
        players = {}

        for _ in range(num_players):
            player, players[player], remainder = Player._parse_single(remainder)

        return players, remainder

    def __str__(self):
        return "Player {} with ships {}".format(self.id, self.all_ships())

    def __repr__(self):
        return self.__str__()

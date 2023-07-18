from __future__ import annotations
from dataclasses import dataclass
from typing import List
from mountain import Mountain
from data_structures.linked_stack import LinkedStack

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        return TrailSeries(mountain, Trail(self))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain,Trail(TrailSeries(mountain,self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain,Trail(TrailSplit(Trail(None),Trail(None),self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Adds a mountain before everything currently in the trail.
        Complexity best/worst: O(1)
        """

        return Trail(TrailSeries(mountain,self))

    def add_empty_branch_before(self) -> Trail:
        """
        Adds an empty branch before everything currently in the trail.
        Complexity best/worst: O(1)
        """
        return Trail(TrailSplit(Trail(None),Trail(None),self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        follow_path function follows a Trail according to a WalkerPersonality
        and adds mountains along the Trail to the WalkerPersonality's
        list of mountains
        Args:
            -personality: WalkerPersonality to follow when transversing the Trail
        Raises:
            -None: Function raises no errors
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(n * t * (personality.select() + personality.add_mountain))
                - in the worst case the function has to go around the for loop
                  the number of trails multiplied by the number of trails in each
                  trail store and call the personality.select() or
                  personality.add_mountain function each time it goes around
                  the loop which gives the functon a worst case complexity
                  of O(n * t * (personality.select() + personality.add_mountain))
                  where n is the number of trails and t is the number of trails
                  within the trails store.
            -Best case:O(O(n * t * personality.add_mountain))
                - in the best case all the trail stores are TrailSeries which mean
                  the for loop will only have to go around the number of trails
                  multiplied by the number of trails in each trail store times
                  and only call the personality.add_mountain() function giving
                  the function a best case complexity of
                  O(O(n * t * personality.add_mountain)) where n is the number of
                  trails and t is the number of trails within the trails store.
        """
        #get current store
        current_trail = self.store
        #create a linked stack
        trail_splits = LinkedStack()

        while True:
            #if type is TrailSeries add mountain
            if type(current_trail) == TrailSeries:
                personality.add_mountain(current_trail.mountain)
                current_trail = current_trail.following.store
            #if trail series is not None go though the following
            #paths in the TrailSplits that have been passed
            if current_trail is None:
                if len(trail_splits) > 0:
                    current_trail = trail_splits.pop()
                    if current_trail is not None:
                        current_trail = current_trail.path_follow.store
                else:
                    return
            #if type is TrailSplit get next trail
            if type(current_trail) == TrailSplit:
                if personality.select_branch(current_trail.path_top, current_trail.path_bottom):
                    trail_splits.push(current_trail)
                    current_trail = current_trail.path_top.store
                else:
                    trail_splits.push(current_trail)
                    current_trail = current_trail.path_bottom.store

    def collect_all_mountains(self) -> list[Mountain]:
        mountains = []
        current = self.store

        while current is not None:
            if isinstance(current, TrailSeries):
                mountains.append(current.mountain)
                current = current.following
            elif isinstance(current, TrailSplit):
                mountains.extend(current.path_top.collect_all_mountains())
                mountains.extend(current.path_bottom.collect_all_mountains())
                current = current.path_follow
            else:
                current = None

        return mountains

    def collect_all_starts(self) -> list[trail]:
        trails = []
        current = self.store

        while current is not None:
            if isinstance(current, TrailSeries):
                trails.append(current)
                current = current.following.store
            elif isinstance(current, TrailSplit):
                trails.extend(current.path_top.collect_all_starts())
                trails.extend(current.path_bottom.collect_all_starts())
                current = current.path_follow.store
            else:
                current = None

        return trails


    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """

        current_trail = self.store
        paths = self.findpath(current_trail)
        result = [sub_list for sub_list in paths if len(sub_list) == k]
        return paths




    def findpath(self, current_trail) -> []:
        path = []

        if isinstance(current_trail, TrailSeries):
            path.append(current_trail.mountain.name)
            if (current_trail.following.store is not None):
                path.extend(self.findpath(current_trail.following.store))
        elif isinstance(current_trail, TrailSplit):
            top_path = []
            bot_path = []
            if (current_trail.path_top.store is not None):
                top_path.extend(self.findpath(current_trail.path_top.store))
                if (current_trail.path_follow.store is not None):
                    if isinstance(top_path[0],list):
                        for i in top_path:
                            i.extend(self.findpath(current_trail.path_follow.store))
                    else:
                        top_path.extend(self.findpath(current_trail.path_follow.store))
                path.append(top_path)
            if (current_trail.path_bottom.store is not None):
                bot_path.extend(self.findpath(current_trail.path_bottom.store))
                if (current_trail.path_follow.store is not None):
                    bot_path.extend(self.findpath(current_trail.path_follow.store))
                path.append(bot_path)
        else:
            path.append(current_trail.store)

        return path


if __name__ == '__main__':

    top_top = Mountain("top-top", 5, 3)
    top_bot = Mountain("top-bot", 3, 5)
    top_mid = Mountain("top-mid", 4, 7)
    bot_one = Mountain("bot-one", 2, 5)
    bot_two = Mountain("bot-two", 0, 0)
    final = Mountain("final", 4, 4)
    trail = Trail(TrailSplit(
        Trail(TrailSplit(
            Trail(TrailSeries(top_top, Trail(None))),
            Trail(TrailSeries(top_bot, Trail(None))),
            Trail(TrailSeries(top_mid, Trail(None))),
        )),
        Trail(TrailSeries(bot_one, Trail(TrailSplit(
            Trail(TrailSeries(bot_two, Trail(None))),
            Trail(None),
            Trail(None),
        )))),
        Trail(TrailSeries(final, Trail(None)))
    ))
    #print(trail.collect_all_starts())
    print(trail.length_k_paths(3))



 

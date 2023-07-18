from mountain import Mountain

class MountainManager:
    def __init__(self):
        self.mountains = []

    def add_mountain(self, mountain: Mountain):
        """
        Complexity:
            - Worst case: O(N) where N is the number of mountains in the list.
                - In the worst case, the given mountain object is the last one in the list
                  or is not in the list at all. In either case, we need to iterate through
                  the entire list to determine this, which takes O(N) time.
            - Best case: O(1)
                - In the best case, the given mountain object is the first one in the list.
                  Therefore, we can remove it in constant time, or O(1).
        """
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain):
        """
    Complexity:
    - Worst case: O(n) where n is the number of mountains in the list.
        - In the worst case, the mountain to be removed is at the end of the list,
          or is not in the list at all. In this case, we have to iterate through
          all the mountains in the list to determine whether the mountain to be
          removed is in the list or not, and then remove it if it is.
    - Best case: O(1)
        - In the best case, the mountain to be removed is at the beginning of the list.
          Therefore, we can remove it directly without having to iterate through any other
          mountains in the list.
        """
        self.mountains.remove(mountain)

    def edit_mountain(self, old_mountain: Mountain, new_mountain: Mountain):
        """
        Complexity:
        - Worst case: O(N) where N is the number of mountains in the list.
            - In the worst case, the old mountain is located at the end of the list,
              which requires iterating through all previous mountains to reach it.
              Additionally, after replacing the mountain, we have to shift all the
              remaining elements to the left by one position, which takes O(N) time.
        - Best case: O(1)
            - In the best case, the old mountain is located at the beginning of the list,
              and we can replace it in constant time without any additional shifting.
        """
        index = self.mountains.index(old_mountain)
        self.mountains[index] = new_mountain

    def mountains_with_difficulty(self, diff: int):
        """
        Returns a list of all the mountains in the collection with the specified difficulty level.

        :param diff: The difficulty level to search for.
        :return: A list of Mountain objects with the specified difficulty level.

        Complexity:
        - Worst case: O(N) where N is the number of mountains in the collection.
            - In the worst case, we have to iterate through all the mountains in the collection
              to find the ones with the specified difficulty level.
        - Best case: O(1)
            - In the best case, the first mountain in the collection has the specified difficulty level,
              so we can immediately return a list containing only that mountain without iterating
              through any other mountains in the collection.
        """
        result = []
        for mountain in self.mountains:
            if mountain.difficulty_level == diff:
                result.append(mountain)
        return result

    def group_by_difficulty(self):
        """
        Groups mountains in the list by their difficulty level.

        Complexity:
        - Worst case: O(N^2) where N is the number of mountains in the list.
            - In the worst case, the mountains in the list are sorted in reverse order by
              difficulty level, and we have to iterate through all previously created groups
              to find the correct group to add each mountain to. This results in O(N^2) time complexity.
        - Best case: O(NlogN)
            - In the best case, the mountains in the list are already sorted by difficulty level.
              Then, we only need to iterate through the list once, and each mountain is added to
              the correct group immediately, resulting in a time complexity of O(NlogN).
         """
        sorted_mountains = sorted(self.mountains, key=lambda m: m.difficulty_level)
        result = []
        for mountain in sorted_mountains:
            for group in result:
                if group[0].difficulty_level == mountain.difficulty_level:
                    group.append(mountain)
                    break
            else:
                result.append([mountain])
        return result



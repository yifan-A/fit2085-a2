from __future__ import annotations

from mountain import Mountain
from algorithms.mergesort import *
from algorithms.binary_search import binary_search, _binary_search_aux


class MountainOrganiser:
    """
    Mountain Organiser. Stores, sorts and returns mountains in terms of there length.
    - __init__: Creates variables needed by the class
    - add_mountains: adds mountain to list of mountains and sorts them in order of
                     length
    - cur_position: returns given mountains length rank
    - search: searches for given mountain and returns position
    """

    def __init__(self) -> None:
        """
        __init__ function creates variables needed by the class
        Args:
            -None: Function takes no arguments
        Raises:
            -None: Function raises no errors
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(1)
                - all operations are constant so worst case complexity is O(1)
            -Best case: O(1)
                - worst case is constant which is the best possible case so best case is constant.
        """
        #list of mountains with tuple values of (length, difficulty_level, name)
        self.mountains: list[tuple[int,int,str]]|None = None
        #list of mountains lengths
        self.lengths: list[int]|None = None


    def cur_position(self, mountain: Mountain) -> int:
        """
        cur_position function takes in a mountain and returns the mountains
        current rank within the mountain organiser in terms of length.
        Args:
            -mountain: mountain whose rank is being searched for
        Raises:
            -KeyError: if mountain given is not in the mountain organiser the
                       keyError is rasied
        Returns:
            -res: rank of the mountain within the mountain organiser in terms
                  of length.
        Complexity:
            -Worst case: O(logN)
                - all operations are constant except for the search function so worst case
                  complexity is worst case complexity of search function which is O(logN)
                  where N is the length of the list of mountains in the mountain organiser.
            -Best case: O(logN)
                - all operations are constant except for the search function so best case
                  complexity is best case complexity of search function which is O(logN)
                  where N is the length of the list of mountains in the mountain organiser.
        """
        #get rank of mountain
        rank = self.search(self.lengths, mountain.length, 0, len(self.lengths), mountain)
        #if rank is None mountain is not with in mountain organiser, rasise keyError
        if rank is None: raise KeyError
        #return the moutains rank
        return rank




    def search(self, list:list[int], val:int, min:int, max:int, mountain:Mountain):
        """
        search function takes in a list of lengths, a min search value, a max search value
        and a mountain and searches for the mountains length in the list of lengths within
        the min and max values index of the list of lengths.
        Args:
            -list: A list of the lengths of the mountains within the mountain organiser
            -val: The length of the mountain being searched for.
            -min: min index value to search in the list.
            -max: max index value to search in the list.
            -mountain: the mountain being looked for.
        Raises:
            -None: Function raises no errors
        Returns:
            -pos: The function returns the position of the mountain in list of lengths.
        Complexity:
            -Worst case: O(logN)
                - The worst case for the _binary_search_aux function in this case is O(logN)
                  where N is the length of the list of lengths being passed into the search
                  function. The worst case complexity of the rest of the function is O(logN)
                  since the function calls itself of on the same list which has been split
                  in half. This gives the function a worst case complexity of O(logN) + O(logN)
                  which can be simplified to O(logN) where N is the length of the list of lengths
                  being passed in.
            -Best case: O(logN)
                - best case = worst case since function performs same operations each time.
                  O(logN) where N is the length of the list of lengths being passed in.
        """
        #search for position
        pos = _binary_search_aux(list, val, min, max)
        #return position if position is found
        if self.mountains[pos][2] == mountain.name and self.mountains[pos][1] == mountain.difficulty_level:
            return pos
        #search again if position is not found
        else:
            if min <= pos - 1 and max >= pos + 1:
                return self.search(list, val, min, pos - 1, mountain) or self.search(list, val, pos + 1, max, mountain)
            if min <= pos - 1 and list[pos - 1] == val:
                return self.search(list, val, min, pos - 1, mountain)
            if max >= pos + 1 and list[pos + 1] == val:
                return self.search(list, val, pos + 1, max, mountain)


    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        add_mountains function takes in a list of mountains and sorts them in terms of there
        length and adds them to the existing list of mountains.
        Args:
            -mountains: A list of mountains being added to the mountain organiser
        Raises:
            -None: Function raises no errors
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(Mlog(M) + N)
                - all operations are constant except for the copy function, the for loop, the
                  mergesort function and the merge function. The copy function has a worst case
                  complexity of O(M) for lists where M is the length of the list as per the
                  python documentation for lists in this case M is the length of the mountains list
                  being passed in, the for loop has a worst case complexity of O(M) where M is the
                  length of the mountains list being passed in, the mergesort function has a worst
                  case complexity of O(MlogM * comp(T)) which in this case is O(MlogM) where M is
                  the length of the mountains list being passed in since the comparison is a
                  comparison of integers which is has a constant time complexity and the merge function
                  has a worst case complexity of O(n comp(T)) which in this case is O(M + N) where M is
                  the length of the mountains list being passed in and N is the length of the existing
                  list of mountains and the complexity of the comparison is ignored since it is a
                  comparison between integers which has a worst case complexity of O(1). In the worst
                  case the function will complete the copy function, the for loop, the mergesort function
                  and the merge function which gives the function a worst case complexity of
                  O(M) + O(M) + O(MlogM) + O(M) + O(N) which can be simplified to O(MlogM + N) where M
                  is the length of the mountains list being passed in and N is the length of the list
                  of existing mountains.

            -Best case: O(MlogM)
                - The best case complexity for the copy function of a list is O(n) where n is the
                  length of the list as per the python documentation which is this case is O(M) where M is the
                  length of the mountains list being passed in, the best case complexity of the for loop is
                  O(M) where M is the length of the mountains list being passed in and the best case complexity
                  of the mergesort function is O(NlogN * comp(T)) which in this case is O(MlogM) where M is the
                  length of the list being passed in since the comparison is a comparison of integers which is
                  constant. In the best case the function completes the copy function, the for loop and the mergesort
                  function which gives the function a best case complexity of O(M) + O(M) + O(MlogM) which can be
                  simplified to O(MlogM) where M is the length of the list of mountains being passed in.
        """

        mountains = mountains
        lengths = mountains.copy()
        #create list of mountains with tuple values of (length, difficulty_level, name)
        #and create list of mountain lengths
        for mountain in range(len(mountains)):
            mountains[mountain] = (mountains[mountain].length, mountains[mountain].difficulty_level, mountains[mountain].name)
            lengths[mountain] = lengths[mountain].length

        #sort list of mountains in terms of lengths
        mountains = mergesort(mountains)
        #sort list of mountain lengths
        lengths = mergesort(lengths)

        #set mountains and lengths if there are none
        if self.mountains is None:
            self.mountains = mountains
            self.lengths = lengths
        #merge mountains and lengths with existing mountains and lengths
        else:
            self.mountains = merge(self.mountains, mountains)
            self.lengths = merge(self.lengths, lengths)

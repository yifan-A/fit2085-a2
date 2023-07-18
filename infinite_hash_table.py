from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR



K = TypeVar("K")
V = TypeVar("V")

class Nodes(Generic[K, V]):
    def __init__(self, key:str, value:int) -> None:
        self.key = key
        self.value = value
class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.
     

    Unless stated otherwise, all methods have O(1) complexity.
    """
    
    TABLE_SIZE = 27

    def __init__(self, level:int = 0) -> None:
        self.table = ArrayR(self.TABLE_SIZE)
        self.level = level

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        Complexity:
        - Worst case: O(N) where N is the number of elements in the hash table.
            - In the worst case, all elements of the hash table have the same hash value,
              and they all get stored in the same bucket. Therefore, when searching for
              an element with a specific key, we have to iterate through all of the elements
              in that bucket to find the element with the correct key.
        - Best case: O(1)
            - In the best case, the element we are searching for is at the beginning of the
              bucket that it hashes to. Therefore, we can access the element directly without
              having to iterate through any other elements in the bucket.
        """
        
        if self.table[self.hash(key)] == None:
            raise KeyError()
        else:
            element = self.table[self.hash(key)]
            if isinstance(element, InfiniteHashTable):
                return element.__getitem__(key)
            else:
                return element.value

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        element = Nodes(key,value)
        if self.table[self.hash(key)]==None:
            self.table[self.hash(key)] = element
        else:
            table = self.table[self.hash(key)]
            if isinstance(table, InfiniteHashTable):
                table.__setitem__(key, value)
            else:
                oldValue = table
                newtable = InfiniteHashTable(self.level + 1)
                newtable.__setitem__(oldValue.key, oldValue.value)
                newtable.__setitem__(key, value)
                self.table[self.hash(key)] = newtable


    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        Complexity:
        - Worst case: O(N) where N is the number of elements in the hash table.
            - In the worst case, all elements of the hash table have the same hash value,
              and they all get stored in the same bucket. Therefore, when deleting an element with
              a specific key, we have to iterate through all of the elements in that bucket to find
              the element with the correct key, which takes O(N) time.
        - Best case: O(1)
            - In the best case, the element we are deleting is at the beginning of the
              bucket that it hashes to. Therefore, we can access the element directly without
              having to iterate through any other elements in the bucket, which takes O(1) time.
        
        """
        
        if self.table[self.hash(key)] == None:
            raise KeyError()
        else:
            element = self.table[self.hash(key)]
            if isinstance(element, InfiniteHashTable):
                self.table[self.hash(key)].__delitem__(key)
                if len(self.table[self.hash(key)]) == 0:
                    self.table[self.hash(key)] = None
                elif len(self.table[self.hash(key)]) == 1:
                    object = self.table[self.hash(key)].lookforlastobject()
                    self.table[self.hash(key)] = object
            else:
                self.table[self.hash(key)] = None

    def lookforlastobject(self):
        object = None
        for item in self.table:
            if item != None:
                object = item
        return object
    

    def __len__(self):

        count = 0
        for i in range(self.TABLE_SIZE):
            if self.table[i] is not None:
                if isinstance(self.table[i], InfiniteHashTable):
                    count+=len(self.table[i])
                else:
                    count += 1
        return count


  

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        items = []
        for i in range(self.TABLE_SIZE):
            if self.table[i] is not None:
                if isinstance(self.table[i], InfiniteHashTable):
                    items.append(f"[{i}]: {str(self.table[i])}")
                else:
                    items.append(f"[{i}]: {self.table[i].value}")
        return "{" + ", ".join(items) + "}"

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
         Complexity:
        - Worst case: O(N) where N is the number of elements in the hash table.
            - In the worst case, all elements of the hash table have the same hash value,
              and they all get stored in the same bucket. Therefore, when searching for
              an element with a specific key, we have to iterate through all of the elements
              in that bucket, as well as any nested InfiniteHashTables, to find the element
              with the correct key.
        - Best case: O(1)
            - In the best case, the element we are searching for is at the top level of the
              hash table, and we can access it directly without having to traverse any
              nested InfiniteHashTables or iterate through any other elements in the same bucket.
        """
        positions = [self.hash(key)]
        table = self.table[self.hash(key)]
        while isinstance(table, InfiniteHashTable):
            positions.append(table.hash(key))
            table = table.table[table.hash(key)]
        if table == None:
            raise KeyError
        elif table.key != key:
            raise KeyError
        return positions

            

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True





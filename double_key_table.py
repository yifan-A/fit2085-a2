from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.

    -__init__: creates top array and variables need by the class
    -hash1: hash function
    -hash2: hash function
    -_linear_probe: finds position of key or position to insert key
    -iter_keys: returns iterator that goes through keys
    -keys: returns keys in table
    -iter_values: returns iterator that goes through values in table
    -values: returns values in table
    -__contains__: checks if table contains a value
    -__setitem__: sets two keys equal to a value
    -__delitem__: deletes item from table
    -rehash: increases size of top array of table and reinserts values
    -__len__: returns number of items in table
    -table_size: returns size of top array
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        """
        __init__ function determines the sizes of the top array and internal hash tables
        based on the input values and creates the top array from the table and creates
        other variables needed by the class.
        Args:
            -sizes: list of tables sizes or None if no list is given.
            -internal_sizes: list of tables sizes for internal table or None if no list is given.
        Raises:
            -None: Function raises no errors
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(top_table_sizes[0])
                - all operations are constant except from creating the top array which has a
                  complexity of O(n) where n is the length of the array, in this case the length
                  of the array is the first value in the top_table_sizes list so the complexity
                  is O(top_table_sizes[0])
            -Best case: O(top_table_sizes[0])
                - same operations occur everytime function is called so best case complexity is
                  equal to worst case complexity.
        """
        #set top_table_sizes and internal_table sizes based on input
        if (sizes is not None) and (internal_sizes is not None):
            self.top_table_sizes = sizes
            self.internal_table_sizes = internal_sizes
        elif (sizes is not None) and (internal_sizes is None):
            self.top_table_sizes = sizes
            self.internal_table_sizes = self.TABLE_SIZES
        elif (sizes is None) and (internal_sizes is not None):
            self.top_table_sizes = self.TABLE_SIZES
            self.internal_table_sizes = internal_sizes
        else:
            self.top_table_sizes = self.TABLE_SIZES
            self.internal_table_sizes = self.TABLE_SIZES
        #create and set variables needed by the class
        self.length = 0
        self.top_length = 0
        self.top_table_sizes_index = 0
        self.table_pos = 1
        self.key_pos = 0
        #create the top array
        self.top_array: ArrayR[K1, LinearProbeTable[K2, V]] = ArrayR(self.top_table_sizes[self.top_table_sizes_index])


    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        _linear_probe finds the position of a key in the table or the position to insert
        a key in the table using linear probing and returns the position.
        Args:
            -key1: top level key position to be found
            -key2: lower level key position to be found
            -is_insert: if the keys are being inserted
        Raises:
            -KeyError: When the key pair is not in the table, but is_insert is False.
            -FullError: When a table is full and a key cannot be inserted.
        Returns:
            -top_position: position for top level key
            -internal_position: position for low level key
        Complexity:
            -Worst case: O(has1(key1)) + O(len(self.top_array) * comp(K)) + O(LinearProbeTable._linear_probe(key2))
                - in the worst case the function has call the hash1 function then go around the for loop
                  len(self.top_array) times and then has to call the LinearProbeTable _linear_probe
                  function. This means that the worst case complexity is
                  O(has1(key1)) + O(len(self.top_array) * comp(P)) + O(LinearProbeTable._linear_probe(key2))
                  which is equal to
                  O(hash1(key1) + O(len(self.top_array) * comp(P)) + O(hash2(key2) + N*comp(K)) where N
                  is the length of the internal table.
            -Best case: O(hash1(key1) + O(comp(P)) + O(hash2(key2) + comp(K))
                - in the best case the for loop only has to go around once and the _linear_probe function
                  in LinearProbeTable has its best case complexity so the best case complexity is
                  O(hash1(key1) + O(comp(P)) + O(LinearProbeTable._linear_probe(key2))
                  or
                  O(hash1(key1) + O(comp(P)) + O(hash2(key2) + comp(K))
        """
        #get top position
        top_position = self.hash1(key1)

        for _ in range(len(self.top_array)):
            #if position is empty return position if is insert is true else raise KeyError
            if self.top_array[top_position] is None:
                if is_insert:
                    self.top_array[top_position] = (key1, LinearProbeTable(self.internal_table_sizes))
                    self.top_array[top_position][self.table_pos].hash = lambda k: self.hash2(k, self.top_array[top_position][self.table_pos])
                    internal_position = self.top_array[top_position][self.table_pos]._linear_probe(key2, is_insert)
                    return top_position, internal_position
                else:
                    raise KeyError()
            #if position already has key set key to new value
            elif self.top_array[top_position][self.key_pos] == key1:
                internal_position = self.top_array[top_position][self.table_pos]._linear_probe(key2, is_insert)
                return top_position, internal_position
            else:
                top_position = (top_position + 1) % self.table_size
        if is_insert:
            raise FullError()
        else:
            raise KeyError()





    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        __iter_keys__ function creates and returns a instance of the
        DoubleKeyKeyIterator class.
        Args:
            -key: if top level key is entered bottom level keys
                  associated with the key are returned else all
                  else in the table are returned
        Raises:
            -None: Function raises no errors
        Returns:
            -Iterator[K1|K2]: Function retuens a DoubleKeyKeyIterator
        Complexity:
            -Worst case: O(1)
                - function creates a instance of the DoubleKeyKeyIterator which
                  is constant since the __init__ function in the
                  DoubleKeyKeyIterator is constant.
            -Best case: O(1)
                - worst case is constant which is the best possible case so best case is constant.
        """
        class DoubleKeyKeyIterator(Generic[K1, K2, V]):
            """
            DoubleKeyKeyIterator is a class that returns a iterator that is able
            to iterate though the keys in a DoubleKeyTable.
            __init__: creates variables needed by the class
            __iter__: returns instance of the class
            __next__: returns next value in the iteration
            """
            def __init__(self, table: DoubleKeyTable, key: K1 | None):
                """
                 __init__ function creates variables needed by the class
                Args:
                    -DoubleKeyTable: DoubleKeyTable being iterated though
                    -key: if top level key is entered bottom level keys
                          associated with the key are returned else all
                          else in the table are returned
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
                self.table = table
                self.key = key
                self.index = 0
                self.position = None

            def __iter__(self):
                """
                __iter__ function returns a instance of the class.
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
                return self

            def __next__(self) -> [K1 | K2]:
                """
                __next__ function returns the next value in the iteration
                Args:
                    -None: Function takes no arguments
                Raises:
                    -StopIteration: StopIteration is raised when there are no more keys
                                    to be iterated though
                Returns:
                    -[K1|K2]: Function returns the next key in the iteration
                Complexity:
                    -Worst case: O(len(self.top_array) * comp(T)) + O(len(LinearProbeTable) * comp(K))
                        - In the worst case the function enters the elif and the function has to go tough all
                          the keys in the top array and perform a comparison and them has to go through all the
                          keys in the LinearProbeTable stored in the array and perform a comparison. This
                          makes the worst case complexity
                          O(len(self.top_array) * comp(T)) + O(len(LinearProbeTable) * comp(K))
                    -Best case: O(len(self.top_array) * comp(T))
                        - In the best case either if statement can be entered and if the table is empty the function
                          will iterate though the top array and perform a comparison and stop giving the function
                          a best case complexity O(len(self.top_array) * comp(T))
                        """
                if self.key is None:
                    #return the top level keys in the table
                    while True:
                        if self.index <= len(self.table.top_array) and self.table.top_array[self.index] is not None:
                            return self.table.top_array[self.index][0]
                        elif self.index < len(self.table.top_array):
                            self.index += 1
                        else:
                            raise StopIteration

                elif self.key is not None:
                    #get position of top key
                    if self.position is None:
                        for space in range(len(self.table.top_array)):
                            if self.table.top_array[space] == self.key:
                                self.position = space
                            elif space == len(self.table.top_array):
                                raise StopIteration
                    #return bottom level key corrosponding to top level key
                    while True:
                        if self.index <= len(self.table.top_array[self.position][1].array) and \
                                self.table.top_array[self.position][1].array[self.index] is not None:
                            print(self.table.top_array[self.position][1].array[self.index][0])
                            return self.table.top_array[self.position][1].array[self.index][0]
                        elif self.index < len(self.table.top_array[self.position][1].array):
                            self.index += 1
                        else:
                            raise StopIteration

        #create and return a instance of the DoubleKeyKeyIterator
        return DoubleKeyKeyIterator(self, key)


    def keys(self, key:K1|None=None) -> list[K1]:
        """
        keys function takes in a key are returns all the top level keys in the
        table in a list if no key is entered or returns all the bottom level
        keys from the top level key if a key is entered.
        Args:
            -Key: if key entered return all bottom level keys associated with the top
                  level key else return all the top level keys.
        Raises:
            -None: Function raises no errors.
        Returns:
            -keys: Function returns a list of keys from the table.
        Complexity:
            -Worst case:
                - in the worst case the function goes through the second for loop
                  and class the keys() function from LinearProbeTable once which
                  gives the function a worst case complexity of
                  O(len(self.top_array)) * O(LinearProbeTable.keys())

            -Best case: O(len(self.top_array)) + O(LinearProbeTable.keys())
                - in the best case the first for loop is entered and the function
                  adds a key to the list giving the function a complexity of
                  O(len(self.top_array)) or the first second for loop is
                  entered and the table is found on the first try so the complexity
                  of the function is O(LinearProbeTable.keys()) so over all the best
                  case complxity of the function is
                  O(len(self.top_array)) + O(LinearProbeTable.keys())
        """

        keys = []

        if key is None:
            #get top level keys
            for space in range(len(self.top_array)):
                if self.top_array[space] is not None:
                    keys.append(self.top_array[space][self.key_pos])
            return keys
            #get bottom level keys corosponding to key
        elif key is not None:
            for space in range(len(self.top_array)):
                if self.top_array[space] is not None and self.top_array[space][self.key_pos] == key:
                    keys = self.top_array[space][self.table_pos].keys()
                    return keys


    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        iter_values function creates and returns a instance of the
        DoubleKeyValueIterator class.
        Args:
            -key: if key is None the function returns all values in the table
                  else if a key is entered the function returns all to values
                  corresponding to the key
        Raises:
            -None: Function raises no errors
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(1)
                - creating and returning a instance of the DoubleKeyValuesIterator
                  is constant so the function is constant.
            -Best case: O(1)
                - worst case is constant which is the best possible case so best case is constant.
        """
        class DoubleKeyValuesIterator(Generic[K1, K2, V]):
            def __init__(self, table: DoubleKeyTable, key: K1 | None):
                """
                 __init__ function creates variables needed by the class
                Args:
                    -DoubleKeyTable: DoubleKeyTable being iterated though
                    -key: if top level key is entered values corresponding to
                          key are returned else all values in hash table are
                          returned.
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
                self.table = table
                self.key = key
                self.index = 0
                self.in_index = 0
                self.position = None

            def __iter__(self):
                """
                __iter__ function returns a instance of the class.
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
                return self

            def __next__(self) -> [K1 | K2]:
                """
                __next__ function returns the next value in the iteration
                Args:
                    -None: Function takes no arguments
                Raises:
                    -StopIteration: StopIteration is raised when there are no more values
                                    to be iterated though
                Returns:
                    -[K1|K2]: Function returns the next key in the iteration
                Complexity:
                    -Worst case: O(len(self.top_array) * comp(T)) + O(len(LinearProbeTable) * comp(K))
                        - In the worst case the function enters the elif and the function has to go tough all
                          the keys in the top array and perform a comparison and them has to go through all the
                          values in the LinearProbeTable stored in the array and perform a comparison. This
                          makes the worst case complexity
                          O(len(self.top_array) * comp(T)) + O(len(LinearProbeTable) * comp(K))
                    -Best case: O(len(self.top_array) * comp(T))
                        - In the best case either if statement can be entered and if the table is empty the function
                          will iterate though the top array and perform a comparison and stop giving the function
                          a best case complexity O(len(self.top_array) * comp(T))
                        """
                if self.key is None:
                    #get value in lower hash table
                    while True:
                        if self.index <= len(self.table.top_array) and self.table.top_array[self.index] is not None:
                            if self.in_index <= len(self.table.top_array[self.index][1].array) and \
                                    self.table.top_array[self.index][1].array[self.in_index] is not None:
                                return self.table.top_array[self.index][1].array[self.in_index][1]
                            else:
                                self.in_index += 1
                        elif self.index < len(self.table.top_array):
                            self.index += 1
                            self.in_index = 0
                        else:
                            raise StopIteration

                elif self.key is not None:
                    #get position of top key
                    if self.position is None:
                        for space in range(len(self.table.top_array)):
                            if self.table.top_array[space] == self.key:
                                self.position = space
                            elif space == len(self.table.top_array):
                                raise StopIteration
                    #return value corrosponding to top level key
                    while True:
                        if self.index <= len(self.table.top_array[self.position][1].array) and \
                                self.table.top_array[self.position][1].array[self.index] is not None:
                            return self.table.top_array[self.position][1].array[self.index][1]
                        elif self.index < len(self.table.top_array[self.position][1].array):
                            self.index += 1
                        else:
                            raise StopIteration

        #return instance of DoubleKeyValuesIterator
        return DoubleKeyValuesIterator(self, key)


    def values(self, key:K1|None=None) -> list[V]:
        """
        values function takes in a key are returns all the values in the table
        in a list if no key is entered or returns all the values from the top
        level key if a key is entered.
        Args:
            -key: if a key is entered all values for that top level key are
                  returned else if no key is entered all values in the table
                  are returned.
        Raises:
            -None: Function raises no errors
        Returns:
            -values: Function returns a list of values from the table
        Complexity:
            -Worst case: O(len(self.top_array)) * O(LinearProbeTable.__getitem__()) + O(LinearProbeTable.values())
                - In the worst case a key is entered which means the second for loop will
                  go around len(self.top_array) times and each time it will call the
                  __getitem__ function in LinearProbeTable and it will call the values
                  function from LinearProbeTable once when it has found the correct table.
                  This makes the worst case complexity of the function
                  O(len(self.top_array)) * O(LinearProbeTable.__getitem__()) + O(LinearProbeTable.values())
            -Best case: O(len(self.top_array)) * O(LinearProbeTable.values()) + O(LinearProbeTable.values())
                - In the best case no key is entered which means the first for loop will
                  go around len(self.top_array) times and each time it will call the values()
                  function on from LinearProbeTable on the table.
                  This makes the best case complexity of the function
                  O(len(self.top_array)) * O(LinearProbeTable.values()) or the second for
                  loop will go around once and find the table and call the values() function on
                  it from the LinearProbeTable and will make the complexity O(LinearProbeTable.values())
                  this gives the function a over all best case complxity of
                  O(len(self.top_array)) * O(LinearProbeTable.values()) + O(LinearProbeTable.values())
        """

        values = []

        if key is None:
            for space in range(len(self.top_array)):
                if self.top_array[space] is not None:
                    values += self.top_array[space][self.table_pos].values()
            return values
        elif key is not None:
            for space in range(len(self.top_array)):
                if self.top_array[space] is not None and self.top_array[space][self.key_pos] == key:
                    values = self.top_array[space][self.table_pos].values()
            return values

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        __getitem__ function gets and returns a value for a given set of keys
        Args:
            -key: a tuple of a upper level and lower level key
        Raises:
            -KeyError: if key is not in the table KeyError is rasied
        Returns:
            -value: value corresponding to given keys
        Complexity:
            -Worst case: O(self._linear_probe(key[0],key[1],False) + O(LinearProbeTable.__getitem__(key[1]))
                - in the worst case the function calls the self._linear_probe function and
                  the __getitem__ function in the LinearProbeTable so the worst case
                  complexity is
                  O(self._linear_probe(key[0],key[1],False) + O(LinearProbeTable.__getitem__(key[1]))
            -Best case: O(best case self._linear_probe(key[0],key[1],False) + O(best case LinearProbeTable.__getitem__(key[1]))
                - Best case complexity is best case complexity of self._linear_probe + best case complexity of
                  LinearProbeTable so best case complexity is
                  O(best case self._linear_probe(key[0],key[1],False) + O(best case LinearProbeTable.__getitem__(key[1]))
        """
        key1, key2 = key
        pos_key1, pos_key2 = self._linear_probe(key1, key2, False)
        return self.top_array[pos_key1][self.table_pos][key2]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        __setitem__ function takes in a pair of keys and a value and sets
        the keys equal to the value in the table.
        Args:
            -key: Function takes in a key pair
            -data Function takes in data to put into the table
        Raises:
            -TableFull: If table is full TableFull error is raised
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(self._linear_probe(key[0],key[1], True)) + O(LinearProbeTable.is_empty)
                         + O(LinearProbeTable.__contains__(key[1]) + O(LinearProbeTable.__setitem__(key[1]) = data)
                         + O(self._rehash)
                - in the worst case the function has to call self._linear_probe,
                  LinearProbeTable.is_empty, LinearProbeTable.__contains__,
                  LinearProbeTable.__setitem__ and self._rehash this makes the
                  worst case complexity
                  O(self._linear_probe(key[0],key[1], True)) + O(LinearProbeTable.is_empty)
                  + O(LinearProbeTable.__contains__(key[1]) + O(LinearProbeTable.__setitem__(key[1]) = data)
                  + O(self._rehash)
            -Best case: O(best case self._linear_probe(key[0],key[1], True)) + O(best case LinearProbeTable.is_empty)
                        + O(best case LinearProbeTable.__contains__(key[1])
                        + O( best caseLinearProbeTable.__setitem__(key[1]) = data)
                - in the best case the function has to call self._linear_probe,
                  LinearProbeTable.is_empty, LinearProbeTable.__contains__ and
                  LinearProbeTable.__setitem__ this makes the worst case complexity
                  O(best case self._linear_probe(key[0],key[1], True)) + O(best case LinearProbeTable.is_empty)
                  + O(best case LinearProbeTable.__contains__(key[1])
                  + O( best caseLinearProbeTable.__setitem__(key[1]) = data)
        """
        key1, key2 = key
        #get key positions
        pos_key1, pos_key2 = self._linear_probe(key1, key2, True)
        #check is top key already has a bottom key and value
        if self.top_array[pos_key1][self.table_pos].is_empty():
            self.length += 1
            self.top_length += 1
        elif not(key2 in self.top_array[pos_key1][self.table_pos]):
            self.length += 1
        #insert data into table
        self.top_array[pos_key1][self.table_pos][key2] = data
        #check if rehash is needed
        if self.top_length > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        __delitem__ function takes in two keys and deletes the corresponding data.
        Args:
            -key: Function takes a tuple of keys
        Raises:
            -KeyError: Function raises KeyError is given keys are not in the table.
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(LinearProbeTable.__delitem__(key[1])) + O(self._linear_probe(key[0],key[1],False))
                         + O(LinearProbeTable.is_empty()) + O(len(self.top_array) * self.__setitem__)
                - in the worst case the function has to call the LinearProbeTable.__delitem__(key[1])
                  function, the self._linear_probe(key[0],key[1],False) function, LinearProbeTable.is_empty
                  function and has to reinsert all other values in the table using the self.__setitem__ function.
                  This makes the worst case complexity of the function
                  O(LinearProbeTable.__delitem__(key[1])) + O(self._linear_probe(key[0],key[1],False))
                  + O(LinearProbeTable.is_empty()) + O(len(self.top_array) * self.__setitem__)
            -Best case: O(best case LinearProbeTable.__delitem__(key[1])) + O(best case self._linear_probe(key[0],key[1],False))
                        + O(best case LinearProbeTable.is_empty())
                - in the best case the function has to call the LinearProbeTable.__delitem__(key[1])
                  function, the self._linear_probe(key[0],key[1],False) function and the
                  LinearProbeTable.is_empty function .
                  This makes the worst case complexity of the function
                  O(best case LinearProbeTable.__delitem__(key[1])) + O(best case self._linear_probe(key[0],key[1],False))
                  + O(best case LinearProbeTable.is_empty())
        """

        key1, key2 = key
        #get positions
        top_position, in_position = self._linear_probe(key1, key2, False)
        #delete item
        del self.top_array[top_position][self.table_pos][key2]
        self.length -= 1
        #check if top key can be deleted
        if self.top_array[top_position][self.table_pos].is_empty():
            self.top_array[top_position] = None
            self.top_length -= 1
            top_position = (top_position + 1) % self.table_size
            #reinsert items up until empty spot
            while self.top_array[top_position] is not None:
                key1, internal_table = self.top_array[top_position]
                self.top_array[top_position] = None
                new_pos_key1, new_pos_key2 = self._linear_probe(key1, " ", True)
                self.top_array[new_pos_key1] = (key1, internal_table)
                top_position = (top_position + 1) % self.table_size


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        _rehash function increases the size of the top array and reinserts the
        LinearProbeTables into the array.
        Args:
            -None: Function takes no arguments
        Raises:
            -None: Function raises no errors
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(N * self.__setitem__ * self.values() * len(self.values()) + O(top_table_sizes[top_table_size_index + 1]
                - in the worst case the function has to call the self.__setitem__ function
                  on every value in the table and has to get all the values using the values
                  function and go through them and it has to create a new array. This gives
                  the function a worst case complexity of
                  O(N * self.__setitem__ * self.values() * len(self.values()) + O(top_table_sizes[top_table_size_index + 1]
                  where N is the length of the initial top array.
            -Best case: O(1)
                - in the best case there are no more table sizes in self.top_table_sizes
                  and the function will go into the first if statement and return None
                  making all the operations the function performs constant so the best
                  case complexity is O(1)
        """
        #increase size index
        self.top_table_sizes_index += 1
        #if array size can not be increased return None
        if self.top_table_sizes_index >= len(self.top_table_sizes):
            return None
        else:
            #create new top array
            current_array = self.top_array
            self.top_array = ArrayR(self.top_table_sizes[self.top_table_sizes_index])
            #reinsert all values into new array
            for space in range(len(current_array)):
                if current_array[space] is not None:
                    key1, table = current_array[space]
                    self.top_length -= 1
                    vals = table.values()
                    vals_index = 0
                    for key2 in table.keys():
                        self[(key1, key2)] = vals[vals_index]
                        vals_index += 1
                        self.length -= 1

    @property
    def table_size(self) -> int:
        """
        table_sizes returns the current size of the table (different from the length)
        Args:
            -None: Function takes no arguments
        Raises:
            -None: Function raises no errors
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(1)
                - all operations are constant to worst case complexity is O(1)
            -Best case: O(1)
                - worst case is constant which is the best possible case so best case is constant.
        """
        return len(self.top_array)

    def __len__(self) -> int:
        """
        __len__ returns number of elements in the hash table
        Args:
            -None: Function takes no arguments
        Raises:
            -None: Function raises no errors
        Returns:
            -None: Function does not return a value
        Complexity:
            -Worst case: O(1)
                - all operations are constant to worst case complexity is O(1)
            -Best case: O(1)
                - worst case is constant which is the best possible case so best case is constant.
        """
        return self.length

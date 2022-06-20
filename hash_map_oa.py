# Name: Riley Rabelos
# OSU Email: rabelosr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/3/2022
# Description: Performs various tasks on an open addressing hash map


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds a key and its value to a hashmap
        :param key: Is a string that represents a key
        :param value: An object representing the value being added to the hashmap
        :return: None
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        index = self._hash_function(key) % self._capacity
        start_index = index

        # if there is nothing at the index it adds the key and its value
        if self._buckets[index] is None:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1

        # if the key matches or if there is a tombstone at its location it updates the value or overwrites it
        elif self._buckets[index].is_tombstone:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        elif self._buckets[index].key == key:
            self._buckets[index].value = value

        # Does quadratic probing to find an index for the entry
        else:
            for val in range(1, self._capacity):
                index = (start_index + val**2) % self._capacity
                if self._buckets[index] is None:
                    self._buckets[index] = HashEntry(key, value)
                    self._size += 1
                    return
                elif self._buckets[index].is_tombstone:
                    self._buckets[index] = HashEntry(key, value)
                    self._size += 1
                    return
                elif self._buckets[index].key == key:
                    self._buckets[index].value = value
                    return

    def table_load(self) -> float:
        """
        Calculates the load factor of the table
        :return: A float representing the load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Checks to see how many buckets are empty
        :return: An integer representing the number of buckets that are empty
        """
        tracker = 0
        for val in range(self._capacity):
            if self._buckets[val] is None:
                tracker += 1
            elif self._buckets[val].is_tombstone:
                tracker += 1
        return tracker

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table based on the new_capacity, it also maintains all of its data
        :param new_capacity: An integer representing the new capacity of the table
        :return: None
        """
        if new_capacity < 1 or new_capacity < self._size:
            return

        new_arr = DynamicArray()
        for val in range(new_capacity):
            new_arr.append(None)

        # Saves and updates values
        save_arr = self._buckets
        old_capacity = self._capacity
        self._buckets = new_arr
        self._capacity = new_capacity
        self._size = 0

        # adds all the data back to the new array
        for val in range(old_capacity):
            if save_arr[val] is not None and save_arr[val].is_tombstone is not True:
                key = save_arr[val].key
                value = save_arr[val].value
                self.put(key, value)

    def get(self, key: str) -> object:
        """
        Gets a value associated with a key if the key exists
        :param key: A string representing the key
        :return: An Object representing the value associated with the key
        """
        index = self._hash_function(key) % self._capacity
        start_index = index

        # Checks to see if the key doesn't exist or if it is a tombstone
        if self._buckets[index] is None:
            return
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone:
            return

        # if they key exists it returns the value associated with that key
        elif self._buckets[index].key == key:
            return self._buckets[index].value

        # Does quadratic probing to see if the key exists
        else:
            for val in range(1, self._capacity):
                index = (start_index + val**2) % self._capacity
                if self._buckets[index] is None:
                    return
                elif self._buckets[index].key == key and self._buckets[index].is_tombstone:
                    return
                elif self._buckets[index].key == key:
                    return self._buckets[index].value
            return

    def contains_key(self, key: str) -> bool:
        """
        Checks to see if the key exists
        :param key: A string representing the key
        :return: A bool that says true if it contains the key and false if it does not
        """
        if self.get(key) is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """
        Removes the key and its associated value
        :param key: A string representing the key
        :return: None
        """
        index = self._hash_function(key) % self._capacity
        start_index = index

        # Checks to see if the key doesn't exist or if it is a tombstone
        if self._buckets[index] is None:
            return
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone:
            return

        # if they key exists it removes the key and makes the size one smaller
        elif self._buckets[index].key == key:
            self._buckets[index].is_tombstone = True
            self._size -= 1

        # Does quadratic probing to see if the key exists
        else:
            for val in range(1, self._capacity):
                index = (start_index + val ** 2) % self._capacity
                if self._buckets[index] is None:
                    return
                elif self._buckets[index].key == key and self._buckets[index].is_tombstone:
                    return
                elif self._buckets[index].key == key:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
            return

    def clear(self) -> None:
        """
        Empties all the buckets in the hashmap
        :return: None
        """
        self._buckets = DynamicArray()
        for val in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Creates an array that has all the keys in the table
        :return: A dynamic array containing the keys
        """
        new_arr = DynamicArray()
        for val in range(self._capacity):
            if self._buckets[val] and self._buckets[val].is_tombstone is not True:
                new_arr.append(self._buckets[val].key)
        return new_arr


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

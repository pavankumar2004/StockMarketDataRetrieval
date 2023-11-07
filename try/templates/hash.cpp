#include <iostream>
#include <unordered_map>
using namespace std;
#define SIZE 10 // Define the size of the hash table
struct DataItem {
    int key;
};
unordered_map<int, DataItem*> hashMap; // Define the hash table as an unordered_map

int hashCode(int key) {
    // Return a hash value based on the key
    return key % SIZE;
}

DataItem* search(int key) {
    // get the hash
    int hashIndex = hashCode(key);

    // move in the map until an empty slot is found or the key is found
    while (hashMap[hashIndex] != nullptr) {
        // If the key is found, return the corresponding DataItem pointer
        if (hashMap[hashIndex]->key == key)
            return hashMap[hashIndex];

        // go to the next cell
        ++hashIndex;

        // wrap around the table
        hashIndex %= SIZE;
    }

    // If the key is not found, return nullptr
    return nullptr;
}

int main() {

    // Initializing the hash table with some sample DataItems
    DataItem item2 = {25}; // Assuming the key is 25
    DataItem item3 = {64}; // Assuming the key is 64
    DataItem item4 = {22}; // Assuming the key is 22

    // Calculate the hash index for each item and place them in the hash table
    
    int hashIndex2 = hashCode(item2.key);
    hashMap[hashIndex2] = &item2;
    
    int hashIndex3 = hashCode(item3.key);
    hashMap[hashIndex3] = &item3;

    int hashIndex4 = hashCode(item4.key);
    hashMap[hashIndex4] = &item4;

    // Call the search function to test it
    int keyToSearch = 64; // The key to search for in the hash table
    DataItem* result = search(keyToSearch);

    if (result != nullptr) {
        cout << "Key " << keyToSearch << " found, Value: " << result->key << endl;
    } else {
        cout << "Key " << keyToSearch << " not found." << endl;
    }

    return 0;
}
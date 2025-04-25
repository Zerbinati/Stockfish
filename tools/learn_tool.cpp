#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <string>
#include <sstream>
#include <iomanip>
#include <algorithm>

// Fallback per std::clamp if not available in older versions of MinGW
template<typename T>
T clamp(T v, T lo, T hi) {
    return (v < lo) ? lo : (v > hi) ? hi : v;
}

struct BookEntry {
    uint64_t key;
    uint16_t move;
    uint16_t weight;
    uint32_t learn;
};

uint64_t hex_to_uint64(const std::string& hex) {
    uint64_t result = 0;
    std::stringstream ss;
    ss << std::hex << hex;
    ss >> result;
    return result;
}

uint16_t hex_to_uint16(const std::string& hex) {
    uint16_t result = 0;
    std::stringstream ss;
    ss << std::hex << hex;
    ss >> result;
    return result;
}

void update_learn(const std::string& filename,
                  uint64_t targetKey,
                  uint16_t targetMove,
                  int32_t delta,
                  bool debug = false) {
    std::ifstream in(filename, std::ios::binary);
    if (!in) {
        std::cerr << "Cannot open book file: " << filename << "\n";
        return;
    }

    std::vector<BookEntry> entries;
    BookEntry entry;

    while (in.read(reinterpret_cast<char*>(&entry), sizeof(BookEntry)))
        entries.push_back(entry);
    in.close();

    bool found = false;

    for (auto& e : entries) {
        if (debug && (e.key == targetKey || e.move == targetMove)) {
            std::cout << "Entry match:\n";
            std::cout << "  Key:    0x" << std::hex << e.key << std::dec << "\n";
            std::cout << "  Move:   0x" << std::hex << e.move << std::dec << "\n";
            std::cout << "  Weight: " << e.weight << "\n";
            std::cout << "  Learn:  " << e.learn << "\n";
        }

        if (e.key == targetKey && e.move == targetMove) {
            int64_t current = static_cast<int64_t>(e.learn);
            int64_t updated = clamp(current + delta, int64_t(0), int64_t(0xFFFFFFFF));
            e.learn = static_cast<uint32_t>(updated);

            std::cout << "Updated learn: from " << current << " to " << updated << "\n";
            found = true;
            break;
        }
    }

    if (!found) {
        std::cerr << "Entry not found for given key/move.\n";
        return;
    }

    std::ofstream out(filename, std::ios::binary | std::ios::trunc);
    for (const auto& e : entries)
        out.write(reinterpret_cast<const char*>(&e), sizeof(BookEntry));

    std::cout << "Book updated successfully.\n";
}

int main(int argc, char* argv[]) {
    if (argc < 5 || argc > 6) {
        std::cerr << "Usage: " << argv[0] << " book.bin <hex_key> <hex_move> <delta> [--debug]\n";
        return 1;
    }

    std::string filename = argv[1];
    uint64_t key = hex_to_uint64(argv[2]);
    uint16_t move = hex_to_uint16(argv[3]);
    int32_t delta = std::stoi(argv[4]);
    bool debug = (argc == 6 && std::string(argv[5]) == "--debug");

    update_learn(filename, key, move, delta, debug);

    return 0;
}

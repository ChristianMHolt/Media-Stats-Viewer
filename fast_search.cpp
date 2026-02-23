#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>
#include <algorithm>
#include <sstream>

namespace py = pybind11;

class SearchEngine {
public:
    void add_items(const std::vector<std::string>& items) {
        corpus.clear();
        corpus.reserve(items.size());
        for (const auto& item : items) {
            std::string lower_item = item;
            std::transform(lower_item.begin(), lower_item.end(), lower_item.begin(), ::tolower);
            corpus.push_back(lower_item);
        }
    }

    std::vector<int> search(std::string query) {
        std::vector<int> result_indices;
        if (query.empty()) return result_indices;

        std::transform(query.begin(), query.end(), query.begin(), ::tolower);

        // Split query into terms
        std::istringstream iss(query);
        std::vector<std::string> terms;
        std::string term;
        while (iss >> term) {
            terms.push_back(term);
        }

        if (terms.empty()) return result_indices;

        for (size_t i = 0; i < corpus.size(); ++i) {
            bool match = true;
            for (const auto& t : terms) {
                if (corpus[i].find(t) == std::string::npos) {
                    match = false;
                    break;
                }
            }
            if (match) {
                result_indices.push_back(static_cast<int>(i));
            }
        }
        return result_indices;
    }

private:
    std::vector<std::string> corpus;
};

PYBIND11_MODULE(fast_search, m) {
    py::class_<SearchEngine>(m, "SearchEngine")
        .def(py::init<>())
        .def("add_items", &SearchEngine::add_items)
        .def("search", &SearchEngine::search);
}

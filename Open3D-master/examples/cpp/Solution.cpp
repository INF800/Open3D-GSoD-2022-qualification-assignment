#include <iostream>
#include <fstream>
#include "open3d/Open3D.h"

int main(int argc, char *argv[]) {
    using namespace open3d;

    std::string MESH_PATH = "../test_mesh.ply";
    std::string OUTPUT_FILE = "./examples/result.txt";

    geometry::TriangleMesh mesh;
    io::ReadTriangleMeshOptions options;
    bool success = io::ReadTriangleMeshFromPLY(MESH_PATH, mesh, options);
    if (!success){
        std::cout<<"[!!!] please make sure test_mesh.ply exists at the given `MESH_PATH`.";
    }

    if (!mesh.HasAdjacencyList()){
        mesh.ComputeAdjacencyList();
    }    
    std::vector<std::vector<long unsigned int>> all_ccs = mesh.IdenticallyColoredConnectedComponents();

    std::string output; 
    for (long unsigned int i=0; i<all_ccs.size(); i++){
        std::vector<long unsigned int> ccs = all_ccs[i];
        for (long unsigned int j=0; j<ccs.size(); j++){
            output += (std::to_string(ccs[j]) + "\t");
        }
        output+="\n";
    }
    std::ofstream f(OUTPUT_FILE);
    f<<output;
    f.close();

    return 0;
}
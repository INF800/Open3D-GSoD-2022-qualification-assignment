# Open3D-GSoD-2022-qualification-assignment

**Deadline:** May 06, 23:59 UTC / May 07, 05:29 AM IST

![](./assets/test_mesh.gif)

### Tasks

You’re expected to:

- [x] 1. Compile Open3D from source: http://www.open3d.org/docs/latest/compilation.html.

  <details closed>
  <summary>Compilation steps</summary>
    <br>

    <h3>1. System specs</h3>

    <b>Note:</b> This is a CPU only machine from github codespaces.

    <pre>
    OS: Ubuntu 20.04.4 LTS (Focal Fossa)                # `cat /etc/os-release`
    gcc: gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0      # `gcc --version`
    clang: clang version 10.0.0-4ubuntu1                # `clang --version`
    cmake: cmake version 3.23.1                         # `cmake --verson` after following steps from `https://apt.kitware.com/` 
    CUDA: n/a
    ccache: ccache version 3.7.7                        # `ccache --version` after `sudo apt install ccache` (CPU Only)
    Python: 3.8.12                                      # `python --version`
    </pre>


    <h3>2. Setup</h3>
    
    A. Clone `git clone https://github.com/isl-org/Open3D`</br>
    B. Install dependencies `cd Open3D && util/install_deps_ubuntu.sh`</br>
    C. Config `mkdir build && cd build && sudo cmake ..`</br>
    D. Build `make -j$(nproc)` <b>(takes veryyy long time)</b></br>
    E. Install Open3d C++ lib `sudo make install`</br>
    F. Install Open3d Python lib `make install-pip-package`</br>
    E. Verify `python -c "import open3d; print(dir(open3d));"`</br>

    </br>
    </br>

  </details>

  <details closed>
  <summary>Bind a dummy printing function to understand pybind</summary>
    <br>    

    <i>You may follow similar steps to add your own custom method</i>

    - Add `DummyMethod` *signature* in `./Open3D/cpp/open3d/geometry/TriangleMesh.h` file<br>
      ```c++
      // just like signature of `IsEdgeManifold` 
      // ---------------------------------------
      ...
      /// Function for testing how to use pybind
      bool DummyMethod(bool arg1 = true) const;
      ...
      ```
    - Add `DummyMethod` *definition* in `./Open3D/cpp/open3d/geometry/TriangleMesh.cpp`<br>
      ```c++
      // outside the TriangleMesh class just like `IsEdgeManifold`'s definition
      // ----------------------------------------------------------------------
      bool TriangleMesh::DummyMethod(
              bool arg1 /* = true */) const {
          // dummy function
          return true;
      }
      ```
    - Add `dummy_method` *binding* in `./Open3D/cpp/pybind/geometry/trianglemesh.cpp`<br> 
      ```c++
      // just like binding `is_edge_manifold`
      // -----------------------------------
      ...
      .def("dummy_method", &TriangleMesh::DummyMethod,
           "Dummy method to test pybinding.")
      ...

      ```
    - Run `cd build && sudo cmake .. && make -j$(nproc) && sudo make install && make install-pip-package` (there should be no c++ errors)<br>
    - Test in python interpreter<br>
      ```
      >>> import open3d as o3d
      >>> o3d.geometry.TriangleMesh().dummy_method(-1)
      True
      ```

  </details>

  <details closed>

  <summary>Add Open3D</summary>
    <br>    

    **Note:** We are simply uploading the Open3D project folder and removing all tracking information by deleting the `.git` folder. A better way to add it is using submodules. But **not using submodules here because it is definitely an overkill!**

    > ### Add as submodule
    > 
    > Add Open3D project as a trackable project inside current project using
    > ```shell
    > git submodule add https://github.com/isl-org/Open3D
    > ```
    > 
    > ALternatively, you may also add Open3d in the main dir by simply cloning it but changes will not be tracked if done so.

  </details>



- [x] 2. Write C++ function `open3d::geometry::TriangleMesh::IdenticallyColoredConnectedComponents` and Python binding `open3d.geometry.TriangleMesh.identically_colored_connected_components`.
  <details closed>
  <summary>My C++ is rusty so write and test/visualize in python first.</summary>
    <br>  
    There are three methods using which we can solve the problem:<br>
    
      1. Transform the graph into a new graph where only **edges with same colored vertices are connected** and then apply DFS<br/>
      2. Using laplacian matrix, eigen values and vectors<br/>
      3. (optimzed) Apply DFS without graph transformation.

    All Three of them are implemented in [core_logic.py](./core_logic.py) file along with visualisations using graph objects.<br>
    Solution `3.` is same as `1` but we make a minor change in DFS to make original graph appear as if it is the skipped new graph<br>

    ```python
    def dfs_custom(visited, graph, node, accumulator, vertex_colors):
        if node not in visited:
            accumulator.append(node)
            visited.add(node)
            for neighbour in graph[node]:
                if vertex_colors[node]!=vertex_colors[neighbour]:
                    continue
                dfs_custom(visited, graph, neighbour, accumulator, vertex_colors)
                
    def identically_colored_connected_compontents_dfs_optimized(adjacency_list, vertex_colors, debug=False):
        # convert to unique string ids (this step is not really required)
        for i in range(len(vertex_colors)):
            vertex_colors[i] = f'rgba({int(vertex_colors[i][0]*255)}, {int(vertex_colors[i][1]*255)}, {int(vertex_colors[i][2]*255)}, 255)'
        # note: no new graph
        # find connected components using DFS
        connected_components = []
        visited = set()
        for v in range(len(adjacency_list)):
            if v in visited:
                continue
            accumulator = []
            dfs_custom(visited, adjacency_list, v, accumulator, vertex_colors)
            connected_components.append(accumulator)
        return connected_components
    ```
    
    > - We won't follow laplacian method becuase it tricky due to precision issues. Moreover it has O(n^3) time complexity.
    > - Results of DFS algotithm are correct for both the meshes - `test_mesh.ply` and graph given in `assignment.pdf` 
  </details>
  <details closed>
  <summary>Replicate algorithm in `Open3D-master`</summary>
    <br>  
    
    First, check how to access `vertices`, `vertex_colors` and `adjacency_list` within `./Open3D/cpp/open3d/geometry/TriangleMesh.cpp` and re-write python logic in C++.
    
    1. Add `IdenticallyColoredConnectedComponents` method signature in `./Open3D/cpp/open3d/geometry/TriangleMesh.h` <br>
    2. Add `IdenticallyColoredConnectedComponents` method definition in `./Open3D/cpp/open3d/geometry/TriangleMesh.cpp` <br>
    3. Add `identically_colored_connected_components` python binding in `./Open3D/cpp/pybind/geometry/trianglemesh.cpp` <br>
    4. Run `cd build && sudo cmake .. && make -j$(nproc) && sudo make install && make install-pip-package` <br>
    5. Test new method in C++ and Python 
    ```
    // python output
    [[0, 10, 20, 30, 40, 41, 1, 34, 24, 15, 5, 14, 23, 13, 21, 29, 19, 9, 8], [2, 12, 3, 4, 11], [6, 7], [16, 25, 17, 27, 18], [22, 32, 33, 31], [26, 36, 37, 28, 38, 39, 35], [42, 53, 63, 44, 52, 50, 49, 48, 47, 46, 55], [43, 83, 64, 74, 65, 73, 82, 72, 81, 71, 80, 62, 54, 77, 67, 76, 58, 59], [45], [51], [56, 66, 57], [60, 70, 61, 69, 68], [75], [78, 79]]
    
    // cpp output
    [[0, 8, 9, 10, 19, 20, 21, 30, 40, 1, 41, 34, 24, 23, 13, 14, 5, 15, 29], [2, 11, 3, 4, 12], [6, 7], [16, 17, 18, 27, 25], [22, 32, 33, 31], [26, 35, 36, 37, 38, 28, 39], [42, 44, 53, 52, 63, 46, 55, 47, 48, 49, 50], [43, 74, 64, 65, 73, 72, 71, 81, 80, 82, 83, 62, 54, 76, 67, 58, 59, 77], [45], [51], [56, 57, 66], [60, 61, 70, 69, 68], [75], [78, 79]]
    ```
    > May need ordering / sorting algorithm

    > ### Common issues
    > while running cpp file using `gcc examples/cpp/IdenticallyColoredConnectedComponents.cpp -lstdc++` error is raised -
    > ```
    > /usr/local/include/open3d/camera/PinholeCameraIntrinsic.h:29:10: fatal error: Eigen/Core: No such file or directory
    > ```
    > Solution is to run in shell:
    > ```
    > sudo apt-get install libeigen3-dev
    > sudo ln -s /usr/include/eigen3/Eigen /usr/include/Eigen
    > ```
    > 
    > similarly the ```sudo apt install libfmt-dev libglfw3-dev ```
  </details>
- [x] 3. Write `examples/python/solution.py` to read the input mesh `test_mesh.ply`, find identically-colored connected components and print results.

  <details closed>
  <summary>How to run the example with python enviroment</summary>
    <br>
    
    Activate enviroment and run from main directory of Open3D:<br>
    ```shell
    $ source venv/bin/activate
    $ cd Open3D-master
    $ python3 examples/python/solution.py 
    ```
    Results will be generated in `examples/result.txt` like the one below for `test_mesh.ply`
    ```txt
    0	10	20	30	40	41	1	34	24	15	5	14	23	13	21	29	19	9	8	
    2	12	3	4	11	
    6	7	
    16	25	17	27	18	
    22	32	33	31	
    26	36	37	28	38	39	35	
    42	53	63	44	52	50	49	48	47	46	55	
    43	83	64	74	65	73	82	72	81	71	80	62	54	77	67	76	58	59	
    45	
    51	
    56	66	57	
    60	70	61	69	68	
    75	
    78	79	
    ```
  </details>
- [x] 4. Write Python unit test integrated with Open3D’s unit test system.
  <details closed>
  <summary>Steps</summary>
    <br>

    - Make sure pytest is present in environment <br>
    
    - Add pytest compatible test in `Open3D-master/python/test/test_solution.py`. <br>
    
    - Run test using `python3 -m pytest python/test/test_solution.py` from `Open3D-master/` directory. 
    
    <br> 
  <details>

- [ ] 5. Write `examples/cpp/Solution.cpp` to read the input mesh `test_mesh.ply`, find identically-colored connected components. **Change the build system** so that an executable can be build.
  <details closed>
  <summary>How to run the example with cmake.</summary>
    <br>
  <details>
  
  > Output the result of task 3 or 4 (their results shall be the same) to `examples/result.txt`.<br>

- [ ] 6. Write C+ unit test integrated with Open3D’s unit test system.
- [ ] 7. Document your code, the algorithm used, how to build and run, and etc.

### Reference
Here are some links for your reference:

• Open3D repository: https://github.com/isl-org/Open3D. <br/>
• Open3D docs: http://www.open3d.org/docs. <br/>
• Pybind11: https://github.com/pybind/pybind11. <br/>
• Send an email to us. <br/>

### Submission

To submit your code:

1. Push the code to a private git repository, share the repository with us and ping us via email.<br/>
2. Include all the necessary files. The git history should indicate the files you changed.<br/>

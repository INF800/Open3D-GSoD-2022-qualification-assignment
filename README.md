# Open3D-GSoD-2022-qualification-assignment

**Deadline:** May 06, 23:59 UTC / May 07, 05:29 AM IST

### Tasks

You’re expected to:

- [x] 1. Compile Open3D from source: http://www.open3d.org/docs/latest/compilation.html.

  <details open>
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

  <details open>
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

- [ ] 2. Write C++ function `open3d::geometry::TriangleMesh::IdenticallyColoredConnectedComponents`
- [ ] 3. Write Python binding `open3d.geometry.TriangleMesh.identically_colored_connected_components`.
- [ ] 4. Write `examples/cpp/Solution.cpp` to read the input mesh `test_mesh.ply`, find identically-colored connected components. **Change the build system** so that an executable can be build.
- [ ] 5. Write `examples/python/solution.py` to read the input mesh `test_mesh.ply`, find identically-colored connected components and print results.
- [ ] 6. Output the result of task 3 or 4 (their results shall be the same) to `examples/result.txt`.
- [ ] 7. Write C++ and Python unit tests integrated with Open3D’s unit test system.
- [ ] 8. Document your code, the algorithm used, how to build and run, and etc.

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

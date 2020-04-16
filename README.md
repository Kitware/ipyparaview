ipyparaview
===============================

A widget for interactive server-side ParaView rendering.


Examples
--------
Example notebooks are avaible in the `notebooks` folder. They are designed to give a broad overview of how to use ipyparaview. New users will probably have the best luck jumping in to the Hello_Jupyter-ParaView.ipynb notebook, which demonstrates basic usage and setting up the ParaView display. The Iso-Surfaces_with_RTX.ipynb notebook demonstrates more advanced usage, with more extensive manipulation of the render state and interactive control. The Dask-MPI_Volume_Render.ipynb notebook demonstrates how to use multi-node rendering by running PVRenderActors on a Dask-MPI cluster.


Installation
------------
There are two ways to install ipyparaview, both of which rely on pip. The lightweight method is to point pip at the GitHub repo, and then enable the notebook extension (note: this will not enable the extension for Jupyter lab). The more fully-featured method is to download a copy of the source code and install from the local version. We typically run inside of a conda environment (see conda setup step in instructions for the full-feature install with conda)

## Lightweight quick install

    $ pip install git+https://github.com/NVIDIA/ipyparaview.git
    $ jupyter nbextension enable --py --sys-prefix ipyparaview

## Fully-featured local source installation

    $ git clone https://github.com/NVIDIA/ipyparaview.git
    $ cd ipyparaview
    $ ./build.sh

## Fully-featured local source installation (with conda)

    $ git clone https://github.com/NVIDIA/ipyparaview.git
    $ cd ipyparaview
    $ conda env create -f environment.yml && conda activate ipy_dev
    $ ./build.sh
    

Running
-------
Within a conda environment

    $ conda activate ipy_dev
    $ export LD_LIBRARY_PATH=$PVPATH/lib/
    $ export PYTHONPATH=$PVPATH/lib/python3.7/site-packages/
    $ jupyter notebook
    


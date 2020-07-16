# Build from the base image so that we can develop and test rapidly
# This will have ParaView and conda all set up properly
# See https://github.com/banesullivan/dockerfiles/tree/master/paraview
#     https://hub.docker.com/repository/docker/banesullivan/paraview
FROM banesullivan/paraview

WORKDIR /root
COPY . ./ipyparaview/
WORKDIR /root/ipyparaview

# Install ipyparaview
RUN pip install -e .
RUN jupyter nbextension install --py --symlink --sys-prefix ipyparaview
RUN jupyter nbextension enable --py --sys-prefix ipyparaview
# RUN jupyter labextension install js

# Set up for use
WORKDIR /root/ipyparaview/notebooks

# Make sure to borrow entry point from parent image
ENTRYPOINT ["tini", "-g", "--", "start_xvfb.sh"]
# CMD ["/bin/bash"]
CMD ["jupyter", "notebook", "--port=8877", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

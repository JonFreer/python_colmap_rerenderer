# Python Colmap Rerenderer

Reads in dense point cloud ply file and renders it out at set camera views.

## Setup
### loadTXT.py
- imgPath: path to the folder of reference images
- cameraTXTPath: path to the cameras.txt file from COLMAP
- imageTXTPath: path to the images.txt file from COLMAP

### main.py
- plyData: set the path to the fused ply data file from COLMAP
- density: 1/density points will be rendered. Higher density less points rendered.

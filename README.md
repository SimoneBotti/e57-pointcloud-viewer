# E57 Point Cloud Viewer

A Python tool for reading, processing and visualising terrestrial laser scanner data in **E57** format — the industry standard output of laser scanners such as Trimble, Leica and FARO instruments.

Developed as part of a laser survey workflow on motorsport circuit infrastructure projects, where E57 scans were acquired on-site and processed to support construction supervision and quality documentation.

---

## Features

- Reads E57 point cloud files via `pye57`
- Extracts XYZ coordinates and intensity data
- Applies **voxel downsampling** for performance (configurable voxel size)
- Renders point cloud coloured by intensity using **Open3D**
- Optionally exports to **LAS** format for use in third-party GIS/surveying software
- Command-line interface for flexible usage

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
# Basic usage
python main.py --input path/to/scan.e57

# Custom voxel size (default: 0.05 m)
python main.py --input path/to/scan.e57 --voxel 0.02

# Export to LAS as well
python main.py --input path/to/scan.e57 --export

# Load a specific scan from a multi-scan E57 file
python main.py --input path/to/scan.e57 --scan-index 1
```

---

## Project Structure

```
├── main.py                 # E57 viewer and LAS exporter
├── requirements.txt
├── output/                 # LAS export destination
└── examples/
    └── ply_viewer.py       # Simple PLY point cloud viewer
```

---

## Dependencies

| Library   | Purpose                              |
|-----------|--------------------------------------|
| open3d    | 3D point cloud visualisation         |
| pye57     | E57 file format I/O                  |
| laspy     | LAS/LAZ file format I/O              |
| numpy     | Array operations                     |

---

## Context

E57 is the ASTM-standardised format for storing 3D point cloud data from terrestrial laser scanners. This tool was built to work directly with scanner output — no intermediate conversion required — and supports the full intensity data channel for visualisation.

LAS export enables integration with surveying platforms such as Trimble Business Center, Autodesk ReCap and CloudCompare.

---

## License

MIT

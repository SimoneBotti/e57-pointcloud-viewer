"""
PLY Point Cloud Viewer (example)
---------------------------------
Loads a PLY point cloud and renders it with Open3D.

Usage:
    python examples/ply_viewer.py --input path/to/cloud.ply
"""

import argparse
import numpy as np
import open3d as o3d


def parse_args():
    parser = argparse.ArgumentParser(description="PLY point cloud viewer")
    parser.add_argument("--input", required=True, help="Path to the .ply file")
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"Loading {args.input} ...")
    pcd = o3d.io.read_point_cloud(args.input)
    print(pcd)
    print(f"Points: {len(pcd.points):,}")

    o3d.visualization.draw_geometries([pcd])


if __name__ == "__main__":
    main()


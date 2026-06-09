"""
E57 Point Cloud Viewer
----------------------
Reads terrestrial laser scanner data in E57 format, applies voxel downsampling,
and visualises the point cloud coloured by intensity.

Optionally exports the scan to LAS format.

Usage:
    python main.py --input path/to/scan.e57
    python main.py --input path/to/scan.e57 --voxel 0.02 --export
"""

import argparse
import time

import numpy as np
import open3d as o3d
import pye57
import laspy


def parse_args():
    parser = argparse.ArgumentParser(description="E57 point cloud viewer")
    parser.add_argument(
        "--input", required=True,
        help="Path to the input .e57 file"
    )
    parser.add_argument(
        "--scan-index", type=int, default=0,
        help="Index of the scan to load (default: 0)"
    )
    parser.add_argument(
        "--voxel", type=float, default=0.05,
        help="Voxel size for downsampling in metres (default: 0.05)"
    )
    parser.add_argument(
        "--export", action="store_true",
        help="Export scan to LAS format in output/out.las"
    )
    return parser.parse_args()


def read_e57(filepath: str, scan_index: int = 0) -> dict:
    """Read a scan from an E57 file and return raw data arrays."""
    print(f"Reading scan {scan_index} from {filepath} ...")
    start = time.time()

    e57 = pye57.E57(filepath)
    data = e57.read_scan_raw(scan_index)

    elapsed = time.time() - start
    print(f"Read complete in {elapsed:.2f}s")

    header = e57.get_header(scan_index)
    print(f"  Point count : {header.point_count:,}")
    print(f"  Rotation    : {header.rotation_matrix}")
    print(f"  Translation : {header.translation}")

    return data


def export_las(data: dict, output_path: str = "output/out.las") -> None:
    """Export point cloud data to a LAS file."""
    las_out = laspy.create(point_format=3, file_version="1.2")

    xmin = np.floor(np.min(data["cartesianX"]))
    ymin = np.floor(np.min(data["cartesianY"]))
    zmin = np.floor(np.min(data["cartesianZ"]))

    las_out.header.offset = [xmin, ymin, zmin]
    las_out.header.scale = [0.001, 0.001, 0.001]

    las_out.x = data["cartesianX"]
    las_out.y = data["cartesianY"]
    las_out.z = data["cartesianZ"]
    las_out.intensity = data["intensity"]

    las_out.write(output_path)
    print(f"Exported LAS to {output_path}")


def build_point_cloud(data: dict) -> o3d.geometry.PointCloud:
    """Build an Open3D PointCloud from raw scan data, coloured by intensity."""
    x = np.asarray(data["cartesianX"])
    y = np.asarray(data["cartesianY"])
    z = np.asarray(data["cartesianZ"])
    intensity = np.asarray(data["intensity"])

    points = np.column_stack((x, y, z))
    # Map intensity to greyscale RGB (values expected in [0, 1])
    colours = np.column_stack((intensity, intensity, intensity))

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colours)
    return pcd


def visualise(pcd: o3d.geometry.PointCloud, voxel_size: float) -> None:
    """Downsample and render the point cloud."""
    print(f"Downsampling with voxel size {voxel_size} m ...")
    downpcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    print(f"  Points after downsampling: {len(downpcd.points):,}")

    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="E57 Point Cloud Viewer", visible=True)
    vis.get_render_option().background_color = [0.0, 0.0, 0.0]
    vis.add_geometry(downpcd)

    ctr = vis.get_view_control()
    ctr.set_zoom(1.0)

    vis.run()
    vis.destroy_window()


def main():
    args = parse_args()

    data = read_e57(args.input, args.scan_index)

    if args.export:
        export_las(data)

    pcd = build_point_cloud(data)
    visualise(pcd, args.voxel)


if __name__ == "__main__":
    main()

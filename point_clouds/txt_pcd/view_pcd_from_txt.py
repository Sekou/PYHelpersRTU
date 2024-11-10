#A. Voronkov, 2023
import open3d as o3d
import numpy as np

if (__name__ == '__main__'):
    # Loading from disk:
    pcd_np = np.loadtxt('0003_clutter_point_cloud.txt', delimiter=';')
    print('Point cloud consists of {0} points each represented by {1} values.'.format(pcd_np.shape[0], pcd_np.shape[1]))

    # Constructing Open3D objects:
    base_frame = o3d.geometry.TriangleMesh().create_coordinate_frame(size=0.1)
    pcd_o3d = o3d.geometry.PointCloud()
    pcd_o3d.points = o3d.utility.Vector3dVector(pcd_np[:, :3])
    pcd_o3d.colors = o3d.utility.Vector3dVector(pcd_np[:, 3:6] / 255)
    # downsampled_pcd = pcd_o3d.farthest_point_down_sample(20000)
    # downsampled_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=30))

    # 3D-drawing:
    # o3d.visualization.draw_geometries([downsampled_pcd])
    o3d.visualization.draw_geometries([pcd_o3d])

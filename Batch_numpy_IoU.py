import numpy as np

def batch_iou(bboxesA, bboxesB):
    # Expand dimensions to allow broadcasting
    A = np.expand_dims(bboxesA, axis=1)  # Shape (n, 1, 4)
    B = np.expand_dims(bboxesB, axis=0)  # Shape (1, m, 4)
    
    # Calculate the intersection coordinates
    inter_min_xy = np.maximum(A[..., :2], B[..., :2])
    inter_max_xy = np.minimum(A[..., 2:], B[..., 2:])
    
    # Calculate intersection area
    inter_wh = np.maximum(inter_max_xy - inter_min_xy, 0)
    inter_area = inter_wh[..., 0] * inter_wh[..., 1]
    
    # Calculate the area of each box in A and B
    area_A = (A[..., 2] - A[..., 0]) * (A[..., 3] - A[..., 1])
    area_B = (B[..., 2] - B[..., 0]) * (B[..., 3] - B[..., 1])
    
    # Calculate union area
    union_area = area_A + area_B - inter_area
    
    # Compute IoU
    iou = inter_area / union_area
    
    return iou

# Example usage:
bboxesA = np.array([[0, 0, 2, 2], [1, 1, 3, 3]])
bboxesB = np.array([[1, 0, 2, 1], [0, 0, 1, 1]])

iou_matrix = batch_iou(bboxesA, bboxesB)
print(iou_matrix)

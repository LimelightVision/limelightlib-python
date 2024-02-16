import json
import time

class GeneralResult:
    def __init__(self, results):
        self.barcode = results.get("Barcode", [])
        self.classifierResults = [ClassifierResult(item) for item in results.get("Classifier", [])]
        self.detectorResults = [DetectorResult(item) for item in results.get("Detector", [])]
        self.fiducialResults = [FiducialResult(item) for item in results.get("Fiducial", [])]
        self.retroResults = [RetroreflectiveResult(item) for item in results.get("Retro", [])]
        self.botpose = results.get("botpose", [])
        self.botpose_wpiblue = results.get("botpose_wpiblue", [])
        self.botpose_wpired = results.get("botpose_wpired", [])
        self.capture_latency = results.get("cl", 0)
        self.pipeline_id = results.get("pID", 0)
        self.robot_pose_target_space = results.get("t6c_rs", [])
        self.targeting_latency = results.get("tl", 0)
        self.timestamp = results.get("ts", 0)
        self.validity = results.get("v", 0)
        self.parse_latency = 0.0


class RetroreflectiveResult:
    def __init__(self, retro_data):
        self.points = retro_data["pts"]
        self.camera_pose_target_space = retro_data["t6c_ts"]
        self.robot_pose_field_space = retro_data["t6r_fs"]
        self.robot_pose_target_space = retro_data["t6r_ts"]
        self.target_pose_camera_space = retro_data["t6t_cs"]
        self.target_pose_robot_space = retro_data["t6t_rs"]
        self.target_area = retro_data["ta"]
        self.target_x_degrees = retro_data["tx"]
        self.target_x_pixels = retro_data["txp"]
        self.target_y_degrees = retro_data["ty"]
        self.target_y_pixels = retro_data["typ"]

class FiducialResult:
    def __init__(self, fiducial_data):
        self.fiducial_id = fiducial_data["fID"]
        self.family = fiducial_data["fam"]
        self.points = fiducial_data["pts"]
        self.skew = fiducial_data["skew"]
        self.camera_pose_target_space = fiducial_data["t6c_ts"]
        self.robot_pose_field_space = fiducial_data["t6r_fs"]
        self.robot_pose_target_space = fiducial_data["t6r_ts"]
        self.target_pose_camera_space = fiducial_data["t6t_cs"]
        self.target_pose_robot_space = fiducial_data["t6t_rs"]
        self.target_area = fiducial_data["ta"]
        self.target_x_degrees = fiducial_data["tx"]
        self.target_x_pixels = fiducial_data["txp"]
        self.target_y_degrees = fiducial_data["ty"]
        self.target_y_pixels = fiducial_data["typ"]

class DetectorResult:
    def __init__(self, detector_data):
        self.class_name = detector_data["class"]
        self.class_id = detector_data["classID"]
        self.confidence = detector_data["conf"]
        self.points = detector_data["pts"]
        self.target_area = detector_data["ta"]
        self.target_x_degrees = detector_data["tx"]
        self.target_x_pixels = detector_data["txp"]
        self.target_y_degrees = detector_data["ty"]
        self.target_y_pixels = detector_data["typ"]

class ClassifierResult:
    def __init__(self, classifier_data):
        self.class_name = classifier_data["class"]
        self.class_id = classifier_data["classID"]
        self.confidence = classifier_data["conf"]


def parse_results(json_data):
    start_time = time.time()
    if(json_data is not None):
        results_data = json_data.get("Results", {})
        parsed_result = GeneralResult(results_data)
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000
        parsed_result.parse_latency = elapsed_time_ms
        return parsed_result
    return None
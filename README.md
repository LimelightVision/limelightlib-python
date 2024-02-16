# LimelightLib Python

## Discover all connected Limelights, and interact with them via REST and Websockets

```
import limelight
import limelightresults

discovered_limelights = limelight.discover_limelights()
print("discovered limelights:", discovered_limelights)

if discovered_limelights:
    limelight_address = discovered_limelights[0] 
    limelight = limelight.Limelight(limelight_address)
    results = limelight.get_results()
    print("targeting results:", results)

    limelight.enable_websocket()
    while(True):
        result = limelight.get_latest_results()

        parsed_result = limelightresults.parse_results(result)
        if parsed_result is not None:
            print(parsed_result.pipeline_id)
            print(parsed_result.parse_latency)

            # Accessing arrays
            for tag in parsed_result.fiducialResults:
                print(tag.robot_pose_target_space, tag.fiducial_id)
```
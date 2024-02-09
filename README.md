# LimelightLib Python

## Discover all connected Limelights, and interact with them via REST and Websockets

```
import limelight

discovered_limelights = limelight.discover_limelights()
print("ll devices:", discovered_limelights)

if discovered_limelights:
    limelight_address = discovered_limelights[0] 
    ll = limelight.Limelight(limelight_address)
    results = ll.get_results()
    print("Targeting results:", results)
    ll.enable_websocket()
    while(True):
        res = ll.get_latest_results()
        print(res)
```
"""
Starting a Stream

This example shows how to search for available Muses and
create a new stream
"""

from muselsl import stream, list_muses

if __name__ == "__main__":

    muses = list_muses()
    muses = [m for m in muses if m["name"] == "MuseS-79AA"]

    # Found device MuseS-79AA, MAC Address 25770FE7-C2E5-8082-FCD6-22319FD37812

    if not muses:
        print("No Muses found")
    else:
        stream(
            muses[0]["address"], ppg_enabled=True, acc_enabled=True, gyro_enabled=True
        )

        # Note: Streaming is synchronous, so code here will not execute until the stream has been closed
        print("Stream has ended")

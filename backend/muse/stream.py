from muselsl import stream, list_muses

if __name__ == "__main__":
    muses = list_muses()
    if not muses:
        print("No Muses found")
    else:
        stream(
            muses[0]["address"], ppg_enabled=True, acc_enabled=True, gyro_enabled=True
        )

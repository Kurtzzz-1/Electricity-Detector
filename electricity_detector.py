import requests

data = requests.get(
    "http://android.shinemonitor.com/public/?sign=287691c99e06e69b9ff09f3d6c243b6f7fc244e9&salt=1752329995474&token=744e59afe09479249fc3f0e90b0ee49e7ee6ea53d85b022626ae5d319adc95ad&action=queryDeviceFlowPower&pn=W0052076387745&sn=96342408108045&devaddr=1&devcode=2451&i18n=en_US&lang=en_US&source=1&_app_client_=android&_app_id_=wifiapp.volfw.watchpower&_app_version_=1.4.5.2"
)

grid_json = [js for js in data.json()["dat"] if js["par"] == "gd_fre"][0]
elec_freq = grid_json["val"]

print(elec_freq)

if float(elec_freq) > 0:
    TOPIC: str = "home_elec_detector_samisamisami"
    TITLE: str = "Electricity is ON!"
    MESSAGE: str = f"Grid Frequency is {elec_freq}"
    try:
        requests.post(
            f"https://ntfy.sh/{TOPIC}",
            data=MESSAGE.encode("utf-8"),
            headers={"Title": TITLE, "Priority": "high", "Tags": "electric_plug"},
        )
        print(f"Notification sent: '{TITLE}'")

        with open("elec_status.txt") as f:
            f.write(1)
    except Exception as e:
        print(f"Failed to send notification: {e}")

else:
    with open("elec_status.txt", 'w') as f:
        f.write(0)

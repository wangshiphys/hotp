"""
Calculate the Time-Based One-Time Password for High Performance Computing
Center of CICAM
"""


from time import time, sleep

import base64
import hmac


TIME_INTERVAL = 30
HOTP_LENGTH = 6
ENCODING = "utf-8"


def OneTimePasswd(key, msg, digestmod="sha1", length=6):
    hmac_hash = hmac.digest(key=key, msg=msg, digest=digestmod)
    offset = hmac_hash[-1] & 0xf
    otp_integer = (
        (hmac_hash[offset] & 0x7f) << 24 |
        (hmac_hash[offset + 1] & 0xff) << 16 |
        (hmac_hash[offset + 2] & 0xff) << 8 |
        (hmac_hash[offset + 3] & 0xff)
    )
    otp = str(otp_integer % (10 ** length)).rjust(length, "0")
    return otp


def TimeBasedOneTimePasswd(key, digestmod="sha1", length=6, time_interval=30):
    return OneTimePasswd(
        key=key,
        msg=int(time() / time_interval).to_bytes(8, byteorder="big"),
        digestmod=digestmod,
        length=length,
    )


if __name__ == "__main__":
    try:
        with open("token", "rb") as fp:
            token_bytes = fp.readline()
            token = token_bytes.decode(encoding=ENCODING, errors="strict")
    except FileNotFoundError:
        token = input("Please input the dynamic token:")
        save = input("Would you like to save the input token ([y]/n)? ").lower()
        if save in ("", "y", "yes"):
            token_bytes = token.encode(encoding=ENCODING, errors="strict")
            with open("token", "wb") as fp:
                fp.write(token_bytes)

    # The character '\r' is `carriage return`
    # It returns the cursor to the start of the line
    msg0 = "Latest Verification Code: {0}"
    msg1 = "Countdown:{0:2d}s\r"
    while True:
        now_window = int(time() / TIME_INTERVAL)
        hotp = OneTimePasswd(
            key=base64.b32decode(token),
            msg=now_window.to_bytes(8, byteorder="big"),
            length=HOTP_LENGTH,
        )
        print(msg0.format(hotp))

        left = (now_window + 1) * TIME_INTERVAL - int(time())
        for i in range(left, 0, -1):
            print(msg1.format(i), end="")
            sleep(1)
        print(msg1.format(0), end="")

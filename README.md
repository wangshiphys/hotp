# TOTP

A Python script for calculating the Time-Based One-Time Password for High
Performance Computing Center of CICAM.

## Requirements

python >= 3.5

## Usage

Run the script `totp.py` with python interper. For example, in windows `powershell` or `cmd` run the following command `python totp.py`.

## Note

For the first time of usage, the user needs to enter the **token**. After that, the user can select to save the **token** for reuse. If the user select to save the **token**, it will be saved to the current working directory with the name `token`. The **token** is saved in binary form without encryption.

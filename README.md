# TinyPiStats

View Raspberry Pi stats on a tiny OLED display

## Prerequisites

I2C must be enabled on the Pi:

1. `sudo raspi-config`
2. Select 'Interfacing Options' and 'I2C' to enable the interface
3. Select Finish
4. Reboot

Build requirements:

```bash
$ pip install -r requirements.txt
```

On some Pis you may need to also `apt install` libopenjp2-7.

## Usage

```bash
./bin/tinypistats start &
```

```bash
./bin/tinypistats stop
```

If something goes wrong, you may need to delete the pid file: `/tmp/.tinypistats.pid`

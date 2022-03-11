# Instrument Server Hello World

Instrument Server Hello World is an [instrument-server](https://github.com/Terrabits/instrument-server) project which implements only one command:

`id_string?`

## Requirements

- Python ~= 3.7
- instrument-server ~= 1.3.7
- An R&S Instrument

## Install

Run `scripts/install` to install a known-good package and version set.

See the lock file for details:

[requirements.txt.lock](./requirements.txt.lock)

## Project Config File

Every `instrument-server` project is required to include a YAML config file. By convention, the config file must contain the following sections:

```yaml
plugins: {...}
devices: {...}
# Translation Commands (Optional)
...
```

The config file for this project is [hello_world.yaml](hello_world.yaml). Each section of the file is explained below.

### Plugins

This application does not include any plugins, and so the `plugins` value is an empty dictionary (no values).

```yaml
plugins: {}
```

### Devices

A single device named `instrument` is defined:

```yaml
instrument:
  type:        socket
  address:     192.168.1.101
  port:        5025
  timeout:     5
```

Edit `address` to include the correct `instrument` IPV4 network IP address or hostname.

R&S instruments typically serve SCPI via a TCP socket on port `5025`. This field is typically left unchanged.

Optionally, the `timeout` time (in seconds) can be adjusted. If omitted, the default value is `2` (seconds).

#### Optional: VISA

To instead communicate with `instrument` via VISA, replace the default instrument definition with:

```yaml
instrument:
  type:         visa
  resource_str: "TCPIP::192.168.1.101::INSTR"
  open_timeout: 0
  timeout:      2000
```

Edit `resource_str` to include the correct `instrument` VISA Resource String.

Optionally, modify `open_timeout` and/or (read) `timeout` (in milliseconds).

### Commands

An `instrument-server` project file may include `Translation` command definition(s). `hello_world.yaml` defines one `Translation` command:

```yaml
id_string?:
  - instrument: "*IDN?"
```

The key `id_string?` contains the command syntax. The trailing `?` indicates that this is a query. This syntax should look familiar to SCPI users.

### Optional: Input Argument(s)

Note that `Translation` commands may include position-based input arguments. These inputs are available to the related SCPI commands via python `f-strings` syntax.

Here is an example that configures two instruments, a Vector Signal Generator and a Vector Signal Analyzer, for a linear frequency sweep:

```yaml
set_points points:
  - generator: 'SOUR:SWE:POIN {points}'
  - analyzer:  'SENS:SWE:POIN {points}'
```

## Start

Run `scripts/start` to serve `hello_world.yaml` on all network interfaces on port `9000`.

`scripts/start` calls the `instrument-server` Command Line Interface (CLI), which provides additional settings.


From `instrument-server --help`:

```comment
usage: instrument-server [-h] [--address ADDRESS] [--port PORT]
                         [--termination TERMINATION] [--debug-mode]
                         config_filename

TCP server for controlling multiple instruments via a simplified SCPI
interface

positional arguments:
  config_filename

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS, -a ADDRESS
                        Set listening address. Default: 0.0.0.0
  --port PORT, -p PORT  Set listening port. Default: random
  --termination TERMINATION, -t TERMINATION
                        Set the termination character. Default: "\n"
  --debug-mode, -d      print debug info to stdout
```

## Client Script

The `client.py` script is provided for testing. It connects to the server, queries `id_string?` and prints the result.

Here is an example that starts the server in the background, then runs `client.py`:

```shell
scripts/start-in-background
# => Running on 0.0.0.0:9000...

# run client
python client.py
# => id_string?
# => Rohde-Schwarz,ZNBT40-8Port,1332900244900059,3.15
```

## References

- [Introduction to YAML](https://dev.to/paulasantamaria/introduction-to-yaml-125f)
- [instrument-server](https://github.com/Terrabits/instrument-server)

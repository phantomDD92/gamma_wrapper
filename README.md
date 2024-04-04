# GAMMA API wannabe wrapper 
Wrapper for the GAMMA API

> [!WARNING]
> In construction.

## Requirements
Python 3.10.12 or greater
No special requirements to be installed

## Configuraton
U can change the API url source in ***config/cfg.py*** file

## Commands
Pass command line arguments like:

```console
python3 gamma_api.py --operation=kpi_dashboard --networks=arbitrum --ini_timestamp=1700064000 --end_timestamp=1708531200 --period_seconds=604800 --save_to_folder=exports --addresses=0xeE5F2E39D8aBF28E449327bfd44317FC500EB4D8 0x6cE9BC2D8093D32ADde4695A4530B96558388f7e 0x30AFBcF9458c3131A6d051C621E307E6278E4110 0xFdF4e57aF777D492037ECA0c50d7F03eB0807f88
```


Available run commands:

    -<operation>: 
     -<kpi_dashboard>: creates a csv file with info related to our kpis


( all commands are present in the ***config/command_line.py*** file )



### List of commands
U can pass a json file as a list of commands. just create a <commands.json> file containing the desired parameters, like this:

> [!NOTE]
> This example file creates a ***csv*** file in the ***exports*** folder with the kpi_dashboard related data for the Arbitrum network, between the timestamps provided and at an interval of 604800 seconds...

```json
{
    "name": " my commands today",
    "commands": [
        [
            "--operation=kpi_dashboard",
            "--networks=42161",
            "--ini_timestamp=1700064000",
            "--end_timestamp=1708531200",
            "--period_seconds=604800",
            "--addresses=0xeE5F2E39D8aBF28E449327bfd44317FC500EB4D8 0x6cE9BC2D8093D32ADde4695A4530B96558388f7e",
            "--save_to_folder=exports",
        ]
    ]
}
```

and pass it as a variab, like:

```console
python3 gamma_api.py --commands_file=commands.json
```
